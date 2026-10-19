#!/usr/bin/env python3
"""gate_check.py - deterministic completeness check of a deep-dive record.

Part of the gsp-deep-dive skill (mission DDV-STD-1009, general standard
GSP-DD-001). Stdlib only, Python >= 3.10. No network, no LLM, no eval().
This tool judges COMPLETENESS and measurement correctness of a record folder
against the general gates G0/G1/G3/G4 plus the profile-specific gates named in
the profile manifest. It never judges business outcomes; see
references/umum/gates.md for the predicate definitions.

Usage:
    python gate_check.py <record-dir> [--profile <name>]
                         [--gate G0|G1|G2T|G2K|G3|G4|all]
                         [--json] [--master-register <csv>]

Without --profile only the general gates run (G0 general predicates, G1, G3,
G4). With --profile <name> the manifest scripts/profiles/<name>.json is loaded
and its gate extensions run under the profile gate ids (typically G2T/G2K for
profile B1 vendor). Exit codes are unchanged from the dd-vendor era:
    0 = all selected gates pass
    1 = at least one FAIL (names printed)
    2 = misuse (bad profile, missing manifest, unreadable folder/register)

Note on the prohibited-vocabulary register (Daftar-A): tokens are assembled
from fragments below so this skill folder stays clean under the same
word-boundary scan it performs (SC-3). The canonical register text lives in
Annex C of the issued standard; this file is the executable mirror.

Regression contract: with --profile vendor this checker must reproduce the
verdicts of the dd-vendor era gate_check.py on identical fixtures (blueprint
02b section 4 term 3). The vendor manifest replicates the old G0-G4
predicates exactly.
"""

import argparse
import csv
import json
import os
import re
import sys

# ---------------------------------------------------------------- schemas ---

DOC_REGISTER_SCHEMA = ["document_name", "date_received", "pages", "doc_type",
                       "status", "what_is_missing"]
FLAG_SEED_SCHEMA = ["class_id", "class_name", "status", "evidence_source", "date"]
FIVE_LAYER_SCHEMA = ["layer", "question_id", "question", "answer", "maturity",
                     "maturity_evidence", "dependency_and_country",
                     "evidence_source", "evidence_date", "ceiling_applied",
                     "unknown_search_route"]
PROSPECT_MAP_SCHEMA = ["institution", "user_unit", "decision_role",
                       "budget_source", "budget_amount", "budget_visibility",
                       "procurement_route", "route_history_ref",
                       "incumbent_supplier", "contract_expiry_estimate",
                       "time_window", "partnership_model",
                       "pipeline_value_estimate", "assumptions_open",
                       "gsp_additions", "gsp_cost", "source_url",
                       "access_date", "query_count", "saturation_note"]
BUYER_MAP_SCHEMA = ["capability", "buyer_institution", "user_unit",
                    "contact_role_if_visible", "demand_evidence",
                    "evidence_source", "evidence_date", "language_requirement",
                    "local_reception_note", "search_classes_touched"]
CLAIMS_SCHEMA = ["claim_id", "vendor_text_verbatim", "source_document",
                 "page_or_location", "claim_type", "test_method",
                 "stated_value", "recomputed_value", "variance_pct",
                 "evidence_label", "carrier_load", "status",
                 "verification_account", "date", "lane"]
QUERY_LOG_SCHEMA = ["query_id", "date", "route_class", "language",
                    "query_or_url", "result_summary", "evidence_status"]

LAYERS = ["L1-Source", "L2-Processing", "L3-Analytics-AI", "L4-Delivery",
          "L5-Operations"]
QUESTIONS = ["Q%d" % i for i in range(1, 8)]
FLAG_CLASSES = ["FL-%d" % i for i in range(1, 8)]
DESCRIPTIVE_STATUS = re.compile(
    r"^(blocker-candidate|caution|note|clear|unresolved-after-\d+-searches)$",
    re.IGNORECASE)
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")

# Frozen indicator weights (matches Annex A of the general standard; revision
# only through the official Decision Log).
WEIGHTS = [15, 15, 15, 10, 10, 10, 10, 10, 5]

# Prohibited-vocabulary register (Daftar-A), assembled from fragments.
def _t(*parts):
    return "".join(parts)

