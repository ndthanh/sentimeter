"""Validate generated media and turn timing without API calls."""
import json,math,subprocess,sys
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent/'generated'
def probe(path):
 d=json.loads(subprocess.check_output(['/opt/homebrew/bin/ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)]));return float(d['format']['duration'])
def main():
 m=json.loads((ROOT/'manifest.json').read_text());report={'blocks':[],'warnings':[],'total_audio_seconds':0,'verified_by_listening':False};seen=set()
 for b in m['blocks']:
  duration=probe(ROOT/b['audio']);report['total_audio_seconds']+=duration;last_start=-1;last_end=0
  for cue in b['cues']:
   assert cue['turn_id'] not in seen;seen.add(cue['turn_id'])
   assert all(math.isfinite(cue[k]) for k in ['start','end'])
   assert 0<=cue['start']<=cue['end']<=duration+.1,(b['id'],cue)
   assert cue['start']>=last_start,'Out-of-order turns'
   if cue['start']<last_end-.02:report['warnings'].append({'block':b['id'],'turn':cue['turn_id'],'overlap_seconds':round(last_end-cue['start'],3)})
   last_start=cue['start'];last_end=cue['end']
  report['blocks'].append({'id':b['id'],'duration_seconds':duration,'turns':len(b['cues']),'final_cue_seconds':last_end,'trailing_seconds':round(duration-last_end,3)})
 assert len(seen)==19
 report['max_hold_seconds_at_20_percent']=round(min(60,report['total_audio_seconds']/4),2)
 report['note']='Timestamp structure and media durations checked; perceptual cue accuracy and accent require listening review.'
 (ROOT/'timing-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
