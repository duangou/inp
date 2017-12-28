import re
class ist:
	def __init__(self,str_search,str_insert = '',filename = 'fn'):
		self.str_insert = str_insert
		self.str_search = str_search
		self.filename = filename
		f = open(self.filename,'r')
		self.content = f.readlines()
		f.close()
	def getid(self):
		duplicate = 0
		for i,line in enumerate(self.content):
			if not line.startswith('**'):
				match = re.search(self.str_search,line[:-1])
				if not match == None:
					id0 = i
					duplicate += 1
		if duplicate == 1:
			return id0
		elif duplicate == 0:
			print 'Warning: \'' + self.str_search + '\' not found.\n'
			return '\''+ self.str_search + '\' not found.\n'
		else:
			return str(duplicate) + ' \'' +self.str_search + '\' was found.\n'
	def insertf(self,offset = 0):
		id0 = self.getid()
		if type(id0) == int:
			if not self.str_insert.endswith(self.content[id0 - 1 + offset]) or self.content[id0 - 1 + offset] == '':
				self.content.insert(id0 + offset,self.str_insert)
				f = open(self.filename,'w')
				for line in self.content:
					f.write(line)
				f.close()
			else:
				print 'Warning: '+'\''+ self.str_insert +'\' may be present, writing operation cancelled.\n'	
	def insertb(self,offset = 0):
		id0 = self.getid()
		if type(id0) == int:
			if not self.str_insert.startswith(self.content[id0 + 1 + offset]) or self.content[id0 + 1 + offset] == '':
				self.content.insert(id0 + 1 +offset,self.str_insert)
				f = open(self.filename,'w')
				for line in self.content:
					f.write(line)
				f.close()
			else:
				print 'Warning: '+'\''+ self.str_insert + '\' may be present, writing operation cancelled.\n'
			
