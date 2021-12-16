from tkinter import *
from tkinter import font
import random

class GameOfLife(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent

		self.grid(row = 0, column = 0)

		self.sizeX = 20

		self.sizeY = 20

		self.numberOfRandomDots = 50

		self.cellButtons = []

		self.generateNext = True

		self.initialUI()

	def initialUI(self):
		self.parent.title('Game of Life')

		# Initialize window for the game
		self.titleFrame = Frame(self.parent)
		self.titleFrame.grid(row = 0, column = 0, columnspan = 4)

		self.titleFont = font.Font(family='Helvetica', size=14)
		title = Label(self.titleFrame, text = "Conway's Game of Life", font = self.titleFont)
		title.pack(side = TOP)

		prompt = Label(self.titleFrame, text = 'Click the cells to create the starting configuration, then press Start Game:')
		prompt.pack(side = BOTTOM)

		# Build area
		self.buildGrid()

		# Create buttons for the game
		self.startButton = Button(self.parent, text = 'Start', command = self.prepareToSimulateGame)
		self.startButton.grid(row = 1, column = 0)

		self.stopButton = Button(self.parent, text = 'Stop', state = DISABLED, command = lambda: self.stopGame(self.activatePlayGround))
		self.stopButton.grid(row = 1, column = 1)

		self.clearButton = Button(self.parent, text = 'Clear', state = NORMAL, command = lambda: self.stopGame(self.clearPlayGround))
		self.clearButton.grid(row = 1, column = 2)

		self.randomButton = Button(self.parent, text = 'Random', state = NORMAL, command = self.createRandomDots)
		self.randomButton.grid(row = 1, column = 3)

	def buildGrid(self):
		# Creates new frame for grid of cells in game
		self.gameFrame = Frame(
			self.parent, width = self.sizeX + 2, height = self.sizeY + 2, borderwidth = 1, relief = SUNKEN)

		self.gameFrame.grid(row = 2, column = 0, columnspan = 4)

		# Instantiates buttons for choosing initial configuration
		self.cellButtons = [[Button(self.gameFrame, highlightbackground = 'white', width = 2, height = 1) for i in range(self.sizeX + 2)] for j in range(self.sizeY + 2)]

		# Creates 2d array of buttons for grid
		for i in range(1, self.sizeY + 1):
			for j in range(1, self.sizeX + 1):	
				self.cellButtons[i][j].grid(row = i, column = j, sticky = W+E)
				self.cellButtons[i][j]['command'] = lambda i=i, j=j:self.cellToggle(self.cellButtons[i][j])

	def prepareToSimulateGame(self):
		self.disableButtons()

		self.generateNext = True

		return self.simulateGame()

	def simulateGame(self):
		# Creates list of buttons in grid to toggle
		cellsToToggle = []
		for i in range(1, self.sizeY + 1):
			for j in range(1, self.sizeX + 1):
				coord = (i, j)
				# If cell dead and has 3 neighbors, add coordinate to list of coords to toggle
				if self.cellButtons[i][j]['highlightbackground'] == 'white' and self.neighborCount(i, j) == 3:
					cellsToToggle.append(coord)
				# If cell alive and does not have 2 or 3 neighbors, add coordinate to list of coords to toggle
				elif self.cellButtons[i][j]['highlightbackground'] == 'black' and self.neighborCount(i, j) != 3 and self.neighborCount(i, j) != 2:
					cellsToToggle.append(coord)

		# Updates (toggles) the cells on the grid
		for coord in cellsToToggle:
			self.cellToggle(self.cellButtons[coord[0]][coord[1]])			

		if self.generateNext:
			return self.after(100, self.simulateGame)
		else:
			return self.stopGame(self.activatePlayGround)

	def createRandomDots(self):
		self.clearPlayGround()

    # Random filling of cells
		i = 0
		while (i < self.numberOfRandomDots):
			randomX = random.randint(0, self.sizeX)
			randomY = random.randint(0, self.sizeY)

			if (self.cellButtons[randomY][randomX]['highlightbackground'] == 'black'):
				continue

			self.cellToggle(self.cellButtons[randomY][randomX])

			i += 1

	def disableButtons(self):
		self.startButton.configure(state = DISABLED)
		self.stopButton.configure(state = NORMAL)
		self.clearButton.configure(state = DISABLED)
		self.randomButton.configure(state = DISABLED)

	def enableButtons(self):
		self.startButton.configure(state = NORMAL)
		self.stopButton.configure(state = DISABLED)
		self.clearButton.configure(state = NORMAL)
		self.randomButton.configure(state = NORMAL)

	def neighborCount(self, xCoord, yCoord):
		# Count the number of neighbors of a cell		
		count = 0

		for i in range(xCoord - 1, xCoord + 2):
			for j in range(yCoord - 1, yCoord + 2):
				if (i != xCoord or j != yCoord) and self.cellButtons[i][j]['highlightbackground'] == 'black':
					count += 1

		return count

	def cellToggle(self, cell):
		if cell['highlightbackground'] == 'white':
			cell['highlightbackground'] = 'black'
		else:
			cell['highlightbackground'] = 'white'

	def stopGame(self, action):
		self.generateNext = False

		self.enableButtons()

		return action()


	def activatePlayGround(self):
		for i in range(0, self.sizeY + 2):
			for j in range(0, self.sizeX + 2):
				self.cellButtons[j][i].configure(state = NORMAL)

	def clearPlayGround(self):
		for i in range(0, self.sizeY + 2):
			for j in range(0, self.sizeX + 2):
				self.cellButtons[i][j]['highlightbackground'] = 'white'
				self.cellButtons[i][j].configure(state = NORMAL)


if __name__ == '__main__':
	root = Tk()
	game = GameOfLife(root)
	root.mainloop()