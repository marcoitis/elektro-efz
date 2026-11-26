#!/usr/bin/env python3
"""Sequential masterclass renderer, 1 lesson at a time.

Inputs: masterclasses/<lesson_id>/script.json with manually edited visual beats.
Outputs: masterclasses/<lesson_id>/audio/masterclass.mp3 + timeline.json.
A beat begins at the PCM sample boundary of its separately spoken segment.
NOT word-for-word forced alignment. The output is technically verified, not
automatically approved for technical/normative accuracy or acoustic quality.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
MODEL=ROOT/".voice-cache"/"de_DE-thorsten-high.onnx"
CONFIG=ROOT/".voice-cache"/"de_DE-thorsten-high.onnx.json"
MODEL_SHA="9df1c43c61149ef9b39e618e2b861fbe41e1fcea9390b2dac62e8761573ea4f1"

def cmd(argv, **kwargs):
    try:
        return subprocess.run(argv,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kwargs)
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.decode('utf-8','replace')[-3000:],file=sys.stderr)
        raise

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as inp:
        for chunk in iter(lambda:inp.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def run(lesson):
    if not __import__('re').fullmatch(r'(?:[1-4]\.\d{2}-[A-Z]|N-[A-Z]\d{2})',lesson):
        raise ValueError('Unrecognized lesson ID')
    base=ROOT/'masterclasses'/lesson
    source=base/'script.json'
    tts_source=ROOT/'tts_scripts'/f'{lesson}.txt'
    course_data=ROOT/'data.js'
    assert tts_source.is_file() and course_data.is_file(), 'Narration source or course data missing'
    sc=json.loads(source.read_text(encoding='utf-8'))
    assert sc['lesson_id']==lesson and sc['id']==lesson+'-master'
    beats=sc['beats']
    assert 15<=len(beats)<=50
    assert [b['id'] for b in beats]==[f'{i:02}' for i in range(1,len(beats)+1)]
    assert all(len(b['text'].split())>=9 and b['visual'] for b in beats)
    assert digest(MODEL)==MODEL_SHA and CONFIG.stat().st_size>1000
    out=base/'audio'
    out.mkdir(parents=True,exist_ok=True)
    sample_rate=None;frames_total=0;timing=[]
    with tempfile.TemporaryDirectory(prefix='efz-master-') as tmp:
        paths=[]
        for idx,beat in enumerate(beats,1):
            target=Path(tmp)/f'{idx:02}.wav'
            cmd(['piper','--model',str(MODEL),'--config',str(CONFIG),
                 '--output_file',str(target),'--length_scale','1.04',
                 '--sentence_silence','0.22'],input=(beat['text'].strip()+'\n').encode('utf-8'),timeout=240)
            with wave.open(str(target),'rb') as wav:
                assert wav.getnchannels()==1 and wav.getsampwidth()==2
                rate=wav.getframerate();frames=wav.getnframes()
            if sample_rate is None:sample_rate=rate
            assert rate==sample_rate and rate in (22050,24000)
            assert frames>rate*2, (beat['id'],frames)
            start_sample=frames_total
            end_sample=frames_total+frames
            timing.append({'id':beat['id'],'visual':beat['visual'],
                           'start_sample':start_sample,'duration_samples':frames,
                           'end_sample':end_sample,
                           'start':round(start_sample/rate,6),
                           'duration':round(frames/rate,6),
                           'end':round(end_sample/rate,6),
                           'narration':beat['text']})
            frames_total=end_sample
            paths.append(target)
            print(f'BEAT {idx:02}/{len(beats)} {beat["visual"]}: {frames/rate:.2f}s',flush=True)
        wave_file=Path(tmp)/'joined.wav'
        with wave.open(str(wave_file),'wb') as dst:
            dst.setnchannels(1);dst.setsampwidth(2);dst.setframerate(sample_rate)
            for src in paths:
                with wave.open(str(src),'rb') as inp:
                    dst.writeframes(inp.readframes(inp.getnframes()))
        mp3=out/'masterclass.mp3'
        cmd(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
             '-i',str(wave_file),'-af','loudnorm=I=-18:LRA=9:TP=-2',
             '-ac','1','-ar','22050','-codec:a','libmp3lame','-b:a','128k',str(mp3)],timeout=400)
    probe=json.loads(cmd(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,channels,sample_rate','-of','json',str(mp3)]).stdout.decode())
    duration=float(probe['format']['duration'])
    assert abs(duration-frames_total/sample_rate)<.25
    assert 110<duration<450
    assert probe['streams'][0]['codec_name']=='mp3' and probe['streams'][0]['channels']==1
    assert 200_000<mp3.stat().st_size<9_000_000
    manifest={'version':1,'lesson_id':lesson+'-master',
              'voice':'Piper de_DE-thorsten-high','model_sha256':MODEL_SHA,
              'source_sha256':digest(source),
              'tts_source_sha256':digest(tts_source),
              'course_data_sha256':digest(course_data),
              'audio_sha256':digest(mp3),
              'duration_seconds':round(duration,6),
              'pcm_duration_seconds':round(frames_total/sample_rate,6),
              'sample_rate':sample_rate,'duration_samples':frames_total,
              'alignment':'beat_exact_via_PCM_frame_count_not_word_aligned',
              'approval':'technical_verified_not_acoustically_or_normatively_signed_off',
              'beats':timing}
    (out/'timeline.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert len(timing)==len(beats)
    assert all(timing[i-1]['end_sample']==timing[i]['start_sample'] for i in range(1,len(timing)))
    assert all(abs(x['start']-x['start_sample']/sample_rate)<1e-7 for x in timing)
    assert timing[-1]['end_sample']==frames_total
    print(f'PASS {lesson}: {duration:.2f} sec, {len(beats)} exact beat starts, {mp3.stat().st_size} bytes',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--lesson',required=True)
    a=parser.parse_args()
    run(a.lesson)
