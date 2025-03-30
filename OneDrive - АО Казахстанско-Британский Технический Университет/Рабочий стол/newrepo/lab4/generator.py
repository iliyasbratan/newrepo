def sqaure_numbers(upper_bound):
  upper_bound = max(1, upper_bound)

  it = 1
  while it <= upper_bound:
    yield it ** 2
    it += 1


def even_numbers(upper_bound):
  upper_bound = max(0, upper_bound)

  it = 0
  while it <= upper_bound:
    if it % 2 == 0:
      yield it
    it += 1


def magic_numbers(upper_bound):
  upper_bound = max(0, upper_bound)

  it = 0
  while it <= upper_bound:
    if it % 3 == 0 and it % 4 == 0:
      yield it
    it += 1


def range_square(lower_bound, upper_bound):
  upper_bound = max(lower_bound, upper_bound)

  it = lower_bound
  while it <= upper_bound:
    yield it ** 2
    it += 1


def decrease_numbers(upper_bound, lower_bound = 0):
  upper_bound = max(lower_bound, upper_bound)

  it = upper_bound
  while it >= lower_bound:
    yield it
    it -= 1


if __name__ == "__main__":
  print(*even_numbers(int(input())), sep=", ")
  # print(*magic_numbers(int(input())), sep=", ")
  # print(*range_square(*map(int, input().split())), sep=", ")
  print(*decrease_numbers(*map(int, input().split())), sep=", ")