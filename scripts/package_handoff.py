"""Build a review-only source bundle. Does not commit, push or publish."""
import hashlib,json,re,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEST=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT.parent/'handoff'/'sentimeter-review-2026-10-28.zip'
TOP='sentimeter-review'
FOLDERS=['dist','integration','audio-plan','scripts']
FILES=['README.md','HANDOFF.md','REVIEW-CHECKLIST.md','PLAN-AND-HANDOFF.md','package.json','.gitignore']
blocked={'.git','.openai','node_modules','__pycache__','.DS_Store'}
paths=[ROOT/f for f in FILES]
for folder in FOLDERS:
 paths += [p for p in (ROOT/folder).rglob('*') if p.is_file() and not any(x in blocked for x in p.relative_to(ROOT).parts) and p.suffix not in {'.zip','.tar','.gz','.pyc'}]
paths=sorted(set(paths))
patterns=[rb'sk_[A-Za-z0-9]{24,}',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{30,}',rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',rb'"api_key"\s*:\s*"[^"\s]{12,}"']
manifest=[];data={}
for p in paths:
 rel=p.relative_to(ROOT).as_posix()
 if p.is_symlink() or p.name.startswith('.env') or '.local.' in p.name: raise SystemExit('Forbidden file: '+rel)
 raw=p.read_bytes()
 if p.suffix in {'.json','.js','.ts','.py','.md','.html','.css','.txt','.sse'}:
  if any(re.search(pattern,raw) for pattern in patterns): raise SystemExit('Potential credential in '+rel+'; package aborted')
 data[rel]=raw;manifest.append({'path':rel,'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
report={'package':'sentimeter-review','status':'awaiting-user-review-no-github-push','created_date':'2026-10-28','files':manifest,'exclusions':['.git','.openai','.env*','*.local.*','nested archives','node_modules'], 'secret_scan':'No matches for configured high-confidence key patterns; not a comprehensive security audit.'}
data['PACKAGE-MANIFEST.json']=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
DEST.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(DEST,'w',zipfile.ZIP_DEFLATED) as z:
 for rel,raw in data.items():z.writestr(TOP+'/'+rel,raw)
for name in ['HANDOFF.md','REVIEW-CHECKLIST.md']:(DEST.parent/name).write_bytes((ROOT/name).read_bytes())
checks=[]
for p in [DEST,DEST.parent/'HANDOFF.md',DEST.parent/'REVIEW-CHECKLIST.md']:
 checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)
(DEST.parent/'CHECKSUMS.sha256').write_text('\n'.join(checks)+'\n')
print(json.dumps({'archive':str(DEST),'files':len(data),'bytes':DEST.stat().st_size,'audio_files':sum(x.endswith('.mp3') for x in data),'secret_pattern_matches':0}))
