from PIL import Image, ImageDraw
import numpy as np
from abc import ABC, abstractmethod


def draw_extrem(image, array_lines):
    length = len(array_lines)
    draw = ImageDraw.Draw(image, "RGB")
    for i in range(length):
        draw.line(array_lines[i], (0, 0, 0), 1)
    del draw
    image.save("/home/vladimir/test2.png", "PNG")

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
        return self.__NpImage

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


class TracerVolosnikov:
    def __init__(self, num):
        self.__matrix = num             #NumPy matrix
        self.__length = num.shape[0]
        self.__width = num.shape[1]

    def search_minimal_period(self, array):
        length = len(array)
        Max = max(array)
        Min = min(array)
        y1 = int (Min + (Max - Min) / 5)
        y2 = int (Max - (Max - Min) / 5)
        average_amount = 0
        for y in range(y1, y2):
            amount_intersections = 0
            for j in range(1, length):
                if ((array[j - 1] <= y and y < array[j]) or (array[j - 1] >= y and y > array[j])):
                    amount_intersections += 1
            average_amount += amount_intersections

        average_amount = average_amount / (y2 - y1)
        period = length * 2 / average_amount
        return int (period)

    def calculation_interval(self, x, l, array, parameter):
        length = l
        if parameter == 0:
            amount_points = self.search_minimal_period(array)
        else:
            amount_points = parameter
        if x < amount_points:
            return range(x + amount_points)
        elif x >= length - amount_points:
            return range(x - amount_points, length)
        else:
            return range(x - amount_points, x + amount_points)

    def array_averaging(self, averaging_parameter, array):
        result_array = []
        interval = []
        for i in range(self.__length):
            interval = self.calculation_interval(i, self.__length, array, averaging_parameter)
            sum = 0
            for j in interval:
                sum += array[j]
            result_array.append(int (sum / (2 * averaging_parameter + 1)))
        return result_array

    def create_array_square_deviation(self, array):
        result_array = []
        for i in range(self.__length):
            interval = self.calculation_interval(i, self.__length, array, 0)
            sum1 = 0
            sum2 = 0
            sum3 = 0
            for j in interval:
                sum1 += (array[j] - array[i]) ** 2
                sum2 += (array[j] - array[i]) * ((j - i) ** 2)
                sum3 += (j - i) ** 4
            res = sum1 - (sum2 ** 2) / sum3
            result_array.append(res)
        return result_array

    def search_minima(self, array):
        intermediate_array = []
        result_array = []
        for i in range(self.__length):
            interval = self.calculation_interval(i, self.__length, array, 0)
            start = interval[0]
            finish = interval[len(interval) - 1]
            intermediate_array.append(min(array[start : finish]))
        j = 0
        while j < self.__length - 1:
            if (j < self.__length - 1 and intermediate_array[j] == intermediate_array[j + 1]):
                t = 0
                while (j < self.__length - 1 and intermediate_array[j] == intermediate_array[j + 1]):
                    j += 1
                    t += 1
                res = j - int(t / 2)
                result_array.append(res)
            else:
                j += 1
        return result_array

    def second_search_extrem(self, x_array, y_array):
        j = 1
        while j < len(x_array) - 1:
            if ((y_array[x_array[j - 1]] < y_array[x_array[j]] and y_array[x_array[j]] < y_array[x_array[j + 1]]) or
                    (y_array[x_array[j - 1]] > y_array[x_array[j]] and y_array[x_array[j]] > y_array[x_array[j + 1]])):
                del x_array[j]
            j += 1
        return x_array

    def create_array_all_extrem(self, averaging_parameter):
        array_all_extrem = []
        for i in range(self.__width):
            average_array = self.array_averaging(averaging_parameter, self.__matrix[:, i, 1])
            square_deviation = self.create_array_square_deviation(average_array)
            first_array_minima = self.search_minima(square_deviation)
            final_array_minima = self.second_search_extrem(first_array_minima, self.__matrix[:, i, 1])
            array_all_extrem.append(final_array_minima)
        return(array_all_extrem)

    def create_lines(self, parameter):
        array_all_extrem = self.create_array_all_extrem(parameter)
        intermediate_array = []
        for i in range(self.__width):
            intermediate_array.append(len(array_all_extrem[i]))
        amount_lines = min(intermediate_array)
        array_lines = []
        for j in range(amount_lines):
            one_line = []
            for k in range(self.__width):
                one_line.append((k, array_all_extrem[k, j]))
            array_lines.append(one_line)
        return array_lines




s = "/home/vladimir/pict.tif"
A = InterferogramModel()
A.set_image(s)
tr = TracerVolosnikov(A.get_image_npmatrix())

print(len(a))
image1 = Image.open(s)
draw1 = ImageDraw.Draw(image1)
for i in range(len(a)):
    draw1.line(a[i], (255, 255, 255), 1)
del draw1
image1.save("/home/vladimir/test1.png", "PNG")
