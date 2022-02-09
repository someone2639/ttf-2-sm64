def get_image_width(img_input):
	arr = []
	earliest_start = []
	img = img_input.convert('RGBA')
	width, height = img.size
	# print(fname, width, height)
	for i in range(height):
		a1 = [img.getpixel((o, i)) for o in range(width)]
		a2 = a1[::-1]
		start = -1
		end = -1
		for l in range(width):
			if a1[l][-1] != 0:
				earliest_start.append(l)
				start = l
				break
		for l in range(width):
			if a2[l][-1] != 0:
				end = width - l
				break
		if start == -1 or end == -1:
			arr.append(0)
		else:
			arr.append(end - start)



	toReturn = max(arr)
	if toReturn == 0:
		return width / 2
	return toReturn