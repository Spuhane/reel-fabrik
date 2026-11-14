#!/bin/bash
cd /home/claude/reel-pipeline
mkdir -p docs/reels
for id in q-hq-ifc-69 q-plqp-16 q-rfi-111 q-hq-mv-63 q-hq-mv-60 q-uf-06 q-hq-lp-36 q-bmc-40; do
  python3 render_quiz_reel.py "content/pool/$id.json" brand/wfw.json "docs/reels/$id.mp4" \
    && echo "FERTIG $id"
done
echo "ALLE REELS FERTIG"
