def piglatinify(key, sentence):
    def strip_consonants(word):
        word_lower = word.lower()
        stripped = ""
        for i, c in enumerate(word_lower):
            if c in 'aeiou':
                stripped = word[i:]
                break
        return stripped

    addition = strip_consonants(key)

    def piglatin(word):
        stripped = strip_consonants(word)
        if len(stripped) > 0:
            return stripped + word[:len(word) - len(stripped)] + addition
        else:
            return word + "w" + addition

    words = sentence.split()
    piglatin_words = []
    for i, word in enumerate(words):
        if word[-1] in '.!?':
            piglatin_words.append(piglatin(word[:-1]) + word[-1])
        else:
            piglatin_words.append(piglatin(word))
    return " ".join(piglatin_words).capitalize()
