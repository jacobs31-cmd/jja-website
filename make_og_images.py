#!/usr/bin/env python3
"""
JJA — Open Graph card generator.
Builds branded 1200x630 JPG OG cards for every page/post and (optionally) rewires
each page's og:image / twitter:image to its card.

Cards: page hero photo (re-fetched from Unsplash as JPG when the hero is a
photo-XXXX id) with a navy gradient + eyebrow + H1 title + JJA branding bar.
Pages whose hero can't be turned into a photo (SVG infographics, custom AVIFs)
get a clean navy branded card instead.

Usage:
  python make_og_images.py generate     # build cards into assets/img/og/ (skips existing)
  python make_og_images.py rewire        # point og:image/twitter:image at the cards
  python make_og_images.py generate force  # rebuild even if card exists
"""
import os, re, sys, glob, html, io, urllib.request

NAVY=(20,54,94); NAVY_DARK=(10,35,66); NAVY_LIGHT=(30,74,122)
WHITE=(255,255,255); GRAY=(203,215,227)
W,H=1200,630
OG_DIR="assets/img/og"
SITE="https://jjainsurance.com"
FORCE = (len(sys.argv)>2 and sys.argv[2]=="force")

from PIL import Image, ImageDraw, ImageFont

def safe_write(path, text):
    """Flush-and-verify file write — guards against the silent mid-file truncation
    that left page footers cut off. Unlike open(path,'w').write(...), this always
    closes the handle, then re-reads the file and aborts loudly if the on-disk
    content does not match, so a truncated page can never be written or deployed again."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != text:
            raise SystemExit("ABORT: short/truncated write to " + path)

def font(sz,bold=True):
    p=("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
       else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    return ImageFont.truetype(p,sz)

def wrap(draw,text,fnt,maxw,maxlines=3):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if draw.textlength(t,font=fnt)<=maxw: cur=t
        else:
            lines.append(cur); cur=w
            if len(lines)==maxlines: break
    if cur and len(lines)<maxlines: lines.append(cur)
    return lines

def fetch_jpg(token):
    url=f"https://images.unsplash.com/{token}?w=1200&h=900&q=80&auto=format&fit=crop&fm=jpg"
    cache=f"/tmp/ogsrc_{token}.jpg"
    if os.path.exists(cache) and os.path.getsize(cache)>2000:
        return cache
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        data=urllib.request.urlopen(req,timeout=25).read()
        if len(data)<2000: return None
        with open(cache,"wb") as f: f.write(data)
        return cache
    except Exception as e:
        print("   fetch fail",token,e); return None

def make_card(src, eyebrow, title, out):
    if src:
        img=Image.open(src).convert("RGB")
        sr=img.width/img.height; tr=W/H
        if sr>tr: nh=H; nw=int(H*sr)
        else: nw=W; nh=int(W/sr)
        img=img.resize((nw,nh))
        img=img.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H)).convert("RGBA")
        grad=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(grad)
        gstart=H-330
        for y in range(gstart,H):
            a=int(252*((y-gstart)/(H-gstart))**1.05)
            gd.line([(0,y),(W,y)],fill=(NAVY_DARK[0],NAVY_DARK[1],NAVY_DARK[2],min(a,250)))
        img=Image.alpha_composite(img,grad).convert("RGB")
    else:
        img=Image.new("RGB",(W,H),NAVY_DARK); d0=ImageDraw.Draw(img)
        for y in range(H):  # subtle vertical navy gradient
            t=y/H; c=tuple(int(NAVY_DARK[i]+(NAVY[i]-NAVY_DARK[i])*t) for i in range(3))
            d0.line([(0,y),(W,y)],fill=c)
    d=ImageDraw.Draw(img)
    d.rectangle([60,H-235,130,H-230],fill=NAVY_LIGHT)
    d.text((60,H-218),eyebrow.upper(),font=font(20,bold=False),fill=GRAY)
    lines=wrap(d,title,font(54),W-120,3)
    size=54 if len(lines)==1 else (44 if len(lines)==2 else 34)
    tf=font(size); lines=wrap(d,title,tf,W-120,3)
    gap=size+8; y=(H-64)-len(lines)*gap
    for ln in lines:
        d.text((60,y),ln,font=tf,fill=WHITE); y+=gap
    d.text((60,H-44),"J. JACOBS & ASSOCIATES  ·  MICHIGAN INSURANCE SINCE 1981",
           font=font(20,bold=False),fill=GRAY)
    url="jjainsurance.com"; uf=font(22)
    d.text((W-60-d.textlength(url,font=uf),H-46),url,font=uf,fill=WHITE)
    img.save(out,"JPEG",quality=86)

def clean(s):
    s=re.sub(r"<[^>]+>","",s); s=html.unescape(s)
    return re.sub(r"\s+"," ",s).strip()

def page_name(path):
    p=path[:-len("/index.html")] if path.endswith("/index.html") else path[:-5]
    return "home" if p in ("","index") else p.replace("/","-")

def hero_token(htmltext):
    m=re.search(r'assets/img/blog/([A-Za-z0-9_\-]+)\.(avif|svg|jpg|jpeg|png)',htmltext)
    return (m.group(1),m.group(2)) if m else (None,None)

def derive(path,htmltext):
    h1=re.search(r"<h1[^>]*>(.*?)</h1>",htmltext,re.S)
    title=clean(h1.group(1)) if h1 else clean((re.search(r"<title>(.*?)</title>",htmltext,re.S) or ["",""])[1]).split("|")[0].strip()
    eb=re.search(r'class="eyebrow"[^>]*>(.*?)</',htmltext,re.S)
    eyebrow=clean(eb.group(1)) if eb else "Michigan Insurance"
    if path.startswith("blog/"): eyebrow=eyebrow or "Insurance"
    tok,ext=hero_token(htmltext)
    src=None
    if tok:
        if tok.startswith("photo-") or tok.startswith("premium_photo-"):
            src=fetch_jpg(tok)
        else:
            for cand in (f"assets/img/blog/{tok}.jpg",f"assets/img/blog/{tok}.jpeg",f"assets/img/blog/{tok}.png"):
                if os.path.exists(cand): src=cand; break
    return eyebrow,title,src

def all_pages():
    pages=sorted(set(glob.glob("**/index.html",recursive=True)+(["404.html"] if os.path.exists("404.html") else [])))
    skip={"privacy-policy","accessibility","sms-terms"}  # legal pages -> still get branded card but low priority kept
    return pages

def generate():
    os.makedirs(OG_DIR,exist_ok=True)
    pages=all_pages(); built=0; skipped=0
    for path in pages:
        name=page_name(path); out=f"{OG_DIR}/{name}.jpg"
        if os.path.exists(out) and not FORCE: skipped+=1; continue
        t=open(path,encoding="utf-8",errors="replace").read()
        eyebrow,title,src=derive(path,t)
        if not title: title="Michigan Insurance"
        make_card(src,eyebrow,title,out)
        built+=1
        print(f"  [{'photo' if src else 'brand'}] {name}.jpg  <- {title[:48]}")
    print(f"\nGenerated {built} cards, skipped {skipped} existing. -> {OG_DIR}/")

def rewire():
    pages=all_pages(); n=0
    for path in pages:
        name=page_name(path); card=f"{SITE}/assets/img/og/{name}.jpg"
        if not os.path.exists(f"{OG_DIR}/{name}.jpg"): continue
        t=open(path,encoding="utf-8",errors="replace").read(); orig=t
        t=re.sub(r'(<meta property="og:image" content=")[^"]*(">)',rf'\1{card}\2',t)
        t=re.sub(r'(<meta name="twitter:image" content=")[^"]*(">)',rf'\1{card}\2',t)
        if t!=orig:
            t=t.rstrip("\x00")
            safe_write(path,t); n+=1
    print(f"Rewired og:image/twitter:image on {n} pages.")

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "generate"
    (generate if mode=="generate" else rewire)()
