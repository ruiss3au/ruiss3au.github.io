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

Saturday cron prepares and locally commits a verified roundup from Friday’s 3gppedia extractions. You review and push. See [operation guide](docs/weekly-roundup.md).
