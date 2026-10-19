#!/usr/bin/env python3
"""make_fixtures.py - regenerate the miniature deep-dive records for self-test.

Profiles covered by THIS generator: technology, market, client-integration.
The vendor fixtures under complete/vendor-record/ and broken/vendor-record/
are a frozen content-kekal port of the dd-vendor era fixtures (which passed
V-GATE 1); they are NOT regenerated here - the vendor regression contract
requires them to stay byte-identical to the input that produced the old
verdicts (blueprint 02b section 4 term 3).

Writes, relative to this directory:
    complete/<profile>-record/   full miniature -> gate_check --profile <p>
                                 exits 0
    broken/<profile>-record/     three deliberate defects -> gate_check exits 1
                                 with named FAILs:
                                   1. lane-grid.csv has four empty cells
                                   2. one saturation statement without numbers
                                   3. one dimension card points to CLM-999 (fake)
Stdlib only; deterministic byte-stable output. Run after editing schemas.
"""

import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))

LANES = {
    "technology": ["capability-vs-physics", "maturity-evidence",
                   "integration-fit"],
    "market": ["demand-evidence", "competitor-matrix", "route-history"],
    "client-integration": ["requirement-fit", "integration-path",
                           "acceptance-evidence"],
}
QUESTIONS = [
    "Is the core capability owned licensed or resold and from whom",
    "What maturity level M1-M5 does the evidence support",
    "How does stated performance compare with physics limits and independent benchmarks",
    "Which supplier license cloud or government dependency exists and in which country",
    "Which deployment or integration modes are supported on Indonesian government networks",
    "What is the security and sovereignty posture on data location visibility certifications audit logs",
    "How do roadmap promises compare with delivered record and past accuracy",
]
SATURATION_FILES = {
    "technology": ["saturation/capability.md", "saturation/maturity.md",
                   "saturation/integration.md"],
    "market": ["saturation/demand.md", "saturation/competition.md",
               "saturation/routes.md"],
    "client-integration": ["saturation/requirements.md",
                           "saturation/integration.md",
                           "saturation/acceptance.md"],
}
BROKEN_SATURATION = {
    "technology": "saturation/maturity.md",
    "market": "saturation/demand.md",
    "client-integration": "saturation/acceptance.md",
}
OBJECT_NAMES = {
    "technology": "Example Analytics Core SDK (fictional)",
    "market": "Example National Video-Analytics Market Sweep (fictional)",
    "client-integration": "Example Agency Command-Center Integration (fictional)",
}

DOC_REGISTER_SCHEMA = ["document_name", "date_received", "pages", "doc_type",
                       "status", "what_is_missing"]
FLAG_SEED_SCHEMA = ["class_id", "class_name", "status", "evidence_source", "date"]
LANE_GRID_SCHEMA = ["lane", "question_id", "question", "answer", "maturity",
                    "maturity_evidence", "dependency_and_country",
                    "evidence_source", "evidence_date", "ceiling_applied",
                    "unknown_search_route"]
BUYER_MAP_SCHEMA = ["capability", "buyer_institution", "user_unit",
                    "contact_role_if_visible", "demand_evidence",
                    "evidence_source", "evidence_date", "language_requirement",
                    "local_reception_note", "search_classes_touched"]
CLAIMS_SCHEMA = ["claim_id", "vendor_text_verbatim", "source_document",
                 "page_or_location", "claim_type", "test_method",
                 "stated_value", "recomputed_value", "variance_pct",
                 "evidence_label", "carrier_load", "status",
                 "verification_account", "date", "lane"]
RISK_SCHEMA = ["risk_id", "stage", "description", "likelihood",
               "likelihood_basis", "impact", "impact_basis", "evidence_source",
               "mitigation_options", "owner", "status", "date"]
ASK_SCHEMA = ["rank", "ask_id", "question", "why_asked", "evidence_requested",
              "affects_metric", "vendor_response", "response_date",
              "ledger_link", "status"]
QUERY_LOG_SCHEMA = ["query_id", "date", "route_class", "language",
                    "query_or_url", "result_summary", "evidence_status"]

