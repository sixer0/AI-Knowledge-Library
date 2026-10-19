#!/usr/bin/env python3
"""recompute-checks.py - deterministic recomputation of vendor numeric claims.

Part of the dd-vendor skill (mission DDV-STD-1009). Stdlib only, Python >= 3.10.
No network, no LLM, no eval(): the test_method grammar is parsed by the
restricted recursive-descent parser below.

Usage:
    python recompute-checks.py <claims-ledger.csv> [--tolerance <pct>] [--json]

Behavior:
    For every ledger row with carrier_load == Y or claim_type in
    {performance, capacity, financial, market} whose stated_value parses as a
    number, evaluate test_method (restricted arithmetic: + - * / parentheses,
    numbers with optional % suffix meaning /100), compare against the stated
    number and compute variance_pct. The input file is never modified; a copy
    with recomputed_value and variance_pct rewritten is written beside it as
    <ledger>.checked.csv (suppressed with --json, which prints the machine
    report to stdout instead).

Output (stdout):
    CHECK <claim_id>: PASS|FAIL|MISMATCH-FLAGGED | stated=... recomputed=... variance=...%
    TOTAL n | PASS a | FAIL b | FLAGGED c
    VERDICT: PASS|FAIL

Exit codes:
    0 = every evaluated numeric claim consistent within tolerance
    1 = mismatch beyond tolerance, or a load-bearing numeric claim without a
        usable test_method, or an unparseable test_method
    2 = misuse, unreadable CSV, or header mismatch against the claims-ledger
        schema (15 fixed columns)
"""

import argparse
import csv
import json
import re
import sys

SCHEMA = ["claim_id", "vendor_text_verbatim", "source_document",
          "page_or_location", "claim_type", "test_method", "stated_value",
          "recomputed_value", "variance_pct", "evidence_label", "carrier_load",
          "status", "verification_account", "date", "lane"]

EVAL_TYPES = {"performance", "capacity", "financial", "market"}


class ExprError(Exception):
    pass


def tokenize(expr):
    tokens = re.findall(r"\d+(?:\.\d+)?%?|[+\-*/()]|.", expr)
    return tokens


class Parser:
    """Restricted arithmetic grammar; '%' on a number literal means /100."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def next(self):
        tok = self.peek()
        if tok is None:
            raise ExprError("unexpected end of expression")
        self.pos += 1
        return tok

    def parse(self):
        value = self.expr()
        if self.peek() is not None:
            raise ExprError("unexpected token '%s'" % self.peek())
        return value

    def expr(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.next()
            rhs = self.term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def term(self):
        value = self.factor()
        while self.peek() in ("*", "/"):
            op = self.next()
            rhs = self.factor()
            if op == "/":
                if rhs == 0:
                    raise ExprError("division by zero")
                value = value / rhs
            else:
                value = value * rhs
        return value

    def factor(self):
        tok = self.peek()
        if tok == "+":
            self.next()
            return self.factor()
        if tok == "-":
            self.next()
            return -self.factor()
        if tok == "(":
            self.next()
            value = self.expr()
            if self.next() != ")":
                raise ExprError("missing closing parenthesis")
            return value
        return self.number()

    def number(self):
        tok = self.next()
        m = re.fullmatch(r"(\d+(?:\.\d+)?)(%?)", tok or "")
        if not m:
            raise ExprError("unexpected token '%s'" % tok)
        value = float(m.group(1))
        if m.group(2) == "%":
            value /= 100.0
        return value


def parse_number(text):
    """First number in a cell, with optional % marker. None if not numeric."""
    if text is None:
        return None, False
    m = re.search(r"(\d+(?:\.\d+)?)\s*(%?)", text.strip())
    if not m:
        return None, False
    return float(m.group(1)), m.group(2) == "%"


def fmt(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return ("%.6f" % value).rstrip("0").rstrip(".")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="recompute-checks.py")
    ap.add_argument("ledger")
    ap.add_argument("--tolerance", type=float, default=2.0)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)

    try:
        with open(args.ledger, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != SCHEMA:
                print("ERROR: header does not match the claims-ledger schema")
                print("expected: %s" % ",".join(SCHEMA))
                print("found:    %s" % ",".join(reader.fieldnames or []))
                return 2
            rows = list(reader)
    except OSError as exc:
        print("ERROR: cannot read %s (%s)" % (args.ledger, exc.strerror))
        return 2

    results = []
    n_pass = n_fail = n_flag = 0
    for row in rows:
        load_bearing = (row["carrier_load"].strip().upper() == "Y"
                        or row["claim_type"].strip().lower() in EVAL_TYPES)
        if not load_bearing:
            continue
        stated, stated_is_pct = parse_number(row["stated_value"])
        if stated is None:
            continue  # non-numeric claim: ledger carries N/A with reason
        method = row["test_method"].strip()
        if not method or method.upper() in {"N/A", "UNKNOWN"}:
            n_fail += 1
            results.append({"claim_id": row["claim_id"], "status": "FAIL",
                            "detail": "load-bearing numeric claim without test_method"})
            print("CHECK %s: FAIL | stated=%s recomputed=NONE variance=N/A | no test_method"
                  % (row["claim_id"], fmt(stated) + ("%" if stated_is_pct else "")))
            continue
        try:
            recomputed = Parser(tokenize(method)).parse()
        except ExprError as exc:
            n_fail += 1
            results.append({"claim_id": row["claim_id"], "status": "FAIL",
                            "detail": "unparseable test_method: %s" % exc})
            print("CHECK %s: FAIL | stated=%s recomputed=NONE variance=N/A | %s"
                  % (row["claim_id"], fmt(stated), exc))
            continue
        if stated != 0:
            variance = abs(recomputed - stated) / abs(stated) * 100.0
        else:
            variance = abs(recomputed) * 100.0
        row["recomputed_value"] = fmt(recomputed)
        row["variance_pct"] = "%.2f" % variance
        if variance > args.tolerance:
            status = "MISMATCH-FLAGGED"
            n_flag += 1
        else:
            status = "PASS"
            n_pass += 1
        results.append({"claim_id": row["claim_id"], "status": status,
                        "stated": stated, "recomputed": recomputed,
                        "variance_pct": round(variance, 2)})
        print("CHECK %s: %s | stated=%s recomputed=%s variance=%.2f%%"
              % (row["claim_id"], status, fmt(stated), fmt(recomputed), variance))

    total = n_pass + n_fail + n_flag
    verdict = "PASS" if (n_fail == 0 and n_flag == 0) else "FAIL"
    print("TOTAL %d | PASS %d | FAIL %d | FLAGGED %d" % (total, n_pass, n_fail, n_flag))
    print("VERDICT: %s" % verdict)

    if args.as_json:
        print(json.dumps({"tolerance_pct": args.tolerance, "results": results,
                          "total": total, "pass": n_pass, "fail": n_fail,
                          "flagged": n_flag, "verdict": verdict},
                         sort_keys=True))
    elif rows:
        out_path = args.ledger + ".checked.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=SCHEMA)
            writer.writeheader()
            writer.writerows(rows)
        print("WROTE %s (input file untouched)" % out_path)

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
