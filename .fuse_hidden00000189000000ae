#!/usr/bin/env python3
"""
JJA Insurance — Schedule Instagram Posts with Branded Images
Creates all future Instagram posts as scheduled posts with the correct
branded image attached. Run once — skips any that are already past.

Run: python schedule_instagram.py
"""

import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

API             = "https://api.buffer.com"
ORG_ID          = "6a14a87235f22ccc6a284ead"
TIMEZONE_OFFSET = -4   # EDT (UTC-4, May–Aug)
SLEEP_SECONDS   = 3    # 26 posts total — no rate limit risk

IMAGES = {
    "home":       "https://jjainsurance.com/social-images/jja_home_insurance.png",
    "auto":       "https://jjainsurance.com/social-images/jja_auto_insurance.png",
    "commercial": "https://jjainsurance.com/social-images/jja_commercial.png",
    "workers":    "https://jjainsurance.com/social-images/jja_workers_comp.png",
    "life":       "https://jjainsurance.com/social-images/jja_life_insurance.png",
    "tips":       "https://jjainsurance.com/social-images/jja_insurance_tips.png",
}

# All 26 Instagram posts from the 90-day calendar
INSTAGRAM_POSTS = [
    ("05/26/2026","11:00","Your home insurance went up — here's why, and what you can do about it.\n\nWe wrote a full breakdown for Michigan homeowners. Link in bio.\n\n#HomeInsurance #Michigan #InsuranceTips #LakeOrion #MichiganHomes #SaveMoney"),
    ("05/28/2026","11:00","Deductible too low? Raising it could save you hundreds a year — if the timing is right.\n\nWe'll help you figure out if it makes sense for your situation. Call us or click the link in bio.\n#InsuranceTip #HomeInsurance #Michigan #SaveMoney #LakeOrion"),
    ("06/01/2026","11:00","Bundling home + auto can save you up to 20%. Most people just never ask.\n\nWe shop 10+ carriers to find your best combined rate. Link in bio to get started.\n#BundleAndSave #Michigan #Insurance #HomeInsurance #AutoInsurance #LakeOrion"),
    ("06/03/2026","11:00","Michigan auto insurance has 6 PIP options. Most people have no idea which one they picked.\n\nRead the breakdown — link in bio.\n#MichiganNoFault #AutoInsurance #Michigan #InsuranceTips #LakeOrion"),
    ("06/08/2026","11:00","Michigan business owners — do you actually need workers' comp insurance? The answer depends on more than just how many employees you have.\n\nFull guide at the link in bio.\n#WorkersComp #MichiganBusiness #SmallBusiness #BusinessInsurance #LakeOrion"),
    ("06/10/2026","11:00","Skipping your workers' comp audit in Michigan can cost you way more than completing it.\n\nHere's what happens — link in bio.\n#WorkersComp #MichiganBusiness #BusinessInsurance #Insurance #LakeOrion"),
    ("06/12/2026","11:00","Storm season's here. Does your Michigan home insurance actually cover the damage?\n\nWind, hail, and fallen trees — usually yes. Flooding and sewer backup — usually NOT.\n\nKnow the gaps before the next storm. Full guide — link in bio.\n#HomeInsurance #Michigan #StormSeason #InsuranceTips #LakeOrion #Homeowners"),
    ("06/15/2026","11:00","Small businesses are the #1 target for ransomware attacks. And your standard business policy? Doesn't cover it.\n\nCyber insurance guide for Michigan businesses — link in bio.\n#CyberInsurance #SmallBusiness #Michigan #BusinessInsurance #LakeOrion"),
    ("06/17/2026","11:00","Summer event coming up? Most Michigan venues now require special event insurance — and it's more affordable than you'd think.\n\nFind out if you need it — link in bio.\n#EventInsurance #Michigan #WeddingInsurance #SummerEvents #LakeOrion"),
    ("06/22/2026","11:00","Collision vs. comprehensive — do you know the difference? One covers deer hits. One doesn't.\n\nMichigan auto insurance glossary — link in bio.\n#AutoInsurance #Michigan #InsuranceTips #CarInsurance #LakeOrion"),
    ("06/24/2026","11:00","1 in 5 Michigan drivers is uninsured. Do you have uninsured motorist coverage?\n\nLet us check your policy — link in bio or call us.\n#AutoInsurance #Michigan #UninsuredMotorist #InsuranceTips #LakeOrion"),
    ("06/29/2026","11:00","Back on two wheels? Make sure your motorcycle insurance is keeping up.\n\nMichigan motorcycle insurance guide — link in bio.\n#MotorcycleInsurance #Michigan #Motorcycle #BikerLife #SummerRiding #LakeOrion"),
    ("07/01/2026","11:00","Boat, RV, ATV, jet ski — don't assume your home or auto policy covers them. Most don't.\n\nGet the right coverage before you hit the water. Link in bio.\n#BoatInsurance #Michigan #SummerFun #RVLife #LakeOrion #Insurance"),
    ("07/06/2026","11:00","25 insurance questions Michigan residents ask most — answered. No jargon, no fluff.\n\nLink in bio.\n#Insurance #Michigan #InsuranceTips #FAQ #LakeOrion"),
    ("07/08/2026","11:00","Should you file that claim — or just pay out of pocket? It's not always obvious.\n\nCall us before you call your carrier. We'll help you think it through.\n(248) 693-6455\n#InsuranceTip #Michigan #Insurance #LakeOrion"),
    ("07/13/2026","11:00","Replacement cost vs. actual cash value — on a roof claim, this difference can be $15,000.\n\nKnow what your policy actually says. Link in bio.\n#HomeInsurance #Michigan #InsuranceTip #Homeowners #LakeOrion"),
    ("07/15/2026","11:00","Michigan homeowners: your home insurance almost certainly does NOT cover flood damage.\n\nFlood insurance is a separate policy — and it matters here.\n\nCall us to find out if you need it: (248) 693-6455\n#FloodInsurance #HomeInsurance #Michigan #Insurance #LakeOrion"),
    ("07/20/2026","11:00","Michigan drivers: auto insurance refund scams are still making the rounds.\n\nHow to spot them — link in bio.\n#InsuranceScam #Michigan #ConsumerProtection #AutoInsurance #LakeOrion"),
    ("07/22/2026","11:00","3 signs that insurance call is actually a scam.\n\n1 They called you\n2 They want your bank info\n3 There's pressure to act now\n\nHang up. Call your real agent.\n(248) 693-6455\n#InsuranceScam #Michigan #ConsumerProtection #LakeOrion"),
    ("07/27/2026","11:00","45 years in Michigan. Lake Orion's Best of the Best 8 years running.\n\nWe shop 10+ carriers so you don't have to. Get a quote — link in bio.\n#JJAInsurance #LakeOrion #Michigan #Insurance #IndependentAgent"),
    ("07/29/2026","11:00","Best of the Best — 8 years straight. Thank you, Lake Orion.\n\nNew here? Get a quote — link in bio.\n#LakeOrion #BestOfTheBest #JJAInsurance #Michigan #Community #Insurance"),
    ("08/03/2026","11:00","Teen driver in your house? Adding them to your policy doesn't have to wreck your budget.\n\nCall us — we'll find the right fit.\n(248) 693-6455\n#TeenDriver #AutoInsurance #Michigan #BackToSchool #Insurance #LakeOrion"),
    ("08/05/2026","11:00","Kid heading to college? Your auto insurance situation just changed — maybe in your favor.\n\nCall us and we'll figure out the right coverage. (248) 693-6455\n#AutoInsurance #Michigan #CollegeStudent #Insurance #LakeOrion"),
    ("08/10/2026","11:00","Would your family be financially okay if something happened to you? Life insurance is the answer — but the right kind matters.\n\nLet's talk it through. Link in bio or call (248) 693-6455.\n#LifeInsurance #Michigan #Insurance #Family #Protection #LakeOrion"),
    ("08/12/2026","11:00","Life insurance rule of thumb: 10-12x your annual income in coverage. Most people fall short.\n\nLet's find out where you stand. Link in bio.\n#LifeInsurance #Michigan #Insurance #FinancialTips #LakeOrion"),
    ("08/17/2026","11:00","Captive agent = one carrier's rates. Independent agent = 10+ carriers, best rate.\n\nJJA has been independent in Michigan since 1981. Get a quote — link in bio.\n#IndependentAgent #Insurance #Michigan #LakeOrion #BestRate"),
    ("08/19/2026","11:00","Got a non-renewal notice from your insurance company? Don't panic — you have options.\n\nCall us and we'll find you coverage. (248) 693-6455\n#Insurance #Michigan #NonRenewal #Insurance #LakeOrion"),
]

