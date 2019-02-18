import sys
import string

class level:
	def __init__(self,width,height,depth):
		self.width = width
		self.height = height
		self.depth = depth
		self.layers = [layer(width,height) for _ in range(depth)]
	
	def tick(self):
		for layer in self.layers:
			layer.tick()
	
	def display(self):
		for layer in self.layers:
			layer.display()
			sys.stdout.write("\n")
		
class layer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.cells = [x%5 for x in range(width*height)]
		self.tempcells = list(self.cells)
	
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
			if self.cells[i] != None and self.cells[i] > 3:
				self.topple(i%self.width, i//self.width)
		if self.cells != self.tempcells:
			self.cells = list(self.tempcells)
			self.tick()
	
	def topple(self,x,y):
		cell = self.index(x,y)
		pileHeight = self.cells[cell]
		grainsMoving = pileHeight//4
		self.tempcells[cell] -= grainsMoving*4
		for neighbor in self.neighbors(x,y):
			if neighbor != None:
				self.tempcells[neighbor] += grainsMoving
	
	def display(self):
		for y in range(self.height):
			row = self.cells[y*self.width:(y+1)*self.width]
			row = " ".join("{0}".format(c) for c in row) + "\n"
			sys.stdout.write(row)

class gameController:
	def getInput(self):
		#Get a round of input
		command = input("Type next action:")
		print(command)
		command.lower()
		tokens = command.split(' ')
		if command == "help":
			print("------------Sandpiles Help-----------")
			print("add g x y z - Places g grains of sand on tile (x, y, z)")
			print("example: to place 8 grains of sand on (0,1,0) type: \"add 8 0 1 0\"\n")
			print("exit - to exit the program")
			print("-----------------------------------")
		elif command == "exit":
			quit()
		elif tokens[0] == "add":
			print("This is the add function, we'll put the input code in here at somepoint")
		else:
			print("Invalid command, type \"help\" for a list of valid commands")

x=level(4,4,1)
controller = gameController()

while True:
	x.tick()
	x.display()
	controller.getInput()
