# Soun profile — design notes

The profile presents **Soun / Lê Nguyễn Trần Tiến**, **Mechanical Engineering**
and the **Aerospace Mechanics** specialization supplied by the owner.

## Direction

The layout combines a large typographic identity, an original wing wireframe,
short project introductions and a restrained neutral palette with a copper accent.
Project overviews provide readable context before tools and technologies.
SVG banners have light/dark and mobile variants; light backgrounds use pure white.

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
The illustrations are schematic design artwork, rather than aerodynamic simulation
results or images of private part geometry.

English is the default profile README. `README.vi.md` provides a Vietnamese version.
The project descriptions are public summaries. FDUT Fractal Simulator has a public
source repository; the Cooling AI source repository remains private.
The Cooling AI project card showcases its browser/PWA edition. The overview
does not claim a live deployment URL when none is recorded in the repository.
