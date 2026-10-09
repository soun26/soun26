"""Generate original vector artwork for Soun's GitHub profile."""
from html import escape
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
THEMES={
    'light':{'bg':'#ffffff','text':'#000000','muted':'#555555','line':'#b4b4b4','border':'#e2e2e2','grid':'#eeeeee','accent':'#b65e35'},
    'dark':{'bg':'#0d1117','text':'#f0f6fc','muted':'#adb6c0','line':'#7f8994','border':'#30363d','grid':'#202832','accent':'#dc976f'},
}

def text(x,y,content,size=20,color='#000000',weight=400,mono=False,spacing=None):
    family='Consolas, monospace' if mono else 'Segoe UI, Arial, sans-serif'
    tracking='' if spacing is None else f' letter-spacing="{spacing}"'
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}"{tracking}>{escape(content)}</text>'

def line(a,b,color,width=1,opacity=1):
    return f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'

def poly(points,color,width=1,opacity=1):
    coordinates=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
    return f'<polyline points="{coordinates}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'

def svg(width,height,title,body,palette):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">'
            f'<title id="title">{escape(title)}</title>'
            f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="22" fill="{palette["bg"]}" stroke="{palette["border"]}"/>'
            +''.join(body)+'</svg>\n')

def aircraft(palette,cx,cy,scale):
    """An original schematic airliner with wings, engines and a tail."""
    def p(x,y,z=0):
        return cx+scale*(.75*x+.65*y),cy+scale*(-.28*x+.42*y-.75*z)
    def surface(points):
        coordinates=' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
        return f'<polygon points="{coordinates}" fill="{palette["bg"]}" stroke="{palette["line"]}" stroke-width="1.3" stroke-linejoin="round"/>'
    out=[]
    for side in (-1,1):
        # Swept main wings and horizontal tail.
        wing=[(.48,side*.085,.02),(-.61,side*1.36,.015),
              (-.93,side*1.36,.015),(-.48,side*.085,.02)]
        out.append(surface([p(*vertex) for vertex in wing]))
        for span in (.25,.45,.7,1.0,1.25):
            t=(span-.085)/(1.36-.085)
            leading=.48+(-.61-.48)*t
            trailing=-.48+(-.93+.48)*t
            out.append(line(p(leading,side*span,.025),p(trailing,side*span,.025),palette['line'],.7,.5))
        tail=[(-.94,side*.05,.02),(-1.32,side*.54,.035),
              (-1.53,side*.54,.035),(-1.4,side*.05,.02)]
        out.append(surface([p(*vertex) for vertex in tail]))
        # Two nacelles make the whole-aircraft silhouette recognizable.
        engine_y=side*.52
        for offset in (-.085,.085):
            out.append(line(p(.10,engine_y+offset,-.16),p(.63,engine_y+offset,-.16),palette['line'],1.2))
        for station in (.10,.63):
            ring=[p(station,engine_y+.085*math.cos(i*math.pi/16),-.16+.085*math.sin(i*math.pi/16)) for i in range(33)]
            out.append(poly(ring,palette['line'],1.2))
    def body_radius(x):
        t=(x+1.5)/3.25
        return .115*max(0,math.sin(math.pi*t))**.62
    stations=[-1.5+3.25*i/52 for i in range(53)]
    silhouette=[p(x,body_radius(x),.10) for x in stations]
    silhouette += [p(x,-body_radius(x),.10) for x in reversed(stations)]
    out.append(surface(silhouette))
    for angle in (math.pi/4,math.pi/2,3*math.pi/4):
        spine=[p(x,body_radius(x)*math.cos(angle),.10+body_radius(x)*math.sin(angle)) for x in stations]
        out.append(poly(spine,palette['line'],.7,.65))
    for x in (-1.15,-.8,-.45,-.1,.25,.6,.95,1.25,1.48):
        radius=body_radius(x)
        out.append(poly([p(x,radius*math.cos(i*math.pi/24),.10+radius*math.sin(i*math.pi/24)) for i in range(25)],palette['line'],.6,.4))
    fin=[(-1.42,0,.10),(-1.12,0,.59),(-.91,0,.59),(-.75,0,.10)]
    out.append(surface([p(*vertex) for vertex in fin]))
    out.append(poly([p(-.7,0,.22),p(.95,0,.21),p(1.43,0,.16)],palette['accent'],1.8))
    for side in (-1,1):
        out.append(poly([p(1.35,side*.055,.16),p(1.47,side*.035,.14),p(1.54,side*.016,.13)],palette['line'],1.6))
    return out

