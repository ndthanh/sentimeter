export const createAgentState=()=>({cards:[],agents:[],recommendation:null,signals:{emotion:'Listening',confidence:'Insufficient evidence',guidance:'Confirm identity and listen to the customer.'}});
export function validateState(s){
 if(!s||!Array.isArray(s.cards)||!Array.isArray(s.agents)||!s.signals||typeof s.signals.emotion!=='string'||typeof s.signals.confidence!=='string'||typeof s.signals.guidance!=='string')throw Error('Invalid AgentState');
 for(const c of s.cards)if(!c||typeof c.id!=='string'||typeof c.source!=='string'||typeof c.title!=='string'||typeof c.body!=='string'||typeof c.status!=='string'||!c.evidence||!Array.isArray(c.evidence.fields)||!Array.isArray(c.evidence.columns)||!Array.isArray(c.evidence.rows))throw Error('Invalid evidence card');
 for(const a of s.agents)if(typeof a.id!=='string'||typeof a.name!=='string'||!['waiting','running','completed','error'].includes(a.status)||typeof a.task!=='string')throw Error('Invalid agent activity');
 if(s.recommendation!==null&&(!s.recommendation||typeof s.recommendation.answer!=='string'||typeof s.recommendation.title!=='string'||typeof s.recommendation.solution!=='string'))throw Error('Invalid recommendation');
 for(const c of s.cards){const e=c.evidence;if(!(['t24','fimi','policy','mcc','ido','portal'].includes(c.id)||/^route-[1-4]-[0-3]$/.test(c.id))||typeof e.screen!=='string'||typeof e.reference!=='string'||typeof e.conclusion!=='string'||e.fields.some(r=>!Array.isArray(r)||r.length!==2||r.some(v=>typeof v!=='string'))||e.columns.some(v=>typeof v!=='string')||e.rows.some(r=>!Array.isArray(r)||r.some(v=>typeof v!=='string')))throw Error('Invalid evidence details');}
 return s;
}
export function applyAgentEvent(state,event){
 if(event.type==='STATE_SNAPSHOT')return validateState(structuredClone(event.snapshot));
 if(event.type!=='STATE_DELTA')return state;
 const next=structuredClone(state);if(!Array.isArray(event.delta))throw Error('Missing delta');
 for(const p of event.delta){if(!['replace','add'].includes(p.op)||!['/cards','/agents','/recommendation','/signals'].includes(p.path))throw Error('Unsupported patch: use top-level add/replace or STATE_SNAPSHOT');next[p.path.slice(1)]=structuredClone(p.value);}
 return validateState(next);
}
export class TranscriptStore{
 constructor(){this.segments=new Map();}
 ingest(s){
  if(!s||typeof s.id!=='string'||typeof s.callId!=='string'||!['customer','operator'].includes(s.speaker)||typeof s.text!=='string'||!Number.isInteger(s.revision)||s.revision<0||typeof s.isFinal!=='boolean'||!Number.isFinite(s.startMs)||s.startMs<0||!Number.isFinite(s.endMs)||s.endMs<s.startMs)throw Error('Invalid TranscriptSegment');
  const old=this.segments.get(s.id);if(old&&(s.revision<=old.revision||(old.isFinal&&!s.isFinal)))return false;
  this.segments.set(s.id,structuredClone(s));return true;
 }
 values(){return [...this.segments.values()].sort((a,b)=>a.startMs-b.startMs);}
 finals(){return this.values().filter(s=>s.isFinal);}
}
export class SSEDecoder{
 constructor(onEvent){this.buffer='';this.onEvent=onEvent;}
 push(text){this.buffer+=text;let match;while((match=/\r?\n\r?\n/.exec(this.buffer))){const frame=this.buffer.slice(0,match.index);this.buffer=this.buffer.slice(match.index+match[0].length);const data=frame.split(/\r?\n/).filter(l=>l.startsWith('data:')).map(l=>l.slice(5).replace(/^ /,'')).join('\n');if(data&&data!=='[DONE]')this.onEvent(JSON.parse(data));}}
 finish(){if(this.buffer.trim())throw Error('Incomplete SSE frame; request a fresh snapshot');}
}
