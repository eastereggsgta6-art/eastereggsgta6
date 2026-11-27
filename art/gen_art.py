import random
W,H=1200,420
def head(grad):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice"><defs>{grad}</defs>'
def palm(x,y,s=1,c="#0f0b1a"):
    # trunk curve + fronds
    t=f'<path d="M{x} {y} q{8*s} {-60*s} {-4*s} {-130*s}" stroke="{c}" stroke-width="{7*s}" fill="none" stroke-linecap="round"/>'
    tx,ty=x-4*s,y-130*s
    fr=""
    for dx,dy,cx,cy in [(-70,10,-35,-30),(70,15,35,-28),(-55,40,-30,0),(60,45,30,5),(-20,-55,-25,-35),(30,-50,25,-35)]:
        fr+=f'<path d="M{tx} {ty} q{cx*s} {cy*s} {dx*s} {dy*s} q{-dx*.35*s} {-18*s} {-dx*s} {-dy*s}" fill="{c}"/>'
    return t+fr
def vice():
    random.seed(7)
    g='''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1033"/><stop offset=".55" stop-color="#5b1f5e"/><stop offset=".8" stop-color="#ff5e7a"/><stop offset="1" stop-color="#ffb347"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset=".5" stop-color="#ff7a59"/><stop offset="1" stop-color="#ff3d8b"/></linearGradient>
<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a1446"/><stop offset="1" stop-color="#0f0b1a"/></linearGradient>
<clipPath id="sc"><circle cx="600" cy="250" r="150"/></clipPath>'''
    s=head(g)+f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    for i in range(40): s+=f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,140)}" r="{random.choice([1,1,1.5])}" fill="#fff" opacity="{random.uniform(.3,.8):.2f}"/>'
    s+='<g clip-path="url(#sc)"><rect x="450" y="100" width="300" height="300" fill="url(#sun)"/>'
    for k in range(7): s+=f'<rect x="440" y="{250+k*16+k*k*1.2:.0f}" width="320" height="{3+k*1.6:.1f}" fill="#5b1f5e"/>'
    s+='</g>'
    # skyline
    x=0
    while x<W:
        w=random.randint(40,90); h=random.randint(70,230)
        if 470<x<730: h=random.randint(60,140)
        s+=f'<rect x="{x}" y="{330-h}" width="{w}" height="{h+10}" fill="#120a24"/>'
        for wy in range(330-h+12,325,16):
            for wx in range(x+8,x+w-8,14):
                if random.random()<.32: s+=f'<rect x="{wx}" y="{wy}" width="6" height="8" fill="{random.choice(["#ffd23f","#ff3d8b","#2de2c8","#ffb347"])}" opacity=".85"/>'
        if random.random()<.25: s+=f'<rect x="{x+w/2-1}" y="{330-h-30}" width="2" height="30" fill="#120a24"/><circle cx="{x+w/2}" cy="{330-h-30}" r="3" fill="#ff3d8b"/>'
        x+=w+random.randint(2,10)
    s+=f'<rect y="330" width="{W}" height="{H-330}" fill="url(#sea)"/>'
    for k in range(14):
        y=340+k*6; s+=f'<rect x="{560-k*6}" y="{y}" width="{80+k*12}" height="2" fill="#ff7a59" opacity="{.6-k*.04:.2f}"/>'
    for k in range(10): s+=f'<rect x="{random.randint(0,W)}" y="{random.randint(345,410)}" width="{random.randint(20,70)}" height="2" fill="#2de2c8" opacity=".35"/>'
    s+=palm(90,360,1.3)+palm(170,370,1)+palm(1080,365,1.35)+palm(1150,375,.95)
    s+=f'<rect y="{H-18}" width="{W}" height="18" fill="#0f0b1a"/></svg>'
    return s
