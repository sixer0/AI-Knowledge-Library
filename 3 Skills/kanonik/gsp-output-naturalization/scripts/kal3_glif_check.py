import glob
bad = []
for p in glob.glob("fixtures_k8/*") + ["kal3_gen_fixtures.py"]:
    data = open(p, encoding="utf-8", errors="replace").read()
    for glif, nama in ((chr(0x2014), "U+2014"), (chr(0x00B7), "U+00B7")):
        if glif in data:
            bad.append((p, nama, data.count(glif)))
print("GLIF A1/A2 pada artefak baru:", bad if bad else "NOL")
