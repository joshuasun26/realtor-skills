#!/usr/bin/env python3
"""
Skill Atlas builder.

Walks the plugin's skills/ tree, parses every SKILL.md (frontmatter + body), works out
which skills reference which other skills, and writes a single self-contained
atlas/index.html with all of it inlined.

Self-contained is the point: the finished page opens from file:// with no web server,
no CDN, no network call of any kind. That is why the data is baked in rather than
fetched -- browsers block fetch() against file:// URLs.

Run:  python atlas/build.py
"""

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO / "plugins" / "realtor-skills" / "skills"
OUT = REPO / "atlas" / "index.html"

DEPT_LABELS = {
    "foundation": "Foundation",
    "listings": "Listings",
    "open-house": "Open House",
    "market": "Market",
    "sphere": "Sphere",
    "pipeline": "Pipeline",
    "content": "Content",
}

# Fixed hues per department so colors do not shuffle between builds.
DEPT_HUES = {
    "foundation": 220,
    "listings": 28,
    "open-house": 152,
    "market": 265,
    "sphere": 340,
    "pipeline": 192,
    "content": 48,
}


def parse_frontmatter(text):
    """Return (meta_dict, body). Minimal YAML: scalars and folded '>' blocks only."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    meta, key, buf = {}, None, []

    def flush():
        if key:
            meta[key] = " ".join(w for w in " ".join(buf).split() if w)

    for line in raw.split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            flush()
            key, rest = m.group(1), m.group(2).strip()
            buf = [] if rest in (">", "|", ">-", "|-", "") else [rest]
        elif key:
            buf.append(line.strip())
    flush()
    return meta, body


def main():
    if not SKILLS_ROOT.is_dir():
        sys.exit(f"No skills directory at {SKILLS_ROOT}")

    skills = []
    for path in sorted(SKILLS_ROOT.rglob("SKILL.md")):
        rel = path.relative_to(SKILLS_ROOT)
        parts = rel.parts
        if len(parts) < 2:
            continue
        folder = parts[-2]
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        name = meta.get("name") or folder
        # Skills sit flat at skills/<name>/SKILL.md because Claude Code only
        # discovers them one level deep, so the department is carried in
        # frontmatter rather than by directory. Fall back to the parent folder
        # for any layout that still nests.
        dept = meta.get("department") or (parts[0] if len(parts) > 2 else "general")
        skills.append({
            "id": name,
            "folder": folder,
            "dept": dept,
            "deptLabel": DEPT_LABELS.get(dept, dept.replace("-", " ").title()),
            "hue": DEPT_HUES.get(dept, 200),
            "description": meta.get("description", ""),
            "body": body,
            "path": str(rel).replace("\\", "/"),
            "orchestrator": "orchestrator" in body[:600].lower(),
        })

    names = {s["id"] for s in skills}
    by_id = {s["id"]: s for s in skills}

    # An edge is A referencing B. Only `backticked` mentions count: these files name
    # sibling skills in backticks by convention, and matching bare prose text instead
    # turns every common word into a false edge and the graph into a hairball.
    edges, seen = [], set()
    for s in skills:
        for token in re.findall(r"`([a-z0-9][a-z0-9-]*)`", s["body"]):
            if token == s["id"] or token not in names:
                continue
            key = (s["id"], token)
            if key not in seen:
                seen.add(key)
                edges.append({"source": s["id"], "target": token})

    for s in skills:
        s["calls"] = sorted(e["target"] for e in edges if e["source"] == s["id"])
        s["calledBy"] = sorted(e["source"] for e in edges if e["target"] == s["id"])

    depts = []
    for d in DEPT_LABELS:
        members = [s for s in skills if s["dept"] == d]
        if members:
            depts.append({
                "id": d,
                "label": DEPT_LABELS[d],
                "hue": DEPT_HUES.get(d, 200),
                "count": len(members),
            })
    for s in skills:
        if s["dept"] not in DEPT_LABELS and not any(x["id"] == s["dept"] for x in depts):
            depts.append({"id": s["dept"], "label": s["deptLabel"], "hue": s["hue"],
                          "count": sum(1 for x in skills if x["dept"] == s["dept"])})

    data = {"skills": skills, "edges": edges, "departments": depts}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    html = TEMPLATE.replace("/*__DATA__*/null", payload)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    print(f"Skill Atlas written to {OUT}")
    print(f"  {len(skills)} skills, {len(depts)} departments, {len(edges)} connections")
    orphans = [s['id'] for s in skills if not s['calls'] and not s['calledBy']]
    if orphans:
        print("  unconnected: " + ", ".join(orphans))


TEMPLATE = r"""<!doctype html>
<html lang="en" data-theme="auto">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Skill Atlas</title>
<style>
:root{
  --bg:#f6f7f9; --panel:#ffffff; --panel-2:#f0f2f5; --edge:#d9dde3;
  --ink:#12161c; --ink-2:#5a636f; --ink-3:#8b939f;
  --accent:#2f6df6; --shadow:0 1px 2px rgba(16,22,30,.06),0 8px 24px rgba(16,22,30,.06);
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --node-l:52%; --node-s:70%;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#0d1117; --panel:#151b23; --panel-2:#1c232d; --edge:#2a323d;
    --ink:#e8edf4; --ink-2:#9aa5b4; --ink-3:#6b7684;
    --accent:#5b8cff; --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
    --node-l:62%; --node-s:62%;
  }
}
:root[data-theme="dark"]{
  --bg:#0d1117; --panel:#151b23; --panel-2:#1c232d; --edge:#2a323d;
  --ink:#e8edf4; --ink-2:#9aa5b4; --ink-3:#6b7684;
  --accent:#5b8cff; --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
  --node-l:62%; --node-s:62%;
}
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
  font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow:hidden}
