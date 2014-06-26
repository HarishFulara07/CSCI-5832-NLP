test1 = open('test1.txt', 'w')
with open('test.txt', 'r') as boom:
	for line in boom:
		 if len(line) > 1 or line != '\n':
			word, tag = line.rsplit()
			test1.write('%s\n'%word)
boom.close()
test1.close()