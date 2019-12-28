from PIL import Image, ImageDraw
import numpy as np
from abc import ABC, abstractmethod
from ctypes import *
import os

from numpy.core._multiarray_umath import ndarray


class InterferogramModel:
    """ Contains the data of the interferogram.
        Can:
        - store the image of the interferogram
        - store image as numpy matrix
        - get the whole numpy matrix
        - get rgb pixel
        - get any channel of the pixel (0-r, 1 - g and so on)
        - get green section
        - get width and height of image
    """
    __image = 0
    __NpImage = 0

    def set_image(self, s):
        self.__image = Image.open(s)
        self.__NpImage = np.asarray(self.__image)

    def get_image_npmatrix(self):
        return self.__NpImage[:, :, 1]

    def get_canal_pixel(self, y, x, c):
        return self.__NpImage[y, x, c]

    def get_rgb_pixel(self, y, x):
        return self.__NpImage[y, x]

    def get_green_section(self, x):
        return self.__NpImage[:, x, 1]

    def get_shape(self):
        return self.__NpImage.shape

    def get_height(self):
        return self.__NpImage.shape[0]

    def get_width(self):
        return self.__NpImage.shape[1]


class Tracer_Vol:
    _amount_lines = 0


    def __init__(self, mat, l):
        self._lib = l
        self._width = mat.shape[1]
        self._height = mat.shape[0]
        self._matrix = np.array(mat)
        self._matrix = self._matrix.astype(np.int32)
        self._lines = np.zeros((self._height, self._width), dtype=np.int32)

    def save_array(self, array, name):
        name = "/home/vladimir/PycharmProjects/search_minima/" + str(name) + ".txt"
        file = open(name, "w")
        for i in range(len(array)):
            file.write(str(array[i]) + "\n")
        file.close()

    def test_load_array(self, nparray1, length, nparray2):
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        nparray1 = nparray1.astype(np.int32)
        nparray2 = nparray2.astype(np.int32)
        self._lib.restypes = None
        self._lib.argtypes = c_p1, c_int, c_p2
        self._lib.test_image(nparray1.ctypes.data_as(c_p1), length, nparray2.ctypes.data_as(c_p2))
        for i in range(length):
            print(i, nparray1[i], nparray2[i])

    def draw_array(self, array, flag, input, output):
        if flag == 0:
            image = Image.open(input)
        else:
            image = Image.new("RGB", (self._height, 256), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        result = []
        for i in range(len(array)):
            result.append((i, array[i]))
        draw.line(result, (0, 0, 0), 1)
        del draw
        image.save(output, "PNG")

    def draw_vertical_lines(self, array, input, output):
        img = Image.open(input)
        draw = ImageDraw.Draw(img)
        for i in range(len(array)):
            draw.line([(array[i], 0), (array[i], 255)], (0, 255, 0), 3)
        del draw
        img.save(output, "PNG")

    def draw_lines(self, input, output):
        for i in range(self._amount_lines):
            self.draw_array(self._lines[i], input, output)

    def test_load_matrix(self, nparray1, width, height):
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        nparray1 = nparray1.astype(np.int32)
        nparray2 = np.zeros(nparray1.shape)
        nparray2 = nparray2.astype(np.int32)
        print(nparray1.shape, nparray2.shape)
        self._lib.restypes = None
        self._lib.argtypes = c_p1, c_int, c_int, c_p2
        self._lib.test_image(nparray1.ctypes.data_as(c_p1), width, height, nparray2.ctypes.data_as(c_p2))
        print(nparray1)
        print('***********************************************')
        print(nparray2)

    def test_int_max(self, nparray, length):
        c_p = POINTER(c_int32)
        nparray = nparray.astype(np.int32)
        self._lib.restypes = c_int
        self._lib.argtypes = c_p, c_int
        x = self._lib.int_max(nparray.ctypes.data_as(c_p), length)
        print(x, max(nparray))
        print(nparray)

    def test_int_min(self, nparray, length):
        c_p = POINTER(c_int32)
        nparray = nparray.astype(np.int32)
        self._lib.restypes = c_int
        self._lib.argtypes = c_p, c_int
        x = self._lib.int_min(nparray.ctypes.data_as(c_p), length)
        print(x, min(nparray))
        print(nparray)

    def test_double_max(self, nparray, length):
        c_p1 = POINTER(c_double)
        c_p2 = POINTER(c_double)
        nparray = nparray.astype(np.double)
        npresult = np.array([0])
        npresult = npresult.astype(np.double)
        self._lib.restypes = None
        self._lib.argtypes = c_p1, c_int, c_p2
        self._lib.double_max(nparray.ctypes.data_as(c_p1), length, npresult.ctypes.data_as(c_p2))
        print(npresult[0], max(nparray))
        print(nparray)

    def test_double_min(self, nparray, length):
        c_p1 = POINTER(c_double)
        c_p2 = POINTER(c_double)
        nparray = nparray.astype(np.double)
        npresult = np.array([0])
        npresult = npresult.astype(np.double)
        self._lib.restypes = None
        self._lib.argtypes = c_p1, c_int, c_p2
        self._lib.double_min(nparray.ctypes.data_as(c_p1), length, npresult.ctypes.data_as(c_p2))
        print(npresult[0], min(nparray))
        print(nparray)

    def test_averaging_array(self, array):
        length = len(array)
        self.draw_array(array, 1, length, "img1")
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        array = array.astype(np.int32)
        average_array = array.astype(np.int32)
        self._lib.restypes = None
        self._lib.argtypes = c_int, c_int, c_p1, c_p2
        self._lib.array_averaging(10, 378, array.ctypes.data_as(c_p1), average_array.ctypes.data_as(c_p2))
        self.draw_array(average_array, 1, length,  "img2")

    def test_create_array_square_deviation(self, array):
        length = len(array)
        self.draw_array(array, "img1")
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        array = array.astype(np.int32)
        average_array = array.astype(np.int32)
        self._lib.restypes = None
        self._lib.argtypes = c_int, c_int, c_p1, c_p2
        self._lib.array_averaging(5, 378, array.ctypes.data_as(c_p1), average_array.ctypes.data_as(c_p2))
        c_p3 = POINTER(c_double)
        square_deviatios = array.astype(np.double)
        self._lib.restypes = None
        self._lib.argtypes = c_p2, c_int, c_p3
        self._lib.create_array_square_deviation(average_array.ctypes.data_as(c_p2), length, square_deviatios.ctypes.data_as(c_p3))
        m = max(square_deviatios)
        for i in range(length):
            square_deviatios[i] = square_deviatios[i] * 256 / m
        self.draw_array(square_deviatios, "sqr_dev")

    def test_rough_search_lows(self, array):
        length = len(array)
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        array = array.astype(np.int32)
        average_array = array.astype(np.int32)
        self._lib.restypes = None
        self._lib.argtypes = c_int, c_int, c_p1, c_p2
        self._lib.array_averaging(5, 378, array.ctypes.data_as(c_p1), average_array.ctypes.data_as(c_p2))
        c_p3 = POINTER(c_double)
        square_deviatios = array.astype(np.double)
        self._lib.restypes = None
        self._lib.argtypes = c_p2, c_int, c_p3
        self._lib.create_array_square_deviation(average_array.ctypes.data_as(c_p2), length,
                                                square_deviatios.ctypes.data_as(c_p3))
        rough_mins = array.astype(np.int32)
        amount_rough_mins = np.array([0])
        c_p4 = POINTER(c_int32)
        c_p5 = POINTER(c_int)
        self._lib.restypes = None
        self._lib.argtypes = c_p3, c_int, c_p4, c_p5
        self._lib.rough_search_lows(square_deviatios.ctypes.data_as(c_p3), length,
                                    rough_mins.ctypes.data_as(c_p4), amount_rough_mins.ctypes.data_as(c_p5))
        res_rough_mins = np.zeros(amount_rough_mins[0])
        res_rough_mins = res_rough_mins.astype(np.int)
        for i in range(amount_rough_mins[0]):
            res_rough_mins[i] = rough_mins[i]
        self.draw_vertical_lines(res_rough_mins, "/home/vladimir/PycharmProjects/search_minima/img2.png", "/home/vladimir/PycharmProjects/search_minima/vert.png")

    def test_accurate_search_extremes(self, array):
        length = len(array)
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        array = array.astype(np.int32)
        average_array = array.astype(np.int32)
        self._lib.restypes = None
        self._lib.argtypes = c_int, c_int, c_p1, c_p2
        self._lib.array_averaging(5, 378, array.ctypes.data_as(c_p1), average_array.ctypes.data_as(c_p2))
        c_p3 = POINTER(c_double)
        square_deviatios = array.astype(np.double)
        self._lib.restypes = None
        self._lib.argtypes = c_p2, c_int, c_p3
        self._lib.create_array_square_deviation(average_array.ctypes.data_as(c_p2), length,
                                                square_deviatios.ctypes.data_as(c_p3))
        rough_mins = array.astype(np.int32)
        amount_rough_mins = np.array([0])
        c_p4 = POINTER(c_int32)
        c_p5 = POINTER(c_int)
        self._lib.restypes = None
        self._lib.argtypes = c_p3, c_int, c_p4, c_p5
        self._lib.rough_search_lows(square_deviatios.ctypes.data_as(c_p3), length,
                                    rough_mins.ctypes.data_as(c_p4), amount_rough_mins.ctypes.data_as(c_p5))
        res_rough_mins = np.zeros(amount_rough_mins[0])
        res_rough_mins = res_rough_mins.astype(np.int)
        for i in range(amount_rough_mins[0]):
            res_rough_mins[i] = rough_mins[i]

        accurate_extrems = np.zeros(amount_rough_mins[0], dtype=np.int32)
        amount_extrems = np.array([0], dtype=np.int)
        amount_rough_mins = amount_rough_mins.astype(np.int)
        res_rough_mins = res_rough_mins.astype(np.int32)
        c_p6 = POINTER(c_int)
        c_p7 = POINTER(c_int)
        c_p8 = POINTER(c_int32)
        c_p9 = POINTER(c_int)
        self._lib.restypes = None
        self._lib.argtypes = c_p6, c_p7, c_p2, c_p8, c_p9
        self._lib.accurate_search_extremes(res_rough_mins.ctypes.data_as(c_p6), amount_rough_mins.ctypes.data_as(c_p7),
                                           average_array.ctypes.data_as(c_p2), accurate_extrems.ctypes.data_as(c_p8),
                                           amount_extrems.ctypes.data_as(c_p9))
        print(amount_rough_mins[0], type(amount_rough_mins[0]))
        print(res_rough_mins, type(res_rough_mins[0]))
        print(amount_extrems[0], type(amount_extrems[0]))
        print(accurate_extrems, type(accurate_extrems[0]))

    def trace(self, matrix):
        amount_lines = np.array([0])
        c_p1 = POINTER(c_int32)
        c_p2 = POINTER(c_int32)
        c_p3 = POINTER(c_int)
        self._lib.restypes = None
        self._lib.argtypes = c_p1, c_int, c_int, c_p2, c_p3
        self._lib.trace(self._matrix.ctypes.data_as(c_p1), self._height, self._width,
                        self._lines.ctypes.data_as(c_p2), amount_lines.ctypes.data_as(c_p3))
        self._amount_lines = amount_lines[0]
        print(amount_lines[0])
        print(self._lines)

    def get_lines(self):
        return self._lines

    def get_amount_lines(self):
        return self._amount_lines


s = "/home/vladimir/PycharmProjects/search_minima/pict.tif"
A = InterferogramModel()
A.set_image(s)
os.system('gcc -shared -o Tracer_Volosnikovc.so Tracer_Volosnikovc.c')
lib = CDLL('./Tracer_Volosnikovc.so')
x = Tracer_Vol(A.get_image_npmatrix(), lib)
matrix = A.get_image_npmatrix()
print(matrix)
file = open("/home/vladimir/PycharmProjects/search_minima/input_matrix.txt", "w")
for i in range(A.get_width()):
    for j in range(A.get_height()):
        file.write(str(matrix[j][i]) + '\n')
file.close()

for i in range(A.get_width()):
    print(matrix[:, i])