def praia():
    random.seed(3)
    g='''<linearGradient id="sky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2de2c8"/><stop offset=".7" stop-color="#9ff3e6"/><stop offset="1" stop-color="#ffe7b8"/></linearGradient>
<linearGradient id="sea2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#18b8c9"/><stop offset="1" stop-color="#0a7f9e"/></linearGradient>'''
    s=head(g)+f'<rect width="{W}" height="{H}" fill="url(#sky2)"/><circle cx="930" cy="110" r="62" fill="#fff6c9"/><circle cx="930" cy="110" r="90" fill="#fff6c9" opacity=".25"/>'
    for cx,cy in [(200,90),(520,60),(760,140)]:
        s+=f'<g fill="#fff" opacity=".85"><ellipse cx="{cx}" cy="{cy}" rx="70" ry="16"/><ellipse cx="{cx+30}" cy="{cy-12}" rx="40" ry="16"/></g>'
    s+=f'<rect y="230" width="{W}" height="90" fill="url(#sea2)"/>'
    for k in range(18): s+=f'<rect x="{random.randint(0,W)}" y="{random.randint(240,310)}" width="{random.randint(30,90)}" height="3" rx="1.5" fill="#fff" opacity=".45"/>'
    s+=f'<path d="M0 300 Q300 285 600 300 T1200 296 V{H} H0Z" fill="#ffd9a0"/><path d="M0 300 Q300 285 600 300 T1200 296" stroke="#fff" stroke-width="5" fill="none" opacity=".8"/>'
    # lifeguard tower
    s+='<g transform="translate(760 210)"><rect x="0" y="40" width="6" height="70" fill="#ff3d8b"/><rect x="74" y="40" width="6" height="70" fill="#ff3d8b"/><rect x="-10" y="30" width="100" height="12" fill="#ffd23f"/><rect x="0" y="-5" width="80" height="38" fill="#ff7a59"/><rect x="10" y="3" width="25" height="18" fill="#0f0b1a" opacity=".55"/><rect x="45" y="3" width="25" height="18" fill="#0f0b1a" opacity=".55"/><path d="M-8 -5 L40 -30 L88 -5Z" fill="#ff3d8b"/></g>'
    # umbrellas
    for x,c in [(240,"#ff3d8b"),(420,"#8b5cf6"),(1000,"#ffd23f")]:
        s+=f'<path d="M{x} 330 L{x} 380" stroke="#5a3d2b" stroke-width="4"/><path d="M{x-48} 335 Q{x} 290 {x+48} 335Z" fill="{c}"/>'
    s+=palm(70,380,1.4,"#0d4b4f")+palm(1130,385,1.4,"#0d4b4f")+palm(1050,395,1,"#0d4b4f")
    s+='</svg>'; return s
def pantano():
    random.seed(11)
    g='''<linearGradient id="sky3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0a1f"/><stop offset=".7" stop-color="#2a1f45"/><stop offset="1" stop-color="#3b2a5a"/></linearGradient>
<linearGradient id="wat3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2a2a"/><stop offset="1" stop-color="#0b0a12"/></linearGradient>
<radialGradient id="moon"><stop offset="0" stop-color="#e9f7ff"/><stop offset=".6" stop-color="#bfe7f0"/><stop offset="1" stop-color="#bfe7f0" stop-opacity="0"/></radialGradient>'''
    s=head(g)+f'<rect width="{W}" height="{H}" fill="url(#sky3)"/>'
    for i in range(60): s+=f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,220)}" r="{random.choice([.8,1,1.3])}" fill="#fff" opacity="{random.uniform(.3,.9):.2f}"/>'
    s+='<circle cx="820" cy="110" r="110" fill="url(#moon)" opacity=".5"/><circle cx="820" cy="110" r="52" fill="#e9f7ff"/>'
    s+=f'<rect y="280" width="{W}" height="{H-280}" fill="url(#wat3)"/><ellipse cx="820" cy="330" rx="40" ry="5" fill="#e9f7ff" opacity=".35"/>'
    # cypress trees
    for x in [40,150,260,980,1090,1170]:
        h=random.randint(170,240); s+=f'<path d="M{x} 290 L{x+6} {290-h} L{x+12} 290Z" fill="#0d1414"/>'
        for k in range(6):
            yy=290-h+k*h/7; ww=26+k*8
            s+=f'<ellipse cx="{x+6}" cy="{yy:.0f}" rx="{ww}" ry="12" fill="#101c1a"/>'
            s+=f'<path d="M{x+6-ww*.6:.0f} {yy+6:.0f} l2 {random.randint(15,35)} M{x+6+ww*.5:.0f} {yy+6:.0f} l-2 {random.randint(15,35)}" stroke="#3d5a4a" stroke-width="1.5" opacity=".7"/>'
    for i in range(14): s+=f'<path d="M{random.randint(300,950)} 300 q4 -30 0 -50" stroke="#16302a" stroke-width="3" fill="none"/>'
    # fog
    for i in range(5): s+=f'<ellipse cx="{random.randint(0,W)}" cy="{random.randint(270,320)}" rx="{random.randint(150,300)}" ry="14" fill="#cfe9ff" opacity=".07"/>'
    # gator eyes + snout
    s+='<g transform="translate(520 330)"><ellipse cx="0" cy="8" rx="110" ry="7" fill="#0b0a12" opacity=".8"/><path d="M-70 6 q20 -16 50 -6 q30 -10 50 2 q40 -4 80 6" fill="#1f3a30"/><circle cx="-28" cy="-4" r="7" fill="#1f3a30"/><circle cx="12" cy="-4" r="7" fill="#1f3a30"/><ellipse cx="-28" cy="-5" rx="4" ry="3" fill="#ffd23f"/><ellipse cx="12" cy="-5" rx="4" ry="3" fill="#ffd23f"/><rect x="-29" y="-8" width="1.6" height="6" fill="#0b0a12"/><rect x="11" y="-8" width="1.6" height="6" fill="#0b0a12"/></g>'
    # fireflies
    for i in range(18): s+=f'<circle cx="{random.randint(280,1000)}" cy="{random.randint(180,300)}" r="2" fill="#2de2c8" opacity="{random.uniform(.4,.9):.2f}"/>'
    s+='</svg>'; return s
