import json
import operator
import matplotlib.pyplot as plt
from collections import Counter


def generate_sorted_dict():
    with open('freq_map.json') as freq_map:
        data = json.load(freq_map)
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_dict)


def adjust_black_letters(letters, word_dict):
    bad_word = []
    for word in word_dict:
        for letter in letters:
            if letter in word:
                bad_word.append(word)
    for word in bad_word:
        word_dict.pop(word, None)
    return word_dict


def adjust_yellow_letters(letters, word_dict):
    bad_word = []
    for word in word_dict:
        for letter in letters:
            if letter not in word:
                bad_word.append(word)
    for word in bad_word:
        word_dict.pop(word, None)
    return word_dict


def adjust_green_letters(green_dict, word_dict):
    bad_word = []
    for word in word_dict:
        i = 0
        while i < 5:
            if green_dict[i] is not None and green_dict[i] is not word[i]:
                bad_word.append(word)
            i += 1
    for word in bad_word:
        word_dict.pop(word, None)
    return word_dict


def adjust(word_dict, black, yellow, green):
    return adjust_green_letters(green, adjust_yellow_letters(yellow, adjust_black_letters(black, word_dict)))


def visualize(word_dict):
    word_dict = dict(Counter(word_dict).most_common(5))
    plt.bar(*zip(*word_dict.items()))
    plt.show()


if __name__ == '__main__':
    sorted_word_dict = generate_sorted_dict()
    black_letters = []
    yellow_letters = []
    green_letters = {0: None, 1: None, 2: None, 3: None, 4: None}
    final_word_list = adjust(sorted_word_dict, black_letters, yellow_letters, green_letters)
    visualize(final_word_list)
