# Rekonstruksi cadangan pra-edit gsp_deleg_watch.py (buang blok yang ditambahkan 18-10)
import hashlib, io

P = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_deleg_watch.py"
BAK = P + ".bak-20261018sysnet"
txt = open(P, encoding="utf-8").read()
start = txt.index("Prasyarat jalan (terukur SYS-NET-RT-PAPAN-1018")
end = txt.index('"""', start)
pre = txt[:start].rstrip("\n") + "\n" + txt[end:]
open(BAK, "w", encoding="utf-8", newline="").write(pre)
n_pre = pre.count("\n")
sha_pre = hashlib.sha256(pre.encode()).hexdigest()[:16]
sha_post = hashlib.sha256(txt.encode()).hexdigest()[:16]
print(f"cadangan: {BAK}")
print(f"pra-edit: {n_pre} baris, sha16 {sha_pre}, {len(pre.encode())} B")
print(f"pasca   : {txt.count(chr(10))} baris, sha16 {sha_post}, {len(txt.encode())} B")
assert n_pre == 351, "baris pra-edit harus 351 (tercatat sebelum sunting)"
print("VERIFIKASI: cadangan pra-edit cocok basal tercatat (351 baris). OK")
