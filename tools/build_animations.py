"""Bake the original profile illustrations into looping GIFs for GitHub.

Requires Pillow and PySide6. No external images or private project data are used.
"""
import os
import argparse
from pathlib import Path
import sys

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from PIL import Image, ImageChops, ImageColor
from PySide6.QtCore import QByteArray, QSize
from PySide6.QtGui import QColor, QFontDatabase, QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

from build_assets import ASSETS, THEMES, hero, project

FRAME_COUNT = 300
HERO_FRAME_COUNT = 480
FRAME_DURATION_MS = 20
RENDER_SCALE = 2


def load_fonts():
    font_dir = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    for font in sorted(font_dir.glob('*.ttf')):
        if font.name.lower().startswith(('segoe', 'arial', 'consola')):
            QFontDatabase.addApplicationFont(str(font))


def render(source, background):
    renderer = QSvgRenderer(QByteArray(source.encode('utf-8')))
    if not renderer.isValid() or renderer.animated():
        raise ValueError('Each baked frame must be a valid, static SVG')
    size = renderer.defaultSize()
    image = QImage(QSize(size.width()*RENDER_SCALE, size.height()*RENDER_SCALE), QImage.Format.Format_RGBA8888)
    image.fill(QColor(background))
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    result = Image.frombytes('RGBA', (image.width(), image.height()), bytes(image.constBits())).convert('RGB')
    return result.resize((size.width(), size.height()), Image.Resampling.LANCZOS)


def save_gif(frames, base, bounds, path, background, foreground):
    # One palette for the entire sequence keeps text and colors identical.
    samples = Image.new('RGB', (base.width*8, base.height), background)
    for i in range(8):
        samples.paste(base, (i*base.width, 0))
        samples.paste(frames[i*len(frames)//8], (i*base.width+bounds[0], bounds[1]))
    palette = samples.quantize(colors=254, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    colors = palette.getpalette()[:762]
    colors += list(foreground) + list(background)
    palette.putpalette(colors)
    def index_frame(frame):
        quantized = frame.quantize(palette=palette, dither=Image.Dither.NONE)
        # Pillow's lookup cache can approximate even an exact palette entry.
        # Restore flat background and text pixels explicitly, including #ffffff.
        for color, index in ((foreground,254),(background,255)):
            diff = ImageChops.difference(frame, Image.new('RGB', frame.size, color))
            red, green, blue = diff.split()
            mask = ImageChops.lighter(red, ImageChops.lighter(green, blue)).point(lambda value: 255 if value == 0 else 0)
            quantized.paste(index, mask=mask)
        return quantized
    indexed_base = index_frame(base)
    indexed = []
    for frame in frames:
        quantized = indexed_base.copy()
        quantized.paste(index_frame(frame), bounds[:2])
        indexed.append(quantized)
    indexed[0].save(path, save_all=True, append_images=indexed[1:], duration=FRAME_DURATION_MS,
                    loop=0, optimize=False, disposal=1)


def motion_bounds(kind, mobile):
    if kind == 'hero':
        return (160,240,479,389) if mobile else (600,45,990,288)
    if mobile:
        return (265,146 if kind == 'cooling' else 118,470,246)
    return (660,10,970,215)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', choices=('hero','cooling','fractal'), help='Rebuild only one illustration')
    parser.add_argument('--theme', choices=tuple(THEMES), help='Rebuild only one theme')
    parser.add_argument('--layout', choices=('desktop','mobile'), help='Rebuild only one layout')
    args = parser.parse_args()
    app = QGuiApplication([])
    load_fonts()
    ASSETS.mkdir(exist_ok=True)
    for theme, colors in THEMES.items():
        if args.theme and theme != args.theme:
            continue
        background = ImageColor.getrgb(colors['bg'])
        for mobile in (False, True):
            if args.layout and mobile != (args.layout == 'mobile'):
                continue
            suffix = '-mobile' if mobile else ''
            for kind in ('hero', 'cooling', 'fractal'):
                if args.only and kind != args.only:
                    continue
                frames = []
                base = None
                bounds = motion_bounds(kind, mobile)
                frame_count = HERO_FRAME_COUNT if kind == 'hero' else FRAME_COUNT
                for index in range(frame_count):
                    phase = index/frame_count
                    source = hero(theme, mobile, phase) if kind == 'hero' else project(kind, theme, mobile, phase)
                    rendered = render(source, colors['bg'])
                    if base is None:
                        base = rendered
                    changed = ImageChops.difference(base, rendered).getbbox()
                    if changed and not (bounds[0] <= changed[0] and bounds[1] <= changed[1]
                                        and bounds[2] >= changed[2] and bounds[3] >= changed[3]):
                        raise ValueError(f'{kind}: motion would extend outside its illustration region: {changed}')
                    frames.append(rendered.crop(bounds))
                path = ASSETS / f'{kind}-{theme}{suffix}.gif'
                save_gif(frames, base, bounds, path, background, ImageColor.getrgb(colors['text']))
                print(f'{path.name}: {path.stat().st_size/1024:.0f} KiB / {frame_count} frames', flush=True)
    del app


if __name__ == '__main__':
    main()
