#!/usr/bin/env python3
"""Quick check — finds all Instagram posts in Buffer regardless of status."""

import json, urllib.request, urllib.error

API    = "https://api.buffer.com"
ORG_ID = "6a14a87235f22ccc6a284ead"
KEY    = input("Paste your Buffer API key: ").strip()

def gql(query, variables):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        API, data=payload,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

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

for status in [["draft"], ["scheduled"], ["sent"]]:
    print(f"\n--- Status: {status} ---")
    variables = {
        "input": {"organizationId": ORG_ID, "filter": {"status": status}},
        "first": 50, "after": None
    }
    result = gql(q, variables)
    edges = result.get("data", {}).get("posts", {}).get("edges", [])
    insta = [e["node"] for e in edges if e["node"].get("channel", {}).get("service") == "instagram"]
    print(f"  Total posts: {len(edges)}  |  Instagram: {len(insta)}")
    for p in insta[:5]:
        print(f"    [{p['status']}] {p.get('text','')[:60]!r}")

print("\nDone.")
