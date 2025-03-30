import re

pattern = r'\d*'
text1 = "Price: 5000 tg, Discount: 10%"
text2 = "The auditorium number is 726"
mathces = re.findall(pattern, text1)
print(mathces)