CLAIMS_ROWS = [
    ["CLM-001", "Detection range up to 12 km at 90% confidence",
     "datasheet-2026.pdf", "p.7", "performance", "(12*0.9)/12*100", "90%",
     "90", "0", "VENDOR-CLAIMED", "Y", "open", "gsp-verifier", "2026-10-09", "S2"],
    ["CLM-002", "ISO 9001:2015 certified manufacturing", "certificate-scan.pdf",
     "page 1", "certification", "N/A: non-numeric", "N/A", "N/A", "N/A",
     "PRIMARY-DOC", "N", "verified-L2", "gsp-verifier", "2026-10-09", "S1"],
    ["CLM-003", "Annual production capacity 240 units",
     "factory-audit-report.pdf", "section 4", "capacity", "200*1.2", "240",
     "240", "0", "PRIMARY-DOC", "Y", "verified-L2", "gsp-verifier",
     "2026-10-09", "S2"],
    ["CLM-005", "Delivered 18 city-scale deployments", "reference-call-notes.md",
     "call 2", "reference", "N/A: not load-bearing", "18", "N/A", "N/A",
     "OBSERVED", "N", "verified-L2", "gsp-verifier", "2026-10-09", "S3"],
    ["CLM-006", "Revenue USD 8.4m FY2025", "annual-report-2025.pdf", "p.12",
     "financial", "6.5+1.9", "8.4", "8.4", "0", "THIRD-PARTY", "Y",
     "verified-L2", "gsp-verifier", "2026-10-09", "S3"],
    ["CLM-007", "Segment growth 11 percent CAGR 2024-2029",
     "analyst-note-a.pdf", "fig 3", "market", "220/20", "11%", "11", "0",
     "THIRD-PARTY", "Y", "verified-L2", "gsp-verifier", "2026-10-09", "S3"],
    ["CLM-008", "Local support office in Jakarta", "partner-agreement.pdf",
     "clause 9", "other", "N/A: non-numeric", "N/A", "N/A", "N/A", "OBSERVED",
     "N", "verified-L2", "gsp-verifier", "2026-10-09", "S3"],
]

SCORES = [3, 4, 3, 3, 4, 2, 3, 4, 3]  # indicator = 325/5 = 65.0
DIM_NAMES = ["Technology and maturity", "Named buyer demand",
             "GSP added value / moat", "Competitive position", "Economy",
             "Sovereignty and deployment", "Regulatory and export route",
             "Counterparty reliability and integrity",
             "Terms and channel position"]
DIM_CLAIMS = [["CLM-001"], ["CLM-007"], ["CLM-005"], ["CLM-005"],
              ["CLM-006"], ["CLM-003"], ["CLM-002"], ["CLM-005,CLM-008"],
              ["CLM-008"]]


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="\n", encoding="utf-8") as fh:
        fh.write(text)


def wcsv(path, schema, rows):
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(schema)
    writer.writerows(rows)
    w(path, buf.getvalue())


def lane_grid_rows(profile, broken=False):
    rows = []
    for li, lane in enumerate(LANES[profile]):
        for qi in range(1, 8):
            qid = "Q%d" % qi
            if li == 1 and qi == 6:  # the one honest UNKNOWN row
                rows.append([lane, qid, QUESTIONS[qi - 1], "UNKNOWN", "n/a",
                             "n/a", "UNKNOWN", "first sweep of official docs",
                             "2026-10-09", "n/a",
                             "official docs + trial report request + support inquiry"])
                continue
            if qi in (2, 3):
                mat, ev, ceil = "M2", "VENDOR-CLAIMED", "Y"
            elif qi == 4:
                mat, ev, ceil = "M3", "THIRD-PARTY", "n/a"
            elif qi == 1:
                mat, ev, ceil = "M4", "PRIMARY-DOC", "n/a"
            else:
                mat, ev, ceil = "M3", "OBSERVED", "n/a"
            rows.append([lane, qid, QUESTIONS[qi - 1],
                         "Documented and cross-checked in lane notes", mat, ev,
                         "GPU supplier, US" if qi in (1, 4) else "none identified",
                         "vendor docs + trial report", "2026-10-09", ceil,
                         "n/a"])
    if broken:  # defect 1: four empty cells
        rows[2][6] = ""
        rows[8][7] = ""
        rows[12][10] = ""
        rows[18][8] = ""
    return rows


def blok_temuan(profile, broken=False):
    lines = ["# Findings Block - %s" % OBJECT_NAMES[profile],
             "Fixture artifact for gate self-test; fictional data.", ""]
    for i in range(9):
        claims = DIM_CLAIMS[i][0]
        if broken and i == 1:  # defect 3: fake claim id
            claims = "CLM-007,CLM-999"
        lines.append("DIM-%d | %s | score: %d | claims: %s | ceiling: %s"
                     % (i + 1, DIM_NAMES[i], SCORES[i], claims,
                        "Y" if i in (0,) else "N"))
    lines += ["", "Indicator: 65.0",
              "arithmetic indicator only; no band-to-verdict mapping", ""]
    return "\n".join(lines)


