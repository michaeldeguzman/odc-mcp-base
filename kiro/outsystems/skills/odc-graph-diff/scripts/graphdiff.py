#!/usr/bin/env python3
"""Compare two saved ODC app model graphs (context_graph output).

Usage:
  python3 graphdiff.py BEFORE AFTER [--scope "Type:Name,Type:Name"] [--out FILE] [--json FILE]

BEFORE and AFTER are files saved from the OutSystems MCP `context_graph` tool,
whole app, no root, one page: a JSON header followed by the XRE graph (one line each, or pretty-printed).

Nodes are matched by _key. Edges are matched by (source key, target key,
attributes without "index"); sibling index changes are counted on their own.
Every difference is assigned to its containing element (screen, action,
entity, ...). Changes that touch only canvas position (X, Y) or only
modification stamps are reported separately from content changes.

Python 3.8+, standard library only. Read-only: it never calls the tenant.
"""
import argparse
import collections
import json
import sys

CONTAINERS = (
    "IESpace", "IMobileFlow", "IMobileScreen", "IMobileBlock", "IServerAction",
    "IClientAction", "IAction", "IEntity", "IStaticEntity", "IStructure", "IRole",
    "ITimer", "ITheme", "IReference", "IConsumedRESTAPI", "IExposedRESTAPI",
    "ISiteProperty", "IResource", "IImage",
)
LAYOUT_FIELDS = {"X", "Y"}
STAMP_FIELDS = {
    "LastModifiedBy", "LastModifiedDate", "LastModifiedByTool", "LastModifiedByAgent",
    "ModifiedByTools", "LastMergedBy", "LastMergedDate",
}


def load(path):
    # The header and the graph are two JSON objects, one after the other.
    # Usually one per line, but pretty-printed copies work too.
    with open(path, encoding="utf-8") as f:
        text = f.read()
    dec = json.JSONDecoder()
    try:
        header, end = dec.raw_decode(text.lstrip())
        rest = text.lstrip()[end:].lstrip()
        graph, _ = dec.raw_decode(rest)
    except ValueError as exc:
        sys.exit(f"{path}: expected a JSON header followed by the JSON graph ({exc})")
    if "nodes" not in graph:
        sys.exit(f"{path}: the second JSON object has no nodes. Is this a context_graph save?")
    if header.get("has_more"):
        sys.exit(f"{path}: graph has more pages (has_more true). Save the whole graph first.")
    return header, graph


def index(graph):
    nodes = graph["nodes"]
    keys = [n.get("_key") for n in nodes]
    by_key = {n.get("_key"): (i, n) for i, n in enumerate(nodes)}
    incoming = collections.defaultdict(list)
    edges = collections.Counter()
    raw_edges = collections.Counter()
    pos = {}
    for s, t, a in zip(graph["edgeSrc"], graph["edgeDst"], graph["edgeAttr"]):
        incoming[t].append((s, a))
        raw_edges[(keys[s], keys[t], json.dumps(a, sort_keys=True))] += 1
        base = {k: v for k, v in a.items() if k != "index"}
        ek = (keys[s], keys[t], json.dumps(base, sort_keys=True))
        edges[ek] += 1
        pos.setdefault(ek, []).append(a.get("index"))
    return nodes, keys, by_key, incoming, edges, raw_edges, pos


def owner_prefix(graph):
    return graph.get("key", "").split("*")[0] + "*"


def container(i, nodes, incoming, own):
    n = nodes[i]
    if not n["_key"].startswith(own):
        return "LIBRARY/" + n["_key"].split("*")[0][:6]
    seen, queue = {i}, [i]
    while queue:
        j = queue.pop(0)
        m = nodes[j]
        if m["_type"] in CONTAINERS and m["_key"].startswith(own) and (j != i or m["_type"] in CONTAINERS):
            return f'{m["_type"]}:{m.get("DisplayName") or m.get("Name")}'
        for s, a in incoming.get(j, []):
            if a.get("_type") == "ValidationMessages" or s in seen:
                continue
            seen.add(s)
            queue.append(s)
    return "?"


def kind_of_change(a, b):
    fields = {f for f in set(a) | set(b) if a.get(f) != b.get(f)}
    if fields <= LAYOUT_FIELDS:
        return "layout", fields
    if fields <= STAMP_FIELDS | LAYOUT_FIELDS:
        return "stamps", fields
    return "content", fields - STAMP_FIELDS


