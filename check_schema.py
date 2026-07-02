#!/usr/bin/env python3
"""Check PostInputMetaData and its Instagram sub-type."""

import json, urllib.request

API = "https://api.buffer.com"
KEY = input("Paste your Buffer API key: ").strip()

def gql(query):
    payload = json.dumps({"query": query}).encode()
    req = urllib.request.Request(API, data=payload,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

for type_name in ["PostInputMetaData", "InstagramInputMetaData", "InstagramMetaData"]:
    q = '{ __type(name: "' + type_name + '") { name inputFields { name type { name kind enumValues { name } ofType { name kind enumValues { name } } } } } }'
    data = gql(q)
    t = (data.get("data") or {}).get("__type")
    if t and t.get("inputFields"):
        print(f"\n=== {type_name} ===")
        for f in t["inputFields"]:
            ft = f["type"]
            fn = ft.get("name") or (ft.get("ofType") or {}).get("name", "?")
            enums = ft.get("enumValues") or (ft.get("ofType") or {}).get("enumValues") or []
            enum_str = f" [{', '.join(e['name'] for e in enums)}]" if enums else ""
            sub = fn
            # Check the sub-type if it's an input object
            if ft.get("kind") == "INPUT_OBJECT" or fn not in (None, "?"):
                sub_q = '{ __type(name: "' + fn + '") { name inputFields { name type { name kind enumValues { name } ofType { name kind enumValues { name } } } } } }'
                sub_data = gql(sub_q)
                sub_t = (sub_data.get("data") or {}).get("__type")
                if sub_t and sub_t.get("inputFields"):
                    sub_fields = []
                    for sf in sub_t["inputFields"]:
                        sft = sf["type"]
                        sfn = sft.get("name") or (sft.get("ofType") or {}).get("name", "?")
                        senums = sft.get("enumValues") or (sft.get("ofType") or {}).get("enumValues") or []
                        senum_str = f" [{', '.join(e['name'] for e in senums)}]" if senums else ""
                        sub_fields.append(f"{sf['name']}: {sfn}{senum_str}")
                    sub = f"{fn} {{ {', '.join(sub_fields)} }}"
            print(f"  {f['name']}: {sub}{enum_str}")
    else:
        print(f"  {type_name}: not found")
