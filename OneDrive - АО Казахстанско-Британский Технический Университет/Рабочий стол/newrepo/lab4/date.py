import datetime


def subtract_date(date = datetime.datetime.now(), days=5):  # takes now instance
  return date - datetime.timedelta(days=days)


def print_sibling_days(date = datetime.datetime.now()):
  print("Yesterday:", (date - datetime.timedelta(days=1)).strftime("%A, %d %B %Y, %H:%M:%S"))
  print("Today:", date.strftime("%A, %d %B %Y, %H:%M:%S"))
  print("Tomorrow:", (date + datetime.timedelta(days=1)).strftime("%A, %d %B %Y, %H:%M:%S"))


def drop_ms(date):
  return date.replace(microsecond=0)


def seconds_diff(date1, date2):
  return round((abs(date1 - date2)).total_seconds())


if __name__ == "__main__":
  now = datetime.datetime.now()
  print(now)
  print(subtract_date(now))

  print_sibling_days(now)

  print(drop_ms(now))
  # print(second_diff(now, datetime.datetime.combine(datetime.date(2023, 1, 1), datetime.datetime.now().time())))
  # print(second_diff(now, datetime.datetime.combine(datetime.date(2025, 1, 22), datetime.datetime.now().time())))