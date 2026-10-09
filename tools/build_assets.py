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

def wing(palette,cx,cy,scale):
    """An illustrative swept wing; no aerodynamic result is encoded."""
    def point(chord,span,upper=True):
        taper=1-.24*(span+1)/2
        x=chord*taper+.22*(span+1)/2
        y=span
        thickness=.115*math.sin(math.pi*math.sqrt(chord))
        z=.025*math.sin(math.pi*chord)+(thickness if upper else -thickness)
        return cx+scale*(.90*x+.61*y-.30),cy+scale*(.35*x-.36*y-z*2.1)
    out=[]
    for i in range(8):
        span=-1+2*i/7
        points=[point(j/40,span) for j in range(41)]
        points += [point(j/40,span,False) for j in range(40,-1,-1)]
        out.append(poly(points,palette['line'],.9,.72))
    for chord in (0,.06,.16,.3,.5,.72,.9,1):
        for upper in (True,False):
            out.append(poly([point(chord,-1+2*i/30,upper) for i in range(31)],palette['line'],.8,.45))
    out.append(poly([point(j/40,.14) for j in range(41)],palette['accent'],1.5))
    tip=point(.30,.14)
    out.append(f'<circle cx="{tip[0]:.2f}" cy="{tip[1]:.2f}" r="3" fill="{palette["accent"]}"/>')
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
        body+=wing(c,300,306,90)
        body+=[text(24,366,'soun26 / github',11,c['muted'],mono=True)]
    else:
        width,height=1000,340
        body=[text(36,40,'MECHANICAL ENGINEERING',13,c['muted'],mono=True,spacing=2),
              text(31,157,'Soun',118,c['text'],700,spacing=-5),
              text(38,207,'Lê Nguyễn Trần Tiến',27,c['text']),
              text(38,249,'Aerospace Mechanics',23,c['text']),
              text(38,302,'DESIGN  /  SIMULATION  /  RESEARCH',12,c['muted'],mono=True,spacing=1)]
        body+=[line((590,54),(590,285),c['border'])]
        body+=wing(c,780,163,144)
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
