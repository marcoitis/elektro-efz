/* v0.5: OPTIONAL Supabase synchronization, no third-party JS dependencies.
   Uses email/password Supabase Auth, PostgREST and row-level security.
   Not enabled until a user provides their own Supabase project and signs in.
   Compare-and-swap revision checking prevents silent overwriting of newer progress. */
(function(){'use strict';
const KCFG='efz-cloud-config-v1',KSESSION='efz-cloud-session-v1',KMETA='efz-cloud-meta-v1';
function read(k){try{return JSON.parse(localStorage.getItem(k)||'null')}catch(_){return null}}
function put(k,v){try{if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,JSON.stringify(v));return true}catch(_){return false}}
let cfg=read(KCFG),session=read(KSESSION),meta=read(KMETA)||{},busy=false,issue='',remote=null,status='Nicht eingerichtet',timer=null,enabled=false;
let hooks={getState:()=>null,onReceive:()=>{},onStatus:()=>{}};
const change=(s)=>{status=s;hooks.onStatus?.(status)};
function config(url,key){url=String(url||'').trim().replace(/\/$/,'');key=String(key||'').trim();if(!/^https:\/\/[a-z0-9.-]+/i.test(url))throw Error('Cloud-Endpunkt muss mit https:// beginnen');if(!key||key.length<15||/service.role|sb_secret_/i.test(key))throw Error('Bitte ausschliesslich den öffentlichen Publishable-/Anon-Key verwenden');cfg={url,key};put(KCFG,cfg);session=null;put(KSESSION,null);remote=null;enabled=false;meta={};put(KMETA,meta);change('Projekt gespeichert – bitte anmelden')}
function headers(token,extra={}){return {'apikey':cfg.key,'Content-Type':'application/json',...(token?{'Authorization':'Bearer '+token}:{}),...extra}}
async function call(path,options={},retry=true){if(!cfg)throw Error('Kein Cloud-Projekt eingerichtet');const token=session?.access_token||null;
 const res=await fetch(cfg.url+path,{...options,headers:headers(token,options.headers||{})});
 if(res.status===401&&retry&&session?.refresh_token){await refresh();return call(path,options,false)}
 let body=null;const raw=await res.text();try{body=raw?JSON.parse(raw):null}catch(_){body=raw}
 if(!res.ok)throw Error((typeof body==='object'&&(body?.msg||body?.message||body?.error_description||body?.error))||`Serverfehler ${res.status}`);
 return body;
}
function storeSession(value){session=value?{access_token:value.access_token,refresh_token:value.refresh_token,expires_at:Math.floor(Date.now()/1000)+(value.expires_in||3600),user:value.user}:null;put(KSESSION,session)}
async function refresh(){if(!session?.refresh_token)throw Error('Bitte erneut anmelden');const res=await fetch(cfg.url+'/auth/v1/token?grant_type=refresh_token',{method:'POST',headers:headers(null),body:JSON.stringify({refresh_token:session.refresh_token})});const data=await res.json();if(!res.ok)throw Error(data.msg||data.message||'Anmeldung erneuern fehlgeschlagen');storeSession(data);return session}
async function ensureSession(){if(!session?.access_token)throw Error('Bitte anmelden');if(session.expires_at&&Date.now()/1000>session.expires_at-120)await refresh();return session}
async function signIn(email,password,signup=false){if(!cfg)throw Error('Zuerst Supabase-Projekt einrichten');const endpoint=signup?'/auth/v1/signup':'/auth/v1/token?grant_type=password';const body={email:String(email||'').trim(),password};const res=await fetch(cfg.url+endpoint,{method:'POST',headers:headers(null),body:JSON.stringify(body)});const d=await res.json();if(!res.ok)throw Error(d.msg||d.error_description||d.message||'Anmeldung fehlgeschlagen');if(d.access_token){storeSession(d);change('Angemeldet – Synchronisierung wird geprüft');await inspect()}else change('Registrierung eingereicht – E-Mail bestätigen und anschliessend anmelden');return !!d.access_token}
function signOut(){if(timer){clearTimeout(timer);timer=null}session=null;enabled=false;remote=null;meta={};put(KSESSION,null);put(KMETA,null);change('Abgemeldet – lokaler Lernstand bleibt erhalten')}
async function retrieve(){await ensureSession();let rows=await call('/rest/v1/efz_progress?select=user_id,revision,progress,updated_at&user_id=eq.'+encodeURIComponent(session.user.id),{method:'GET',headers:{'Accept':'application/json'}});return Array.isArray(rows)?rows[0]||null:null}
function fingerprint(x){return JSON.stringify(x||{});} // Snapshot identity, not cryptographic
function locallySynced(local){return !!meta.savedState&&fingerprint(local)===fingerprint(meta.savedState)}
async function inspect(){if(!session){change('Nicht angemeldet');return null}try{remote=await retrieve();if(!remote){enabled=false;change('Cloud noch leer – lokalen Lernstand hochladen');return null}if(remote.revision===meta.revision){enabled=true;change('Verbunden · synchronisiert (Revision '+remote.revision+')');return remote}enabled=false;change('Cloud-Stand weicht ab – bitte wählen: Cloud, lokal oder zusammenführen');return remote}catch(e){enabled=false;issue=e.message;change('Cloud nicht erreichbar: '+issue);return null}}
async function saveConditional(progress,expected,allowInsert=false){await ensureSession();const url='/rest/v1/efz_progress';const uid=session.user.id;if(allowInsert){try{const data=await call(url,{method:'POST',headers:{Prefer:'return=representation'},body:JSON.stringify({user_id:uid,revision:1,progress})});return data?.[0]||null}catch(e){if(/409|duplicate|unique/i.test(e.message))return null;throw e}}
 const rows=await call(url+'?user_id=eq.'+encodeURIComponent(uid)+'&revision=eq.'+Number(expected),{method:'PATCH',headers:{Prefer:'return=representation'},body:JSON.stringify({revision:Number(expected)+1,progress})});return rows?.[0]||null}
async function upload(local,force=false){if(busy){change('Synchronisierung läuft bereits – erneuter Versuch später');return false}busy=true;try{
 if(force||!remote)remote=await retrieve();if(remote&&!force&&meta.revision!==remote.revision){enabled=false;change('Konflikt: neuerer Cloud-Stand gefunden. Bitte manuell entscheiden');return false}
 const saved=await saveConditional(local,remote?remote.revision:0,!remote);
 if(!saved){remote=await retrieve();enabled=false;change('Konflikt bei gleichzeitiger Änderung: Bitte neu vergleichen');return false}
 remote=saved;meta={revision:saved.revision,savedState:JSON.parse(JSON.stringify(local))};put(KMETA,meta);enabled=true;issue='';change('Synchronisiert · Revision '+saved.revision);return true
 }catch(e){issue=e.message;change('Synchronisierung fehlgeschlagen: '+issue);return false}finally{busy=false}}
async function choose(which){const cloud=remote||await retrieve();const local=hooks.getState();if(which==='cloud'){if(!cloud){change('In der Cloud liegt noch kein Stand');return false}meta={revision:cloud.revision,savedState:cloud.progress};put(KMETA,meta);enabled=true;hooks.onReceive(cloud.progress);change('Cloud-Stand übernommen');return true}
 if(which==='local'){return upload(local,true)}
 if(which==='merge'){const merged=window.ElektroReviews.merged(local,cloud?.progress||{});hooks.onReceive(merged);return upload(merged,true)}
 throw Error('Unbekannte Option')}
function queue(local){if(!enabled||!session||!cfg)return; if(timer)clearTimeout(timer);const pending=JSON.parse(JSON.stringify(local));timer=setTimeout(async()=>{timer=null;await upload(pending)},1800)}
async function start(h){hooks={...hooks,...h};if(!cfg){change('Nicht eingerichtet – optional');return}if(!session){change('Cloud-Projekt eingerichtet · nicht angemeldet');return}try{await inspect();if(remote&&meta.revision===remote.revision&&locallySynced(hooks.getState())){enabled=true;change('Synchronisierung bereit')}else if(remote){enabled=false;change('Cloud-Stand prüfen: Lokal, Cloud oder zusammenführen')}else{enabled=false;change('Cloud leer: lokalen Stand hochladen')}}catch(e){change('Cloud-Start fehlgeschlagen: '+e.message)}}
window.ElektroCloud={start,config,signIn,signOut,inspect,choose,queue,get:()=>({configured:!!cfg,config:cfg?{url:cfg.url,key:cfg.key}:null,authenticated:!!session?.access_token,email:session?.user?.email||'',revision:meta.revision||0,remoteRevision:remote?.revision||0,enabled,busy,status,issue})};
})();
