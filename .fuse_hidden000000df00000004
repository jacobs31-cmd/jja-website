#!/usr/bin/env python3
"""
JJA Insurance — Add Images to Buffer Posts (All Platforms)
- Facebook / LinkedIn / X: adds branded image to all scheduled posts
- Instagram: matches each draft to its original scheduled date, adds image,
  and flips it from draft → properly scheduled post

Resume-safe: tracks completed post IDs in buffer_images_done.txt
Auto-retry: waits 16 minutes automatically if rate limited, then continues

Run: python add_images_to_buffer.py
Key: nqDdUW6a5cm41J2aIpGgTxG7gBra0pUsI7Ge3GBvu5n
"""

import json, sys, time, os, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

API    = "https://api.buffer.com"
ORG_ID = "6a14a87235f22ccc6a284ead"
TIMEZONE_OFFSET = -4   # EDT (UTC-4, May–Aug)
SLEEP_SECONDS   = 10   # between every API call — 90 req/15 min, safely under limit
DONE_FILE       = r"C:\Website\buffer_images_done.txt"  # tracks successful post IDs for resume

IMAGES = {
    "home":       "https://jjainsurance.com/social-images/jja_home_insurance.png",
    "auto":       "https://jjainsurance.com/social-images/jja_auto_insurance.png",
    "commercial": "https://jjainsurance.com/social-images/jja_commercial.png",
    "workers":    "https://jjainsurance.com/social-images/jja_workers_comp.png",
    "life":       "https://jjainsurance.com/social-images/jja_life_insurance.png",
    "tips":       "https://jjainsurance.com/social-images/jja_insurance_tips.png",
}

INSTAGRAM_SCHEDULE = [
    ("05/26/2026", "11:00", "Your home insurance went up"),
    ("05/28/2026", "11:00", "Deductible too low"),
    ("06/01/2026", "11:00", "Bundling home + auto"),
    ("06/03/2026", "11:00", "Michigan auto insurance has 6 PIP"),
    ("06/08/2026", "11:00", "Michigan business owners — do you actually need workers"),
    ("06/10/2026", "11:00", "Skipping your workers' comp audit"),
    ("06/15/2026", "11:00", "Small businesses are the #1 target for ransomware"),
    ("06/17/2026", "11:00", "Summer event coming up"),
    ("06/22/2026", "11:00", "Collision vs. comprehensive"),
    ("06/24/2026", "11:00", "1 in 5 Michigan drivers is uninsured"),
    ("06/29/2026", "11:00", "Back on two wheels"),
    ("07/01/2026", "11:00", "Boat, RV, ATV, jet ski"),
    ("07/06/2026", "11:00", "25 insurance questions Michigan residents ask most"),
    ("07/08/2026", "11:00", "Should you file that claim"),
    ("07/13/2026", "11:00", "Replacement cost vs. actual cash value"),
    ("07/15/2026", "11:00", "Michigan homeowners: your home insurance almost certainly does NOT cover flood"),
    ("07/20/2026", "11:00", "Michigan drivers: auto insurance refund scams"),
    ("07/22/2026", "11:00", "3 signs that insurance call is actually a scam"),
    ("07/27/2026", "11:00", "45 years in Michigan"),
    ("07/29/2026", "11:00", "Best of the Best — 8 years straight"),
    ("08/03/2026", "11:00", "Teen driver in your house"),
    ("08/05/2026", "11:00", "Kid heading to college"),
    ("08/10/2026", "11:00", "Would your family be financially okay"),
    ("08/12/2026", "11:00", "Life insurance rule of thumb"),
    ("08/17/2026", "11:00", "Captive agent = one carrier"),
    ("08/19/2026", "11:00", "Got a non-renewal notice"),
]

# ── Resume helpers ─────────────────────────────────────────────────────────────

def load_done_ids():
    """Return set of post IDs already successfully updated."""
    if not os.path.exists(DONE_FILE):
        return set()
    with open(DONE_FILE) as f:
        return set(line.strip() for line in f if line.strip())

def mark_done(post_id):
    """Append a post ID to the done file."""
    with open(DONE_FILE, "a") as f:
        f.write(post_id + "\n")

# ── Utility ────────────────────────────────────────────────────────────────────

def to_iso(date_str, time_str):
    dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
    tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    return dt.replace(tzinfo=tz).isoformat()

def normalize_due_at(due_at):
    """Buffer may return dueAt as ISO string or Unix timestamp — always return ISO string."""
    if due_at is None:
        return None
    if isinstance(due_at, str):
        return due_at
    if isinstance(due_at, (int, float)):
        ts = due_at / 1000 if due_at > 1e10 else due_at
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    return str(due_at)

