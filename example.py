from PIL import Image, ImageDraw
import numpy as np
from abc import ABC, abstractmethod
from ctypes import *
import os


nparray1 = np.array([[1, 2], [3, 5]])
print(nparray1)
nparray1 = nparray1.astype(np.double)
print(nparray1)
nparray2 = np.zeros((2, 2))
print(nparray2)
os.system('gcc -shared -o Test.so Test.c')
lib = CDLL('./Test.so')
c_p1 = POINTER(c_double)
c_p2 = POINTER(c_double)
x = np.array([0.0])
lib.restypes = c_double
lib.argtypes = c_p1, c_int
x = lib.double_max(nparray1.ctypes.data_as(c_p1), 4)
print(x, nparray1.max())
print(nparray1)