DAFTAR_A = [
    _t("G", "O"),
    _t("NO", "-G", "O"),
    _t("CONDI", "TIONAL"),
    _t("HO", "LD"),
    _t("DR", "OP"),
    _t("PA", "RK"),
    _t("PRO", "CEED"),
    _t("kill criterion ", "fi", "red"),
    _t("fi", "red"),
    _t("reco", "mmend"),
    _t("reco", "mmendation"),
    _t("ad", "visable"),
    _t("we ", "suggest"),
    _t("should ", "partner"),
    _t("should not ", "partner"),
    _t("not ", "via", "ble"),
    _t("via", "ble"),
]
DAFTAR_A_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:" +
    "|".join(re.escape(t) for t in DAFTAR_A) +
    r")(?![A-Za-z0-9])", re.IGNORECASE)
SLOT_EXEMPT = re.compile(r"director\s+decision\s*:", re.IGNORECASE)

# Nomination line keys: general key is Object:; legacy key Vendor: is accepted
# as an alias so the frozen vendor fixtures stay byte-identical (AD-1 era
# schema retention). At least one of the two must carry a value.
OBJECT_KEYS = ("Object:", "Vendor:")

# ---------------------------------------------------------------- helpers ---

class Report:
    def __init__(self, as_json=False):
        self.checks = []
        self.n = 0
        self.as_json = as_json

    def add(self, gate, name, ok, reason):
        self.n += 1
        self.checks.append({"n": self.n, "gate": gate, "name": name,
                            "status": "PASS" if ok else "FAIL",
                            "reason": reason})
        if not self.as_json:
            print("CHECK %d: %s - %s | %s"
                  % (self.n, "PASS" if ok else "FAIL", name, reason))

    def info(self, text):
        if not self.as_json:
            print("INFO - %s" % text)

    def failed(self, gate=None):
        return [c for c in self.checks
                if c["status"] == "FAIL" and (gate is None or c["gate"] == gate)]

    def total(self, gate=None):
        return [c for c in self.checks if gate is None or c["gate"] == gate]


def read_text(path):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return fh.read()
    except OSError:
        return None


def read_csv(path, schema):
    """Return (rows, error). error None on success."""
    if not os.path.isfile(path):
        return None, "missing file"
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != schema:
                return None, ("header mismatch: expected %s, found %s"
                              % (",".join(schema),
                                 ",".join(reader.fieldnames or [])))
            return list(reader), None
    except OSError as exc:
        return None, "unreadable (%s)" % exc.strerror


