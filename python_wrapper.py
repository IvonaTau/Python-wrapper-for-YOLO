import os
from PIL import Image
import ctypes
from ctypes.util import find_library

mylib = ctypes.cdll.LoadLibrary('libdarknet.so')

class image (ctypes.Structure):
	_fields_ = [('h', ctypes.c_int),
				('w', ctypes.c_int),
				('c', ctypes.c_int),
				('data', ctypes.POINTER(ctypes.c_float))]

class box (ctypes.Structure):
	_fields_ = [('x', ctypes.c_float),
				('y', ctypes.c_float),
				('w', ctypes.c_float),
				('h', ctypes.c_float),]

#C funtions bindings

# void test_detector(char *datacfg, char *cfgfile, char *weightfile, char *filename, float thresh, float hier_thresh)
_test_detector = mylib.test_detector
_test_detector.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_float, ctypes.c_float)
_test_detector.restype = None

def test_detector(datacfg, cfgfile, weightfile, filename, thresh, hier_thresh):
	_test_detector(datacfg, cfgfile, weightfile, filename, thresh, hier_thresh)

# image load_image_color(char *filename, int w, int h)
_load_image_color = mylib.load_image_color
_load_image_color.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
_load_image_color.restype = image

def load_image_color(filename, w, h):
	im = _load_image_color(filename, w, h)
	return im


def read_bounding_boxes(filename):
	f = open(filename)
	objects = []
	weight = 0
	height = 0
	for line in f:
		print (line)
		first_word = line.split(';')[0]
		if first_word == "Dimensions":
			weight = line.split(';')[1]
			height = line.split(';')[2]
		if first_word == "Object":
			objects.append((line.split(';')[1], line.split(';')[2], line.split(';')[4], line.split(';')[5], line.split(';')[6], line.split(';')[7]))
	return weight, height, objects


def crop_bounding_boxes (boxes, image_path, crop_path):
	"""Crops bounding boxes from original images and saves them to location"""
	original_image = Image.open(image_path)
	index = 0
	print('Objects detected in the image', len(boxes))
	for box in boxes:
		index += 1
		print(box[2], box[4], box[3], box[5])
		cropped_image = original_image.crop((int(box[2]), int(box[4]), int(box[3]), int(box[5])))
		object_class = box[0]
		filename =  object_class + '_' + str(index) +'_cropped.jpg'
		cropped_image.save(os.path.join(crop_path, filename))


def crop_box_for_class (boxes, image_path, object_class):
	"""Crops a bounding box for a given class name with highest probability""" 
	original_image = Image.open(image_path)
	general_image = Image.open(image_path)
	probs = 0
	probs_class = 0
	objects_found = 0
	for box in boxes:
		box_prob = float(box[1].strip('%'))/100.0
		if box[0] == object_class:
			objects_found += 1
			print('Object of correct class found!')
			if box_prob > probs_class:
				probs_class = box_prob
				cropped_image = original_image.crop((int(box[2]), int(box[4]), int(box[3]), int(box[5])))
		# else: #give a box for different class with highest probability
		# 	if box_prob > probs:
		# 		probs = box_prob
		# 		general_image = original_image.crop((int(box[2]), int(box[4]), int(box[3]), int(box[5])))
	if objects_found == 0:
		return general_image
	else:
		return cropped_image


def run_detector_onpic (image_path):
	try:
		Image.open(image_path)
		print('running detector on %s' %  image_path)
		test_detector(b'cfg/coco.data', b'cfg/yolo.cfg', b'yolo.weights', image_path.encode('utf-8'), 0.1 , 0.5)
		w, h, o = read_bounding_boxes('bounding_boxes.txt')
		print(o)
		print ('height ', h)
		print ('weight ', w)
		return w, h, o
	except:
		return 0,0,0


def run_detector_indir (images_path):
	"""Runs detector for all images in given directory"""
	for filename in os.listdir(images_path):
		try:
			print(filename) 
			Image.open(os.path.join(images_path,filename))
			test_detector(b'cfg/coco.data', b'cfg/yolo.cfg', b'yolo.weights', os.path.join(images_path, filename), 0.1 , 0.5)
			w, h, o = read_bounding_boxes('bounding_boxes.txt')
			print (w)
			print (h)
			print (o)
		except:
			continue



if __name__ == '__main__':
	run_detector_indir('/data')
