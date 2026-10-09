"""Generate resolution-independent, declarative SVG profile animations.

No scripts, remote resources or raster images are embedded.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

from build_assets import ASSETS, THEMES, hero, project

SVG='http://www.w3.org/2000/svg'
ET.register_namespace('',SVG)
KEYFRAME_COUNT=240


def animate(kind,theme,mobile=False):
    build=lambda phase: hero(theme,mobile,phase) if kind=='hero' else project(kind,theme,mobile,phase)
    frames=[ET.fromstring(build(index/KEYFRAME_COUNT)) for index in range(KEYFRAME_COUNT+1)]
    nodes=[list(frame.iter()) for frame in frames]
    base=frames[0]
    if any(len(frame)!=len(nodes[0]) for frame in nodes):
        raise ValueError('Every keyframe must have the same vector structure')
    duration='9.6s' if kind=='hero' else '6s'
    for position,element in enumerate(nodes[0]):
        peers=[frame[position] for frame in nodes]
        if any(peer.tag!=element.tag for peer in peers):
            raise ValueError('Mismatched vector primitives')
        for name in tuple(element.attrib):
            values=[peer.attrib[name] for peer in peers]
            if any(value!=values[0] for value in values[1:]):
                if name not in ('points','x','y','x1','x2','y1','y2','cx','cy','opacity'):
                    raise ValueError(f'Unexpected animated attribute: {name}')
                ET.SubElement(element,f'{{{SVG}}}animate',{
                    'attributeName':name,'values':';'.join(values),
                    'dur':duration,'repeatCount':'indefinite','calcMode':'linear',
                })
    return ET.tostring(base,encoding='unicode')+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',choices=('hero','cooling','fractal'))
    args=parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    for theme in THEMES:
        for mobile in (False,True):
            for kind in ('hero','cooling','fractal'):
                if args.only and kind!=args.only:
                    continue
                suffix='-mobile' if mobile else ''
                path=ASSETS/f'{kind}-{theme}{suffix}-motion.svg'
                path.write_text(animate(kind,theme,mobile),encoding='utf-8',newline='\n')
                print(f'{path.name}: {path.stat().st_size/1024:.0f} KiB',flush=True)


if __name__=='__main__':
    main()
