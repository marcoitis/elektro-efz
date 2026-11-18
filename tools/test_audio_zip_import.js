/* Fast ZIP_STORED importer smoke test; no network or browser needed. */
'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const encoder=new TextEncoder();
function makeZip(name,payload){
 const filename=Buffer.from(name,'utf8'),data=Buffer.from(payload);
 const local=Buffer.alloc(30);
 local.writeUInt32LE(0x04034b50,0);
 local.writeUInt16LE(20,4);
 local.writeUInt32LE(data.length,18);
 local.writeUInt32LE(data.length,22);
 local.writeUInt16LE(filename.length,26);
 const central=Buffer.alloc(46);
 central.writeUInt32LE(0x02014b50,0);
 central.writeUInt16LE(20,4);
 central.writeUInt16LE(20,6);
 central.writeUInt32LE(data.length,20);
 central.writeUInt32LE(data.length,24);
 central.writeUInt16LE(filename.length,28);
 central.writeUInt32LE(0,42);
 const ending=Buffer.alloc(22);
 ending.writeUInt32LE(0x06054b50,0);
 ending.writeUInt16LE(1,8);
 ending.writeUInt16LE(1,10);
 ending.writeUInt32LE(central.length+filename.length,12);
 ending.writeUInt32LE(local.length+filename.length+data.length,16);
 return new File([local,filename,data,central,filename,ending],'Audio_Thorsten_High_Batch_01.zip',{type:'application/zip'});
}
const contents=Buffer.concat([Buffer.from('ID3'),Buffer.alloc(9000,12)]);
const files={};
const context={DataView,Uint8Array,TextDecoder,File,Blob,console,window:{ElektroAudio:{importFile:async(id,file)=>{files[id]=file;}}}};
vm.runInNewContext(fs.readFileSync('audio-zip-import.js','utf8'),context,{filename:'audio-zip-import.js'});
(async()=>{
 const result=await context.window.ElektroAudioZip.importArchives([makeZip('1.01-A.mp3',contents)],['1.01-A']);
 assert.strictEqual(result.archives,1);
 assert.strictEqual(result.imported,1);
 assert.strictEqual(result.errors.length,0);
 assert.strictEqual(files['1.01-A'].size,contents.length);
 const bytes=Buffer.from(await files['1.01-A'].arrayBuffer());
 assert.strictEqual(bytes.compare(contents),0);
 console.log('PASS ZIP import: 1 uncompressed MP3, matching content, safe memory slices.');
})().catch(e=>{console.error(e);process.exit(1)});
