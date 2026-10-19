# Findings Block - <object legal name>
General frame for S4 output (record page 1). Section order is fixed. Every
score points at ledger claim ids; every unknown carries its search count.
Companion sentence on the indicator is mandatory and verbatim. Classification
default: RAHASIA - INTERNAL unless the Director sets otherwise per mission.
The profile may pin a concrete variant (see templates/profiles/<class>/).

## 1. Flag Register Status
| class | status | evidence_source | date |
|---|---|---|---|
| FL-1 Sanctions screening | clear | <source> | <YYYY-MM-DD> |
| FL-2 Export control | caution | <source> | <YYYY-MM-DD> |
| FL-3 Counterparty stance vs buyer interest | note | <source> | <YYYY-MM-DD> |
| FL-4 Rights position in Indonesia | unresolved-after-N-searches | <source> | <YYYY-MM-DD> |
| FL-5 Deployment-mode gap | clear | <source> | <YYYY-MM-DD> |
| FL-6 Material misrepresentation | blocker-candidate | <source> | <YYYY-MM-DD> |
| FL-7 Financial capability | caution | <source> | <YYYY-MM-DD> |

## 2. Dimension Cards
Nine cards; each score 0-5 names its ledger claims; ceiling marked where all
referenced evidence is self-reported (label VENDOR-CLAIMED, frozen name; score
capped at 3).
```
DIM-1 | Technology and maturity | score: <0-5> | claims: CLM-xxx[,CLM-yyy] | ceiling: Y|N
DIM-2 | Named buyer demand | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-3 | GSP added value / moat | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-4 | Competitive position | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-5 | Economy | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-6 | Sovereignty and deployment | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-7 | Regulatory and export route | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-8 | Counterparty reliability and integrity | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
DIM-9 | Terms and channel position | score: <0-5> | claims: CLM-xxx | ceiling: Y|N
```

## 3. One Arithmetic Indicator
Weights frozen at 15/15/15/10/10/10/10/10/5; indicator = sum(weight_i * score_i) / 5.
```
Indicator: <value to 1 decimal>
arithmetic indicator only; no band-to-verdict mapping
```

## 4. Sensitivity
- Measurement that moves the indicator most per one-level change: <which card
  or ledger row, with the recomputed delta printed by the parser>

## 5. Known Unknowns
| item | searches performed | routes still open |
|---|---|---|
| <unknown> | <int> | <routes> |

## 6. Top Ask-List
(1) <top asks from ask-list.csv, ranked>

## 7. Demand Headline (profile shapes this slot)
- Named buyers: <institutions>
- Pipeline or value figure: <workbook-printed figure + workbook file reference>

## 8. Director decision: ______
