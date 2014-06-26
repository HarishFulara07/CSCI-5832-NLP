#! /usr/bin/env/python

a = open('testt.txt', 'r')
b = open ('result.txt', 'r')
countera = 0
counterb = 0
aarray = []
barray = []
alines = a.readlines()
blines = b.readlines()
for line in alines:
	line=line.strip('\n\t')
	if line:
		aarray.append(line)
for line in blines:
	line=line.strip('\n\t')
	if line:
		barray.append(line)
countero = 0
counterx = 0
wrong = []
wrong2 = []
for i in range(len(barray)):
	if aarray[i] == barray[i]:
		countero+=1

	else:
		wrong.append(aarray[i])
		wrong2.append(barray[i])
		counterx+=1

print 'Number right:', countero
print 'Number wrong:', counterx
print 'Wrong tags:'
print 'Test Data           ||    POS Tagger Data'


for j in range(counterx):
	print wrong[j], '\t', wrong2[j]
tot = float(counterx) + float(countero)
print 'Accuracy of the tagger:', (countero/tot)*100, '%'
