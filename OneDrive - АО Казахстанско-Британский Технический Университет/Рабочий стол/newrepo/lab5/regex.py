import re

pattern1 = r"ab*"

pattern2 = r"ab{2,3}"

pattern3 = r"\b[a-z]+(?:_+[a-z]+)*\b"

pattern4 = r"\b[A-Z][a-z]*\b"

pattern5 = r"a.+b"

pattern6 = r"( |,|\.)"
def task6(text):
  return re.sub(pattern6, ";", text)


pattern7 = r"[a-z]_[a-zA-Z]"
def task7(text):
  return re.sub(
    pattern7,
    lambda match: match.group(0)[0] + match.group(0)[2].upper(),
    text
  )


pattern8 = r"[A-Z]"
def task8(text):
  return re.sub(
    pattern8,
    lambda match: (" " if match.start() > 0 else "") + (match.group(0)[0]) + (" " if match.end() < len(text) else ""),
    text
  )
  return re.split(
    pattern8,
    text
  )


pattern9 = r"[A-Za-z][A-Z]"
def task9(text):
  return re.sub(
    pattern9,
    lambda match: " ".join(match.group(0)),
    text
  )


pattern10 = r"[A-Za-z][A-Z]"
def task10(text):
  return re.sub(
    pattern10,
    lambda match: match.group(0)[0] + "_" + match.group(0)[1].lower(),
    text
  )


print(re.findall(pattern1, "asdbbbabbabbbbababbbba"))

print(re.findall(pattern2, "asdbbbabbabbbbababbbba"))

print(re.findall(pattern3, " today i_have a worn_der_ful_ _day ah__yes"))

print(re.findall(pattern4, " I believe we Are going to visit Astana with IoT Infrastracture"))

print(re.findall(pattern5, " I believe we are going to visit Astana with IoT Infrastracture but we have some troubles"))

print(task6(" Hello, world. This is a Python program to replace spaces, commas, and dots. "))

print(re.findall(pattern7, "I HaveThis Camel_But Snake_case char_s_, sO gooD DDamn"))

print(task7("  I HaveThiS Camel_But Snake_case char_s_, sO gooD DDamn_ "))

print(task8("USA IS Possibly worSeR than KazaKhstaNN"))

print(task9("CaptialWords Meant I hope Like This: ThisIsAnExampleOfCamelCaseButAlsoCapitalWords :)"))

print(task10("  I HaveThiS Camel_But Snake_case char_s_, sO gooD DDamn_. iLoveRegExGenuinely! "))