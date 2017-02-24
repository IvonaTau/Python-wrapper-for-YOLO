import os
from PIL import Image
import ctypes

IMAGES_PATH = './data'

mylib = ctypes.cdll.LoadLibrary('libdarknet.so')


#relevant structures from C

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
  
def run_detector ():
	for filename in os.listdir(IMAGES_PATH):
		try:
			print(filename)
			Image.open(os.path.join(IMAGES_PATH,filename))
			test_detector('cfg/coco.data', 'cfg/yolo.cfg', 'yolo.weights', os.path.join(IMAGES_PATH, filename), 0.05, 0.5)
		except:
			continue
      
if __name__ == '__main__':
  run_detector()