button{font:inherit;color:inherit;cursor:pointer}

#app{display:grid;grid-template-rows:auto 1fr;height:100vh}

header{display:flex;align-items:center;gap:18px;padding:12px 18px;
  background:var(--panel);border-bottom:1px solid var(--edge);flex-wrap:wrap}
.brand{font-size:16px;font-weight:650;letter-spacing:-.015em;white-space:nowrap}
.counts{display:flex;gap:14px;color:var(--ink-2);font-size:12.5px;white-space:nowrap}
.counts b{color:var(--ink);font-variant-numeric:tabular-nums;font-weight:600}
.grow{flex:1 1 120px}
#search{width:100%;max-width:340px;padding:7px 11px;border-radius:8px;
  border:1px solid var(--edge);background:var(--panel-2);color:var(--ink);font-size:13px}
#search:focus{outline:2px solid var(--accent);outline-offset:-1px}
.tbtn{background:var(--panel-2);border:1px solid var(--edge);border-radius:8px;
  padding:6px 11px;font-size:12.5px}
.tbtn:hover{border-color:var(--accent)}

main{display:grid;grid-template-columns:250px minmax(0,1fr) minmax(0,440px);
  min-height:0;overflow:hidden}
@media (max-width:1100px){main{grid-template-columns:210px minmax(0,1fr)}
  #detail{position:fixed;inset:0 0 0 auto;width:min(440px,100%);z-index:20;
    box-shadow:var(--shadow);transform:translateX(100%);transition:transform .18s ease}
  #detail.open{transform:none}}
@media (max-width:720px){main{grid-template-columns:1fr}#sidebar{display:none}}

#sidebar{background:var(--panel);border-right:1px solid var(--edge);
  overflow-y:auto;padding:10px 0}
.dept{padding:2px 0 8px}
.dept-h{display:flex;align-items:center;gap:8px;padding:7px 14px 5px;
  font-size:10.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-2)}
.dot{width:9px;height:9px;border-radius:50%;flex:none}
.dept-h span.n{margin-left:auto;color:var(--ink-3);font-weight:600;letter-spacing:0}
.sk{display:block;width:100%;text-align:left;background:none;border:0;
  padding:5px 14px 5px 31px;font-size:13px;color:var(--ink-2);
  border-left:2px solid transparent;overflow:hidden;text-overflow:ellipsis;
  white-space:nowrap}
