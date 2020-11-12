---
layout: post
title: local build
date: 2020-11-11 11:02 +0100
tags: [jekyll, blog, AWS]
---
[travis-ci.com](https://travis-ci.com/) has some type of credits ticking down (it is unclear to me 
how I am supposed to get mote) and I have realized I don't really need real continuos integration.
So I just added a script to build locally and upload to the s3 bucket via the aws cli. There may be
some downside to this I do not understand. If I want to have parts of the
site unpublished and only available locally I can work on them in branches.

```python
    import os
    print('starting build script')
    os.system('bundle exec jekyll build')
    os.system('aws s3 sync public/ s3://www.anion.se --acl public-read --delete')
    os.system('aws cloudfront create-invalidation --distribution-id E379E2RCB0S37Y --paths /*')
    print('build done')
```
/Jonas

<iframe src="https://open.spotify.com/embed/track/7oY5dKG6d3vYR2QcdGWsHA" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>