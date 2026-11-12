import os, sys, hashlib, json, subprocess, urllib.request, urllib.error
TEAM = "team_DkRXYwyRxWZUQsOAueGPLbBq"; ROOT = sys.argv[1]; API = "https://api.vercel.com"
def req(method, url, data=None, headers=None):
    r = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp: return resp.status, resp.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
files = []
for d, _, fs in os.walk(ROOT):
    for f in sorted(fs):
        p = os.path.join(d, f); rel = os.path.relpath(p, ROOT)
        if rel in ("build.py",) or rel.startswith("."): continue
        b = open(p, "rb").read(); sha = hashlib.sha1(b).hexdigest()
        st, body = req("POST", f"{API}/v2/files?teamId={TEAM}", b, {"Content-Type": "application/octet-stream", "x-vercel-digest": sha, "Content-Length": str(len(b))})
        if st not in (200, 201): print("UPLOAD FAIL", rel, st, body[:200]); sys.exit(1)
        files.append({"file": rel, "sha": sha, "size": len(b)})
print("uploaded", len(files), "files", sum(f["size"] for f in files) // 1024, "KB")
payload = {"name": "cercle-energie", "files": files, "target": "production",
           "projectSettings": {"framework": None, "buildCommand": None, "installCommand": None, "outputDirectory": None}}
st, body = req("POST", f"{API}/v13/deployments?teamId={TEAM}&skipAutoDetectionConfirmation=1", json.dumps(payload).encode(), {"Content-Type": "application/json"})
d = json.loads(body); print(st, {k: d.get(k) for k in ("id", "url", "readyState", "alias", "error")})
json.dump(d, open("/tmp/claude-0/-home-user-11studio-fr/85fbdb28-8fac-5f9b-81ec-450efc44e123/scratchpad/vdeploy.json", "w"))