def compare(before, after, scope):
    (ha, ga), (hb, gb) = before, after
    na, _, ka, ia, ea, rea, pa = index(ga)
    nb, _, kb, ib, eb, reb, pb = index(gb)
    own = owner_prefix(gb)
    groups = collections.defaultdict(collections.Counter)
    detail = collections.defaultdict(list)

    for k, (i, n) in kb.items():
        if k not in ka:
            c = container(i, nb, ib, own)
            groups[c]["added"] += 1
            detail[c].append(("added", n["_type"], n.get("DisplayName") or n.get("Name") or ""))
        else:
            old = ka[k][1]
            if old != n:
                kind, fields = kind_of_change(old, n)
                c = container(i, nb, ib, own)
                groups[c]["changed " + kind] += 1
                if kind == "content":
                    detail[c].append(("changed", n["_type"], (n.get("DisplayName") or n.get("Name") or "") + " " + ",".join(sorted(fields))))
    for k, (i, n) in ka.items():
        if k not in kb:
            c = container(i, na, ia, own)
            groups[c]["removed"] += 1
            detail[c].append(("removed", n["_type"], n.get("DisplayName") or n.get("Name") or ""))

    edges_added, edges_removed = eb - ea, ea - eb
    index_changed = sum(1 for ek in set(pa) & set(pb) if sorted(map(str, pa[ek])) != sorted(map(str, pb[ek])))
    in_scope = set(s.strip() for s in scope.split(",") if s.strip()) if scope else None

    def is_out(c, counts):
        if in_scope is None:
            return False
        if c in in_scope or c.startswith("LIBRARY/"):
            return False
        return any(v and (name in ("added", "removed", "changed content")) for name, v in counts.items())

    out_of_scope = sorted(c for c, v in groups.items() if is_out(c, v))
    return {
        "before": {"revision": ha.get("revision"), "nodes": len(na), "edges": len(ga["edgeSrc"])},
        "after": {"revision": hb.get("revision"), "nodes": len(nb), "edges": len(gb["edgeSrc"])},
        "nodes": {
            "added": sum(v["added"] for v in groups.values()),
            "removed": sum(v["removed"] for v in groups.values()),
            "changed": sum(v[x] for v in groups.values() for x in ("changed content", "changed layout", "changed stamps")),
            "changed_content": sum(v["changed content"] for v in groups.values()),
        },
        "edges": {
            "added": sum(edges_added.values()),
            "removed": sum(edges_removed.values()),
            "index_changed": index_changed,
            "raw_added": sum((reb - rea).values()),
            "raw_removed": sum((rea - reb).values()),
        },
        "by_container": {c: dict(v) for c, v in sorted(groups.items())},
        "detail": {c: v[:50] for c, v in sorted(detail.items())},
        "scope": sorted(in_scope) if in_scope is not None else None,
        "out_of_scope": out_of_scope,
    }


def markdown(r):
    b, a, n, e = r["before"], r["after"], r["nodes"], r["edges"]
    lines = [
        f"# Graph diff: revision {b['revision']} -> {a['revision']}",
        "",
        f"- Nodes {b['nodes']:,} -> {a['nodes']:,}: {n['added']} added, {n['removed']} removed, "
        f"{n['changed']} changed ({n['changed_content']} in content, the rest layout or stamps only).",
        f"- Edges {b['edges']:,} -> {a['edges']:,}: {e['added']} added, {e['removed']} removed, "
        f"{e['index_changed']} with a changed sibling index.",
        "",
        "## By element",
        "",
    ]
    for c, v in r["by_container"].items():
        lines.append(f"- {c}: " + ", ".join(f"{k} {v[k]}" for k in sorted(v)))
    lines += ["", "## Out of scope", ""]
    if r["scope"] is None:
        lines.append("No scope given. Compare the list above with the spec by hand.")
    elif r["out_of_scope"]:
        lines += [f"- {c}" for c in r["out_of_scope"]]
    else:
        lines.append("None.")
    lines += ["", "Library entries (LIBRARY/...) are usually derived types and are not flagged. Check them if they look unexpected."]
    lines += ["", "## Content changes (first 50 per element)", ""]
    for c, items in r["detail"].items():
        lines.append(f"### {c}")
        lines += [f"- {kind} {typ} {name}".rstrip() for kind, typ, name in items]
        lines.append("")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("before")
    p.add_argument("after")
    p.add_argument("--scope", help='Elements the change may touch, e.g. "IMobileScreen:Employee_List,IEntity:Department"')
    p.add_argument("--out", help="Write the Markdown report here")
    p.add_argument("--json", help="Write the full result as JSON here")
    args = p.parse_args()
    result = compare(load(args.before), load(args.after), args.scope)
    report = markdown(result)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report + "\n")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    print(report.split("\n## Content changes")[0])
    return 2 if result["out_of_scope"] else 0


if __name__ == "__main__":
    sys.exit(main())
