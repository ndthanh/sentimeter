import json,shutil,sys,zipfile
from pathlib import Path
p=Path(sys.argv[1]).resolve();m=json.loads((p/'ui-manifest.json').read_text());voice_ids={}
for i,b in enumerate(m['blocks'],1):
 raw=json.loads((p/b['audio'].replace('.mp3','.json')).read_text())
 for segment in raw['response']['voice_segments']:
  turn=b['cues'][segment['dialogue_input_index']];voice_ids[turn['speaker']]=segment['voice_id']
 name=f'{i:02}-{b["id"]}.mp3';shutil.copyfile(p/b['audio'],p/name);b['audio']=name
(p/'playback-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(p/'voice-selection.json').write_text(json.dumps({'voice_ids':voice_ids,'script_sha256':m['script_sha256'],'note':'This variant has its own audio timing. Do not reuse another variant cue manifest.'},indent=2))
archive=p.parent/(p.name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in ['01-verification.mp3','02-request.mp3','03-resolution.mp3','playback-manifest.json','timing-report.json','voice-selection.json']:
  z.write(p/name,name)
print(str(archive))
