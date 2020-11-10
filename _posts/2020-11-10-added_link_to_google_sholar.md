---
layout: post
title: added link to google scholar
date: 2020-11-10 11:02 +0100
---
I wanted to see if you could add additional icons to the index page. Again, this was surprisingly easy.
I'm really starting to like Jekyll!

I started by duplicating the mail button part of the header.html in _includes:

```html
	{% raw %}{% if site.author.email %}{% endraw %}
        <!-- Email -->
        <li class="navigation__item">
            <a href="mailto:{% raw %}{{ site.author.email }}{% endraw %}" title="Email {% raw %}{{ site.author.email }}{% endraw %}
			"target="_blank">
            	<i class="icon icon-mail"></i>
            	<span class="label">Email</span>
            </a>
        </li>
	{% raw %}{% endif %}{% endraw %}
```

and changed the copy to:
```html
    {% raw %}{% if site.author.scholar %{% endraw %}}
        <!-- Scholar -->
        <li class="navigation__item">
            <a href="{% raw %}{{ site.author.scholar }}{% endraw %}" title="{% raw %}{{ site.author.name }{% endraw %}} on Google Scholar"
			target="_blank">
            	<i class="icon icon-book"></i>
            	<span class="label">Email</span>
            </a>
        </li>
    {% raw %}{% endif %}{% endraw %}
```


The icons you can use are available here: 
[Zurb foundations]("https://zurb.com/playground/foundation-icon-fonts-3").
I chose the a book ('icon-book') which seemed fitting, as there was no google scholar icon. For the code to work I also
added scholar to the _config.yml:

```yml
author:
  name: 'Jonas Ångström'
  email: jonas.aangstroem@gmail.com
  twitter_username: AngstromJonas
  github_username:  jonasangstrom
  linkedin_username:  jonasangstrom
  scholar: https://scholar.google.com/citations?hl=en&user=pbYHl4UAAAAJ
```

/Jonas

<iframe src="https://open.spotify.com/embed/track/4tljE9gIKxc5s0Z0VV90VN" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>

Addendum: I had to
[use {% raw %} {% raw %} {% endraw %} in the code blocks](https://rachelmad.github.io/entries/2016/11/06/code-in-jekyll) in markdown
or they would be interpreted. *i.e.* it would show **{{ site.author.email }}** and 
not **{% raw %}{{ site.author.email }}{% endraw %}.**