def pick_image(text):
    t = text.lower()
    if any(k in t for k in ["home insurance", "homeowners", "flood", "roof", "deductible", "replacement cost"]):
        return IMAGES["home"]
    if any(k in t for k in ["workers", "wcaudit"]):
        return IMAGES["workers"]
    if any(k in t for k in ["commercial", "cyber", "ransomware", "business policy", "special event", "summer event", "event insurance"]):
        return IMAGES["commercial"]
    if any(k in t for k in ["life insurance", "10-12x", "financially okay"]):
        return IMAGES["life"]
    if any(k in t for k in ["auto", "vehicle", "car", "motorcycle", "no-fault", "driver", "scam", "refund", "collision", "comprehensive", "uninsured", "pip", "two wheels", "teen driver", "boat", "atv", "jet ski"]):
        return IMAGES["auto"]
    return IMAGES["tips"]

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
        return {"error": e.read().decode()}
    except Exception as e:
        return {"error": str(e)}

def get_instagram_channel(api_key):
    q = """query GetChannels($input: ChannelsInput!) {
      channels(input: $input) { id name service }
    }"""
    result = gql(q, {"input": {"organizationId": ORG_ID}}, api_key)
    channels = result.get("data", {}).get("channels", [])
    for ch in channels:
        if ch["service"].lower() == "instagram":
            return ch["id"], ch["name"]
    return None, None

