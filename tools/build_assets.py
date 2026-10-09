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

def wing(palette,cx,cy,scale,animated=True,phase=None):
    """The original swept-wing illustration, with gentle optional motion."""
    def point(chord,span,upper=True):
        taper=1-.24*(span+1)/2
        x=chord*taper+.22*(span+1)/2
        y=span
        thickness=.115*math.sin(math.pi*math.sqrt(chord))
        z=.025*math.sin(math.pi*chord)+(thickness if upper else -thickness)
        if phase is not None:
            yaw=.09*math.sin(phase*math.tau)
            pitch=.05*math.sin(phase*math.tau+math.pi/2)
            x,z=.45+(x-.45)*math.cos(yaw)+z*math.sin(yaw),-(x-.45)*math.sin(yaw)+z*math.cos(yaw)
            y,z=y*math.cos(pitch)-z*math.sin(pitch),y*math.sin(pitch)+z*math.cos(pitch)
        return cx+scale*(.90*x+.61*y-.30),cy+scale*(.35*x-.36*y-z*2.1)
    out=[]
    ribs=[]
    for i in range(8):
        span=-1+2*i/7
        points=[point(j/40,span) for j in range(41)]
        points += [point(j/40,span,False) for j in range(40,-1,-1)]
        ribs.append(points)
        out.append(poly(points,palette['line'],1.05,.8))
    for chord in (0,.06,.16,.3,.5,.72,.9,1):
        for upper in (True,False):
            out.append(poly([point(chord,-1+2*i/30,upper) for i in range(31)],palette['line'],.9,.53))
    if phase is not None:
        sweep=phase*len(ribs)
        current=int(sweep)%len(ribs)
        progress=sweep%1
        travel_end=.65 if current==len(ribs)-1 else .90
        transfer=max(0,(progress-travel_end)/(1-travel_end))
        fade=(1-math.cos(transfer*math.pi))/2
        for rib,opacity in ((current,1-fade),((current+1)%len(ribs),fade)):
            out.append(poly(ribs[rib],palette['accent'],3.5,.12*opacity))
            out.append(poly(ribs[rib],palette['accent'],1.5,opacity))
        if progress<travel_end:
            # Alternate direction on successive closed sections.
            path=ribs[current] if current%2==0 else list(reversed(ribs[current]))
            lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(path,path[1:])]
            distance=(progress/travel_end)*sum(lengths)
            marker=path[-1]
            for a,b,length in zip(path,path[1:],lengths):
                if distance<=length:
                    t=distance/length if length else 0
                    marker=(a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
                    break
                distance-=length
        else:
            a,b=ribs[current][0],ribs[(current+1)%len(ribs)][0]
            marker=(a[0]+(b[0]-a[0])*fade,a[1]+(b[1]-a[1])*fade)
        out.append(f'<circle cx="{marker[0]:.2f}" cy="{marker[1]:.2f}" r="5.5" fill="{palette["accent"]}" opacity=".16"/>')
        out.append(f'<circle cx="{marker[0]:.2f}" cy="{marker[1]:.2f}" r="2.8" fill="{palette["text"]}" stroke="{palette["accent"]}" stroke-width="1"/>')
        return out
    highlight=[point(j/40,.14) for j in range(41)]
    out.append(poly(highlight,palette['accent'],1.5))
    tip=point(.30,.14)
    if not animated:
        out.append(f'<circle cx="{tip[0]:.2f}" cy="{tip[1]:.2f}" r="3" fill="{palette["accent"]}"/>')
        return out
    motion_path='M '+' L '.join(f'{x-tip[0]:.2f},{y-tip[1]:.2f}' for x,y in highlight)
    rotation=';'.join(f'{angle} {cx} {cy}' for angle in (0,4,0,-4,0))
    style='<style>.wing-static{display:none}@media(prefers-reduced-motion:reduce){.wing-motion{display:none}.wing-static{display:inline}}</style>'
    start=(f'<g class="wing-motion"><animateTransform attributeName="transform" type="rotate" '
           f'values="{rotation}" dur="14s" repeatCount="indefinite" calcMode="spline" '
           'keyTimes="0;0.25;0.5;0.75;1" keySplines=".42 0 .58 1;.42 0 .58 1;.42 0 .58 1;.42 0 .58 1"/>')
    marker=(f'<circle cx="{tip[0]:.2f}" cy="{tip[1]:.2f}" r="3" fill="{palette["accent"]}"><animateMotion path="{motion_path}" '
            'dur="6s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;0.5;1" '
            'calcMode="spline" keySplines=".42 0 .58 1;.42 0 .58 1"/></circle>')
    return [style,start]+out+[marker,'</g><g class="wing-static">']+wing(palette,cx,cy,scale,False)+['</g>']

def cooling(palette,cx,cy,scale,phase=None):
    def p(x,y,z):
        if phase is not None:
            yaw=.09*math.sin(phase*math.tau)
            pitch=.05*math.sin(phase*math.tau)
            x,y=x*math.cos(yaw)-y*math.sin(yaw),x*math.sin(yaw)+y*math.cos(yaw)
            y,z=y*math.cos(pitch)-z*math.sin(pitch),y*math.sin(pitch)+z*math.cos(pitch)
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
    if phase is not None:
        # Moving highlights illustrate flow; they are not computed thermal results.
        for offset in (0,.5):
            progress=(phase+offset)%1
            if progress<.35:
                t=progress/.35
                points=[p(-.96+.67*t,.045*math.sin(t*3.12),-.05)]*4
            elif progress<.6:
                t=(progress-.35)/.25
                points=[p(-.29+.42*t,side*.38*t**.8,-.05) for side in (-1,1) for child in (-1,1)]
            else:
                t=(progress-.6)/.4
                points=[p(.13+.78*t,side*.38+child*.19*t**.85,-.05)
                        for side in (-1,1) for child in (-1,1)]
            opacity=min(1,progress/.04,(1-progress)/.04)
            for x,y in points:
                radius=2.3 if scale<60 else 3.2
                out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius+2}" fill="{palette["accent"]}" opacity="{.15*opacity:.3f}"/>')
                out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{palette["accent"]}" opacity="{opacity:.3f}"/>')
    return out

