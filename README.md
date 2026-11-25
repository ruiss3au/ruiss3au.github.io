# ruiss3au :: tech blog

Static site built with [Hugo](https://gohugo.io), deployed on GitHub Pages.

## Prerequisites

- **Hugo** (extended edition, >= 0.120)

## Development

```bash
hugo server -D    # live preview at http://localhost:1313
hugo              # build to public/
```

## CI/CD

Push to `main`. GitHub Actions builds and deploys to GitHub Pages automatically.

## Weekly roundup

Saturday cron researches Friday’s 3gppedia extractions and locally commits a broad RAN1/RAN4 report covering several important technical developments. The writer surveys both agendas, explains company positions and technical dependencies, and holds publication when the evidence cannot support broad coverage. You review and push. See [operation guide](docs/weekly-roundup.md).
