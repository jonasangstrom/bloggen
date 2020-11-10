---
layout: post
title: added link to google scholar
date: 2020-11-10 11:02 +0100
---
I wanted to see if you could add additional icons to the index page. Again, this was surprisingly easy.
I'm really starting to like Jekyll!

I started by duplicating the mail button part of the header.html in _includes:
```html
              {% if site.author.email %}
              <!-- Email -->
              <li class="navigation__item">
                <a href="mailto:{{ site.author.email }}" title="Email {{ site.author.email }}" target="_blank">
                  <i class="icon icon-mail"></i>
                  <span class="label">Email</span>
                </a>
              </li>
              {% endif %}
```
and changed the copy to:
```html
              {% if site.author.scholar %}
              <!-- Scholar -->
              <li class="navigation__item">
                <a href="{{ site.author.scholar }}" title="{{ site.author.name }} on Google Scholar" target="_blank">
                  <i class="icon icon-book"></i>
                  <span class="label">Email</span>
                </a>
              </li>
              {% endif %}
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