def create_post(api_key, channel_id, text, due_at, image_url):
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        __typename
        ... on PostActionSuccess { post { id } }
        ... on InvalidInputError { message }
        ... on LimitReachedError { message }
        ... on UnauthorizedError { message }
        ... on UnexpectedError   { message }
        ... on NotFoundError     { message }
        ... on RestProxyError    { message }
      }
    }
    """
    inp = {
        "channelId":      channel_id,
        "text":           text,
        "dueAt":          due_at,
        "mode":           "customScheduled",
        "schedulingType": "automatic",
        "assets":         [{"image": {"url": image_url}}],
        "metadata":       {"instagram": {"type": "post", "shouldShareToFeed": True}},
    }
    return gql(mutation, {"input": inp}, api_key)

def to_iso(date_str, time_str):
    dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
    tz = timezone(timedelta(hours=TIMEZONE_OFFSET))
    return dt.replace(tzinfo=tz).isoformat()

def main():
    print("\n" + "="*60)
    print("  JJA Insurance — Instagram Scheduler with Images")
    print("="*60)

    # Use the BUFFER_API_KEY environment variable if set, otherwise prompt.
    api_key = os.environ.get("BUFFER_API_KEY", "").strip()
    if api_key:
        print("\nUsing Buffer API key from the BUFFER_API_KEY environment variable.")
    else:
        api_key = input("\nPaste your Buffer API key: ").strip()
    if not api_key:
        print("No key entered. Exiting.")
        sys.exit(1)
    if not api_key.isascii() or " " in api_key:
        print("\nThat doesn't look like just an API key — it contains spaces or special")
        print("characters, which usually means extra text got pasted in by accident.")
        print("Paste ONLY your Buffer API key (or set the BUFFER_API_KEY variable). Exiting.")
        sys.exit(1)

    # Instagram channel ID confirmed from previous successful run
    channel_id   = "6a15047ec687a22dd427b704"
    channel_name = "jjacobs_and_associates"
    print(f"Using Instagram channel: {channel_name} (ID: {channel_id})")

    now = datetime.now(timezone(timedelta(hours=TIMEZONE_OFFSET)))
    ok = skipped = errors = 0
    n = len(INSTAGRAM_POSTS)

    print(f"\nScheduling {n} Instagram posts...\n")

    for i, (date_str, time_str, text) in enumerate(INSTAGRAM_POSTS, 1):
        dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %H:%M")
        dt = dt.replace(tzinfo=timezone(timedelta(hours=TIMEZONE_OFFSET)))

        if dt <= now:
            print(f"  [{i:2}/{n}] SKIP  {date_str} {time_str} (past)")
            skipped += 1
            continue

        due_at    = to_iso(date_str, time_str)
        image_url = pick_image(text)
        img_label = image_url.split("/")[-1].replace(".png", "")

        result = create_post(api_key, channel_id, text, due_at, image_url)

        cp       = (result.get("data") or {}).get("createPost") or {}
        typename = cp.get("__typename", "")
        err      = result.get("error") or result.get("errors")

        if err or typename not in ("PostActionSuccess", ""):
            msg = cp.get("message") or str(err)
            print(f"  [{i:2}/{n}] ERROR {date_str} {time_str}: {msg}")
            errors += 1
        else:
            post_id = (cp.get("post") or {}).get("id", "?")
            print(f"  [{i:2}/{n}] OK    {date_str} {time_str} [{img_label}] → {post_id}")
            ok += 1

        time.sleep(SLEEP_SECONDS)

    print(f"\n{'='*60}")
    print(f"  Done! Created: {ok}  |  Skipped (past): {skipped}  |  Errors: {errors}")
    print(f"  View at: https://publish.buffer.com")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
