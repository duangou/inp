import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class seperate():
	def __init__(self,filename):
		self.f = open(filename,'r+')
		self.partstr = ''
	def part(self):
		readon = False
		for line in self.f:
			if line.startswith('*Part'):
				readon = True
			if readon == True:
				self.partstr += line
			if line.startswith('*End Part'):
				readon = False
				self.f.close()
				break
		if self.partstr != '':
			self.part = open('Part','w+')
			self.part.write(self.partstr)
			print 'Part.txt has been updated\n'
			self.part.close()
		else: print 'No part found in inp file\n'
class nodes():
	def __init__(self):
		self.f = open('Part','r')
		self.nodes = []
	def node(self):
		addon = False
		for line in self.f:
			if line.startswith('**'):
				continue
			if line.startswith('*Node'):
				addon = True
				continue
			if addon == True:
				if not line[0].isdigit():
					addon = False
					self.f.close()
					break
				self.nodes.append([])
				nodestr = line[:-1].split(',')
				for i in nodestr:
					self.nodes[-1].append(float(i))
		return self.nodes
	def figure(self):
		self.node()
		x = []
		y = []
		z = []
		for i in self.nodes:
			x.append(i[1])
			y.append(i[2])
			z.append(i[3])
		ax = plt.subplot(111,projection='3d')
		ax.scatter(x,y,z)
		plt.show()
		ax.scatter(self.nodes[:])
