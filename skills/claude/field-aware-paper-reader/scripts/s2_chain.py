#!/usr/bin/env python3
"""
Citation chaining helper.

Backends:
  s2        Semantic Scholar Graph API (default). Gives the sentence in which each
            citing paper cites the node ("contexts"), which is the best signal for
            "B fixes / benchmarks against A". Set S2_API_KEY for higher rate limits.
  openalex  OpenAlex API. Fallback when S2 is blocked or rate-limited. No citation
            contexts, so ranking uses title + abstract keywords.

Usage:
  python s2_chain.py search "<paper title or method keywords>" [--backend openalex]
  python s2_chain.py forward <id> [--backend s2|openalex] [--limit 300] [--top 25] [--since 2023]
  python s2_chain.py backward <id> [--backend s2|openalex] [--top 25]

<id>: S2 paperId, DOI:10.xxx, ARXIV:xxxx (s2)  |  OpenAlex W-id or DOI:10.xxx (openalex)
If a backend fails, the script says so explicitly: treat that as "channel failed",
never as "no successors exist".
"""
import json, os, re, sys, time, argparse, urllib.parse, urllib.request, urllib.error

SIGNAL = re.compile(
    r"\b(limitation|limited|however|unlike|fail\w*|suffer\w*|drawback|shortcoming|"
    r"cannot|unable|restrict\w*|assum\w*|bias\w*|improv\w*|extend\w*|overcome|"
    r"address\w*|alleviat\w*|instead|in contrast|remed\w*|mitigat\w*|beyond|"
    r"generaliz\w*|baseline\w*|compar\w*|outperform\w*|competing|state[- ]of[- ]the[- ]art)\b",
    re.I)


REQUESTS = []


def http_json(url, headers=None):
    # No automatic retry: a rate-limited or blocked channel should not stall a reading.
    safe_url = re.sub(r"([?&]api_key=)[^&]+", r"\1REDACTED", url)
    entry = {"url": safe_url, "status": "pending"}
    REQUESTS.append(entry)
    headers = {"User-Agent": "field-aware-paper-reader/2", **(headers or {})}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15) as response:
            data = json.loads(response.read().decode())
            entry["status"] = response.status
            return data
    except Exception as exc:
        entry["status"] = getattr(exc, "code", "transport_or_decode_error")
        # Do not include exception text: URLs can contain credentials.
        raise RuntimeError(f"Request failed: {entry['status']} ({type(exc).__name__})") from None


# ---------------- Semantic Scholar ----------------
S2 = "https://api.semanticscholar.org/graph/v1"
S2F = "title,year,venue,citationCount,externalIds,url"


def s2_get(path, params):
    h = {"x-api-key": os.environ["S2_API_KEY"]} if os.environ.get("S2_API_KEY") else {}
    return http_json(f"{S2}{path}?{urllib.parse.urlencode(params)}", h)


def s2_search(q):
    return [norm_s2(p) for p in s2_get("/paper/search", {"query": q, "limit": 10, "fields": S2F}).get("data", [])]


def s2_links(pid, kind, limit):
    key = "citingPaper" if kind == "citations" else "citedPaper"
    fields = "contexts,intents,isInfluential," + ",".join(f"{key}.{f}" for f in S2F.split(",")) + f",{key}.paperId"
    out, off = [], 0
    while off < limit:
        res = s2_get(f"/paper/{urllib.parse.quote(pid, safe='')}/{kind}", {"fields": fields, "limit": min(100, limit - off), "offset": off})
        data = res.get("data", [])
        for d in data:
            p = norm_s2(d.get(key) or {})
            p.update(contexts=d.get("contexts") or [], intents=d.get("intents") or [], influential=bool(d.get("isInfluential")))
            out.append(p)
        if res.get("next") is None or not data: break
        next_off = res["next"]
        if not isinstance(next_off, int) or next_off <= off:
            raise ValueError("Non-advancing Semantic Scholar pagination")
        off = next_off
    return out


def norm_s2(p):
    ids = p.get("externalIds") or {}
    return {"id": p.get("paperId"), "title": p.get("title"), "year": p.get("year"), "venue": p.get("venue"),
            "cites": p.get("citationCount"), "doi": ids.get("DOI"), "arxiv": ids.get("ArXiv"),
            "url": p.get("url"), "text": ""}


# ---------------- OpenAlex ----------------
OA = "https://api.openalex.org"


def oa_get(path, params):
    params = dict(params)
    if os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = os.environ["OPENALEX_API_KEY"]
    return http_json(f"{OA}{path}?{urllib.parse.urlencode(params)}")


def oa_abstract(inv):
    if not inv: return ""
    pos = {i: w for w, idxs in inv.items() for i in idxs}
    return " ".join(pos[i] for i in sorted(pos))


