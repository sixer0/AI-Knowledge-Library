import glob
for p in ["kal3_gen_fixtures.py", "kal3_glif_check.py"] + sorted(glob.glob("fixtures_k8/*")):
    data = open(p, "rb").read()
    print(p, len(data), "CR=", data.count(b"\r"))