def keys():
    random.seed(5)
    g='''<linearGradient id="sky4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a6b"/><stop offset=".6" stop-color="#ffc49a"/><stop offset="1" stop-color="#ffe2c2"/></linearGradient>
<linearGradient id="sea4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2de2c8"/><stop offset="1" stop-color="#0f8aa0"/></linearGradient>'''
    s=head(g)+f'<rect width="{W}" height="{H}" fill="url(#sky4)"/><circle cx="260" cy="200" r="70" fill="#fff1d6" opacity=".9"/>'
    s+=f'<rect y="240" width="{W}" height="{H-240}" fill="url(#sea4)"/>'
    for k in range(22): s+=f'<rect x="{random.randint(0,W)}" y="{random.randint(250,410)}" width="{random.randint(20,80)}" height="3" rx="1.5" fill="#fff" opacity=".35"/>'
    # islands
    for cx,rx in [(120,140),(1050,170)]:
        s+=f'<ellipse cx="{cx}" cy="262" rx="{rx}" ry="22" fill="#e9cf9c"/><ellipse cx="{cx}" cy="252" rx="{rx*.8:.0f}" ry="18" fill="#2f7a55"/>'
    s+=palm(80,255,.7,"#1d4d3a")+palm(140,258,.55,"#1d4d3a")+palm(1020,255,.75,"#1d4d3a")+palm(1100,258,.6,"#1d4d3a")
    # bridge
    s+='<path d="M-20 230 Q600 190 1220 230" stroke="#f4eefc" stroke-width="10" fill="none"/><path d="M-20 240 Q600 200 1220 240" stroke="#c9bfe0" stroke-width="4" fill="none"/>'
    for x in range(0,1220,60):
        y=230-40*(1-((x-600)/620)**2); s+=f'<rect x="{x-4}" y="{y:.0f}" width="8" height="{300-y:.0f}" fill="#d9d0ea"/>'
    # car
    s+='<g transform="translate(700 196) rotate(1)"><rect x="0" y="0" width="46" height="12" rx="4" fill="#ff3d8b"/><rect x="10" y="-8" width="24" height="10" rx="3" fill="#ff3d8b"/><circle cx="10" cy="13" r="4" fill="#0f0b1a"/><circle cx="36" cy="13" r="4" fill="#0f0b1a"/></g>'
    # boat
    s+='<g transform="translate(860 330)"><path d="M0 0 L90 0 L75 16 L8 16Z" fill="#f4eefc"/><rect x="25" y="-12" width="35" height="12" fill="#8b5cf6"/><path d="M-60 12 Q-30 6 0 10" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/></g>'
    # seagulls
    for x,y in [(500,90),(540,110),(900,70)]: s+=f'<path d="M{x} {y} q8 -8 16 0 q8 -8 16 0" stroke="#5b1f5e" stroke-width="2.5" fill="none"/>'
    s+='</svg>'; return s
for n,f in [("vice",vice),("praia",praia),("pantano",pantano),("keys",keys)]:
    open(f"{n}.svg","w").write(f())
