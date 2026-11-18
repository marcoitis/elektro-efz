#!/usr/bin/env python3
"""Extend the 178 authored lesson transcripts with individual goals, worked steps and feedback.
The additions use existing course data rather than inventing normative requirements.
Usage: python tools/build_extended_lectures.py [--dry-run]
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, subprocess
ROOT=Path(__file__).resolve().parent.parent
D=json.loads((ROOT/'data.js').read_text(encoding='utf-8').split('=',1)[1].strip(' ;\n'))
N=json.loads((ROOT/'norm_course.json').read_text(encoding='utf-8'))
EXAMPLE_JS="const fs=require('fs'),vm=require('vm');const w={};const c={window:w};vm.runInNewContext(fs.readFileSync('studio.js','utf8'),c);vm.runInNewContext(fs.readFileSync('studio-examples-extra.js','utf8'),c);process.stdout.write(JSON.stringify(w.ElektroStudio.examples));"
EX=json.loads(subprocess.check_output(['node','-e',EXAMPLE_JS],cwd=ROOT,text=True))

def lead(l,norm=False):
    if norm:
        return f"Vertiefende Normenlektion: {l['title']}. Wir erläutern die Quelle {l['source']} anhand selbst formulierter Fälle. Die Ausführungen sind ein Lerntext und ersetzen die gültige Originalnorm nicht."
    return f"Lektion {l['id']}: {l['title']}. Wir betrachten die theoretischen Grundlagen und übertragen sie auf einen sicheren Lernauftrag."

def build(l,norm=False):
    id=('N-'+l['id']) if norm else l['id']
    # Source reading is the authored narration already present in v0.9, not licensed standards text.
    initial=(ROOT/'tts_scripts'/f'{id}.txt').read_text(encoding='utf-8').split('\n\n---\n\nZusätzliche Unterrichtsvertiefung.')[0].strip()
    pieces=[initial,'\n\n---\n\nZusätzliche Unterrichtsvertiefung.']
    if norm:
        pieces.append('Als Leitfrage für diese Lektion gilt: '+l['scenario'])
        pieces.append('Ordne die Fallstudie zuerst ein, bevor Du die Musterlösung anhörst. Welche Informationen fehlen? Welche Rollen und Prüfungen müssen wir unterscheiden?')
        pieces.append('Begründung zum Fall: '+l['model'])
        pieces.append('Möglicher sicherer Übungsauftrag: '+l['check'])
        quiz=l['quiz']
    else:
        goals=l['objectives']
        pieces.append('Deine Lernziele lauten: '+'; '.join(goals[:5])+'.')
        ex=EX.get(l['moduleId'])
        if ex:
            pieces.append('Jetzt ein zusätzliches Rechen- und Anwendungsbeispiel zum Themengebiet '+ex['topic']+'. '+ex['givens'])
            pieces.extend(f'Schritt {i}. {step}' for i,step in enumerate(ex['steps'],1))
            pieces.append('Kontrolle des Ergebnisses: '+ex['check'])
        else:
            pieces.append('Wir gehen eine fachliche Entscheidung schrittweise durch. Ausgangsfrage: '+l['quiz'][0]['question'])
            pieces.append('Erstens: Was ist sicher bekannt und was ist lediglich eine Annahme? Zweitens: Welche Begriffe oder Wirkzusammenhänge aus dieser Lektion helfen bei der Entscheidung?')
            pieces.append('Drittens: Begründe Deine Antwort. '+l['quiz'][0]['why'])
            pieces.append('Viertens: Wo sind die Grenzen dieses Lernbeispiels? Welche Herstellerangaben, aktuellen Fachregeln oder fachlichen Nachweise wären bei einem realen Auftrag zusätzlich nötig?')
        pieces.append('Übungsauftrag zur Anwendung: '+l['task'])
        pieces.append('Für eine saubere Dokumentation notierst Du die Annahmen, den entscheidenden fachlichen Zusammenhang, Deinen Rechen- oder Denkweg und eine Kontrolle des Ergebnisses.')
        quiz=l['quiz']
    pieces.append('Zum Abschluss besprechen wir die Kontrollfragen samt Begründungen. Du kannst zuerst selbst antworten, bevor Du weiterhörst.')
    for i,q in enumerate(quiz,1):
        question=q.get('question',q.get('q',''))
        answer=q['answers'][q['correct']]
        pieces.append(f'Frage {i}: {question} Die richtige Antwort lautet: {answer}. Warum? {q["why"]}')
    pieces.append('Fazit: Verstehe und begründe jede Entscheidung mit konkreten Angaben. Bei Netzspannung, PV-Gleichstrom, Messungen und Arbeiten an Installationen genügt Selbststudium nicht; es gelten die erforderlichen Fachkompetenzen, Zuständigkeiten und Bewilligungen.')
    return '\n\n'.join(x.strip() for x in pieces if x and x.strip())+'\n'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dry-run',action='store_true');args=parser.parse_args()
    lectures={};counts=[]
    for norm,items in [(False,D['lessons']),(True,N['lessons'])]:
        for l in items:
            id=('N-'+l['id']) if norm else l['id']
            content=build(l,norm);lectures[id]=content;counts.append((id,len(content.split())))
            if not args.dry_run:
                (ROOT/'tts_scripts'/f'{id}.txt').write_text(content,encoding='utf-8')
    if not args.dry_run:
        (ROOT/'lecture-scripts.js').write_text('/* Sprecher-Manuskripte für 178 Unterrichtseinheiten · keine Originalnormtexte. */\nwindow.ElektroLectures = '+json.dumps(lectures,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    print('Lektionen:',len(lectures),'Wörter:',sum(i[1] for i in counts),'min/mean/max:',min(i[1] for i in counts),round(sum(i[1] for i in counts)/len(counts)),max(i[1] for i in counts))
    for s in counts[:3]:print(s)
if __name__=='__main__':main()