def pick_image(text):
    t = text.lower()
    if any(k in t for k in [
        "homeowners", "home insurance", "home-insurance", "why-home", "homegl",
        "replacement cost", "actual cash value", "flood insurance", "flood damage",
        "deductible", "roof claim"
    ]):
        return IMAGES["home"]
    # "workers" only — NOT "comp" because "comp" is a substring of "comprehensive"
    if any(k in t for k in ["workers", "wcaudit", "wcguide"]):
        return IMAGES["workers"]
    if any(k in t for k in [
        "commercial", "cyber", "special-event", "special event", "business insurance",
        "bop", "contractor", "ransomware", "event insurance", "key person"
    ]):
        return IMAGES["commercial"]
    if any(k in t for k in [
        "life insurance", "life-insurance", "term life", "whole life",
        "financially okay", "10-12x your annual"
    ]):
        return IMAGES["life"]
    if any(k in t for k in [
        "auto", "vehicle", "car ", "motorcycle", "no-fault", "nofault", "driver",
        "scam", "refund", "autogl", "autoterm", "collision", "comprehensive",
        "uninsured motorist", "pip option", "two wheels", "teen driver"
    ]):
        return IMAGES["auto"]
    return IMAGES["tips"]

def match_instagram_schedule(text):
    t = text.lower()
    for date_str, time_str, snippet in INSTAGRAM_SCHEDULE:
        if snippet.lower() in t:
            return to_iso(date_str, time_str)
    return None

# ── API ────────────────────────────────────────────────────────────────────────

def gql(query, variables, api_key):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API, data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode()
        except Exception:
            body = str(e)
        return {"error": body}
    except Exception as e:
        return {"error": str(e)}

def get_rate_limit_window(result):
    """
    Returns the rate limit window string if rate limited, else None.
    e.g. "15m" or "24h"
    """
    errs = result.get("errors", [])
    if errs:
        ext  = errs[0].get("extensions", {})
        code = ext.get("code", "")
        msg  = errs[0].get("message", "")
        if "RATE_LIMIT" in code or "Too many requests" in msg:
            return ext.get("window", "15m")
    return None

def is_rate_limited(result):
    return get_rate_limit_window(result) is not None

def fetch_posts(api_key, status_filter):
    """Fetch all posts with the given status list (e.g. ["scheduled"] or ["draft"])."""
    q = """
    query GetPosts($input: PostsInput!, $first: Int, $after: String) {
      posts(input: $input, first: $first, after: $after) {
        edges {
          node {
            id text status schedulingType dueAt
            channel { id service }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
    """
    all_posts = []
    cursor = None
    page   = 1
    while True:
        variables = {
            "input": {
                "organizationId": ORG_ID,
                "filter": {"status": status_filter}  # "filter" singular; status is a list — verified by schema
            },
            "first": 50,
            "after": cursor
        }
        result = gql(q, variables, api_key)

        # Rate limit on fetch — handle by window type
        window = get_rate_limit_window(result)
        if window:
            if window == "24h":
                print(f"\n  !! 24-HOUR RATE LIMIT HIT !!")
                print(f"  Buffer allows 500 requests per day. You've reached that limit.")
                print(f"  Wait until tomorrow (same time or later) and run the script again.")
                print(f"  The script will automatically skip posts already completed.")
                print(f"  Done so far: {len(load_done_ids())} posts saved in {DONE_FILE}")
                sys.exit(0)
            else:
                print(f"  Rate limited (15-min window). Waiting 16 minutes...")
                time.sleep(16 * 60)
                continue  # retry same page

        if "error" in result:
            print(f"  ERROR fetching page {page}: {result['error'][:200]}")
            return []
        errs = result.get("errors")
        if errs:
            print(f"  ERROR fetching page {page}: {errs[0].get('message','?')[:200]}")
            return []

        posts_data = result.get("data", {}).get("posts", {})
        edges      = posts_data.get("edges", [])
        all_posts.extend([e["node"] for e in edges])
        print(f"  Page {page}: got {len(edges)} posts (running total: {len(all_posts)})")

        page_info = posts_data.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
        page  += 1
        time.sleep(SLEEP_SECONDS)

    return all_posts

def update_post(api_key, post_id, image_url, scheduling_type, due_at, service):
    """
    Edit a Buffer post to add a branded image.
    Facebook MUST include metadata.facebook.type — same requirement as createPost.
    """
    mutation = """
    mutation EditPost($input: EditPostInput!) {
      editPost(input: $input) {
        __typename
        ... on PostActionSuccess { post { id } }
        ... on InvalidInputError { message }
        ... on UnexpectedError   { message }
        ... on NotFoundError     { message }
        ... on UnauthorizedError { message }
        ... on RestProxyError    { message }
        ... on LimitReachedError { message }
      }
    }
    """
    inp = {
        "id":             post_id,
        "schedulingType": scheduling_type or "automatic",
        "mode":           "customScheduled",   # confirmed valid enum via schema introspection
        "dueAt":          due_at,
        "assets":         [{"image": {"url": image_url}}]
    }
    # Facebook requires a post type — identical to what createPost uses
    if service == "facebook":
        inp["metadata"] = {"facebook": {"type": "post"}}

    return gql(mutation, {"input": inp}, api_key)

# ── Batch processor ────────────────────────────────────────────────────────────

