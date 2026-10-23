from pathlib import Path
import subprocess,sys,tempfile,json
ROOT=Path(__file__).resolve().parents[1]
assert len(sys.argv)==2 and sys.argv[1]=='refs/remotes/origin/candidate'
ref=sys.argv[1]
changed=subprocess.check_output(['git','diff','--name-only','--diff-filter=AM','-z','HEAD',ref,'--','submissions/'],cwd=ROOT).split(b'\0')
files=[x.decode('utf-8') for x in changed if x]
assert len(files)<=20,'Split large submission batches'
count=0
with tempfile.TemporaryDirectory() as td:
 for rel in files:
  p=Path(rel)
  if p.suffix!='.json':continue
  assert p.parts[0]=='submissions' and '..' not in p.parts and not p.is_absolute()
  size=int(subprocess.check_output(['git','cat-file','-s',ref+':'+rel],cwd=ROOT));assert size<=2000000,'Certificate too large'
  data=subprocess.check_output(['git','show',ref+':'+rel],cwd=ROOT);json.loads(data)
  local=Path(td)/f'{count}.json';local.write_bytes(data)
  subprocess.run([sys.executable,str(ROOT/'tools/verify_submission.py'),str(local)],cwd=ROOT,check=True,timeout=120);count+=1
print(f'Verified {count} candidate certificates using trusted base code')
