file1 = 'file1.inp'
file2 = 'file2.inp'
f1 = open('.\\inputfiles\\' + file1,'r')
f1_content = f1.readlines()
f1.close()
f2 = open('.\\inputfiles\\' + file2,'r')
f2_content = f2.readlines()
f2.close()
f1minusf2 = list(set(f1_content).difference(set(f2_content)))
f2minusf1 = list(set(f2_content).difference(set(f1_content)))
f = open('.\inputfiles\cmp.txt','w+')
f.write(file1 + ' has '+ str(len(f1_content)) + ' lines.\n' + file2 + ' has ' + str(len(f2_content)) +' lines.\n\n\'' + file1 + '\' - \'' + file2 + '\':\n')
for line in f1minusf2:
	f.write(line)
f.write('\n------\n\n\'' + file2 + '\' - \'' + file1 + '\':\n')
for line in f2minusf1:
	f.write(line)
f.close()