.sk:hover{background:var(--panel-2);color:var(--ink)}
.sk.sel{background:var(--panel-2);color:var(--ink);font-weight:600}
.sk.orch::after{content:"chain";float:right;font-size:9.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--ink-3);font-weight:700}
.sk.dim{opacity:.25}

#graphwrap{position:relative;min-width:0;overflow:hidden;background:var(--bg)}
#graph{display:block;width:100%;height:100%;cursor:grab}
#graph.drag{cursor:grabbing}
.hint{position:absolute;left:14px;bottom:12px;color:var(--ink-3);font-size:11.5px;
  pointer-events:none;user-select:none}
#tip{position:absolute;pointer-events:none;background:var(--panel);
  border:1px solid var(--edge);border-radius:7px;padding:5px 9px;font-size:12px;
  box-shadow:var(--shadow);opacity:0;transition:opacity .1s;white-space:nowrap;z-index:5}

#detail{background:var(--panel);border-left:1px solid var(--edge);
  overflow-y:auto;min-width:0}
.d-head{position:sticky;top:0;background:var(--panel);border-bottom:1px solid var(--edge);
  padding:14px 18px 12px;z-index:2}
.d-dept{display:inline-flex;align-items:center;gap:6px;font-size:10.5px;font-weight:700;
  letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2)}
.d-title{font-size:19px;font-weight:660;letter-spacing:-.02em;margin:6px 0 2px;
  font-family:var(--mono)}
.d-path{font-size:11.5px;color:var(--ink-3);font-family:var(--mono);word-break:break-all}
.d-close{position:absolute;top:12px;right:14px;background:none;border:0;
  color:var(--ink-3);font-size:19px;line-height:1;padding:2px 6px}
.links{display:flex;flex-wrap:wrap;gap:6px;padding:11px 18px 0}
.links .lbl{width:100%;font-size:10.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-3);margin-bottom:-2px}
.chip{background:var(--panel-2);border:1px solid var(--edge);border-radius:20px;
  padding:3px 10px;font-size:11.5px;font-family:var(--mono);color:var(--ink-2)}
.chip:hover{border-color:var(--accent);color:var(--ink)}

.md{padding:14px 18px 60px;font-size:13.5px;color:var(--ink-2);overflow-wrap:break-word}
.md h1,.md h2,.md h3{color:var(--ink);letter-spacing:-.015em;line-height:1.3}
.md h1{font-size:17px;margin:20px 0 8px}
.md h2{font-size:15px;margin:22px 0 7px;padding-top:12px;border-top:1px solid var(--edge)}
.md h3{font-size:13.5px;margin:16px 0 5px}
.md p{margin:0 0 9px}
.md ul,.md ol{margin:0 0 10px;padding-left:20px}
.md li{margin-bottom:3px}
.md strong{color:var(--ink);font-weight:640}
.md code{font-family:var(--mono);font-size:12px;background:var(--panel-2);
  border:1px solid var(--edge);border-radius:4px;padding:.5px 4px}
.md pre{background:var(--panel-2);border:1px solid var(--edge);border-radius:8px;
  padding:10px 12px;overflow-x:auto;margin:0 0 11px}
.md pre code{background:none;border:0;padding:0;font-size:11.5px;line-height:1.5}
.md blockquote{margin:0 0 11px;padding:2px 0 2px 12px;border-left:3px solid var(--edge);
  color:var(--ink-3)}
.md hr{border:0;border-top:1px solid var(--edge);margin:16px 0}
.md .tw{overflow-x:auto;margin:0 0 12px}
.md table{border-collapse:collapse;font-size:12.5px;min-width:100%}
.md th,.md td{border:1px solid var(--edge);padding:5px 9px;text-align:left;
  vertical-align:top}
