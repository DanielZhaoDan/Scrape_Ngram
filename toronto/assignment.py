def count_words(string, dictionary):
    words = str(string).split(' ')
    punctuations = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',]
    for word in words:
        try:
            word = str(word.lower())
            if word not in punctuations and not word.startswith('#') and not word.startswith('@'):
                count = dictionary.get(word, 0) + 1
                dictionary[word] = count

def common_words(dictionary, number):
    sorted_asc = sorted(dictionary.items(), key=lambda x: x[1])
    sorted_desc = dd.reverse()

