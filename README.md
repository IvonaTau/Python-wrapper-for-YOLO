# Python-wrapper-for-YOLO

Python bindings for YOLO v2 (https://pjreddie.com/darknet/yolo/) detector function with ctypes.

## Download YOLOv2 source code 

```python
git clone https://github.com/pjreddie/darknet
cd darknet
make
wget http://pjreddie.com/media/files/yolo.weights
```

## Create shared library object and copy it to your darknet directory

```python
cd src
gcc -c -FPIC *.c
gcc -shared -fPIC  -o libdarknet.so  *.o -lc
cp ./libdarknet.so ../
cd ..
```

## Copy python_wrapper.py from this repository to your darknet directory

```python
python python_wrapper.py
```

## Putl all your test images to darknet/data directory.
