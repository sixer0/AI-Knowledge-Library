# -*- coding: utf-8 -*-
"""make_chart.py — diagram vektor deterministik utk slide (jalur non-difusi).
Usage: uv run --python 3.11 --with matplotlib python make_chart.py <out.png>
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "chart.png"
    cats = ["CCTV", "Fiber", "Power", "Grounding"]
    gsp = [72, 58, 45, 30]
    non = [40, 52, 61, 55]
    x = range(len(cats))
    fig, ax = plt.subplots(figsize=(6.4, 2.8), dpi=200)
    w = 0.38
    ax.bar([i - w/2 for i in x], gsp, w, label="GSP (jam engineering)", color="#0B2D5C")
    ax.bar([i + w/2 for i in x], non, w, label="Benchmark industri", color="#9DB6D4")
    ax.set_xticks(list(x)); ax.set_xticklabels(cats, fontsize=9)
    ax.set_ylabel("cakupan domain", fontsize=9)
    ax.legend(fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Cakupan Kapabilitas Engineering GSP", fontsize=11, loc="left", color="#0B2D5C", weight="bold")
    fig.tight_layout()
    fig.savefig(out, transparent=False)
    print("SAVED", out)

if __name__ == "__main__":
    main()
