from PIL import Image, ImageFilter
import os, os.path
import argparse
from string import Template

parser = argparse.ArgumentParser(description='Convert images to 16:9 aspect ratio with blurred sidebars')
parser.add_argument('path', metavar='path', help='Directory where to load files from')

def landscapeDimensions(size):
	width, height = size
	width = int(height * 16.0 / 9)
	return width, height

def blurImage(path):
	image_paths = []
	valid_images = ['.jpg','.gif','.png','.tga']
	for f in os.listdir(path):
		ext = os.path.splitext(f)[1]
		if ext.lower() not in valid_images:
			continue
		image_paths.append(os.path.join(path,f))
	
	for image_path in image_paths:
		#Read image
		background = Image.open(image_path)
		new_dimensions = landscapeDimensions(background.size)
		resized_background = background.resize(new_dimensions)

		#Applying a filter to the image
		im_blur = resized_background.filter(ImageFilter.GaussianBlur(radius=30))
		foreground = Image.open(image_path)
		width, height = foreground.size
		
		new_width, _ = new_dimensions
		x_offset = int((new_width - width) / 2)
		im_blur.paste(foreground, (x_offset, 0))
		
		base_filename = os.path.basename(image_path)
		template = Template('_processed_$base_filename')
		filename = template.substitute(base_filename=base_filename)
		#Saving the filtered image to a new file
		im_blur.save(os.path.join(path, filename), 'JPEG' )

if __name__ == '__main__':
	args = parser.parse_args()
	blurImage(args.path)
