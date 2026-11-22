# Purple Star Astrology Charting

A charting and study tool for Zi Wei Dou Shu (Purple Star Astrology), based on traditional rules.
Traditional Chinese culture / divination-study project — **not** a scientific product and **not** a prediction service.

## Features

- Natal chart: palaces, five-element bureau, Ziwei/Tianfu, 14 major stars, auxiliary stars, four transformations
- Strength scoring (five-element generation/overcoming method; no edition-specific temple table shipped)
- 28 common patterns (geju)
- Decadal (daxian), annual (liunian), monthly (liuyue) and daily (liuri) flow
- Flying stars (palace-stem four transformations)
- 10 topics: marriage, career, wealth, health, study, children, parents, travel, partnership, legal
- Compatibility (hepan): palace comparison, four-transformation exchange, marriage windows, daxian sync
- Event timing (contract/interview/travel/date/medical/opening) and fortune curve
- School switches: four-transformation table, fire/ring star method, daxian start
- True solar time correction by city or longitude
- JSON output, HTML report, batch CSV
- Offline; no data leaves your machine

## Install

    git clone https://github.com/Shzyhao/purple-star-charting.git
    cd purple-star-charting
    pip install -r requirements.txt

## Usage

    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --year 2026 --out out
    python -m purple_star --gender 男 --solar 1990-05-15 --time 14:30 --topic all --liuyue 2026 --html --out out

See README.md (Chinese) and docs/ for full documentation.

## Disclaimer

For study of traditional Chinese divination culture only. Not medical, financial, legal or marital advice.
No lifespan or death prediction. See DISCLAIMER.md.

## License

Code: MIT. Documentation: CC BY-NC-SA 4.0. No source text of any copyrighted edition is included.