def fractal(palette,cx,cy,scale,phase=None):
    def p(x,y,z):
        return cx+scale*(x*.7+y*.42),cy+scale*(x*.24-y*.22-z*.65)
    out=[]
    for x in (-.85,.85):
        for y in (-.75,.75):
            out.append(line(p(x,y,-1),p(x,y,1),palette['line'],1.6))
    for z in (-1,1):
        corners=[p(-.85,-.75,z),p(.85,-.75,z),p(.85,.75,z),p(-.85,.75,z),p(-.85,-.75,z)]
        out.append(poly(corners,palette['line'],1.3))
    if phase is not None:
        tilt=.23+.12*math.sin(phase*math.tau)
        yaw=.22*math.sin(phase*math.tau)
        def table_point(x,y,z):
            y,z=y*math.cos(tilt)-z*math.sin(tilt),y*math.sin(tilt)+z*math.cos(tilt)
            x,y=x*math.cos(yaw)-y*math.sin(yaw),x*math.sin(yaw)+y*math.cos(yaw)
            return x,y,z-.2
        out.append(poly([p(*table_point(.68*math.cos(i*math.pi/32),.68*math.sin(i*math.pi/32),0)) for i in range(65)],palette['line'],1.4))
        for z in (.12,.20,.28,.36,.44,.52):
            out.append(poly([p(*table_point(.22*math.cos(i*math.pi/24),.22*math.sin(i*math.pi/24),z)) for i in range(49)],palette['accent'],1.6))
        angle=phase*math.tau*2
        nozzle=table_point(.22*math.cos(angle),.22*math.sin(angle),.52)
        out.append(line(p(-.85,0,.8),p(.85,0,.8),palette['line'],2))
        out.append(line(p(nozzle[0],nozzle[1],.8),p(*nozzle),palette['line'],2))
        out.append(line(p(nozzle[0],nozzle[1],nozzle[2]+.09),p(*nozzle),palette['accent'],3))
        head=p(nozzle[0],nozzle[1],.8)
        out.append(f'<rect x="{head[0]-3:.2f}" y="{head[1]-3:.2f}" width="6" height="6" rx="1" fill="{palette["muted"]}"/>')
        return out
    out.append(poly([p(.68*math.cos(i*math.pi/32),.68*math.sin(i*math.pi/32),-.2+.32*math.sin(i*math.pi/32)) for i in range(65)],palette['line'],1.4))
    for z in (0,.08,.16,.24,.32,.40):
        out.append(poly([p(.22*math.cos(i*math.pi/24),.22*math.sin(i*math.pi/24),z) for i in range(49)],palette['accent'],1.6))
    out.append(line(p(-.85,0,.8),p(.85,0,.8),palette['line'],2))
    out.append(line(p(0,0,.8),p(0,0,.42),palette['accent'],3))
    return out

def hero(theme,mobile=False,phase=None):
    c=THEMES[theme]
    if mobile:
        width,height=480,390
        body=[text(24,35,'MECHANICAL ENGINEERING',12,c['muted'],mono=True,spacing=1.4),
              text(20,124,'Soun',92,c['text'],700,spacing=-4),
              text(24,166,'Lê Nguyễn Trần Tiến',21,c['text']),
              text(24,203,'Learning through interdisciplinary work',18,c['text']),
              text(24,233,'DESIGN  /  SIMULATION  /  PROGRAMMING',11,c['muted'],mono=True,spacing=.7)]
        body+=wing(c,300,306,86,phase=phase)
        body+=[text(24,366,'soun26 / github',11,c['muted'],mono=True)]
    else:
        width,height=1000,340
        body=[text(36,40,'MECHANICAL ENGINEERING',13,c['muted'],mono=True,spacing=2),
              text(31,157,'Soun',118,c['text'],700,spacing=-5),
              text(38,207,'Lê Nguyễn Trần Tiến',27,c['text']),
              text(38,249,'Learning through interdisciplinary work',22,c['text']),
              text(38,302,'DESIGN  /  SIMULATION  /  PROGRAMMING',12,c['muted'],mono=True,spacing=1)]
        body+=[line((590,54),(590,285),c['border'])]
        body+=wing(c,780,155,144,phase=phase)
        body+=[text(662,298,'FORM / STRUCTURE / MOTION',11,c['muted'],mono=True,spacing=1)]
    return svg(width,height,'Soun — Lê Nguyễn Trần Tiến / Mechanical Engineering / Learning through interdisciplinary work',body,c)

def project(kind,theme,mobile=False,phase=None):
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
        body+=(cooling if is_cooling else fractal)(c,347,193 if is_cooling else 184,49 if is_cooling else 58,phase=phase)
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
        body+=(cooling if is_cooling else fractal)(c,806,120 if is_cooling else 114,101 if is_cooling else 95,phase=phase)
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