def content_lines(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def scan_daftar_a(paths):
    """Return list of (path, lineno, snippet) hits outside exempt lines."""
    hits = []
    for path in sorted(paths):
        text = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if SLOT_EXEMPT.search(line):
                continue
            m = DAFTAR_A_RE.search(line)
            if m:
                hits.append((path, i, m.group(0)))
    return hits


def saturation_ok(path):
    """True if the file carries query count, exhausted classes and date."""
    text = read_text(path)
    if text is None:
        return False, "missing file"
    missing = []
    if not re.search(r"^Query count:\s*\d+\s*$", text, re.MULTILINE):
        missing.append("Query count: <int>")
    if not re.search(r"^Route classes exhausted:\s*\d+/8\s*$", text, re.MULTILINE):
        missing.append("Route classes exhausted: <n>/8")
    if not re.search(r"^Date:\s*\d{4}-\d{2}-\d{2}\s*$", text, re.MULTILINE):
        missing.append("Date: YYYY-MM-DD")
    if missing:
        return False, "missing numbered lines: " + "; ".join(missing)
    return True, "numbered saturation statement present"


def object_slug(nom):
    """Object slug from nomination.md, accepting Object: and legacy Vendor:."""
    for key in OBJECT_KEYS:
        m = re.search(r"^%s\s*(.+)$" % re.escape(key), nom, re.MULTILINE)
        if m and m.group(1).strip():
            return m.group(1).strip().lower()
    return None


# ------------------------------------------------------------------- gates --

class MasterRegisterMisuse(Exception):
    """--master-register supplied but unusable; Annex B maps this to exit 2."""


def gate_g0(rec, rep, args):
    g = "G0"
    nom = read_text(os.path.join(rec, "00-record", "nomination.md"))
    em = read_text(os.path.join(rec, "00-record", "entity-match.md"))
    if em is None:
        rep.add(g, "entity-match.md present", False, "file missing")
    else:
        has_result = "Entity match:" in em
        has_date = bool(ISO_DATE.search(em))
        rep.add(g, "entity-match dated result",
                has_result and has_date,
                "token 'Entity match:' %s, ISO date %s"
                % ("found" if has_result else "absent",
                   "found" if has_date else "absent"))

    # duplicate dossier against master register when supplied
    if args.master_register:
        # DEF-2 fix (card t_ca8b0b0a, Annex B): an unreadable or malformed
        # --master-register is misuse -> exit 2, never a silent PASS on the
        # duplicate check.
        mr = args.master_register
        if not os.path.isfile(mr):
            raise MasterRegisterMisuse("file not found: %s" % mr)
        try:
            header = read_header(mr)
            rows, err = (read_csv(mr, list(header)) if header
                         else (None, "empty or headerless CSV"))
        except UnicodeDecodeError:
            raise MasterRegisterMisuse("not UTF-8 decodable: %s" % mr)
        if not header:
            raise MasterRegisterMisuse("empty or headerless CSV: %s" % mr)
        if err:
            raise MasterRegisterMisuse("%s: %s" % (mr, err))
        obj = object_slug(nom) if nom else None
        if not obj:
            raise MasterRegisterMisuse(
                "object name not found in nomination.md (no 'Object:' or "
                "'Vendor:' line); duplicate check cannot run against %s"
                % os.path.basename(mr))
        dup = False
        for row in rows:
            joined = " ".join(v or "" for v in row.values()).lower()
            if obj in joined:
                dup = True
                break
        rep.add(g, "no duplicate dossier (master register)", not dup,
                "slug found in master register" if dup
                else "checked against %s (%d rows)"
                     % (os.path.basename(mr), len(rows)))
    else:
        rep.info("G0 duplicate-dossier check skipped: no --master-register given")

    rows, err = read_csv(os.path.join(rec, "00-record", "document-register.csv"),
                         DOC_REGISTER_SCHEMA)
    if err:
        rep.add(g, "document-register.csv complete", False, err)
    else:
        blanks = [r.get("document_name", "?") for r in rows
                  if not (r.get("what_is_missing") or "").strip()]
        rep.add(g, "document-register.csv complete", not blanks,
                "%d rows; what_is_missing blank for: %s"
                % (len(rows), ", ".join(blanks)) if blanks
                else "%d rows, what_is_missing filled everywhere" % len(rows))

    pt = read_text(os.path.join(rec, "00-record", "thesis.md"))
    legacy = False
    if pt is None:
        pt = read_text(os.path.join(rec, "00-record", "prospect-thesis.md"))
        legacy = pt is not None
    if pt is None:
        rep.add(g, "thesis 3-5 lines", False,
                "neither thesis.md nor legacy prospect-thesis.md present")
    else:
        n = len(content_lines(pt))
        # Legacy filename keeps the exact old check name so the vendor
        # regression diff stays byte-identical (blueprint 02b section 4 term 3).
        rep.add(g, "prospect-thesis 3-5 lines" if legacy else "thesis 3-5 lines",
                3 <= n <= 5, "%d content lines" % n)

    rows, err = read_csv(os.path.join(rec, "00-record", "flag-register.seed.csv"),
                         FLAG_SEED_SCHEMA)
    if err:
        rep.add(g, "seed flag register has 7 classes", False, err)
    else:
        ids = [r["class_id"].strip() for r in rows]
        ok = ids == FLAG_CLASSES
        rep.add(g, "seed flag register has 7 classes", ok,
                "class ids %s" % ("FL-1..FL-7 exact" if ok else str(ids)))

    if nom is None:
        rep.add(g, "tier and deadline recorded", False, "nomination.md missing")
    else:
        tier = re.search(r"^Tier:\s*(T[123])\s*$", nom, re.MULTILINE)
        dl = re.search(r"^Deadline:\s*(\d{4}-\d{2}-\d{2})\s*$", nom, re.MULTILINE)
        rep.add(g, "tier and deadline recorded", bool(tier and dl),
                "tier %s, deadline %s" % (tier.group(1) if tier else "absent",
                                          dl.group(1) if dl else "absent"))


def gate_g1(rec, rep):
    g = "G1"
    sr_path = os.path.join(rec, "01-screen", "screen-report.md")
    sr = read_text(sr_path)
    if sr is None:
        rep.add(g, "screen-report.md present", False, "file missing")
        return
    rep.add(g, "screen-report.md present", True, sr_path)

    rows = [l for l in sr.splitlines() if re.match(r"^\|\s*FL-\d", l)]
    bad = []
    for line in rows:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[1] or not cells[2] or not cells[3]:
            bad.append(cells[0] if cells else line)
        elif not DESCRIPTIVE_STATUS.match(cells[1]):
            bad.append(cells[0] + " status '" + cells[1] + "'")
    rep.add(g, "flag first-pass 7 dated rows", len(rows) == 7 and not bad,
            "%d rows%s" % (len(rows), "; defects: " + ", ".join(bad) if bad else
                           ", all rows status+source+date with descriptive labels"))

    ledger, err = read_csv(os.path.join(rec, "claims-ledger.csv"), CLAIMS_SCHEMA)
    if err:
        rep.add(g, "claims ledger backs cited claims", False, err)
        return
    ids = {r["claim_id"].strip() for r in ledger}
    cited = set(re.findall(r"CLM-\d+", sr))
    dangling = sorted(c for c in cited if c not in ids)
    rep.add(g, "claims ledger backs cited claims",
            bool(ledger) and not dangling,
            "%d ledger rows; cited %d; dangling: %s"
            % (len(ledger), len(cited), ", ".join(dangling) if dangling else "none"))

    hits = scan_daftar_a([sr_path,
                          os.path.join(rec, "claims-ledger.csv"),
                          os.path.join(rec, "risk-register.csv"),
                          os.path.join(rec, "ask-list.csv")])
    rep.add(g, "prohibited-vocabulary scan (screen surface)", not hits,
            "0 hits" if not hits else
            "; ".join("%s:%d '%s'" % h for h in hits[:5]))


def gate_g3(rec, rep):
    g = "G3"
    bt_path = os.path.join(rec, "04-package", "blok-temuan.md")
    bt = read_text(bt_path)
    if bt is None:
        rep.add(g, "blok-temuan.md present", False, "file missing")
        return
    rep.add(g, "blok-temuan.md present", True, bt_path)

    ledger, err = read_csv(os.path.join(rec, "claims-ledger.csv"), CLAIMS_SCHEMA)
    if err:
        rep.add(g, "dimension cards reference real claims", False, err)
        return
    ids = {r["claim_id"].strip(): r for r in ledger}

    cards = {}
    for line in bt.splitlines():
        m = re.match(r"^\s*(DIM-\d)\s*\|.*?score:\s*(\d)\s*\|\s*claims:\s*"
                     r"([A-Za-z0-9,\s\-]+)", line)
        if m:
            cards[m.group(1)] = (int(m.group(2)),
                                 [c.strip() for c in m.group(3).split(",") if c.strip()])
    want = ["DIM-%d" % i for i in range(1, 10)]
    missing = [d for d in want if d not in cards]
    rep.add(g, "nine dimension cards present", not missing,
            "DIM-1..DIM-9 found" if not missing else "missing: " + ", ".join(missing))

    dangling = []
    ceiling_bad = []
    for dim in want:
        if dim not in cards:
            continue
        score, claims = cards[dim]
        for cid in claims:
            if cid not in ids:
                dangling.append("%s -> %s" % (dim, cid))
        labels = {ids[c]["evidence_label"].strip().upper()
                  for c in claims if c in ids}
        if labels == {"VENDOR-CLAIMED"} and score > 3:
            ceiling_bad.append("%s score %d over vendor-claim-only evidence"
                               % (dim, score))
    rep.add(g, "dimension scores point at real ledger claims", not dangling,
            "all claim ids resolve" if not dangling else "; ".join(dangling))
    rep.add(g, "mechanical ceiling 3 on vendor-claim-only dimensions",
            not ceiling_bad,
            "ceiling satisfied" if not ceiling_bad else "; ".join(ceiling_bad))

    m = re.search(r"^Indicator:\s*([\d.]+)\s*$", bt, re.MULTILINE)
    sentence = "arithmetic indicator only; no band-to-verdict mapping" in bt
    if not m or len(cards) != 9:
        rep.add(g, "indicator equals frozen-weight recomputation", False,
                "Indicator line or nine cards unavailable for recomputation")
    else:
        printed = float(m.group(1))
        expected = sum(w * cards["DIM-%d" % i][0] for i, w in enumerate(WEIGHTS, 1)) / 5.0
        rep.add(g, "indicator equals frozen-weight recomputation",
                abs(printed - expected) <= 0.05 and sentence,
                "printed %.1f vs parser %.1f; companion sentence %s"
                % (printed, expected, "present" if sentence else "MISSING"))

    bc = read_text(os.path.join(rec, "04-package", "blind-challenge.md"))
    ok = bc is not None and bc.strip() and "Reviewer account:" in bc
    rep.add(g, "blind completeness challenge from separate account", ok,
            "blind-challenge.md present and names reviewer account" if ok
            else "missing, empty, or reviewer account not named")

    all_files = []
    for root, _dirs, files in os.walk(rec):
        for f in files:
            if f.endswith((".md", ".csv")):
                all_files.append(os.path.join(root, f))
    hits = scan_daftar_a(all_files)
    rep.add(g, "prohibited-vocabulary scan (whole record)", not hits,
            "0 hits across %d files" % len(all_files) if not hits
            else "; ".join("%s:%d '%s'" % h for h in hits[:5]))


def gate_g4(rec, rep):
    g = "G4"
    closeout = os.path.join(rec, "05-closeout")
    for name, label in [("il-promotion-note.md", "IL promotion note"),
                        ("master-register-update.md", "master register update")]:
        text = read_text(os.path.join(closeout, name))
        rep.add(g, label + " recorded", text is not None and bool(text.strip()),
                name + (" present and non-empty" if text and text.strip()
                        else " missing or empty"))
    rt = read_text(os.path.join(closeout, "refresh-triggers.md"))
    n = len(content_lines(rt)) if rt else 0
    rep.add(g, "refresh triggers listed (>= 4)", n >= 4, "%d trigger lines" % n)

    nom = read_text(os.path.join(rec, "00-record", "nomination.md")) or ""
    first = re.search(r"^First real DD:\s*(yes|no)\s*$", nom, re.MULTILINE | re.IGNORECASE)
    if first and first.group(1).lower() == "yes":
        attached = any(os.path.isfile(os.path.join(closeout, f))
                       for f in ("validation-first-arrival.md",
                                 "validation-first-arrival.csv"))
        rep.add(g, "first-real-DD validation form attached", attached,
                "form present in 05-closeout/" if attached
                else "nomination says First real DD: yes but no form attached")
    else:
        rep.add(g, "first-real-DD validation form attached", True,
                "not required (First real DD: no)")


# ------------------------------------------------- generic lane gate engine --

def run_lane_gate(rec, rep, gid, spec):
    """Generic lane-dissection gate driven by a profile-manifest spec.

    spec keys:
      grid: {path, schema, min_rows, cap_column_pairs? ...}
      saturation: [relative paths that must carry numbered statements]
      query_log: relative path whose route_class column must cover 1..8
    """
    grid = spec.get("grid")
    if grid:
        rows, err = read_csv(os.path.join(rec, grid["path"]), grid["schema"])
        label = "%s grid complete" % os.path.basename(grid["path"])
        if err:
            rep.add(gid, label, False, err)
        else:
            rep.add(gid, "%s >= %d rows" % (os.path.basename(grid["path"]),
                                            grid.get("min_rows", 1)),
                    len(rows) >= grid.get("min_rows", 1),
                    "%d data rows" % len(rows))
            empties = []
            for idx, r in enumerate(rows, 2):
                for col in grid["schema"]:
                    if not (r.get(col) or "").strip():
                        empties.append("row %d col %s" % (idx, col))
            rep.add(gid, "%s zero empty cells" % os.path.basename(grid["path"]),
                    not empties,
                    "0 empty cells" if not empties
                    else "%d empty cells: %s" % (len(empties), "; ".join(empties[:6])))
            unpaired = []
            ans_col = grid.get("answer_column", "answer")
            mat_col = grid.get("maturity_column")
            route_col = grid.get("route_column", "unknown_search_route")
            for idx, r in enumerate(rows, 2):
                ans = (r.get(ans_col) or "").strip().upper()
                mat = (r.get(mat_col) or "").strip().upper() if mat_col else ""
                route = (r.get(route_col) or "").strip()
                if (ans == "UNKNOWN" or mat == "UNKNOWN") and (not route or route == "n/a"):
                    unpaired.append("row %d" % idx)
            rep.add(gid, "UNKNOWN paired with search route", not unpaired,
                    "all UNKNOWN rows carry a route" if not unpaired
                    else "unpaired: " + ", ".join(unpaired))
            ev_col = grid.get("evidence_column")
            cap_col = grid.get("ceiling_column")
            if ev_col and mat_col and cap_col:
                capped = []
                for idx, r in enumerate(rows, 2):
                    ev = (r.get(ev_col) or "").strip().upper()
                    mat = (r.get(mat_col) or "").strip().upper()
                    ceil = (r.get(cap_col) or "").strip().upper()
                    if ev == "VENDOR-CLAIMED":
                        if mat in {"M3", "M4", "M5"}:
                            capped.append("row %d maturity %s above M2" % (idx, mat))
                        elif mat == "M2" and ceil != "Y":
                            capped.append("row %d M2 without %s=Y" % (idx, cap_col))
                rep.add(gid, "self-report-only maturity capped at M2", not capped,
                        "ceiling satisfied" if not capped else "; ".join(capped))
    for sat in spec.get("saturation", []):
        ok, reason = saturation_ok(os.path.join(rec, sat))
        rep.add(gid, "saturation numbered: %s" % sat, ok, reason)
    ql = spec.get("query_log")
    if ql:
        rows, err = read_csv(os.path.join(rec, ql), QUERY_LOG_SCHEMA)
        if err:
            rep.add(gid, "query log ladder covers 8 route classes", False, err)
        else:
            classes = {(r.get("route_class") or "").strip() for r in rows}
            missing = [str(i) for i in range(1, 9) if str(i) not in classes]
            rep.add(gid, "query log ladder covers 8 route classes", not missing,
                    "classes seen: %s" % ",".join(sorted(classes))
                    + ("" if not missing else "; missing: " + ",".join(missing)))


def run_map_gate(rec, rep, gid, spec):
    """Generic map gate: required CSVs with exact headers, non-empty, plus
    per-column rules (url/date/workbook-pointer) shared across profiles."""
    checks = []
    maps = spec.get("maps", [])
    for m in maps:
        rows, err = read_csv(os.path.join(rec, m["path"]), m["schema"])
        checks.append((m, rows, err))
    present = all((e is None and bool(r)) for _m, r, e in checks)
    detail = "; ".join("%s: %s (%d rows)"
                       % (os.path.basename(m["path"]), e or "ok", len(r or []))
                       for m, r, e in checks)
    rep.add(gid, "required maps present with exact headers", present, detail)
    for m, rows, err in checks:
        if not rows:
            continue
        bad = []
        for idx, r in enumerate(rows, 2):
            url_col = m.get("url_column")
            if url_col:
                url = (r.get(url_col) or "").strip()
                if not url.lower().startswith(("http://", "https://")):
                    bad.append("row %d %s" % (idx, url_col))
            date_col = m.get("date_column")
            if date_col and not ISO_DATE.fullmatch((r.get(date_col) or "").strip()):
                bad.append("row %d %s" % (idx, date_col))
            wb_col = m.get("workbook_column")
            if wb_col and ".xlsx" not in (r.get(wb_col) or "").lower():
                bad.append("row %d %s is a bare literal (must point into the "
                           "economy workbook)" % (idx, wb_col))
        if url_col or date_col or wb_col:
            rep.add(gid, "%s rows sourced%s" % (os.path.basename(m["path"]),
                                                "/workbook-backed" if wb_col else ""),
                    not bad,
                    "all rows carry required source fields"
                    if not bad else "; ".join(bad))
    for sat in spec.get("saturation", []):
        ok, reason = saturation_ok(os.path.join(rec, sat))
        rep.add(gid, "saturation numbered: %s" % sat, ok, reason)


# ------------------------------------------------------------------- main ---

def read_header(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            return next(csv.reader(fh), None)
    except OSError:
        return None


def load_profile(name):
    """Load scripts/profiles/<name>.json next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "profiles", "%s.json" % name)
    if not os.path.isfile(path):
        available = sorted(f[:-5] for f in os.listdir(os.path.join(here, "profiles"))
                           if f.endswith(".json")) if os.path.isdir(os.path.join(here, "profiles")) else []
        raise KeyError("profile manifest not found: %s (available: %s)"
                       % (path, ", ".join(available) or "none"))
    text = read_text(path)
    if text is None:
        raise KeyError("profile manifest unreadable: %s" % path)
    return json.loads(text)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gate_check.py")
    ap.add_argument("record", help="deep-dive record folder docs/<date>_dd-<object>/")
    ap.add_argument("--profile", default=None,
                    help="profile name (vendor|technology|market|client-integration); "
                         "loads scripts/profiles/<name>.json for gate extensions")
    ap.add_argument("--gate", default="all",
                    choices=["G0", "G1", "G2T", "G2K", "G3", "G4", "all"])
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--master-register", default=None,
                    help="optional master register CSV for duplicate check")
    args = ap.parse_args(argv)

    rec = args.record
    if not os.path.isdir(rec):
        print("ERROR: deep-dive record folder not readable: %s" % rec)
        return 2

    manifest = None
    if args.profile:
        try:
            manifest = load_profile(args.profile)
        except (KeyError, ValueError) as exc:
            print("ERROR: --profile unusable: %s" % exc)
            return 2

    rep = Report(as_json=args.as_json)
    selected = ["G0", "G1", "G2T", "G2K", "G3", "G4"] \
        if args.gate == "all" else [args.gate]

    runners = {"G0": lambda: gate_g0(rec, rep, args),
               "G1": lambda: gate_g1(rec, rep),
               "G3": lambda: gate_g3(rec, rep),
               "G4": lambda: gate_g4(rec, rep)}

    # Profile gate specs map onto the same gate ids; when a profile defines a
    # spec for a gate id, the spec REPLACES the generic runner for that id
    # (vendor uses embedded legacy predicates, which are byte-equivalent to
    # the old hardcoded runners). Without a profile, G2T/G2K have no runner:
    # they are reported as skipped via INFO, never as silent PASS.
    gate_specs = (manifest or {}).get("gates", {})
    for gid in ("G2T", "G2K"):
        if gid in gate_specs:
            runners[gid] = (lambda gid=gid: run_gate_spec(rec, rep, gid, gate_specs[gid]))

    for gate in selected:
        if gate not in runners:
            rep.info("gate %s has no predicates without --profile "
                     "(lane gates are defined by the profile)" % gate)
            continue
        try:
            runners[gate]()
        except MasterRegisterMisuse as exc:
            print("ERROR: --master-register unusable: %s" % exc)
            return 2

    if args.as_json:
        summary = {gate: {"checks": len(rep.total(gate)),
                          "failed": len(rep.failed(gate))}
                   for gate in selected if gate in runners}
        print(json.dumps({"record": rec.replace(os.sep, "/"),
                          "profile": args.profile,
                          "selected_gates": [g for g in selected if g in runners],
                          "checks": rep.checks, "summary": summary,
                          "verdict": "PASS" if not rep.failed() else "FAIL"},
                         sort_keys=True))
    else:
        for gate in selected:
            if gate not in runners:
                continue
            fails = rep.failed(gate)
            print("GATE %s: %s (%d checks, %d failed)"
                  % (gate, "PASS" if not fails else "FAIL",
                     len(rep.total(gate)), len(fails)))
            for c in fails:
                print("   FAILED CHECK %d: %s | %s" % (c["n"], c["name"], c["reason"]))
        print("VERDICT: %s" % ("PASS" if not rep.failed() else "FAIL"))

    return 0 if not rep.failed() else 1


def run_gate_spec(rec, rep, gid, spec):
    kind = spec.get("kind")
    if kind == "legacy_vendor":
        run_legacy_vendor(rec, rep, spec)
    elif kind == "lane_grid":
        run_lane_gate(rec, rep, gid, spec)
    elif kind == "maps":
        run_map_gate(rec, rep, gid, spec)
    else:
        rep.add(gid, "manifest gate spec recognized", False,
                "unknown kind %r in profile manifest" % kind)


def run_legacy_vendor(rec, rep, spec):
    """Vendor profile (B1): the full legacy G2T/G2K predicate set, ported
    content-kekal from the dd-vendor era checker (five-layer 35-row grid etc).
    Selected via --gate so the old CLI surface keeps working verbatim."""
    which = spec.get("which")
    if which == "G2T":
        gate_g2t(rec, rep)
    elif which == "G2K":
        gate_g2k(rec, rep)
    else:
        rep.add(spec.get("id", "G2?"), "legacy vendor gate id known", False,
                "unknown 'which' %r" % which)


def gate_g2t(rec, rep):
    g = "G2T"
    rows, err = read_csv(os.path.join(rec, "02-technical", "five-layer.csv"),
                         FIVE_LAYER_SCHEMA)
    if err:
        rep.add(g, "five-layer grid complete", False, err)
    else:
        rep.add(g, "five-layer grid >= 35 rows", len(rows) >= 35,
                "%d data rows" % len(rows))
        empties = []
        for idx, r in enumerate(rows, 2):
            for col in FIVE_LAYER_SCHEMA:
                if not (r.get(col) or "").strip():
                    empties.append("row %d col %s" % (idx, col))
        rep.add(g, "five-layer zero empty cells", not empties,
                "0 empty cells" if not empties
                else "%d empty cells: %s" % (len(empties), "; ".join(empties[:6])))
        unpaired = []
        for idx, r in enumerate(rows, 2):
            ans = (r.get("answer") or "").strip().upper()
            mat = (r.get("maturity") or "").strip().upper()
            route = (r.get("unknown_search_route") or "").strip()
            if (ans == "UNKNOWN" or mat == "UNKNOWN") and (not route or route == "n/a"):
                unpaired.append("row %d" % idx)
        rep.add(g, "UNKNOWN paired with search route", not unpaired,
                "all UNKNOWN rows carry a route" if not unpaired
                else "unpaired: " + ", ".join(unpaired))
        capped = []
        for idx, r in enumerate(rows, 2):
            ev = (r.get("maturity_evidence") or "").strip().upper()
            mat = (r.get("maturity") or "").strip().upper()
            ceil = (r.get("ceiling_applied") or "").strip().upper()
            if ev == "VENDOR-CLAIMED":
                if mat in {"M3", "M4", "M5"}:
                    capped.append("row %d maturity %s above M2" % (idx, mat))
                elif mat == "M2" and ceil != "Y":
                    capped.append("row %d M2 without ceiling_applied=Y" % idx)
        rep.add(g, "vendor-claim-only maturity capped at M2", not capped,
                "ceiling satisfied" if not capped else "; ".join(capped))

    ok, reason = saturation_ok(os.path.join(rec, "saturation", "technical.md"))
    rep.add(g, "technical saturation statement numbered", ok, reason)

    rows, err = read_csv(os.path.join(rec, "query-log.csv"), QUERY_LOG_SCHEMA)
    if err:
        rep.add(g, "query log ladder covers 8 route classes", False, err)
    else:
        classes = {(r.get("route_class") or "").strip() for r in rows}
        missing = [str(i) for i in range(1, 9) if str(i) not in classes]
        rep.add(g, "query log ladder covers 8 route classes", not missing,
                "classes seen: %s" % ",".join(sorted(classes))
                + ("" if not missing else "; missing: " + ",".join(missing)))


def gate_g2k(rec, rep):
    g = "G2K"
    pm, err = read_csv(os.path.join(rec, "03-commercial", "prospect-map.csv"),
                       PROSPECT_MAP_SCHEMA)
    bm, err2 = read_csv(os.path.join(rec, "03-commercial", "buyer-map.csv"),
                        BUYER_MAP_SCHEMA)
    rep.add(g, "prospect-map + buyer-map present with exact headers",
            not err and not err2 and bool(pm) and bool(bm),
            "prospect: %s (%d rows); buyer: %s (%d rows)"
            % (err or "ok", len(pm or []), err2 or "ok", len(bm or [])))
    if pm:
        bad = []
        for idx, r in enumerate(pm, 2):
            url = (r.get("source_url") or "").strip()
            ad = (r.get("access_date") or "").strip()
            pv = (r.get("pipeline_value_estimate") or "").strip()
            if not url.lower().startswith(("http://", "https://")):
                bad.append("row %d source_url" % idx)
            if not ISO_DATE.fullmatch(ad):
                bad.append("row %d access_date" % idx)
            if ".xlsx" not in pv.lower():
                bad.append("row %d pipeline_value_estimate is a bare literal "
                           "(must point into the economy workbook)" % idx)
        rep.add(g, "prospect rows sourced and workbook-backed", not bad,
                "all rows carry source_url, access_date, workbook pointer"
                if not bad else "; ".join(bad))
    ok1, why1 = saturation_ok(os.path.join(rec, "saturation", "commercial.md"))
    ok2, why2 = saturation_ok(os.path.join(rec, "saturation", "prospect.md"))
    rep.add(g, "commercial + prospect saturation numbered", ok1 and ok2,
            "commercial: %s; prospect: %s" % (why1, why2))


if __name__ == "__main__":
    sys.exit(main())
