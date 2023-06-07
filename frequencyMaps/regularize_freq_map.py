import json

def regularize_freq_map(filename):
    with open(filename, 'r') as f:
        freq_map = json.load(f)

    # Regularize by dividing each frequency by the total sum
    total = sum(freq_map.values())
    regularized_freq_map = {key: value / total for key, value in freq_map.items()}

    return regularized_freq_map

def write_to_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    word_freq_map = regularize_freq_map('../frequencyMaps/word_freq_map.json')
    write_to_json('../frequencyMaps/regularized_word_freq_map.json', word_freq_map)

    letter_freq_map = regularize_freq_map('../frequencyMaps/letter_freq_map.json')
    write_to_json('../frequencyMaps/regularized_letter_freq_map.json', letter_freq_map)
