import re
def clearopen(filename):
	f = open(filename,'r')
	content = []
	for line in f.readlines():
		if not line.startswith('**') and re.match('\s*\n$',line) == None:
			content.append(line)
	f.close()
	return content

def getid(str_search,lst):
	duplicate = 0
	for i,line in enumerate(lst):
		if not line.startswith('**'):
			match = re.search(str_search,line[:-1],2)
			if not match == None:
				duplicate += 1
				if duplicate == 1: 
					id0 = i
	if duplicate == 1:
		return id0
	elif duplicate == 0:
		print 'Warning: \'' + str_search + '\' not found.\n'
		return '\''+ str_search + '\' not found.\n'
	else:
		print 'Warning: \'' + str(duplicate) + str_search + '\' was found.\n'
		return id0

def getsection(str_mark,lst):
	id_start = getid(str_mark,lst)
	id_end = len(lst)
	for i,line in enumerate(lst[id_start+1:]):
		if re.search('^\*[A-Z]',line[:-1]):
			id_end = i + id_start + 1
			break
	return lst[id_start:id_end]

def insertlist(id0,content,lst):
	str1 = ''
	if type(content) == list:
		for line in content:
			str1 += line
	if type(lst) == str:
		str1 = content
	return lst.insert(id0,str1)

def replacesection(str_mark,content,lst):
	id_start = getid(str_mark,lst)
	id_end = len(lst)
	for i,line in enumerate(lst[id_start+1:]):
		if re.search('^\*[A-Z]',line[:-1]):
			id_end = i + id_start + 1
			break
	del lst[id_start:id_end]
	insertlist(id_start,content,lst)
	return lst

def writelist(lst,filename):
	f = open(filename,'w+')
	for line in lst:
		f.write(line)
	f.close()

def recombine(lst):
	str1 = ''
	for line in lst:
		str1 += line
	lst1 = str1.strip('\n').split('\n')
	lst1 = [line + '\n' for line in lst1]
	return lst1

def renumbernodedict(lst):
	lst1 = recombine(lst)
	nodelist = getsection('^\*NODE',lst1)
	renumdict = {int(line.split(',')[0]):i+1 for i,line in enumerate(nodelist[1:])}
	return renumdict

def getframe(lst):
	frame = []
	for line in lst:
		if re.match('^\*[A-Za-z]',line):
			frame.append(line)
	return frame

def rotateground(lst,axis = 1): #1:x;2:y;3:z
	groundsection = getsection('^\*ELEMENT.+rigid_ground',lst)[1:]
	elementset = set()
	for line in groundsection:
		for i in line[:-1].split(',')[1:]:
			elementset.add(int(i))
	nodelist = getsection('^\*NODE',lst)[1:]
	nodes = []
	for line in nodelist:
		nodes.append(map(eval,line[:-1].split(',')))
	groundrotated = []
	id1 = getid('^\*NODE',lst)
	groundrotated.append(lst[id1])
	for node in nodes:
		if node[0] in elementset:
			if axis == 3:
				x = node[1]
				y = node[2]
				node[1] = -y
				node[2] = x
			elif axis == 2:
				x = node[1]
				z = node[3]
				node[1] = -z
				node[3] = x
			elif axis == 1:
				y = node[2]
				z = node[3]
				node[2] = -z
				node[3] = y
		groundrotated.append(str(node[0])  +',' + str(node[1]) + ',' + str(node[2]) + ',' + str(node[3]) + '\n')
	return replacesection('^\*NODE',groundrotated,lst)

def moveground(lst,x = 0, y = 0, z = 0):
	groundsection = getsection('^\*ELEMENT.+rigid_ground',lst)[1:]
	elementset = set()
	for line in groundsection:
		for i in line[:-1].split(',')[1:]:
			elementset.add(int(i))
	nodelist = getsection('^\*NODE',lst)[1:]
	nodes = []
	for line in nodelist:
		nodes.append(map(eval,line[:-1].split(',')))
	groundmoved = []
	id1 = getid('^\*NODE',lst)
	groundmoved.append(lst[id1])
	for node in nodes:
		if node[0] in elementset:
			node[1] = node[1] + x
			node[2] = node[2] + y
			node[3] = node[3] + z
		groundmoved.append(str(node[0])  +',' + str(node[1]) + ',' + str(node[2]) + ',' + str(node[3]) + '\n')
	return replacesection('^\*NODE',groundmoved,lst)

def getedgepoint(lst,section = '^\*cover'):
	targetsection = getsection(section,lst)[1:]

#Creat set for nodes number in targetsection 
	elementset = set()
	for line in targetsection:
		for i in line[:-1].split(',')[1:]:
			elementset.add(int(i))

#All nodes in the inp file are included in (list)nodes
	nodelist = getsection('^\*NODE',lst)[1:]
	nodes = []
	for line in nodelist:
		nodes.append(map(eval,line[:-1].split(',')))

#edgepoint initial:[x+,x-,y+,y-,z+,z-]
	edgepoint = [nodes[0][1],nodes[0][1],nodes[0][2],nodes[0][2],nodes[0][3],nodes[0][3]]

	for node in nodes:
		if node[0] in elementset:
			if node[1] > edgepoint[0]:edgepoint[0] = node[1]
			if node[1] < edgepoint[1]:edgepoint[1] = node[1]
			if node[2] > edgepoint[2]:edgepoint[2] = node[2]
			if node[2] < edgepoint[3]:edgepoint[3] = node[2]
			if node[3] > edgepoint[4]:edgepoint[4] = node[3]
			if node[3] < edgepoint[5]:edgepoint[5] = node[3]
	return edgepoint
