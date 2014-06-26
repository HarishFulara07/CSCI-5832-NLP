testt = open('testt.txt', 'w')
with open('test.txt') as test:
	for line in test:
		if line!= "\n":
			testt.write(line)
