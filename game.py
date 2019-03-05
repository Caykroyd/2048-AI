import numpy as np;
import random as rnd;
from enum import Enum;

Action = Enum('Action', 'UP DOWN LEFT RIGHT')
	
class Game:
		
	def __init__(self, player, shape = (4,4)):
		self._player = player
		self._shape = shape
		self._board = np.zeros(shape,dtype='uint16')
	
	def run(self):
		
		self._add_random_piece();
		
		while(len(Game.allowed_actions(self._board))>0):
			print(self._board, '\nPlayer\'s turn...')
			print('Actions: ', Game.allowed_actions(self._board))
			act = self._choose_action(self._board);
			print('Choosing action ', act)
			if(act == Action.UP): self._shift_up()
			if(act == Action.LEFT): self._shift_left()
			if(act == Action.DOWN): self._shift_down()
			if(act == Action.RIGHT): self._shift_right()
			
			print(self._board)
			self._add_random_piece();
			
		print(self._board,'\nGame Ended.')
		
	def _choose_action(self, state):
		action = self._player.choose_action(state)
		if(not (action in Game.allowed_actions(self._board))):
			raise ValueError('Player tried to perform unallowed action')
		return action
	
	def _add_random_piece(self):
		empty = np.argwhere(self._board==0)
		random_empty_position = empty[rnd.randint(0,len(empty)-1),:]
		print('Adding tile:', random_empty_position)
		self._board[tuple(random_empty_position)] = 2	
	
	def allowed_actions(board):
		(rows, cols) = board.shape
		actions = set()
		for i in range(rows):
			row_i = board[i,:].nonzero()[0]
			if len(row_i)==0 or row_i[-1] >= len(row_i):
				actions.add(Action.LEFT)
			if len(row_i)==0 or cols-1 - row_i[0] >= len(row_i):
				actions.add(Action.RIGHT)
			#IMPORTANT: CHECK IF THERE ARE REPEATED NUMBERS TO JOINT TOGETHER
			for j in range(cols-1):
				if(board[i][j]!=0 and board[i][j]==board[i][j+1]):
					#print('Duplicate numbers on the horizontal!')
					actions.add(Action.LEFT)
					actions.add(Action.RIGHT)
		for j in range(cols):
			column_j = board[:,j].nonzero()[0]
			if len(column_j)==0 or column_j[-1] >= len(column_j):
				actions.add(Action.UP)
			if len(column_j)==0 or rows-1 - column_j[0] >= len(column_j):
				actions.add(Action.DOWN)
			#IMPORTANT: CHECK IF THERE ARE REPEATED NUMBERS TO JOINT TOGETHER
			for i in range(rows-1):
				if(board[i][j]!=0 and board[i][j]==board[i+1][j]):
					#print('Duplicate numbers on the vertical!')
					actions.add(Action.UP)
					actions.add(Action.DOWN)
		return actions
	
	# From Wikipedia: 
	# Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid. 
	# If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.
	# The resulting tile cannot merge with another tile again in the same move.
	def _shift_up(self):
		full = list(np.transpose(self._board.nonzero()))
		
		board_shifted = np.zeros(self._shape)
		shift_count = np.zeros(self._shape[1], dtype='uint8')
		for i,j in full:
			#check to see if two tiles will merge (i.e., if they have the same value)
			if(shift_count[j]>0 and board_shifted[shift_count[j]-1][j]==self._board[i][j]):
				board_shifted[shift_count[j]-1][j] *= 2
			else:
				board_shifted[shift_count[j]][j] = self._board[i][j]
				shift_count[j]+=1
		self._board = board_shifted
	
	def _shift_left(self):
		full = list(np.transpose(self._board.nonzero()))
		board_shifted = np.zeros(self._shape)
		shift_count = np.zeros(self._shape[0], dtype='uint8')
		for i,j in full:
			print(i,j)
			#check to see if two tiles will merge (i.e., if they have the same value)
			if(shift_count[i]>0 and board_shifted[i][shift_count[i]-1]==self._board[i][j]):
				board_shifted[i][shift_count[i]-1] *= 2
			else:
				board_shifted[i][shift_count[i]] = self._board[i][j]
				shift_count[i]+=1
		self._board = board_shifted
		
	def _shift_down(self):
		full = reversed(list(np.transpose(self._board.nonzero())))
		
		board_shifted = np.zeros(self._shape)
		shift_count = np.zeros(self._shape[1], dtype='uint8')
		for i,j in full:
			#check to see if two tiles will merge (i.e., if they have the same value)
			if(shift_count[j]>0 and board_shifted[shift_count[j]-1][j]==self._board[i][j]):
				board_shifted[shift_count[j]-1][j] *= 2
			else:
				board_shifted[shift_count[j]][j] = self._board[i][j]
				shift_count[j]+=1
		self._board = board_shifted
	
	def _shift_right(self):
		full = reversed(list(np.transpose(self._board.nonzero())))
		board_shifted = np.zeros(self._shape)
		shift_count = np.zeros(self._shape[0], dtype='uint8')
		n = self._shape[0]
		for i,j in full:
			#check to see if two tiles will merge (i.e., if they have the same value)
			if(shift_count[i]>0 and board_shifted[i][n-1-shift_count[i]+1]==self._board[i][j]):
				board_shifted[i][n-1-shift_count[i]+1] *= 2
			else:
				board_shifted[i][n-1-shift_count[i]] = self._board[i][j]
				shift_count[i]+=1
		self._board = board_shifted