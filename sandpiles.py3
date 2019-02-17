#python 3.7.1
import sys

class level:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.cells = [x%5 for x in range(width*height)]
	def index(self, x, y):
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return None
		return x+(y*self.width)
	def neighbors(self, x, y):
		up = self.index(x,y-1)
		down = self.index(x,y+1)
		left = self.index(x-1,y)
		right = self.index(x+1,y)
		return [up,down,left,right]
	def tick(self):
		for i in range(len(self.cells)):
			if self.cells[i] > 3:
				self.topple(i%self.width, i//self.width)
	def topple(self,x,y):
		cell = self.index(x,y)
		pileHeight = self.cells[cell]
		grainsMoving = pileHeight//4
		self.cells[cell] = pileHeight%4
		for neighbor in self.neighbors(x,y):
			if neighbor:
				self.cells[neighbor] += grainsMoving
	def display(self):
		for y in range(self.height):
			row = self.cells[y*self.width:(y+1)*self.width]
			sys.stdout.write(str(row)+"\n")

#x=level(4,4)
#x.display()
#print("\n")
#x.tick()
#x.display()