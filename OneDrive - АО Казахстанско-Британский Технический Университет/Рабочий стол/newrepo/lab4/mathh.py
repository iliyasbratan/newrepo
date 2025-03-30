import math

def convert_to_rad(degree):
  return degree / 180 * math.pi


def calc_trapezoid_area(height, base1, base2):
  return height * (base1 + base2) / 2;


def calc_reg_polython_area(sides, side_len):
  apophem =  side_len / (2 * math.tan(convert_to_rad(180 / sides)))
  return round(sides * side_len * apophem / 2, 5)


def calc_parallelogram_area(base, height):
  return base * height;


print(calc_trapezoid_area(5, 5, 6))
print(calc_reg_polython_area(4, 25))
print(calc_parallelogram_area(5, 6))