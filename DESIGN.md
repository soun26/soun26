# Soun profile — design notes

The profile presents **Soun / Lê Nguyễn Trần Tiến** with **Mechanical Engineering**
as the main focus. The introduction emphasizes curiosity and learning through
interdisciplinary work across design, simulation, programming and manufacturing.

## Direction

The layout combines a large typographic identity, an original swept-wing wireframe,
short project introductions and a restrained neutral palette with a copper accent.
Project overviews provide readable context before tools and technologies.
The banners have light/dark and mobile variants; light backgrounds use pure white.
The profile embeds looping GIFs so all three illustrations can move on GitHub:
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
Run `python tools/build_animations.py` with Pillow and PySide6 to regenerate the
12 animated GIFs. The wing has 480 frames (9.6 seconds); the project cards have
300 frames (6 seconds). All frames last 20 milliseconds (50 fps). Each GIF
uses a shared color palette to keep the static text and background consistent.
Motion is rendered directly from the vector geometry in `tools/build_assets.py`.
GitHub supports GIF images; its repository SVG viewer does not support animation
([GitHub documentation](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)).
The illustrations are schematic design artwork, rather than aerodynamic simulation
results or images of private part geometry.

The profile README and project overviews are in English.
The project descriptions are public summaries. The 5-axis printing simulator has a public
source repository; the Cooling AI source repository remains private.
The Cooling AI project card showcases its browser/PWA edition. The overview
does not claim a live deployment URL when none is recorded in the repository.
