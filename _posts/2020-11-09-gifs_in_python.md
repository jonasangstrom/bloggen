---
layout: post
title: gifs in python
date: 2020-11-09 09:12 +0100
---
I have always made gifs from a set of images in [Gimp](https://www.gimp.org/), but for an upcoming project I
wanted to make a gif from mp4 file. Doing this in Gimp seemed to be a bit involved including first extracting images in
[VLC](https://www.videolan.org/index.sv.html). So this was a good excuse to learn how to do it in python,
as I was sure [there must be a better way](https://www.youtube.com/watch?v=wf-BqAjZb8M). 

I found [this script](https://gist.github.com/michaelosthege/cd3e0c3c556b70a79deba6855deb2cc8) using imageio by some
quick googling which was doing approximately what I wanted. I had imageio installed already but when I ran the code
I had to install imageio-ffmpeg which was easily done.

```bash
pip install imageio-ffmpeg
```

However, I wanted to do some additional things:

1. Speed up by about 5 times.
2. Reduce the size of the file

We could achieve 1 and 2 by skipping frames when writing. We can also achieve 2 by lowering the framerate and resolution.
This is what I came up with:


```python
import imageio
from tqdm import tqdm # tqdm is not necessary, it just adds a progress bar

reduce_resolution_by =  4
reduce_framerate_by = 1
increase_speed_by = 5

input_path = 'my_mp4.mp4'
output_path = 'my_gif.gif'


def get_resolution(input_path):
	reader = imageio.get_reader(input_path)
	return reader.get_meta_data()['size']


def gif_from_mp4(input_path, output_path, reduce_framerate_by=1,
                 reduce_resolution_by=1, increase_speed_by=1):
	x_shape, y_shape = get_resolution(input_path)
	new_resolution = (x_shape//reduce_resolution_by,
                      y_shape//reduce_resolution_by)

	reader = imageio.get_reader(input_path, size=new_resolution)

	fps = reader.get_meta_data()['fps']
	new_fps = fps//reduce_framerate_by

	with imageio.get_writer(output_path, fps=new_fps) as writer:
		for i, im in tqdm(enumerate(reader)):
			if i%(reduce_framerate_by*increase_speed_by) == 0:
				writer.append_data(im)


gif_from_mp4(input_path, output_path, reduce_framerate_by, reduce_resolution_by,
		     increase_speed_by)

```
/Jonas