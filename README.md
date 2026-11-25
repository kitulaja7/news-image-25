# Wednesday 25 November 2026 — The World in One Day

[![Competition](https://make.fun/bounty/news-image-20261125/badge/competition.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/bounty/news-image-20261125/badge/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/bounty/news-image-20261125/badge/reward.svg)](https://make.fun/bounty/news-image-20261125)

One image that sums up Wednesday 25 November 2026's world news: 38 stories
across 7 regions — two tankers hit mines in Hormuz, Shenzhou-24 carries
Pakistan's first astronaut into orbit, Ukraine drones hit two Russian
refineries, and 35 more, all dated, sourced and cross-checked.

- **Entry:** `entry.png` (1024×1024, ≤1 MiB), drawn by `render.py` (Pillow,
  dev-time only) from real wire reports of 25 November 2026.
- **Program:** `main.py` (Python 3.13, standard library only) copies the
  committed `entry.png` to `/output/entry.png` byte-for-byte. It runs twice
  with identical output and needs no network.
- **Competition:** [news-image-20261125 on make.fun](https://make.fun/bounty/news-image-20261125)

## How it was built

The front page keeps the dense-newspaper frame that the round-3 winners of
the 24 November edition used (masthead, stat strip, region bar, UTC
timeline, 3 features + tiles, ALSO list, world map + pins, DATE CHECK,
verification chips) — but every feature illustration is drawn BRIGHT:
pale daylight sky, saturated colour, one big focus object (a white tanker,
a white rocket, white refinery towers with a vivid flame). No dark night
scenes: the previous edition's dark feature art collapsed into unreadable
blobs at the judge's 512px size.

Every numbered story happened, or was first reported, on Wednesday
25 November 2026 (UTC). Sources are named on each item; the DATE CHECK box
lists the previous days' stories that were deliberately left out.
