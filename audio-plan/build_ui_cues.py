"""Derive precise confirmation cues from returned character alignment, no API calls."""
import json,sys
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent/'generated'
anchors={
 'verify_dob':'Dạ, ngày sinh của chị đã khớp với thông tin trên hệ thống.',
 'verify_national_id':'Em đã đối chiếu, thông tin căn cước của chị trùng khớp.',
 'identity_verified':'Em đã đối chiếu, thông tin căn cước của chị trùng khớp.'
}
def main():
 p=ROOT/'manifest.json';m=json.loads(p.read_text())
 for block in m['blocks']:
  meta=json.loads((ROOT/block['audio'].replace('.mp3','.json')).read_text())
  alignment=meta['response'].get('alignment')
  if not alignment:raise SystemExit('Missing character alignment; manual cue review required.')
  text=''.join(alignment['characters']);ends=alignment['character_end_times_seconds']
  assert len(text)==len(ends)
  block['ui_cues']=[]
  for turn in block['cues']:
   for event in turn['on_end']:
    if event in anchors:
     anchor=anchors[event];idx=text.find(anchor)
     if idx<0 or text.find(anchor,idx+1)>=0:raise SystemExit('Missing or ambiguous anchor: '+event)
     t=ends[idx+len(anchor)-1]
     assert turn['start']<=t<=turn['end']+.02
     mode='character_alignment';quote=anchor
    else:t=turn['end'];mode='turn_boundary';quote=turn['text']
    block['ui_cues'].append({'event':event,'time_seconds':t,'turn_id':turn['turn_id'],'source':mode,'anchor':quote})
   turn['on_end']=[] # Dispatch ui_cues only to prevent duplicate effects.
  block['ui_cues'].sort(key=lambda c:c['time_seconds'])
 m['cue_dispatch']='Use ui_cues only; original turn on_end events moved here.'
 (ROOT/'ui-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
 for b in m['blocks']:
  print(b['id'],[(c['event'],round(c['time_seconds'],3)) for c in b['ui_cues']])
if __name__=='__main__':main()
