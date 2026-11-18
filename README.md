# The World Today — 18 November 2026

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/charlyies/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/charlyies/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

An entry for the [make.fun competition "Sum up 18 November's world news in one image"](https://make.fun/bounty/news-image-20261118).

## The image

A newspaper front page, drawn entirely in code with Python and Pillow
(no AI image generation), summing up Wednesday 18 November 2026 in five
stories:

- **Lead — U.S. strikes Iran as Gulf war escalates.** U.S. jets hit a
  Revolutionary Guard missile site on Qeshm Island and sank five Iranian
  oil tankers; Iran answered with drones over Bahrain and Kuwait and
  missiles at a U.S. base in Jordan. The lead illustration is a night
  scene over the Gulf: a burning tanker under a fire-lit sky, an intact
  tanker beside it, fighter jets, drones and arcing missile trails.
- **Kerch Bridge hit again.** Ukraine strikes the bridge for a second
  day; part of the road span falls into the strait.
- **Three leaders meet in Shenzhen.** Xi hosts the APEC summit as Putin
  and Trump arrive for talks this week.
- **Democrats take 56 Senate seats.** Mary Peltola wins Alaska's Senate
  race, unseating Dan Sullivan.
- **Ebola cases double in Congo.** The outbreak passes 11,000 cases and
  5,400 deaths in three months, the U.N. says.

## How to run it

Build the image (deterministic — two runs give the same bytes):

```sh
python3 compose.py
```

Copy it to the output directory with the entry program:

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` checks the PNG signature, the 1024×1024 dimensions and the
1 MiB size cap before copying `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Files

- `compose.py` — the script that draws the 1024×1024 front page.
- `entry.png` — the finished image.
- `main.ts` — the entry program (Node 22, standard library only).
- `LICENSE` — MIT license.
