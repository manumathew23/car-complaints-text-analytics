from text_analytics import known_words_list
learned_words = {}

def data_learner(words):
    for word in words:
        if word not in (known_words_list):
            learned_words.update({word: learned_words.get(word, 0) + 1})

def get_new_words_list():
	new_words_list = []
	for word in sorted(learned_words, key=learned_words.get, reverse=True):
		new_words_list.append([word, learned_words.get(word)])
	return new_words_list

		
