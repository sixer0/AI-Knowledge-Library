#!/bin/bash
# Write anti-repeat markers for 24 done-unacked WAKE rows (class done-unacked only).
EPOCH=$(date +%s)
IDS="t_0913266d t_0918b6d2 t_0ac8927f t_0f3e37eb t_19930381 t_5291d587 t_5715d1fc t_6aa0384c t_7124c228 t_7707a0cd t_7f36de9e t_80a9fb43 t_896447e4 t_99bb85a4 t_a148a692 t_a66ce30a t_ad5d8e6f t_b2b82e31 t_c2180f14 t_ccfca3b8 t_de326482 t_de73c01d t_deb670d0 t_ed8b0b54"
OK=0; FAIL=0
for id in $IDS; do
  if hermes kanban --board default comment "$id" "RANTAI-WAKE done-unacked $EPOCH" >/dev/null 2>&1; then
    OK=$((OK+1)); echo "MARK-OK $id"
  else
    FAIL=$((FAIL+1)); echo "MARK-FAIL $id"
  fi
done
echo "SUMMARY epoch=$EPOCH ok=$OK fail=$FAIL"
