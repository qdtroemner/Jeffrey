import re

alphabet = {
	"a": "ooo",
	"b": "aaaah",
	"c": "aaaha",
	"d": "aaahh",
	"e": "ooh",
	"f": "aahah",
	"g": "aahha",
	"h": "aahhh",
	"i": "oho",
	"j": "ahaah",
	"k": "ahaha",
	"l": "ahahh",
	"m": "ahhaa",
	"n": "ahhah",
	"o": "ohh",
	"p": "ahhhh",
	"q": "haaaa",
	"r": "haaah",
	"s": "haaha",
	"t": "haahh",
	"u": "oahh",
	"v": "hahah",
	"w": "hahha",
	"x": "hahhh",
	"y": "hhaaa",
	"z": "hhaah",
	" ": "eeee"
}

"""
def translateToMonkey(phrase):
	output = ''
	for letter in phrase.lower():
		if letter in alphabet.keys():
			output += alphabet[letter]
		# Added
		elif letter == " ":
			output += letter
		#else:
		#	output += letter

	return output

def translateToEnglish(phrase):
	output = ''
	monkeyPhrase = [phrase[i:i + 2] for i in range(0, len(phrase), 2)]
	for monkeyLetter in monkeyPhrase:
		print(monkeyLetter)
		if monkeyLetter in alphabet.values():
			output += list(alphabet.keys())[list(alphabet.values()).index(monkeyLetter)]
		else:
			output += monkeyLetter

	return output
"""

def translateToMonkey(phrase):
	output = ''
	for letter in phrase.lower():
		if letter in alphabet.keys():
			output += alphabet[letter] + ' '
		else:
			output += letter

	return output

def translateToEnglish(phrase):
	output = ''
	for monkeyLetter in phrase.split(' '):
		if monkeyLetter in alphabet.values():
			output += list(alphabet.keys())[list(alphabet.values()).index(monkeyLetter)]
		else:
			output += monkeyLetter

	return output

def emojify(phrase):
	output = ''
	for letter in list(phrase):
		if re.match('[a-zA-Z]', letter):
			output += f":regional_indicator_{letter.lower()}:"
		else:
			output += letter
	
	return output