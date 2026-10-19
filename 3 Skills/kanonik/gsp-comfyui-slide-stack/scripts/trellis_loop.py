# -*- coding: utf-8 -*-
"""trellis_loop.py — satu percobaan varian: bangun workflow dari base, submit, render multi-sudut bertekstur.
Pakai: python trellis_loop.py <variant_id> ; hasil: out/<variant>.png + out/<variant>.glb + hasil print."""
import json, sys, time, urllib.request, subprocess, os

WS = r"C:\Users\TRIAL\workspace\comfyui-check\satellite"
BASE_WF = WS + r"\trellis2_satellite.json"
OUT = WS + r"\out"; os.makedirs(OUT, exist_ok=True)
SERVER = "http://127.0.0.1:8188"

def free_gpu():
    try:
        urllib.request.urlopen(urllib.request.Request(SERVER + "/free", data=json.dumps({"unload": True, "clear_cache": True}).encode(), headers={"Content-Type": "application/json"}), timeout=30).read()
        time.sleep(3)
    except Exception as e:
        print("free gagal:", e)

def submit_and_wait(wf, tag, timeout=2100):
    free_gpu()
    data = json.dumps({"prompt": wf, "client_id": f"loop-{tag}"}).encode()
    pid = json.loads(urllib.request.urlopen(urllib.request.Request(SERVER + "/prompt", data=data, headers={"Content-Type": "application/json"}), timeout=30).read())["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(4)
        h = json.load(urllib.request.urlopen(f"{SERVER}/history/{pid}", timeout=15))
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                for m in st.get("messages", []):
                    if m[0] == "execution_error":
                        return None, f"{m[1].get('node_type')}: {m[1].get('exception_message','')[:200]}"
                return None, "error tanpa detail"
            outs = h[pid].get("outputs", {})
            found = None
            for nid, o in outs.items():
                for key in ("gltf", "3d", "images"):
                    for g in o.get(key, []) or []:
                        if isinstance(g, dict) and str(g.get("filename", "")).endswith(".glb"):
                            found = (g.get("subfolder", "") + "/" + g["filename"]).lstrip("/")
            if found:
                return found, "ok"
            return None, "sukses tapi tak ada file glb di outputs"
    return None, "timeout"

def render(glb_abs, png_abs, views="[(15,-70),(25,110),(60,30),(0,0)]"):
    r = subprocess.run(["uv","run","--python","3.11","--with","trimesh","--with","matplotlib","--with","numpy","--with","pillow","python", WS + r"\render_textured.py", glb_abs, png_abs, views], capture_output=True, text=True, timeout=420)
    return r.returncode == 0, (r.stdout + r.stderr)[-200:]

def variant(v):
    wf = json.load(open(BASE_WF, encoding="utf-8"))
    p = {"res": 1536, "algo": "surface net", "thr": 0.5, "seed": 20260901, "tex": 2048, "img": "satellite_cut.png"}
    p.update(v["params"])
    wf["11"]["inputs"]["image"] = p["img"]
    wf["35"]["inputs"]["target_resolution"] = p["res"]
    wf["38"]["inputs"]["algorithm"] = p["algo"]
    wf["38"]["inputs"]["threshold"] = p["thr"]
    wf["44"]["inputs"]["texture_size"] = p["tex"]
    for sid in ("31","34","36","41"):
        wf[sid]["inputs"]["seed"] = p["seed"]
    wf["50"]["inputs"]["filename_prefix"] = f"satellite/loop_{v['id']}"
    return wf, p

if __name__ == "__main__":
    vid = sys.argv[1]
    variants = json.load(open(WS + r"\variants.json", encoding="utf-8"))
    v = next(x for x in variants if x["id"] == vid)
    wf, p = variant(v)
    rel, msg = submit_and_wait(wf, vid)
    if not rel:
        print(json.dumps({"id": vid, "params": p, "status": "FAIL", "detail": msg}))
        sys.exit(1)
    glb_abs = r"C:\Users\TRIAL\Documents\comfy\ComfyUI\output" + "\\" + rel.replace("/", "\\")
    ok, log = render(glb_abs, OUT + "\\" + vid + ".png")
    shutil_glb = OUT + "\\" + vid + ".glb"
    import shutil; shutil.copyfile(glb_abs, shutil_glb)
    print(json.dumps({"id": vid, "params": p, "status": "RENDER_OK" if ok else "RENDER_FAIL", "glb": shutil_glb, "png": OUT + "\\" + vid + ".png", "render_log": log if not ok else "", "size_glb": os.path.getsize(shutil_glb)}))
