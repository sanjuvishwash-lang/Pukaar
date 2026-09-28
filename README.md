# Pukaar.ai Case Study

Interactive UI/UX case study for Pukaar.ai, a doctor-led co-parent for a baby's first 1,000 days.

## Structure

- `site/` the deployable static site (HTML, images, icons, fonts)
- `scripts/build_site.py` rebuilds `site/` from the local page source
- `vercel.json` tells Vercel to serve `site/` as a static site with no build step

## Deploy

Import this repository in Vercel. No framework or build command is needed; the output directory is `site`.

## Update

Edit the page source locally, run `python3 scripts/build_site.py`, then commit and push. Vercel redeploys on every push to `main`.

Design and case study by Saurabh Yadav.