def norm_oa(w):
    return {"id": (w.get("id") or "").rsplit("/", 1)[-1], "title": w.get("display_name"), "year": w.get("publication_year"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "cites": w.get("cited_by_count"), "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "arxiv": None, "url": w.get("doi") or w.get("id"), "text": oa_abstract(w.get("abstract_inverted_index")),
            "contexts": [], "intents": [], "influential": False}


def oa_resolve(pid):
    if pid.upper().startswith("DOI:"):
        return oa_get(f"/works/doi:{pid[4:]}", {})["id"].rsplit("/", 1)[-1]
    if not re.fullmatch(r"W\d+", pid):
        raise ValueError("OpenAlex requires DOI:<doi> or W<digits>")
    return pid


def oa_search(q):
    return [norm_oa(w) for w in oa_get("/works", {"search": q, "per-page": 10}).get("results", [])]


def oa_links(pid, kind, limit):
    wid = oa_resolve(pid)
    if kind == "references":
        refs = oa_get(f"/works/{wid}", {}).get("referenced_works", [])[:limit]
        out = []
        for i in range(0, len(refs), 50):
            ids = "|".join(r.rsplit("/", 1)[-1] for r in refs[i:i + 50])
            out += [norm_oa(w) for w in oa_get("/works", {"filter": f"openalex:{ids}", "per-page": 50}).get("results", [])]
        return out
    out, cursor = [], "*"
    while cursor and len(out) < limit:
        res = oa_get("/works", {"filter": f"cites:{wid}", "per-page": min(100, limit - len(out)), "cursor": cursor, "sort": "cited_by_count:desc"})
        out += [norm_oa(w) for w in res.get("results", [])]
        next_cursor = (res.get("meta") or {}).get("next_cursor")
        if not res.get("results"):
            break
        if next_cursor == cursor:
            raise ValueError("Non-advancing OpenAlex pagination")
        cursor = next_cursor
    return out[:limit]


# ---------------- ranking / output ----------------
def score(p, since):
    if since and (p.get("year") or 0) < since: return None
    txt = " ".join(p.get("contexts") or []) + " " + (p.get("title") or "") + " " + (p.get("text") or "")
    s = 3 * len(SIGNAL.findall(txt)) + (5 if p.get("influential") else 0)
    s += 2 * sum(1 for i in p.get("intents") or [] if i in ("methodology", "result"))
    s += min(5, (p.get("cites") or 0) ** 0.5 / 4)
    s += 2 if (p.get("year") or 0) >= time.gmtime().tm_year - 1 else 0   # recency bonus
    return s


def fmt(p):
    tag = f"arXiv:{p['arxiv']}" if p.get("arxiv") else (f"DOI:{p['doi']}" if p.get("doi") else "")
    return f"{p.get('title')} ({p.get('year')}, {p.get('venue') or '-'}) cites={p.get('cites')} {tag}\n    id={p.get('id')} {p.get('url') or ''}"


def fetch_urls(mode, arg):
    """Credential-free fallback URLs. DOI resolution must precede OA chaining."""
    q = urllib.parse.quote(arg, safe="")
    if mode == "search":
        return [f"{S2}/paper/search?query={q}&limit=10&fields={S2F}",
                f"{OA}/works?search={q}&per-page=10"]
    kind = "citations" if mode == "forward" else "references"
    key = "citingPaper" if kind == "citations" else "citedPaper"
    urls = [f"{S2}/paper/{q}/{kind}?limit=100&fields=contexts,intents,isInfluential,{key}.title,{key}.year,"
            f"{key}.venue,{key}.externalIds,{key}.citationCount"]
    if arg.upper().startswith("DOI:"):
        urls.append(f"{OA}/works/https://doi.org/{urllib.parse.quote(arg[4:], safe='/')}")
    elif re.fullmatch(r"W\d+", arg):
        urls.append(f"{OA}/works?filter=cites:{arg}&per-page=100" if mode == "forward" else f"{OA}/works/{arg}")
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["search", "forward", "backward"])
    ap.add_argument("arg")
    ap.add_argument("--backend", choices=["s2", "openalex"], default="s2")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--since", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--urls-only", action="store_true")
    a = ap.parse_args()
    if not 1 <= a.limit <= 1000 or a.top < 1:
        ap.error("--limit must be 1..1000 and --top must be positive")
    if a.urls_only:
        print("\n".join(fetch_urls(a.mode, a.arg)))
        return
    REQUESTS.clear()
    report = {"backend": a.backend, "mode": a.mode, "query": a.arg,
              "searched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "limit": a.limit, "top": a.top, "since": a.since,
              "requests": REQUESTS, "status": "ok", "items": []}
    try:
        if a.mode == "search":
            items = (s2_search if a.backend == "s2" else oa_search)(a.arg)
        else:
            kind = "citations" if a.mode == "forward" else "references"
            items = (s2_links if a.backend == "s2" else oa_links)(a.arg, kind, a.limit)
        unique, seen = [], set()
        for item in items:
            key = (item.get("doi") or item.get("id") or item.get("title") or "").lower()
            if key and key not in seen:
                unique.append(item); seen.add(key)
        ranked = [(score(p, a.since), p) for p in unique]
        ranked = sorted((v for v in ranked if v[0] is not None), key=lambda v: -v[0])
        report.update(fetched_count=len(items), unique_count=len(unique),
                      at_fetch_cap=len(items) >= (10 if a.mode == "search" else a.limit),
                      items=[dict(p, ranking_score=value) for value, p in ranked[:a.top]],
                      exhaustive=False)
    except Exception as exc:
        report.update(status="failed", error=str(exc), fallback_urls=fetch_urls(a.mode, a.arg))
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(serialized + "\n")
    if a.json:
        print(serialized)
    elif report["status"] == "failed":
        print(f"CHANNEL FAILED ({a.backend}): {report['error']}. Not evidence of zero citations.", file=sys.stderr)
        print("\n".join(report["fallback_urls"]), file=sys.stderr)
    else:
        print(f"{report['fetched_count']} records fetched via {a.backend}; capped search, not exhaustive")
        for p in report["items"]:
            print("\n" + fmt(p))
            for context in p.get("contexts", [])[:3]:
                print("    >", re.sub(r"\s+", " ", context)[:500])
    if report["status"] == "failed":
        sys.exit(2)


if __name__ == "__main__":
    main()
