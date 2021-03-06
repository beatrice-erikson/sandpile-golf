import sys
import string
import copy

class level:
	def __init__(self,width,height,depth):
		self.width = width
		self.height = height
		self.depth = depth
		self.layers = [layer(width,height) for _ in range(depth)]
	
	def tick(self):
		for layer in self.layers:
			layer.tick()
	
	def add(self,x,y,z,grains):
		if z >= self.depth or z < 0:
			return str("layer depth out of range")
		return self.layers[z].add(x,y,z,grains)

	def display(self):
		for layer in self.layers:
			layer.display()
			sys.stdout.write("\n")

class tile:
	def __init__(self, sandGrains):
		self.traveledTo = False
		self.sand = sandGrains
	def __eq__(self, other):
		return other and self.sand == other.sand

class layer:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = [tile(0) for _ in range(width*height)]
		self.temptiles = copy.deepcopy(self.tiles)
	
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
		for i in range(len(self.tiles)):
			if self.tiles[i] != None and self.tiles[i].sand > 3:
				self.topple(i%self.width, i//self.width)
		if self.tiles == self.temptiles:
			return
			#This being here instead of in level.tick() is critical to holes working,
			#depositing all toppled sand at once instead of interspersed with topples on lower layers
		self.tiles = copy.deepcopy(self.temptiles)
		self.tick()
	
	def topple(self,x,y):
		tile = self.index(x,y)
		pileHeight = self.tiles[tile].sand
		grainsMoving = pileHeight//4
		self.temptiles[tile].sand -= grainsMoving*4
		for neighbor in self.neighbors(x,y):
			if neighbor != None:
				self.temptiles[neighbor].sand += grainsMoving
	
	def add(self,x,y,z,grains):
		tile = self.index(x,y)
		if not self.tiles[tile]:
			return "tile out of bounds"
		#self.tiles[tile].sand += grains
		self.temptiles[tile].sand += grains
		return "added {0} grains of sand to tile {1}, {2} of layer {3}".format(grains,x,y,z)

	def display(self, temp=False):
		for y in range(self.height):
			if temp:
				row = self.temptiles[y*self.width:(y+1)*self.width]
			else:
				row = self.tiles[y*self.width:(y+1)*self.width]
			row = " ".join("{0}".format(c.sand) for c in row) + "\n"
			sys.stdout.write(row)
		sys.stdout.write("display" + str(temp))

class gameController:
	def getInput(self, table):
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
			if len(tokens) < 5:
				print("Not enough args for add. Expected 4, got ", len(tokens)-1)
			else:
				try:
					grains,x,y,z = [int(i) for i in tokens[1:5]]
					print(table.add(x,y,z,grains))
				except:
					print("invalid values for add")
		else:
			print("Invalid command, type \"help\" for a list of valid commands")

table=level(11,11,1)
controller = gameController()

while True:
	table.tick()
	table.display()
	controller.getInput(table)
