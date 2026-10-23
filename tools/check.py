from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
count=0
omitted=json.loads((ROOT/'external-inputs.json').read_text())['omitted_archival_assets']
skipped=[]
for rel in ['research/manifest.json','research/round2/manifest.json','research/distribution-prep/manifest.json']:
 path=ROOT/rel
 if not path.exists():
  assert rel!='research/manifest.json','Initial evidence manifest missing'
  continue
 for file,expected in json.loads(path.read_text())['sha256'].items():
  if file in omitted and not (ROOT/file).exists():
   assert omitted[file]['sha256']==expected,'Incorrect omitted-asset record'
   skipped.append(file)
   continue
  assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==expected,f'Changed frozen evidence: {file}'
  count+=1
assert json.loads((ROOT/'discover.json').read_text())['review']['paused'] is False
subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=True)
print(f'Verified {count} frozen evidence hashes; tests passed.')

print('External reference snapshots intentionally not bundled:', ', '.join(skipped))
