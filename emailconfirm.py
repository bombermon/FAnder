from validate_email import validate_email
is_valid = validate_email('example@edu.fa.ru')


import re
pattern = re.compile(r'[1-2]{1}[0-9]{5}@edu.fa.ru')
test = input()
result = re.match(pattern, test)
print(result)