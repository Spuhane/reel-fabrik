import json, sys, collections

FILES = sys.argv[1:]
by_topic = collections.defaultdict(list)

def ok(q):
    o = q.get("options", [])
    if len(o) != 4 or len(set(o)) != 4: return False
    if not isinstance(q.get("correct"), int): return False
    if not (0 <= q["correct"] < 4): return False
    if not isinstance(q.get("explanation"), str): return False
    if len(q["question"]) > 85: return False
    if max(len(x) for x in o) > 46: return False
    if len(q["explanation"]) < 35: return False
    if "?" in q["explanation"].replace("?.", "") and " ? " in q["explanation"]: return False
    return True

for p in FILES:
    d = json.load(open(p, encoding="utf-8"))
    for tk, t in d["topics"].items():
        for q in t.get("questions", []) or []:
            if ok(q):
                q = dict(q)
                q["_topic_key"] = tk
                q["_topic_name"] = t.get("name", "")
                q["_track"] = t.get("track", "")
                by_topic[tk].append(q)

print("Geeignete Fragen je Thema:")
for k, v in sorted(by_topic.items(), key=lambda x: -len(x[1])):
    print(f"  {k:8s} {len(v):4d}  {v[0]['_topic_name']}")
print("  GESAMT:", sum(len(v) for v in by_topic.values()))

# gleichmaessig streuen: 2 je Thema, kuerzeste zuerst (lesbarste Karten)
picked = []
for k, v in sorted(by_topic.items()):
    v.sort(key=lambda q: len(q["question"]) + max(len(o) for o in q["options"]))
    picked.extend(v[:2])
json.dump(picked, open("work/candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\nAusgewaehlt:", len(picked))
for q in picked:
    print(f"\n[{q['id']}] {q['_topic_name']}")
    print("  F:", q["question"])
    for i, o in enumerate(q["options"]):
        print(f"   {'ABCD'[i]}{'*' if i == q['correct'] else ' '} {o}")
    print("  E:", q["explanation"].replace("\n", " | "))
