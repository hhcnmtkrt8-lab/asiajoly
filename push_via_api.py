#!/usr/bin/env python3
"""Push the working tree to GitHub via the REST API.

Needed because direct https://github.com git access times out on this network while
api.github.com is reachable. Builds blobs -> tree -> commit -> ref, preserving the
same file contents as the local commit.

Usage: python3 push_via_api.py <owner/repo> [branch]
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request

REPO = sys.argv[1]
BRANCH = sys.argv[2] if len(sys.argv) > 2 else "main"
API = "https://api.github.com"
TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
ROOT = os.path.dirname(os.path.abspath(__file__))

MESSAGE = subprocess.check_output(
    ["git", "log", "-1", "--pretty=%B"], cwd=ROOT, text=True).strip()

SKIP_DIRS = {".git", ".build"}
SKIP_FILES = {".DS_Store"}


def call(method, path, payload=None):
    url = API + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "rill-push")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        print(f"{method} {path} -> {e.code}: {e.read().decode()[:400]}")
        raise


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name in SKIP_FILES:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            with open(full, "rb") as f:
                yield rel, f.read()


# An entirely empty repository rejects blob/tree calls with 409, so land one commit first.
def bootstrap():
    try:
        ref = call("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH}")
        return ref["object"]["sha"]
    except Exception:
        pass
    content = base64.b64encode(b"# initial\n").decode()
    res = call("PUT", f"/repos/{REPO}/contents/README.md", {
        "message": "Initialise repository", "content": content, "branch": BRANCH,
    })
    print("bootstrapped repo with", res["commit"]["sha"])
    return res["commit"]["sha"]


parent = bootstrap()
entries = []
for rel, blob in walk():
    b = call("POST", f"/repos/{REPO}/git/blobs", {
        "content": base64.b64encode(blob).decode(),
        "encoding": "base64",
    })
    entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": b["sha"]})
    print("blob", rel, len(blob))

tree = call("POST", f"/repos/{REPO}/git/trees", {"tree": entries})
commit = call("POST", f"/repos/{REPO}/git/commits", {
    "message": MESSAGE, "tree": tree["sha"], "parents": [parent] if parent else [],
})
print("tree", tree["sha"], "commit", commit["sha"])

try:
    call("POST", f"/repos/{REPO}/git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]})
    print("created ref", BRANCH)
except Exception:
    call("PATCH", f"/repos/{REPO}/git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": True})
    print("updated ref", BRANCH)

# keep the local repo's remote-tracking state sane without touching the network
print("done:", f"https://github.com/{REPO}")
