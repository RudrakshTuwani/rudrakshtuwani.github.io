# Rudraksh Tuwani

The homepage is in `docs/index.md`. Add articles to `extra.posts` in `mkdocs.yml` in newest-first order. The homepage displays the first three entries, and the blog displays the full list. Each article can still be built and deployed from its project repo.

GitHub Actions builds the site with MkDocs and publishes it to GitHub Pages when `main` changes. To preview locally, install `requirements-docs.txt`, run `mkdocs serve`, and open [localhost](http://127.0.0.1:8000/).

To enable opt-in Google Analytics, set the public GA4 measurement ID in `docs/assets/analytics.js`. Use the same web stream and cross-domain measurement for any Render articles you want included. To track Google Search performance, add a URL-prefix property for `https://rudrakshtuwani.github.io/`, verify it in Search Console, and submit `/sitemap.xml`.
