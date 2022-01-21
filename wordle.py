# # Need to run the following for the first time only
# import nltk
# nltk.download('words')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.corpus import words
from nltk.corpus import wordnet as wn
import re

"""
User can set specific settings to reduce amount of values
"""
default_settings = {
	'contains_letters': 'orp',
	'does_not_contain_letters': 'audistewl',
	'limit_to_5': True,
	'exclude_specific_string': ['iii', 'igigi', '_', '-'],
	# In the format ('letter', location starting with 0) i.e. for 'price' it would be [('p', 0), ('i', 2), ('e', 4)] 
	'letters_in_specific_locations': [('o', 2), ('r', 1), ('p', 0)],
	'letters_not_in_specific_locations': [('o', 4), ('r', 2), ('p', 4)],
	'debug': False,
}

def get_words_with_setting(settings: dict) -> list:
	# Get all words from both NLTK corposes
	wordnet_words = [word.lower() for word in wn.all_lemma_names() if len(word) == 5] if settings.get('limit_to_5', True) else [word.lower() for word in wn.all_lemma_names() if len(word) <= 5]
	words_words = [word.lower() for word in words.words() if len(word) == 5] if settings.get('limit_to_5', True) else [word.lower() for word in words.words() if len(word) <= 5]
	all_words = list(set(wordnet_words + words_words))
	reduced_word_list = all_words

	# Display debug stats
	debug = settings.get('debug', False)
	if debug:
		print(f'{len(wordnet_words)} words from nltk.wordnet.')
		print(f'{len(words_words)} words from nltk.words.')
		print(f'{len(all_words)} words to start.')

	# Reduce by any specifically known letters
	for specific_letter_location in settings.get('letters_in_specific_locations', []):
		reduced_word_list = [word for word in reduced_word_list if word[specific_letter_location[1]] == specific_letter_location[0]]
		if debug:
			print(f"{len(reduced_word_list)} words after finding letter {specific_letter_location[0]} at position {specific_letter_location[1]}.")

	# Reduce by any specifically excluded letter positions
	for specific_letter_location in settings.get('letters_not_in_specific_locations', []):
		reduced_word_list = [word for word in reduced_word_list if word[specific_letter_location[1]] != specific_letter_location[0]]
		if debug:
			print(f"{len(reduced_word_list)} words after not finding letter {specific_letter_location[0]} at position {specific_letter_location[1]}.")

	# Only include words that contain certain letters
	contains_letters = settings.get('contains_letters', '')
	if contains_letters != '':
		for letter in contains_letters:
			reduced_word_list = [word for word in reduced_word_list if len(re.findall(f'[{letter}]', word)) > 0]
			if debug:
				print(f"{len(reduced_word_list)} words after contains {contains_letters}.")

	# Only include words that don't include certain letters
	does_not_contain_letters = settings.get('does_not_contain_letters', '')
	if does_not_contain_letters != '':
		reduced_word_list = [word for word in reduced_word_list if len(re.findall(f'[{does_not_contain_letters}]', word)) == 0]
		if debug:
			print(f"{len(reduced_word_list)} words after does not contain {does_not_contain_letters}.")

	# Remove words that will never actually be used
	for exclude_string in settings.get('exclude_specific_string', []):
		reduced_word_list = [word for word in reduced_word_list if word.find(exclude_string, 0) < 0]
		if debug:
			print(f"{len(reduced_word_list)} words after excluding {exclude_string}.")

	# Return possible values to user
	if debug:
		print("Solutions include...")
	return reduced_word_list

print(get_words_with_setting(default_settings))