def sat_text(title):
    return ("# Saturation statement - %s\n"
            "Query count: 31\nRoute classes exhausted: 8/8\nDate: 2026-10-11\n" % title)


def build(root, profile, broken):
    r = os.path.join(root, "%s-record" % profile)
    obj = OBJECT_NAMES[profile]
    w(os.path.join(r, "00-record", "nomination.md"),
      "# Nomination record - %s\n"
      "Nominated by: Director via chat, 2026-10-09\n"
      "Object: %s\n"
      "Class: %s\n"
      "Deadline: 2026-10-30\n"
      "Tier: T1\n"
      "First real DD: no\n"
      "Attachments: intake email, one background PDF\n"
      % (obj, obj, profile.upper()))
    w(os.path.join(r, "00-record", "entity-match.md"),
      "# Entity disambiguation\n"
      "Entity match: PASS - confirmed distinct from similarly named entities.\n"
      "Evidence: official site footer + registry extract, 2026-10-09.\n")
    wcsv(os.path.join(r, "00-record", "document-register.csv"),
         DOC_REGISTER_SCHEMA, [
             ["intake-email.pdf", "2026-10-09", "3", "email", "received", "none"],
             ["background-pdf.pdf", "2026-10-09", "12", "report", "received", "none"],
             ["audit-report.pdf", "", "", "certification", "requested",
              "latest audit report not yet supplied"],
         ])
    w(os.path.join(r, "00-record", "thesis.md"),
      "# Thesis\n"
      "The named buyer group needs this class of capability on existing infrastructure.\n"
      "The object supplies the core; GSP adds integration, certification, ID language, hosting.\n"
      "Budget visibility exists in planning documents for one named unit.\n"
      "Winning route likely an e-katalog LKPP listing before the Q1 award cycle.\n")
    wcsv(os.path.join(r, "00-record", "flag-register.seed.csv"), FLAG_SEED_SCHEMA,
         [["FL-%d" % i, name, "note", "intake review", "2026-10-09"] for i, name in enumerate(
             ["Sanctions screening", "Export control",
              "Counterparty stance vs buyer interest", "Rights position in Indonesia",
              "Deployment-mode gap", "Material misrepresentation",
              "Financial capability"], 1)])
    w(os.path.join(r, "01-screen", "screen-report.md"),
      "# Screen Report - %s\n"
      "## 1. Object Identity Block\n"
      "Legal name: %s.\n"
      "Entity-match evidence dated 2026-10-09.\n"
      "## 3. Material Claims Summary\n"
      "Top rows: CLM-001 range claim recomputed consistent; CLM-003 capacity verified-L2.\n"
      "## 4. Flag Register First Pass\n"
      "| class | status | evidence_source | date |\n"
      "|---|---|---|---|\n"
      "| FL-1 Sanctions screening | clear | OFAC EU UK UN BIS screens | 2026-10-09 |\n"
      "| FL-2 Export control | caution | ECCN candidate per datasheet p.3 | 2026-10-09 |\n"
      "| FL-3 Counterparty stance vs buyer interest | unresolved-after-6-searches | registry extract press | 2026-10-09 |\n"
      "| FL-4 Rights position in Indonesia | note | partner agreement clause 9 | 2026-10-09 |\n"
      "| FL-5 Deployment-mode gap | clear | deployment matrix p.6 | 2026-10-09 |\n"
      "| FL-6 Material misrepresentation | clear | recompute run 2026-10-09 | 2026-10-09 |\n"
      "| FL-7 Financial capability | caution | annual report 2025 | 2026-10-09 |\n"
      "## 5. Top Five Ask-List\n"
      "(1) raw trial dataset behind CLM-001; (2) latest audit report; (3) reference customers;\n"
      "(4) price list with volume tiers; (5) ownership chain disclosure.\n"
      "## 6. Prospect Sketch\n"
      "Buyers seen: Ministry of Example Affairs maritime unit. Competitors seen: two incumbents.\n"
      "Query count behind this sketch: 12.\n"
      "## 7. Deadline and Progress Checkpoints\n"
      "User deadline 2026-10-30; checkpoint S1 reached 2026-10-09.\n"
      "## 8. Open Items Without Answer\n"
      "Ownership chain, last contact 2026-10-09, carried forward without inference.\n"
      "## 9. Director decision: ______\n" % (obj, obj))
    wcsv(os.path.join(r, "claims-ledger.csv"), CLAIMS_SCHEMA, CLAIMS_ROWS)
    wcsv(os.path.join(r, "risk-register.csv"), RISK_SCHEMA, [[
        "RSK-001", "S3",
        "Incumbent contract renews before budget window opens", "medium",
        "two prior renewals without open tender (LPSE history 2023 2025)",
        "high", "single award covers 80 percent of modeled pipeline",
        "LPSE tender archive",
        "early e-katalog listing | partner-of-incumbent route | demo before Q1 lock",
        "gsp-pm-planner", "open", "2026-10-09"]])
    wcsv(os.path.join(r, "ask-list.csv"), ASK_SCHEMA, [[
        "1", "ASK-001",
        "Provide raw trial dataset with method notes behind the 12 km detection claim",
        "range is load-bearing for DIM-1 and FL-6",
        "raw data + collection method + environment log", "DIM-1; CLM-001",
        "", "", "CLM-001", "open"]])
    wcsv(os.path.join(r, "02-lanes", "lane-grid.csv"), LANE_GRID_SCHEMA,
         lane_grid_rows(profile, broken))
    if profile == "market":
        wcsv(os.path.join(r, "03-commercial", "buyer-map.csv"), BUYER_MAP_SCHEMA, [[
            "video analytics", "Bandung City Government", "Transport Command Center",
            "Head of IT (from tender doc)",
            "2025 tender for 400-camera analytics lot", "LPSE tender page",
            "2026-10-05", "ID interface mandatory",
            "incumbent is a local SI with foreign core", "1,2,4,5,6"]])
    w(os.path.join(r, "04-package", "blok-temuan.md"), blok_temuan(profile, broken))
    w(os.path.join(r, "04-package", "blind-challenge.md"),
      "# Blind completeness challenge\n"
      "Reviewer account: gsp-pm-verifier (wrote no lane in this record).\n"
      "Tested: ledger arithmetic, dropped contradictions, cherry-picked rows,\n"
      "route-class coverage. Result: numbers remain valid; nothing was silently removed.\n")
    for rel in SATURATION_FILES[profile]:
        title = os.path.basename(rel)[:-3]
        if broken and rel == BROKEN_SATURATION[profile]:  # defect 2: no numbers
            w(os.path.join(r, rel),
              "# Saturation statement - %s\n"
              "We looked around quite a bit and feel the lane is covered.\n" % title)
        else:
            w(os.path.join(r, rel), sat_text(title))
    wcsv(os.path.join(r, "query-log.csv"), QUERY_LOG_SCHEMA, [
        ["QRY-%03d" % i, "2026-10-09", str(i), lang, target, summary, "logged"]
        for i, (lang, target, summary) in enumerate([
            ("EN", "official site exact pages", "primary docs captured"),
            ("EN", "subdomain + sitemap variants", "press archive found"),
            ("EN", "CMS probe /wp-json", "case-study CPT listed"),
            ("ID", "lpse site tender phrases", "tender history rows"),
            ("EN", "CDX archive of datasheet URL", "prior revision captured"),
            ("ZH", "registry filings search", "ownership extract"),
            ("EN", "news + social name sweep", "funding announcements"),
            ("EN", "browser render XHR hunt", "price endpoint captured"),
        ], 1)])
    w(os.path.join(r, "05-closeout", "il-promotion-note.md"),
      "# IL promotion note\nRecord promoted via gsp-librarian; attestation recorded 2026-10-12.\n")
    w(os.path.join(r, "05-closeout", "master-register-update.md"),
      "# Master register update\nTrust tier PROVISIONAL -> reviewed; DD status complete; date 2026-10-12.\n")
    w(os.path.join(r, "05-closeout", "refresh-triggers.md"),
      "# Refresh triggers\n"
      "- six-month cycle\n"
      "- ownership funding or acquisition change\n"
      "- sanctions or export list change\n"
      "- counterparty signs another Indonesian partner\n"
      "- before any signature or tender naming\n")


if __name__ == "__main__":
    for variant, broken in (("complete", False), ("broken", True)):
        for profile in ("technology", "market", "client-integration"):
            target = os.path.join(HERE, variant)
            build(target, profile, broken)
            print("built %s" % os.path.join(target, "%s-record" % profile))
