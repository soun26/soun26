# Soun profile — design notes

The profile presents **Soun / Lê Nguyễn Trần Tiến** with **Mechanical Engineering**
as the main focus. The introduction emphasizes curiosity and learning through
interdisciplinary work across design, simulation, programming and manufacturing.

## Direction

The layout combines a large typographic identity, an original swept-wing wireframe,
short project introductions and a restrained neutral palette with a copper accent.
Project overviews provide readable context before tools and technologies.
The banners have light/dark and mobile variants; light backgrounds use pure white.
The profile embeds animated vector SVGs directly from the repository's raw URLs
so typography and geometry stay sharp at any display density. All three move:
the wing changes angle as its eight sections light up in sequence. A small marker
traces each closed section, reversing direction on successive sections, and then
returns to the first section along the leading edge. Highlights
travel through the cooling channels as the block gently turns, and the
printer nozzle follows the part while its table tilts. Typography stays still.
These movements are illustrative, rather than calculated engineering results.

These choices apply ideas from design work published in 2025–2026:

- [Google Design — Material 3 Expressive research, May 2025](https://design.google/library/expressive-material-design-google-research?pubDate=20250521):
  use size, grouping and containment to establish attention and hierarchy.
- [Microsoft Design — When outputs are the experience, June 2026](https://microsoft.design/articles/when-outputs-are-the-experience/):
  use typography, editorial pacing and restraint to make content readable.
- [GitSkins — GitHub Profile README Examples, July 2026](https://www.gitskins.com/blog/github-profile-readme-examples):
  organize a profile around identity, selected work, context and useful links.
- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme):
  reference gallery for Markdown-native profile structures.
- [GitHub — Quickstart for writing](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github):
  picture sources support light/dark image selection.

## Assets and maintenance

Run `python tools/build_assets.py` to regenerate the original SVG assets.
Run `python tools/build_vector_animations.py` to regenerate the 12 animated vector
variants used by the profile. Geometry uses 240 synchronized interpolation steps
per loop; the browser interpolates between them at its own rendering rate.
Only the illustration's coordinates and highlight opacity animate. Text stays
as vector text, rather than becoming part of a raster animation.
The profile uses declarative SVG animation without scripts or external resources
([SVG animation](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/animate)).
The explicit motion variants do not include the old automatic static-image
selection for reduced-motion preferences, matching the requested moving artwork.
Run `python tools/build_animations.py` with Pillow and PySide6 to regenerate the
12 optional GIF assets. The wing has 480 frames (9.6 seconds); the project cards have
300 frames (6 seconds). All frames last 20 milliseconds (50 fps). Each GIF
uses a shared color palette to keep the static text and background consistent.
Motion is rendered directly from the vector geometry in `tools/build_assets.py`.
GitHub supports GIF images; its repository SVG viewer does not support animation
([GitHub documentation](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)).
The illustrations are schematic design artwork, rather than aerodynamic simulation
results or images of private part geometry.

The profile README and project overviews are in English. Navigation links use short
labels without arrow symbols. Project link rows use regular spaces and no forced
line breaks, allowing natural wrapping on narrow screens.
The project descriptions are public summaries. The 5-axis printing source is private;
`soun26/fdut-5axis-printing` is a public presentation containing its English README,
animated recording preview and source-access contact link. The preview uses the
recording's native 1920 × 1012 resolution at 30 fps. Public descriptions embed the
GIF directly, with no MP4 link. Interface previews have rounded transparent corners,
using matching proportions across the static cooling image and the printing GIF.
The cooling screenshot uses a self-contained SVG clip; the GIF contains its own
transparency mask. The public project overview has no reference footer. The supplied
10.005-second recording retains its first 7.005 seconds, with the last three seconds
removed. Original third-party notices remain
with the private source. The original Cooling AI source repository remains private.
The Cooling AI project card links directly to its browser edition at
https://cooling-ai-user.lengtrtien2610.workers.dev/. The research overview also
links to the web app. An actual web-interface screenshot links to the user edition.
The browser interface and gateway are published separately in `soun26/cooling-ai-web`.
The original research source remains private. Research interests also include
structural strength in aerospace applications. The redundant illustration caption
has been removed from the hero.