.md th{background:var(--panel-2);color:var(--ink);font-weight:620;white-space:nowrap}
.empty{padding:44px 22px;color:var(--ink-3);text-align:center;font-size:13px}
</style>
</head>
<body>
<div id="app">
  <header>
    <div class="brand">Skill Atlas</div>
    <div class="counts">
      <span><b id="c-s">0</b> skills</span>
      <span><b id="c-d">0</b> departments</span>
      <span><b id="c-e">0</b> connections</span>
    </div>
    <div class="grow"><input id="search" type="search" placeholder="Search skills, descriptions, contents..." autocomplete="off"></div>
    <button class="tbtn" id="theme">Theme</button>
  </header>
  <main>
    <nav id="sidebar"></nav>
    <div id="graphwrap">
      <canvas id="graph"></canvas>
      <div id="tip"></div>
      <div class="hint">Click a node to read it. Drag to pan, scroll to zoom.</div>
    </div>
    <aside id="detail"><div class="empty">Select a skill to read it.</div></aside>
  </main>
</div>
<script>
const DATA = /*__DATA__*/null;
const S = DATA.skills, E = DATA.edges, D = DATA.departments;
const byId = Object.fromEntries(S.map(s => [s.id, s]));
const $ = id => document.getElementById(id);

$("c-s").textContent = S.length;
$("c-d").textContent = D.length;
$("c-e").textContent = E.length;

/* ---------- theme ---------- */
const root = document.documentElement;
$("theme").onclick = () => {
  const cur = root.getAttribute("data-theme");
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  const now = cur === "auto" ? (dark ? "light" : "dark") : (cur === "dark" ? "light" : "dark");
  root.setAttribute("data-theme", now);
  css = null; draw();
};

let css = null;
function C(){
  if (!css) {
    const cs = getComputedStyle(root);
    css = {
      edge: cs.getPropertyValue("--edge").trim(),
      ink: cs.getPropertyValue("--ink").trim(),
      ink2: cs.getPropertyValue("--ink-2").trim(),
      ink3: cs.getPropertyValue("--ink-3").trim(),
      panel: cs.getPropertyValue("--panel").trim(),
      accent: cs.getPropertyValue("--accent").trim(),
      l: cs.getPropertyValue("--node-l").trim() || "52%",
      s: cs.getPropertyValue("--node-s").trim() || "70%"
    };
  }
  return css;
}
const hue = h => `hsl(${h} ${C().s} ${C().l})`;

/* ---------- sidebar ---------- */
function buildSidebar(){
  const nav = $("sidebar");
  nav.innerHTML = "";
  D.forEach(d => {
    const wrap = document.createElement("div");
    wrap.className = "dept";
    const h = document.createElement("div");
    h.className = "dept-h";
    h.innerHTML = `<i class="dot" style="background:${hue(d.hue)}"></i>${d.label}<span class="n">${d.count}</span>`;
    wrap.appendChild(h);
    S.filter(s => s.dept === d.id).forEach(s => {
      const b = document.createElement("button");
      b.className = "sk" + (s.orchestrator ? " orch" : "");
      b.dataset.id = s.id;
      b.textContent = s.id;
      b.onclick = () => select(s.id);
      wrap.appendChild(b);
    });
    nav.appendChild(wrap);
  });
}

