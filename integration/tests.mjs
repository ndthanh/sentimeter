import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createAgentState,applyAgentEvent,TranscriptStore,SSEDecoder} from '../dist/bridge.js';
const store=new TranscriptStore(),seg={id:'a',callId:'c',speaker:'customer',text:'Chị chưa được cộng điểm.',revision:0,isFinal:false,startMs:0,endMs:1000};
assert.equal(store.ingest(seg),true);assert.equal(store.finals().length,0);assert.equal(store.ingest(seg),false);assert.equal(store.ingest({...seg,revision:1,isFinal:true}),true);assert.equal(store.ingest({...seg,revision:2,isFinal:false}),false);assert.equal(store.ingest({...seg,revision:3,isFinal:true,text:'Corrected'}),true);assert.equal(store.finals()[0].text,'Corrected');assert.throws(()=>store.ingest({...seg,endMs:-1}));
const s=createAgentState();assert.throws(()=>applyAgentEvent(s,{type:'STATE_DELTA',delta:[{op:'replace',path:'/cards',value:[]},{op:'replace',path:'/__proto__',value:{}}]}));assert.equal(s.recommendation,null);assert.throws(()=>applyAgentEvent(s,{type:'STATE_SNAPSHOT',snapshot:{}}));assert.throws(()=>applyAgentEvent(s,{type:'STATE_DELTA',delta:[{op:'replace',path:'/agents',value:[{id:'x'}]}]}));
const events=[],parser=new SSEDecoder(e=>events.push(e));const frame=': ping\r\ndata: '+JSON.stringify({type:'CUSTOM',value:'Tiếng Việt'})+'\r\n\r\n';for(const c of frame)parser.push(c);parser.finish();assert.equal(events[0].value,'Tiếng Việt');assert.throws(()=>{const p=new SSEDecoder(()=>{});p.push('data: {}');p.finish();});
for(const variant of ['oanh-thao-linh','quynh-chi']){const m=JSON.parse(fs.readFileSync(`dist/audio/${variant}/playback-manifest.json`));assert.equal(m.blocks.reduce((n,b)=>n+b.cues.length,0),19);for(const b of m.blocks){assert.ok(fs.statSync(`dist/audio/${variant}/${b.audio}`).size>1000);const set=new Set();for(const c of b.ui_cues){assert.ok(!set.has(c.event));set.add(c.event);const turn=b.cues.find(x=>x.turn_id===c.turn_id);assert.ok(c.time_seconds>=turn.start&&c.time_seconds<=turn.end+.01);}}}
console.log('PASS: transcript revisions/finals, atomic validation, SSE chunks, audio files and all 19 turns in both variants.');

const {routes}=await import('../dist/workflows.js');
const {validateState}=await import('../dist/bridge.js');
assert.equal(routes.length,5);
for(const route of routes){assert.equal(route.path.length,4);assert.equal(new Set(route.systems.map(c=>c.id)).size,route.systems.length);validateState({...createAgentState(),cards:route.systems});for(const card of route.systems){assert.ok(card.evidence.rows.length);assert.ok(card.evidence.conclusion);}}
console.log('PASS: five workflow catalogs, unique card IDs and complete evidence schemas.');