def cooling(palette,cx,cy,scale):
    def p(x,y,z):
        return cx+scale*(x*.8+y*.38),cy+scale*(x*.24-y*.25-z*.65)
    out=[]
    corners=[p(x,y,z) for z in (-.55,.55) for y in (-1,1) for x in (-1,1)]
    for a,b in ((0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(2,6),(3,7)):
        out.append(line(corners[a],corners[b],palette['line'],1.1,.8))
    for y in (-.8,-.4,0,.4,.8):
        out.append(poly([p(-1+2*i/20,y,.55+.05*math.sin(i*.3)) for i in range(21)],palette['line'],.8,.4))
    # An original branching schematic, rather than a private research geometry.
    out.append(poly([p(-.96+.67*i/24,.045*math.sin(i*.13),-.05) for i in range(25)],palette['accent'],2.6))
    for side in (-1,1):
        out.append(poly([p(-.29+.42*i/24,side*.38*(i/24)**.8,-.05) for i in range(25)],palette['accent'],2.2))
        for child in (-1,1):
            out.append(poly([p(.13+.78*i/24,side*.38+child*.19*(i/24)**.85,-.05) for i in range(25)],palette['accent'],1.8))
    return out

def fractal(palette,cx,cy,scale):
    def p(x,y,z):
        return cx+scale*(x*.7+y*.42),cy+scale*(x*.24-y*.22-z*.65)
    out=[]
    for x in (-.85,.85):
        for y in (-.75,.75):
            out.append(line(p(x,y,-1),p(x,y,1),palette['line'],1.6))
    for z in (-1,1):
        corners=[p(-.85,-.75,z),p(.85,-.75,z),p(.85,.75,z),p(-.85,.75,z),p(-.85,-.75,z)]
        out.append(poly(corners,palette['line'],1.3))
    out.append(poly([p(.68*math.cos(i*math.pi/32),.68*math.sin(i*math.pi/32),-.2+.32*math.sin(i*math.pi/32)) for i in range(65)],palette['line'],1.4))
    for z in (0,.08,.16,.24,.32,.40):
        out.append(poly([p(.22*math.cos(i*math.pi/24),.22*math.sin(i*math.pi/24),z) for i in range(49)],palette['accent'],1.6))
    out.append(line(p(-.85,0,.8),p(.85,0,.8),palette['line'],2))
    out.append(line(p(0,0,.8),p(0,0,.42),palette['accent'],3))
    return out

def hero(theme,mobile=False):
    c=THEMES[theme]
    if mobile:
        width,height=480,390
        body=[text(24,35,'MECHANICAL ENGINEERING',12,c['muted'],mono=True,spacing=1.4),
              text(20,124,'Soun',92,c['text'],700,spacing=-4),
              text(24,166,'Lê Nguyễn Trần Tiến',21,c['text']),
              text(24,203,'Aerospace Mechanics',19,c['text']),
              text(24,233,'DESIGN  /  SIMULATION  /  RESEARCH',11,c['muted'],mono=True,spacing=.7)]
        body+=aircraft(c,318,306,70)
        body+=[text(24,366,'soun26 / github',11,c['muted'],mono=True)]
    else:
        width,height=1000,340
        body=[text(36,40,'MECHANICAL ENGINEERING',13,c['muted'],mono=True,spacing=2),
              text(31,157,'Soun',118,c['text'],700,spacing=-5),
              text(38,207,'Lê Nguyễn Trần Tiến',27,c['text']),
              text(38,249,'Aerospace Mechanics',23,c['text']),
              text(38,302,'DESIGN  /  SIMULATION  /  RESEARCH',12,c['muted'],mono=True,spacing=1)]
        body+=[line((590,54),(590,285),c['border'])]
        body+=aircraft(c,792,151,121)
        body+=[text(662,298,'FORM / STRUCTURE / MOTION',11,c['muted'],mono=True,spacing=1)]
    return svg(width,height,'Soun — Lê Nguyễn Trần Tiến / Mechanical Engineering / Aerospace Mechanics',body,c)

def project(kind,theme,mobile=False):
    c=THEMES[theme]
    is_cooling=kind=='cooling'
    number='01' if is_cooling else '02'
    label='INJECTION MOLDING' if is_cooling else 'ADDITIVE MANUFACTURING'
    title='Bio-inspired evolutionary cooling channels' if is_cooling else '5-axis 3D printing'
    subtitle='For complex, variable-thickness parts.' if is_cooling else 'Exploring multi-axis additive manufacturing.'
    tags='THERMAL PERFORMANCE   ·   WEB EDITION' if is_cooling else 'MOTION   ·   PRINT ORIENTATION   ·   RESEARCH'
    if mobile:
        width,height=480,254
        body=[text(24,32,f'{number} / {label}',10,c['muted'],mono=True,spacing=.8)]
        if is_cooling:
            body += [text(22,76,'Bio-inspired evolutionary',28,c['text'],600,spacing=-.7),
                     text(22,110,'cooling channels',30,c['text'],600,spacing=-.7),
                     text(24,142,subtitle,16,c['text'])]
        else:
            body += [text(22,82,title,31,c['text'],600,spacing=-.8),
                     text(24,116,'Exploring multi-axis manufacturing.',16,c['text'])]
        body += [text(24,227,'WEB EDITION' if is_cooling else 'RESEARCH PROJECT',10,c['muted'],mono=True,spacing=.7)]
        body+=(cooling if is_cooling else fractal)(c,347,193 if is_cooling else 184,49 if is_cooling else 58)
    else:
        width,height=1000,220
        body=[text(28,34,f'{number} / {label}',11,c['muted'],mono=True,spacing=1.3)]
        if is_cooling:
            body += [text(26,80,'Bio-inspired evolutionary',35,c['text'],600,spacing=-1),
                     text(26,126,'cooling channels',42,c['text'],600,spacing=-1.2),
                     text(29,158,subtitle,18,c['text']),
                     text(29,192,tags,11,c['muted'],mono=True)]
        else:
            body += [text(26,92,title,42,c['text'],600,spacing=-1.2),
                     text(29,129,subtitle,20,c['text']),
                     text(29,185,tags,12,c['muted'],mono=True)]
        body+=(cooling if is_cooling else fractal)(c,806,120,101)
    return svg(width,height,title,body,c)

def main():
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        for mobile in (False,True):
            suffix='-mobile' if mobile else ''
            (ASSETS/f'hero-{theme}{suffix}.svg').write_text(hero(theme,mobile),encoding='utf-8',newline='\n')
            for kind in ('cooling','fractal'):
                (ASSETS/f'{kind}-{theme}{suffix}.svg').write_text(project(kind,theme,mobile),encoding='utf-8',newline='\n')
    print(f'Generated 12 SVG assets in {ASSETS}')

if __name__=='__main__':
    main()
