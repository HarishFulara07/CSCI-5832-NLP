#! /usr/bin/env/python
# Darya Tarasova
# LING/CSCI 5832
def hmm(train, test):
	corpussize = len(train)
	tag_set = set()
	seen = set()
	tagf = {}
	bigram = {}
	wordtag = {}
	wordfreqs = {}
	wordfreqs['UNK'] = 0
	for i in range(corpussize-1):
		if train[i][1] not in wordfreqs:
			wordfreqs[train[i][1]] = 1
		else:
			wordfreqs[train[i][1]] +=1
	for i in range(corpussize-1):

		# write down all the tags
		if train[i][0] not in seen:
			tag_set.add(train[i][0])
			seen.add(train[i][0])

		# Replace words that only occur once with UNK
		if wordfreqs[train[i][1]] < 2 :
			train[i][1] = 'UNK'
			wordfreqs[train[i][1]] +=1

		#tag frequency
		if train[i][0] not in tagf:
			tagf[train[i][0]] = 1
		else:
			tagf[train[i][0]] += 1

		# tag bigram
		if i != 0:
			if (train[i][0], train[i+1][0]) not in bigram:
				bigram[(train[i][0], train[i+1][0])] = 1
			else:
				bigram[(train[i][0], train[i+1][0])] += 1 

		# word-tag
		if tuple(train[i]) not in wordtag:
			wordtag[tuple(train[i])] = 1
		else:
			wordtag[tuple(train[i])] += 1
	wordfreqs2 = dict((k,v) for k, v in wordfreqs.iteritems() if v>1)

	def transition_probs():
		trans = {}
		trans2 = {}
		#transition probability for things that exist
		for line in bigram:
			if line not in trans:
				# The easiest smoothing method ever - add .0000001 to everything, Should have probably done log(something) for this because
				# underflow is scary but... D: 
				trans[line] = float(.0000001 + float(bigram[line]))/(.0000001  + float(tagf[line[1]])/float(corpussize))
		#transition probability for things that don't exist
		for tag_a in tag_set:
			for tag_b in tag_set:
					if (tag_a, tag_b) not in trans:
						trans[(tag_a, tag_b)] = .0000001/((.0000001  + float(tagf[tag_a])/float(corpussize)))
		return trans
	
	def emission_probs():
		emit = {}
		#emission probability for things that exist
		for line in train:
			if tuple(line) not in emit:
				emit[tuple(line)] = float(.000001 + (float(wordtag[tuple(line)]))/(float(.000001  + (float(wordfreqs2[line[1]])))))
		#emission probability for things that don't exist
		for tag in tag_set:
			for line in train:
				if (tag, line[1]) not in emit:
						emit[(tag, line[1])] = .000001/(.000001 + (float(wordfreqs2[line[1]])/float(len(wordfreqs2))))
		return emit		
		# 
	trans = transition_probs()
	emit = emission_probs()
	fin = []
	#start viterbi
	unique = []
	for i in range(len(test) - 2):
		obs = test[i][0]
		this_word = obs
		temp = {}
		if this_word not in wordfreqs2:
			unique.append(this_word)
			this_word = 'UNK'
		for tag in tag_set:
			if (tag, this_word) in emit:
				emission = emit[(tag, this_word)]
			if (this_word == ".") or (i == 0):	
				transition = 1
				bp_prob = 1
			else:
				bp_tag = fin[i-1][0]
				transition = trans[(bp_tag, tag)]
				bp_prob = fin[i-1][2]
			temp[tag] = emission * transition * bp_prob
		fin_prob = max(temp.values())
		fin_tag = ''
		
		#find the tag with the highest probability
		for tag in temp.keys():
			if temp[tag] == fin_prob:
				fin_tag = tag
				break
		fin.append([fin_tag, obs, fin_prob])
	print_results(fin)	
# Prints to file
def print_results(data):

	with open('result.txt', 'w') as done:
		for line in data:
			done.write(line[1] + '\t' + line[0] + '\n')
	done.close()

# baseline method - if word is in the training data - assign highest frequency tag, if not
# NNP
def baseline(train, test):
	tag = []
	wordtag2 = {}
	fin2 = []

	for i in range(len(train)-2):
		if train[i][1] not in wordtag2:
			wordtag2[train[i][1]] = {}
			wordtag2[train[i][1]][train[i][0]] = 1
		elif train[i][0] not in wordtag2[train[i][1]]:
			wordtag2[train[i][1]][train[i][0]] = 1
		else:
			wordtag2[train[i][1]][train[i][0]] +=1
	for i in range(len(test)):
		fintag = ''
		if test[i][0] in wordtag2:
			maximum = max(wordtag2[test[i][0]].values())
			for tag, n in wordtag2[test[i][0]].iteritems():
				if n == maximum:
					fintag = tag
				else:
					fintag = 'NNP'
				# tag[i] = 'NNP'
		fin2.append([fintag, test[i][0]])
	print_results(fin2)

				 


train = []
test = []
train_data = open('berp-POS-train.txt', 'r').read().splitlines()
test_data = open('berp-POS-test-sentences.txt', 'r').read().splitlines()
for line in train_data:
	if line:
		d = line.split()
		# I confused myself with the dictionary notation in python since it's my first time using python and
		# I reversed everything to make it more sense to me but really it just makes it a lot slower. :(
		# Sorry!
		d.reverse()
		train.append(d)
for line in test_data:
	if line:
		d = line.split()
		test.append(d)
hmm(train, test)