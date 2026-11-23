# Rudraksh Tuwani

The homepage is in `docs/index.md`. Add articles to `extra.posts` in `mkdocs.yml` in newest-first order. The homepage displays the first three entries, and the blog displays the full list. Each article can still be built and deployed from its project repo.

GitHub Actions builds the site with MkDocs and publishes it to GitHub Pages when `main` changes. Each deployment refreshes the copy of the public Argon article at `/blog/argon-binding/`. The Publish GitHub Pages workflow can also be run manually after an article update.

To preview the site and article together, install `requirements-docs.txt`, run `mkdocs build --strict`, then run `python3 scripts/mirror_argon.py site/blog/argon-binding` and `python3 -m http.server --directory site 8000`. Open [localhost](http://127.0.0.1:8000/).

To enable opt-in Google Analytics, set the public GA4 measurement ID in `docs/assets/analytics.js`. Use the same web stream and cross-domain measurement for any Render articles you want included. To track Google Search performance, add a URL-prefix property for `https://rudrakshtuwani.github.io/`, verify it in Search Console, and submit `/sitemap.xml`.
