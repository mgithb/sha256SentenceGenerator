import hashlib
import random
import string

def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def number_to_word(num):
    words = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        'a': 'a',
        'b': 'b',
        'c': 'c',
        'd': 'd',
        'e': 'e',
        'f': 'f',
    }
    return words[num]

def generate_sentence_with_hash_prefix(prefix_length=7):
    while True:
        sentence = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        hashed = sha256(sentence)
        if hashed[:prefix_length] == prefix_length * "0":
            words = ', '.join([number_to_word(char) for char in hashed[:prefix_length-1]]) + ' and ' + number_to_word(hashed[prefix_length-1])
            return f'The SHA256 for the sentence "{sentence}" begins with: {words}.'

length = int(input("Enter the length of the hash prefix you want in the resulting sentence (1-64): "))
print(generate_sentence_with_hash_prefix(length))
