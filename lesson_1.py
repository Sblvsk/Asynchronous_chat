import subprocess

# задание 1

word_1 = 'разработка'
word_2 = 'сокет'
word_3 = 'декоратор'

print(type(word_1), word_1)
print(type(word_2), word_2)
print(type(word_3), word_3)

unicode_word1 = word_1.encode('unicode_escape').decode()
unicode_word2 = word_2.encode('unicode_escape').decode()
unicode_word3 = word_3.encode('unicode_escape').decode()

print(type(unicode_word1), unicode_word1)
print(type(unicode_word2), unicode_word2)
print(type(unicode_word3), unicode_word3)


# задание 2
print()

word_1 = b'class'
word_2 = b'function'
word_3 = b'method'

print(type(word_1), word_1, len(word_1))
print(type(word_2), word_2, len(word_2))
print(type(word_3), word_3, len(word_3))


# задание 3
# Слова "класс" и "функция" невозможно записать в байтовом типе,
# так как они содержат символы, не поддерживаемые в ASCII-кодировке.


# задание 4
print()

word_1 = 'разработка'
word_2 = 'администрирование'
word_3 = 'protocol'
word_4 = 'standard'

byte_word_1 = word_1.encode()
byte_word_2 = word_2.encode()
byte_word_3 = word_3.encode()
byte_word_4 = word_4.encode()

print(type(byte_word_1), byte_word_1)
print(type(byte_word_2), byte_word_2)
print(type(byte_word_3), byte_word_3)
print(type(byte_word_4), byte_word_4)

decoded_word_1 = byte_word_1.decode()
decoded_word_2 = byte_word_2.decode()
decoded_word_3 = byte_word_3.decode()
decoded_word_4 = byte_word_4.decode()

print(type(decoded_word_1), decoded_word_1)
print(type(decoded_word_2), decoded_word_2)
print(type(decoded_word_3), decoded_word_3)
print(type(decoded_word_4), decoded_word_4)


# задание 5
print()

import subprocess

response_yandex = subprocess.Popen(['ping', 'yandex.ru'], stdout=subprocess.PIPE)
response_youtube = subprocess.Popen(['ping', 'youtube.com'], stdout=subprocess.PIPE)

for line in response_yandex.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))


for line in response_youtube.stdout:
    line = line.decode('cp866').encode('utf-8')
    print(line.decode('utf-8'))


# задание 6
print()


with open('test_file.txt', 'rb') as f:
    content = f.read()
    print(content)

with open('test_file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)