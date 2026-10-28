"""Offline preview by default. Paid API calls require --generate and exact approved SHA.
Use only after the human has approved script.vi.json. API key is read from environment.
"""
import argparse,base64,hashlib,json,os,sys,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser();p.add_argument('--script',type=Path,default=ROOT/'script.vi.json');p.add_argument('--output',type=Path,default=ROOT/'generated');p.add_argument('--config',type=Path,default=Path.home()/'.config/sentimeter/elevenlabs.local.json');p.add_argument('--generate',action='store_true');p.add_argument('--approved-sha256');a=p.parse_args()
 raw=a.script.read_bytes();digest=hashlib.sha256(raw).hexdigest();script=json.loads(raw)
 print('Script SHA256:',digest)
 for block in script['blocks']:
  count=sum(len(t['text']) for t in block['turns'])
  if count>2000:raise SystemExit(f"Block {block['id']} exceeds 2,000 characters; split before generation.")
  print(f"{block['id']}: {len(block['turns'])} turns, {count} characters; gate={block['start_gate']}")
 if not a.generate:
  print('DRY RUN: no network requests. Await human script approval before --generate.');return
 if a.approved_sha256!=digest:raise SystemExit('Refusing generation: approved script SHA is missing or does not match.')
 config=json.loads(a.config.read_text()) if a.config.exists() else {}
 key=os.environ.get('ELEVENLABS_API_KEY') or config.get('api_key');voices={r:os.environ.get('ELEVENLABS_'+r.upper()+'_VOICE_ID') or config.get(r+'_voice_id') for r in ['operator','customer']}
 if not key or not all(voices.values()):raise SystemExit('Fill the private configuration file with API key and two voice IDs, or set the corresponding environment variables.')
 if voices['operator']==voices['customer']:raise SystemExit('Choose two distinct female Vietnamese voice IDs.')
 a.output.mkdir(parents=True,exist_ok=True);manifest={'script_sha256':digest,'language':'vi','blocks':[]}
 for block in script['blocks']:
  body={'inputs':[{'text':t['text'],'voice_id':voices[t['speaker']]} for t in block['turns']],'model_id':script['model_id'],'language_code':'vi'}
  fingerprint=hashlib.sha256(json.dumps(body,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
  stem=block['id']+'-'+fingerprint[:12];meta=a.output/(stem+'.json');audio=a.output/(stem+'.mp3')
  if meta.exists() and audio.exists():
   record=json.loads(meta.read_text());print('Reusing:',block['id'])
  else:
   req=urllib.request.Request('https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps?output_format=mp3_44100_128',data=json.dumps(body,ensure_ascii=False).encode(),headers={'xi-api-key':key,'Content-Type':'application/json'},method='POST')
   try:
    with urllib.request.urlopen(req,timeout=180) as response:result=json.load(response)
   except urllib.error.HTTPError as e:raise SystemExit(f'API HTTP {e.code} for {block["id"]}. No automatic retry; inspect account before retrying.') from None
   except urllib.error.URLError:raise SystemExit('Network failure. No automatic retry: generation may already have been charged.') from None
   payload=base64.b64decode(result.pop('audio_base64'),validate=True)
   record={'fingerprint':fingerprint,'audio':audio.name,'response':result}
   audio.write_bytes(payload);meta.write_text(json.dumps(record,ensure_ascii=False,indent=2))
  segments=record['response'].get('voice_segments',[]);cues=[]
  for i,turn in enumerate(block['turns']):
   matches=[s for s in segments if s.get('dialogue_input_index')==i]
   if not matches:raise SystemExit(f'Missing timing for {turn["id"]}; saved audio requires manual review. Do not fabricate timestamps.')
   cues.append({'turn_id':turn['id'],'speaker':turn['speaker'],'text':turn['text'],'start':min(s['start_time_seconds'] for s in matches),'end':max(s['end_time_seconds'] for s in matches),'on_end':turn['on_end']})
  manifest['blocks'].append({'id':block['id'],'start_gate':block['start_gate'],'audio':audio.name,'cues':cues})
  print('Prepared:',block['id'])
 (a.output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print('Saved audio and manifest. Listen and verify pronunciation/timing before wiring the UI.')
if __name__=='__main__':main()
