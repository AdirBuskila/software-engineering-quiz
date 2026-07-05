# -*- coding: utf-8 -*-
"""Validate the per-exam JSON files the structuring agents produced (SE course)."""
import json, pathlib, collections, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAW = pathlib.Path(__file__).parent / "raw"
CODES = ["19B-B","19B-C","20-A","20-B","21-A","21-B","21S-A","21S-B","22B-A","22S-A",
         "23-EX","23B-A","23S-A","24B-A","24B-B","24S-A","25F0a","25F0b","25S-A","25B-N","25-EX",
         "SP-SPC","SP-DGM","SP-AMR","SP-MDA"]
TOPICS = {"intro","agile","requirements","uml","architecture","patterns","solid",
          "testing","oop_java","metrics","config"}

total = usable = 0
by_topic = collections.Counter(); by_official = collections.Counter()
by_conf = collections.Counter()
problems = []; flagged = []
for code in CODES:
    p = RAW / f"{code}.json"
    if not p.exists():
        problems.append(f"{code}: FILE MISSING (agent may still be running)"); continue
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"{code}: JSON parse error: {e}"); continue
    nimg = 0
    for q in data:
        total += 1
        n = len(q.get("options", []))
        if n < 2 or n > 6:
            problems.append(f"{code} Q{q.get('num')}: {n} options")
        ci = q.get("correctIndex")
        if not isinstance(ci, int) or ci < 0 or ci >= n:
            problems.append(f"{code} Q{q.get('num')}: bad correctIndex {ci} (n={n})")
        if q.get("topic") not in TOPICS:
            problems.append(f"{code} Q{q.get('num')}: bad topic {q.get('topic')}")
        if not str(q.get("question", "")).strip():
            problems.append(f"{code} Q{q.get('num')}: empty question")
        if any(not str(o).strip() for o in q.get("options", [])):
            problems.append(f"{code} Q{q.get('num')}: blank option")
        by_conf[q.get("confidence", "?")] += 1
        if q.get("flag"):
            flagged.append(f"{code} Q{q.get('num')} [{q.get('confidence','?')}]: {q['flag']}")
        if q.get("hasImage"):
            nimg += 1
        else:
            usable += 1; by_topic[q.get("topic")] += 1
            by_official["official" if q.get("official") else "derived"] += 1
    print(f"{code}: {len(data)} questions, {nimg} image-flagged, {len(data)-nimg} usable")

print(f"\nTOTAL: {total} raw, {usable} usable (non-image)")
print("by topic (usable):", dict(by_topic.most_common()))
print("by source (usable):", dict(by_official))
print("by confidence (all):", dict(by_conf))
print(f"\nPROBLEMS ({len(problems)}):")
for x in problems: print("  -", x)
print(f"\nFLAGGED for review ({len(flagged)}):")
for x in flagged: print("  -", x)
