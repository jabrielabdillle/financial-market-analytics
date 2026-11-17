# Deployment and maintenance

Host: free GitHub Pages, public repository, GitHub Actions source.
URL: https://jabrielabdillle.github.io/financial-market-analytics/

`.github/workflows/web.yml` installs the locked Python environment, runs Python tests, regenerates the synthetic dataset, installs the locked Node environment, checks browser/Python metric agreement, runs production Playwright checks and uploads the built `web/dist` artifact. The deploy job runs only on main. Pull requests validate without publishing.

Build locally with `python -m src.export`, then `cd web && npm ci && npm run build`. Do not publish `web/` source or a source HTML shell; deploy `web/dist/`. Relative Vite assets and data URLs support the repository subdirectory.

The source is public and generated synthetic data is publicly downloadable. No credentials or API keys are used. SQLite runs in the visitor's browser; it provides no shared writes, user accounts or durable server storage. Google Fonts are requested for typography, with local fallbacks.

For updates: use a branch, run relevant checks, open a PR, merge after passing CI, and verify the deployment run and live page. Revert the relevant PR through a new PR to roll back. For a 404, inspect Settings → Pages → Source (GitHub Actions), then the main workflow's deploy job and its URL. For missing data, confirm `python -m src.export` ran before the Vite build.

The optional yfinance downloader is not part of deployment. Never publish locally supplied data without reviewing its redistribution rights. Pin and review dependencies when upgrading; regenerate the dataset and check the provenance hash if NumPy or the simulation changes.
