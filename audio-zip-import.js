/* ZIP import for the approved-voice GitHub release archives (ZIP_STORED).
 * Reads only the central directory and each requested file slice, without
 * loading a 200 MB archive into mobile Safari memory. Browser-side only.
 * No files or learner progress are transmitted to a server. */
(function(){'use strict';
const LE16=(data,offset)=>data.getUint16(offset,true);
const LE32=(data,offset)=>data.getUint32(offset,true);
const decoder=new TextDecoder('utf-8');

async function entries(zip){
 const tailStart=Math.max(0,zip.size-65557);
 const tail=new DataView(await zip.slice(tailStart).arrayBuffer());
 let eof=-1;
 for(let offset=tail.byteLength-22;offset>=0;offset--){
  if(LE32(tail,offset)===0x06054b50){eof=offset;break}
 }
 if(eof<0)throw Error('ZIP-Endverzeichnis fehlt; bitte originales Paket wählen');
 const disks=LE16(tail,eof+4),entriesOnDisk=LE16(tail,eof+8);
 const total=LE16(tail,eof+10),length=LE32(tail,eof+12),start=LE32(tail,eof+16);
 if(disks!==0||entriesOnDisk!==total||total>40||!total||start+length>zip.size)
  throw Error('ZIP-Datei nicht unterstütztes Format');
 const data=new DataView(await zip.slice(start,start+length).arrayBuffer());
 const result=[];
 let i=0;
 while(i<data.byteLength){
  if(i+46>data.byteLength||LE32(data,i)!==0x02014b50)throw Error('ZIP-Inhaltsverzeichnis beschädigt');
  const method=LE16(data,i+10),length=LE32(data,i+20),raw=LE32(data,i+24);
  const nameLength=LE16(data,i+28),extra=LE16(data,i+30),comment=LE16(data,i+32);
  const offset=LE32(data,i+42);
  if(i+46+nameLength+extra+comment>data.byteLength)throw Error('ZIP-Dateiname beschädigt');
  const name=decoder.decode(new Uint8Array(data.buffer,data.byteOffset+i+46,nameLength));
  result.push({name,method,length,raw,offset});
  i+=46+nameLength+extra+comment;
 }
 if(result.length!==total)throw Error('ZIP-Dateianzahl stimmt nicht überein');
 return result;
}
async function audioSlice(zip,entry){
 if(entry.method!==0||entry.raw!==entry.length)throw Error('ZIP muss unkomprimierte MP3s enthalten');
 if(entry.length<4096||entry.length>80*1024*1024)throw Error('MP3 hat eine unzulässige Grösse');
 if(entry.offset+30>zip.size)throw Error('ZIP-Offset ausserhalb der Datei');
 const header=new DataView(await zip.slice(entry.offset,entry.offset+30).arrayBuffer());
 if(LE32(header,0)!==0x04034b50)throw Error('ZIP-Dateikopf beschädigt');
 const nameSize=LE16(header,26),extraSize=LE16(header,28);
 const at=entry.offset+30+nameSize+extraSize;
 if(at+entry.length>zip.size)throw Error('MP3 liegt ausserhalb der ZIP-Datei');
 const blob=zip.slice(at,at+entry.length,'audio/mpeg');
 const prefix=new Uint8Array(await blob.slice(0,3).arrayBuffer());
 if(!(prefix[0]===73&&prefix[1]===68&&prefix[2]===51)&&!(prefix[0]===255&&(prefix[1]&224)===224))
  throw Error('MP3-Kopf nicht erkannt');
 return blob;
}
async function importArchives(archives,knownIds,progress=()=>{}){
 const known=new Set(knownIds),result={imported:0,skipped:0,errors:[],archives:0};
 for(const zip of [...archives]){
  if(!/\.zip$/i.test(zip.name)){result.errors.push(zip.name+': keine ZIP-Datei');continue}
  try{
   const contents=await entries(zip);
   for(const entry of contents){
    if(!/^(?:[1-4]\.[0-9]{2}-[A-Z]|N-[A-Z][0-9]{2})\.mp3$/.test(entry.name)){
     result.skipped++;continue;
    }
    const id=entry.name.slice(0,-4);
    if(!known.has(id)){result.skipped++;continue}
    try{
     const blob=await audioSlice(zip,entry);
     await window.ElektroAudio.importFile(id,new File([blob],id+'.mp3',{type:'audio/mpeg'}));
     result.imported++;
     progress(result.imported,id,zip.name);
    }catch(e){result.errors.push(zip.name+' / '+id+': '+e.message)}
   }
   result.archives++;
  }catch(e){result.errors.push(zip.name+': '+e.message)}
 }
 return result;
}
window.ElektroAudioZip={importArchives};
})();
