import json
from collections import Counter

import matplotlib.pyplot as plt


def generate_common_word(letters):
    with open('common_words.txt', 'r') as f:
        myWords = f.readlines()
    for word in myWords:
        word = word[:2]
    return letters


def generate_sorted_word():
    with open('word_freq_map.json') as freq_map:
        data = json.load(freq_map)
    sorted_dict = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_dict)


def generate_sorted_letter():
    with open('letter_freq_map.json') as freq_map:
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


def adjust_yellow_letters_at(yellow_dicts, word_dict):
    bad_word = []
    for word in word_dict:
        for yellow_dict in yellow_dicts:
            i = 0
            while i < 5:
                if yellow_dict[i] is not None and yellow_dict[i] is word[i]:
                    bad_word.append(word)
                i += 1
    for word in bad_word:
        word_dict.pop(word, None)
    return word_dict


def adjust(word_dict, black, yellow, green, yellow_at):
    return adjust_green_letters(green, adjust_yellow_letters(yellow, adjust_black_letters(black,
                                                                                          adjust_yellow_letters_at(
                                                                                              yellow_at, word_dict))))


def adjust_data(word_dict):
    word_sum = 0
    for word in word_dict:
        word_sum += word_dict[word]
    for word in word_dict:
        word_dict[word] = (word_dict[word] / word_sum) * 100
    return word_dict


def visualize_words(word_dict):
    word_dict = dict(Counter(word_dict).most_common(5))
    plt.bar(*zip(*word_dict.items()))
    plt.title('Viability of Answers by Word Commonality')
    plt.xlabel('Top 5 Words')
    plt.ylabel('Percentage of Viability')
    plt.show()


def visualize_letters(word_dict):
    word_dict = dict(Counter(word_dict).most_common(5))
    plt.bar(*zip(*word_dict.items()))
    plt.title('Viability of Answers by Letter Commonality')
    plt.xlabel('Top 5 Words')
    plt.ylabel('Percentage of Viability')
    plt.show()


def visualize_word_letters(word_dict):
    word_dict = dict(Counter(word_dict).most_common(5))
    plt.bar(*zip(*word_dict.items()))
    plt.title('Viability of Answers by Letter/Word Commonality')
    plt.xlabel('Top 5 Words')
    plt.ylabel('Percentage of Viability')
    plt.show()


def generate_word_letters(words, letters):
    words_letters = {}

    for word in words:
        words_letters[word] = words[word] * letters[word]

    words_letters = adjust_data(words_letters)
    return words_letters


if __name__ == '__main__':
    black_letters = ""
    yellow_letters = ""
    yellow_letters_at = [{0: None, 1: None, 2: None, 3: None, 4: None},
                         {0: None, 1: None, 2: None, 3: None, 4: None},
                         {0: None, 1: None, 2: None, 3: None, 4: None},
                         {0: None, 1: None, 2: None, 3: None, 4: None},
                         {0: None, 1: None, 2: None, 3: None, 4: None},
                         {0: None, 1: None, 2: None, 3: None, 4: None}]
    green_letters = {0: None, 1: None, 2: None, 3: None, 4: None}

    words = adjust_data(adjust(generate_sorted_word(), black_letters, yellow_letters, green_letters, yellow_letters_at))
    letters = adjust_data(
        adjust(generate_sorted_letter(), black_letters, yellow_letters, green_letters, yellow_letters_at))
    word_letters = generate_word_letters(words, letters)

    # visualize_words(words)
    visualize_letters(generate_common_word(letters))
    visualize_word_letters(word_letters)