def run_batch(api_key, posts, done_ids):
    now = datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))
    ok = errors = skipped = already_done = 0
    n  = len(posts)

    for i, post in enumerate(posts, 1):
        pid    = post["id"]
        text   = post.get("text", "")
        svc    = post.get("channel", {}).get("service", "?")
        sched  = post.get("schedulingType", "automatic")
        due_at = normalize_due_at(post.get("dueAt"))
        image  = pick_image(text)
        label  = image.split("/")[-1].replace(".png", "")

        # Skip posts already successfully updated in a previous run
        if pid in done_ids:
            print(f"  [{i:3}/{n}] SKIP  {svc:10} (already done)")
            already_done += 1
            continue

        # Instagram drafts have no dueAt — look up from original schedule
        if svc == "instagram" and not due_at:
            due_at = match_instagram_schedule(text)
            if not due_at:
                print(f"  [{i:3}/{n}] SKIP  instagram  (no date match): {text[:50]!r}")
                skipped += 1
                continue
            dt = datetime.fromisoformat(due_at)
            if dt <= now:
                print(f"  [{i:3}/{n}] SKIP  instagram  (past-dated)")
                skipped += 1
                continue

        # Call editPost with auto-retry on rate limit
        result = None
        for attempt in range(5):  # up to 5 retries
            result = update_post(api_key, pid, image, sched, due_at, svc)
            window = get_rate_limit_window(result)
            if window == "24h":
                print(f"\n  [{i:3}/{n}] !! 24-HOUR RATE LIMIT HIT !!")
                print(f"  Buffer allows 500 requests per day. You've reached that limit.")
                print(f"  Wait until tomorrow (same time or later) and run the script again.")
                print(f"  Progress saved: {len(done_ids)} posts completed in {DONE_FILE}")
                sys.exit(0)
            elif window:
                print(f"  [{i:3}/{n}] Rate limited (15-min). Waiting 16 minutes...")
                time.sleep(16 * 60)
                continue
            break  # real response

        gql_errs = result.get("errors") if result else None
        api_err  = result.get("error")  if result else "no response"
        cp       = (result.get("data") or {}).get("editPost") or {}
        typename = cp.get("__typename", "")

        if api_err or gql_errs:
            msg = api_err if api_err else (gql_errs[0].get("message", "unknown") if gql_errs else "unknown")
            print(f"  [{i:3}/{n}] ERROR {svc:10} {pid}: {str(msg)[:80]}")
            errors += 1
        elif typename == "PostActionSuccess":
            print(f"  [{i:3}/{n}] OK    {svc:10} → {label}")
            mark_done(pid)
            done_ids.add(pid)
            ok += 1
        elif typename:
            print(f"  [{i:3}/{n}] ERROR {svc:10} {pid}: {cp.get('message', typename)}")
            errors += 1
        else:
            print(f"  [{i:3}/{n}] WARN  {svc:10} → {label} (no confirmation)")
            ok += 1

        time.sleep(SLEEP_SECONDS)

    return ok, errors, skipped, already_done

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "="*60)
    print("  JJA Insurance — Add Images to Buffer Posts")
    print("  Facebook / LinkedIn / X: scheduled posts")
    print("  Instagram: drafts → scheduled with image")
    print(f"  Pacing: {SLEEP_SECONDS}s between requests")
    print(f"  Resume file: {DONE_FILE}")
    print("="*60)

    api_key  = input("\nPaste your Buffer API key: ").strip()
    if not api_key:
        print("No key entered. Exiting.")
        sys.exit(1)

    done_ids = load_done_ids()
    if done_ids:
        print(f"\n  Resuming — {len(done_ids)} posts already done from previous run.")

    # ── PART 1: Scheduled posts (Facebook, LinkedIn, X) ──────────────────────
    print("\n[1/2] Fetching scheduled posts (Facebook / LinkedIn / X)...")
    scheduled = fetch_posts(api_key, ["scheduled"])
    scheduled = [p for p in scheduled if p.get("channel", {}).get("service") != "instagram"]
    remaining = [p for p in scheduled if p["id"] not in done_ids]
    print(f"\nFound {len(scheduled)} non-Instagram scheduled posts "
          f"({len(remaining)} still need images).\n")
    ok1, err1, skip1, done1 = run_batch(api_key, scheduled, done_ids)

    # ── PART 2: Instagram drafts → schedule + image ───────────────────────────
    print(f"\n[2/2] Fetching Instagram draft posts...")
    all_drafts = fetch_posts(api_key, ["draft"])
    ig_drafts  = [p for p in all_drafts if p.get("channel", {}).get("service") == "instagram"]
    print(f"\nFound {len(ig_drafts)} Instagram drafts. Scheduling with images...\n")
    ok2, err2, skip2, done2 = run_batch(api_key, ig_drafts, done_ids)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  [1/2] Scheduled posts  — OK: {ok1}  Errors: {err1}  Skipped: {skip1}  Already done: {done1}")
    print(f"  [2/2] Instagram drafts — OK: {ok2}  Errors: {err2}  Skipped: {skip2}  Already done: {done2}")
    print(f"  Total updated this run: {ok1 + ok2}")
    if err1 + err2 > 0:
        print(f"  {err1+err2} errors — re-run the script to retry them.")
    print(f"\n  View everything at: https://publish.buffer.com")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