/* ---------- markdown ---------- */
function esc(t){ return t.replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }
function inline(t){
  return esc(t)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[\s(])\*([^*\n]+)\*/g, "$1<em>$2</em>");
}
function md(src){
  const L = src.split("\n"); let o = "", i = 0;
  const row = l => l.trim().replace(/^\||\|$/g, "").split("|").map(c => c.trim());
  while (i < L.length){
    let l = L[i];
    if (/^```/.test(l)){
      i++; let b = [];
      while (i < L.length && !/^```/.test(L[i])) b.push(L[i++]);
      i++; o += "<pre><code>" + esc(b.join("\n")) + "</code></pre>"; continue;
    }
    if (/^<!--/.test(l)){ while (i < L.length && !/-->/.test(L[i])) i++; i++; continue; }
    if (/^\s*$/.test(l)){ i++; continue; }
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(l)){ o += "<hr>"; i++; continue; }
    let m = l.match(/^(#{1,6})\s+(.*)$/);
    if (m){ const n = Math.min(m[1].length, 3); o += `<h${n}>${inline(m[2])}</h${n}>`; i++; continue; }
    if (/^\s*\|/.test(l) && i + 1 < L.length && /^\s*\|?[\s:|-]+\|/.test(L[i+1])){
      const head = row(l); i += 2; let body = [];
      while (i < L.length && /^\s*\|/.test(L[i])) body.push(row(L[i++]));
      o += '<div class="tw"><table><thead><tr>' +
        head.map(c => `<th>${inline(c)}</th>`).join("") + "</tr></thead><tbody>" +
        body.map(r => "<tr>" + r.map(c => `<td>${inline(c)}</td>`).join("") + "</tr>").join("") +
        "</tbody></table></div>";
      continue;
    }
    if (/^\s*>/.test(l)){
      let b = [];
      while (i < L.length && /^\s*>/.test(L[i])) b.push(L[i++].replace(/^\s*>\s?/, ""));
      o += "<blockquote>" + md(b.join("\n")) + "</blockquote>"; continue;
    }
    if (/^\s*([-*+]|\d+\.)\s+/.test(l)){
      const ol = /^\s*\d+\./.test(l); let items = [];
      while (i < L.length && /^\s*([-*+]|\d+\.)\s+/.test(L[i])){
        let t = L[i++].replace(/^\s*([-*+]|\d+\.)\s+/, "");
        while (i < L.length && /^\s{2,}\S/.test(L[i]) && !/^\s*([-*+]|\d+\.)\s+/.test(L[i]))
          t += " " + L[i++].trim();
        items.push(`<li>${inline(t)}</li>`);
      }
      o += (ol ? "<ol>" : "<ul>") + items.join("") + (ol ? "</ol>" : "</ul>"); continue;
    }
    let p = [];
    while (i < L.length && !/^\s*$/.test(L[i]) && !/^(#{1,6}\s|\s*[-*+]\s|\s*\d+\.\s|\s*>|\s*\||```|<!--)/.test(L[i]))
      p.push(L[i++]);
    if (p.length) o += `<p>${inline(p.join(" "))}</p>`; else i++;
  }
  return o;
}

/* ---------- detail ---------- */
let sel = null;
function select(id){
  sel = id; const s = byId[id];
  const d = $("detail");
  const chips = (arr, lbl) => arr.length
    ? `<div class="links"><span class="lbl">${lbl}</span>` +
      arr.map(n => `<button class="chip" data-go="${n}">${n}</button>`).join("") + "</div>"
    : "";
  d.innerHTML =
    `<div class="d-head">
       <button class="d-close" title="Close">&times;</button>
       <div class="d-dept"><i class="dot" style="background:${hue(s.hue)}"></i>${s.deptLabel}</div>
       <div class="d-title">${esc(s.id)}</div>
       <div class="d-path">skills/${esc(s.path)}</div>
     </div>
     ${chips(s.calls, "Calls")}${chips(s.calledBy, "Called by")}
     <div class="md">${md(s.body)}</div>`;
  d.classList.add("open");
  d.scrollTop = 0;
  d.querySelector(".d-close").onclick = () => d.classList.remove("open");
  d.querySelectorAll("[data-go]").forEach(b => b.onclick = () => select(b.dataset.go));
  document.querySelectorAll(".sk").forEach(b => b.classList.toggle("sel", b.dataset.id === id));
  const cur = document.querySelector(".sk.sel");
  if (cur) cur.scrollIntoView({ block: "nearest" });
  draw();
}

/* ---------- search ---------- */
let matches = null;
$("search").oninput = e => {
  const q = e.target.value.trim().toLowerCase();
  matches = q ? new Set(S.filter(s =>
    s.id.toLowerCase().includes(q) ||
    s.description.toLowerCase().includes(q) ||
    s.body.toLowerCase().includes(q)).map(s => s.id)) : null;
  document.querySelectorAll(".sk").forEach(b =>
    b.classList.toggle("dim", !!matches && !matches.has(b.dataset.id)));
  draw();
};

/* ---------- force graph ---------- */
const cv = $("graph"), cx = cv.getContext("2d");
let W = 0, H = 0, dpr = 1;
const N = S.map(s => ({ id: s.id, dept: s.dept, hue: s.hue, orch: s.orchestrator,
  deg: 0, x: 0, y: 0, vx: 0, vy: 0 }));
const nById = Object.fromEntries(N.map(n => [n.id, n]));
E.forEach(e => { if (nById[e.source]) nById[e.source].deg++; if (nById[e.target]) nById[e.target].deg++; });
const LK = E.filter(e => nById[e.source] && nById[e.target])
            .map(e => ({ a: nById[e.source], b: nById[e.target] }));
const rOf = n => 5.5 + Math.min(9, Math.sqrt(n.deg) * 2.6) + (n.orch ? 2.2 : 0);

const hubs = {};
function layout(){
  const n = D.length, R = Math.min(W, H) * 0.30;
  D.forEach((d, i) => {
    const a = (i / n) * Math.PI * 2 - Math.PI / 2;
    hubs[d.id] = { x: W / 2 + Math.cos(a) * R, y: H / 2 + Math.sin(a) * R };
  });
}
function seed(){
  layout();
  N.forEach(nd => {
    const h = hubs[nd.dept] || { x: W / 2, y: H / 2 };
    nd.x = h.x + (Math.random() - .5) * 90;
    nd.y = h.y + (Math.random() - .5) * 90;
    nd.vx = nd.vy = 0;
  });
}
function tick(){
  // repulsion
  for (let i = 0; i < N.length; i++) for (let j = i + 1; j < N.length; j++){
    const a = N[i], b = N[j];
    let dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy || .01;
    if (d2 > 62500) continue;
    const d = Math.sqrt(d2), f = 1750 / d2;
    const ux = dx / d * f, uy = dy / d * f;
    a.vx -= ux; a.vy -= uy; b.vx += ux; b.vy += uy;
  }
  // links
  LK.forEach(l => {
    let dx = l.b.x - l.a.x, dy = l.b.y - l.a.y;
    const d = Math.hypot(dx, dy) || .01, f = (d - 108) * .012;
    const ux = dx / d * f, uy = dy / d * f;
    l.a.vx += ux; l.a.vy += uy; l.b.vx -= ux; l.b.vy -= uy;
  });
  // cluster gravity
  N.forEach(nd => {
    const h = hubs[nd.dept] || { x: W / 2, y: H / 2 };
    nd.vx += (h.x - nd.x) * .026; nd.vy += (h.y - nd.y) * .026;
    nd.vx *= .82; nd.vy *= .82;
    nd.x += nd.vx; nd.y += nd.vy;
  });
}

let view = { x: 0, y: 0, k: 1 };
const sx = n => n.x * view.k + view.x, sy = n => n.y * view.k + view.y;

function draw(){
  const c = C();
  cx.setTransform(dpr, 0, 0, dpr, 0, 0);
  cx.clearRect(0, 0, W, H);

  // department halos
  cx.save();
  D.forEach(d => {
    const h = hubs[d.id]; if (!h) return;
    const pts = N.filter(n => n.dept === d.id);
    if (!pts.length) return;
    let r = 0; pts.forEach(p => r = Math.max(r, Math.hypot(p.x - h.x, p.y - h.y)));
    cx.globalAlpha = .07;
    cx.fillStyle = hue(d.hue);
    cx.beginPath();
    cx.arc(h.x * view.k + view.x, h.y * view.k + view.y, (r + 34) * view.k, 0, 7);
    cx.fill();
    cx.globalAlpha = 1;
    cx.fillStyle = c.ink3;
    cx.font = `700 ${Math.max(9, 10.5 * view.k)}px ${getComputedStyle(document.body).fontFamily}`;
    cx.textAlign = "center";
    cx.fillText(d.label.toUpperCase(),
      h.x * view.k + view.x, h.y * view.k + view.y - (r + 44) * view.k);
  });
  cx.restore();

  const near = sel ? new Set([sel, ...(byId[sel].calls), ...(byId[sel].calledBy)]) : null;

  // edges
  LK.forEach(l => {
    const hot = near && (l.a.id === sel || l.b.id === sel);
    cx.strokeStyle = hot ? c.accent : c.edge;
    cx.globalAlpha = near ? (hot ? .95 : .18) : .55;
    cx.lineWidth = hot ? 1.7 : 1;
    cx.beginPath(); cx.moveTo(sx(l.a), sy(l.a)); cx.lineTo(sx(l.b), sy(l.b)); cx.stroke();
  });
  cx.globalAlpha = 1;

  // nodes
  N.forEach(n => {
    const r = rOf(n) * Math.max(.62, view.k);
    const dim = (matches && !matches.has(n.id)) || (near && !near.has(n.id));
    cx.globalAlpha = dim ? .2 : 1;
    cx.beginPath(); cx.arc(sx(n), sy(n), r, 0, 7);
    cx.fillStyle = hue(n.hue); cx.fill();
    if (n.id === sel){
      cx.lineWidth = 2.5; cx.strokeStyle = c.ink; cx.stroke();
    } else if (n.orch){
      cx.lineWidth = 1.6; cx.strokeStyle = c.panel; cx.stroke();
    }
    if (view.k > .72 || n.deg > 3 || n.id === sel){
      cx.globalAlpha = dim ? .18 : .92;
      cx.fillStyle = c.ink2;
      cx.font = `${n.orch ? 600 : 400} ${Math.max(9, 10.5 * Math.min(1.25, view.k))}px ui-monospace,monospace`;
      cx.textAlign = "center";
      cx.fillText(n.id, sx(n), sy(n) + r + 11);
    }
    cx.globalAlpha = 1;
  });
}

function hit(mx, my){
  for (let i = N.length - 1; i >= 0; i--){
    const n = N[i], r = rOf(n) * Math.max(.62, view.k) + 4;
    if ((mx - sx(n)) ** 2 + (my - sy(n)) ** 2 <= r * r) return n;
  }
  return null;
}

let drag = null, moved = 0;
cv.addEventListener("pointerdown", e => {
  const r = cv.getBoundingClientRect();
  drag = { x: e.clientX - r.left, y: e.clientY - r.top, n: hit(e.clientX - r.left, e.clientY - r.top) };
  moved = 0; cv.setPointerCapture(e.pointerId); cv.classList.add("drag");
});
cv.addEventListener("pointermove", e => {
  const r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
  if (drag){
    const dx = mx - drag.x, dy = my - drag.y;
    moved += Math.abs(dx) + Math.abs(dy);
    if (drag.n){ drag.n.x += dx / view.k; drag.n.y += dy / view.k; drag.n.vx = drag.n.vy = 0; }
    else { view.x += dx; view.y += dy; }
    drag.x = mx; drag.y = my; draw(); return;
  }
  const n = hit(mx, my), t = $("tip");
  if (n){
    t.textContent = n.id + "  (" + n.deg + ")";
    t.style.left = (mx + 13) + "px"; t.style.top = (my + 13) + "px"; t.style.opacity = 1;
    cv.style.cursor = "pointer";
  } else { t.style.opacity = 0; cv.style.cursor = ""; }
});
cv.addEventListener("pointerup", e => {
  cv.classList.remove("drag");
  if (drag && drag.n && moved < 5) select(drag.n.id);
  drag = null;
});
cv.addEventListener("wheel", e => {
  e.preventDefault();
  const r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
  const k = Math.min(3, Math.max(.35, view.k * (e.deltaY < 0 ? 1.11 : .9)));
  view.x = mx - (mx - view.x) * (k / view.k);
  view.y = my - (my - view.y) * (k / view.k);
  view.k = k; draw();
}, { passive: false });

function resize(){
  const r = $("graphwrap").getBoundingClientRect();
  dpr = Math.min(2, devicePixelRatio || 1);
  W = r.width; H = r.height;
  cv.width = W * dpr; cv.height = H * dpr;
  cv.style.width = W + "px"; cv.style.height = H + "px";
  layout();
}
addEventListener("resize", () => { resize(); draw(); });
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { css = null; buildSidebar(); draw(); });

buildSidebar();
resize(); seed();
for (let i = 0; i < 420; i++) tick();
draw();
(function settle(n){ if (n > 0){ tick(); draw(); requestAnimationFrame(() => settle(n - 1)); } })(160);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
