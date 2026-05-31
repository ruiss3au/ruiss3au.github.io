# ruiss3au :: tech blog

Static site built with [Hugo](https://gohugo.io), deployed on GitLab Pages.

## Prerequisites

- **Hugo** (extended edition, >= 0.120)

## Development

```bash
hugo server -D    # live preview at http://localhost:1313
hugo              # build to public/
```

## CI/CD

Push to `main`. `.gitlab-ci.yml` builds and deploys to GitLab Pages automatically.
