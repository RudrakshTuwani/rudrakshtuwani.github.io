# Rudraksh Tuwani

The homepage is in `docs/index.md`. Add articles to `extra.posts` in `mkdocs.yml` in newest-first order. The homepage displays the first three entries, and the blog displays the full list. Each article can still be built and deployed from its project repo.

GitHub Actions builds the site with MkDocs and publishes it to GitHub Pages when `main` changes. Each deployment refreshes the copy of the public Argon article at `/blog/argon-binding/`. The Publish GitHub Pages workflow can also be run manually after an article update.

To preview the site and article together, install `requirements-docs.txt`, run `mkdocs build --strict`, then run `python3 scripts/mirror_argon.py site/blog/argon-binding` and `python3 -m http.server --directory site 8000`. Open [localhost](http://127.0.0.1:8000/).

The Argon mirror adds the same navigation and social links as the homepage using `theme/site-header.html` and the links in `mkdocs.yml`.

Umami Cloud tracks visits on the personal site and the mirrored article using the shared script in `theme/analytics.html`. Latest posts and the social icons report click events. The tracker limits collection to `rudrakshtuwani.github.io`.

To track Google Search performance, add a URL-prefix property for `https://rudrakshtuwani.github.io/`, verify it in Search Console, and submit `/sitemap.xml`.
