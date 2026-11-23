const list = document.querySelector("#latest-posts");

try {
  const response = await fetch("/blog/");
  if (response.ok) {
    const blog = new DOMParser().parseFromString(await response.text(), "text/html");
    const links = Array.from(blog.querySelectorAll("#blog-posts > li h2 a[href]")).slice(0, 3);

    for (const link of links) {
      const item = document.createElement("li");
      const post = document.createElement("a");
      post.href = new URL(link.getAttribute("href"), response.url).href;
      post.textContent = link.textContent;
      item.append(post);
      list.append(item);
    }

    list.hidden = links.length === 0;
  }
} catch {
  // The All posts link remains available if the blog index cannot be loaded.
}
