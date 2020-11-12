---
layout: post
title: new theme!
date: 2020-11-09 21:54 +0100
tags: [jekyll, blog]
---
I didn't like the way syntax highlighting looked in athena so I decided to change the Jekyll theme to
[Jekyll-uno](https://github.com/joshgerdes/jekyll-uno). It was reasonably easy. I ran in to a couple of minor problems:
1. I got strange error messages from Travis-CI about things being deprecated. After some googling this could be resolved by
removing Gemfile.lock and adding it to the .gitignore  (I know almost nothing about Ruby, but this seems to be replaced
during the build. I guess its supposed to do a check that the build environments(?) are the same, so it may not be ideal).
2. The site built into another directory, _site, instead of public, so I changed the destination in the _config.yml or the build
 failed in Travis-CI.
3. I wanted to attribute the background image (a 90 year old areal photography of the ironworks in the village I grew up in) to its source.
I added this by changing the _footer.html in _includes.
4. I wanted an *about* section. This was easier than I thought, I just copied the blog button code, pasted it above and changed the
link and all the "blog"s to 'about' and it seems to work.
```html
	<nav class="cover-navigation cover-navigation--primary">
		<ul class="navigation">
		<li class="navigation__item"><a href="{% raw %}{{ site.baseurl }}{% endraw %}/about" title="link to about"
    	class="about-button">about</a></li>
    	</ul>
	</nav>
	<nav class="cover-navigation cover-navigation--primary">
		<ul class="navigation">
		<li class="navigation__item"><a href="{% raw %}{{ site.baseurl }}{% endraw %}/#blog" title="link to blog"
		class="blog-button">blog</a></li>
		</ul>
	</nav>
```
This may be super hacky, I am not very good at .html, but it seems to work.

Anyway, I am really happy with the new look.

/Jonas

<iframe src="https://open.spotify.com/embed/track/2CGi0kPFzrErHlYjzQpLAh" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>