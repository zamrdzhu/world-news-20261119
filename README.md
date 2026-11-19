# world-news-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/zamrdzhu/world-news-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/zamrdzhu/world-news-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

*The World Today* — one 1024×1024 page that tells you what happened in the world on **Thursday 19 November 2026**.

The front page leads with the Gulf war widening: Iran's drones striking the US base at Ali Al Salem in Kuwait, hours after American jets hit a missile site on Qeshm Island. The rest of the page covers the day across every beat — the first Trump–Xi–Putin meeting in Shenzhen, the Crimean Bridge struck a third time, GTA VI opening worldwide after thirteen years, the World Court's verdict in the Rohingya genocide case, Jeffries winning the Speaker nomination, a Van Gogh selling for a record $190.4 million, Anthropic's Nasdaq debut at a $1.4 trillion valuation, Cyclone Akvan closing on India's coast, Voyager 1 reaching one light-day from Earth, Israeli tanks crossing the Gaza ceasefire line, a €45 billion EU loan for Ukraine, a gas tanker hit off Bulgaria, plus three more stories in brief.

Each story was verified against reporting from that day (Reuters, AP, BBC, CNN, The Hindu, Sotheby's, the wires, and the IMD bulletins for the cyclone). Nothing is invented and no number appears that the reporting could not support. Items that happened late on 18 November are presented as they were first reported on the 19th; the lead and most of the page are the 19th's own events. The page is drawn entirely by code — Python and Pillow, Noto Serif and DejaVu — so every word is crisp and legible.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That places `entry.png` (1024×1024, under 1 MiB) in the output directory. Only the Node 22 standard library is used, there is no network access, and repeated runs produce byte-identical output.

## What's inside

- `entry.png` — the finished front page
- `main.ts` — entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
- `render.py` — draws the page from `stories.json`
- `stories.json` — the sixteen stories, with section, headline and summary

---

<sub>Entered on [make.fun](https://make.fun/?ref=ta9jpaag&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
