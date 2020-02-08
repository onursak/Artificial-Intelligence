import chess
import random

# Material points in centipawn unit
pawn_point = 100
knight_point = 320
bishop_point = 330
rook_point = 500
queen_point = 900
king_point = 20000

# Piece square tables for white player which shows scores according to square for corresponding piece
pawn_table = [[0,  0,  0,  0,  0,  0,  0,  0],
			  [50, 50, 50, 50, 50, 50, 50, 50], 
			  [10, 10, 20, 30, 30, 20, 10, 10],
 			  [5,  5, 10, 25, 25, 10,  5,  5],
 			  [0,  0,  0, 20, 20,  0,  0,  0],
 		      [5, -5,-10,  0,  0,-10, -5,  5],
 			  [5, 10, 10,-20,-20, 10, 10,  5],
 			  [0,  0,  0,  0,  0,  0,  0,  0]]

knight_table = [[-50,-40,-30,-30,-30,-30,-40,-50],
				[-40,-20,  0,  0,  0,  0,-20,-40],
				[-30,  0, 10, 15, 15, 10,  0,-30],
				[-30,  5, 15, 20, 20, 15,  5,-30],
				[-30,  0, 15, 20, 20, 15,  0,-30],
				[-30,  5, 10, 15, 15, 10,  5,-30],
				[-40,-20,  0,  5,  5,  0,-20,-40],
				[-50,-40,-30,-30,-30,-30,-40,-50]]

bishop_table = [[-20,-10,-10,-10,-10,-10,-10,-20],
				[-10,  0,  0,  0,  0,  0,  0,-10],
				[-10,  0,  5, 10, 10,  5,  0,-10],
				[-10,  5,  5, 10, 10,  5,  5,-10],
				[-10,  0, 10, 10, 10, 10,  0,-10],
				[-10, 10, 10, 10, 10, 10, 10,-10],
				[-10,  5,  0,  0,  0,  0,  5,-10],
				[-20,-10,-10,-10,-10,-10,-10,-20]]

rook_table = [[0,  0,  0,  0,  0,  0,  0,  0],
  			  [5, 10, 10, 10, 10, 10, 10,  5],
 			  [-5,  0,  0,  0,  0,  0,  0, -5],
 			  [-5,  0,  0,  0,  0,  0,  0, -5],
 			  [-5,  0,  0,  0,  0,  0,  0, -5],
 			  [-5,  0,  0,  0,  0,  0,  0, -5],
 			  [-5,  0,  0,  0,  0,  0,  0, -5],
  			  [0,  0,  0,  5,  5,  0,  0,  0]]

queen_table = [[-20,-10,-10, -5, -5,-10,-10,-20],
			   [-10,  0,  0,  0,  0,  0,  0,-10],
			   [-10,  0,  5,  5,  5,  5,  0,-10],
 			   [-5,  0,  5,  5,  5,  5,  0, -5],
  			   [0,  0,  5,  5,  5,  5,  0, -5],
			   [-10,  5,  5,  5,  5,  5,  0,-10],
			   [-10,  0,  5,  0,  0,  0,  0,-10],
			   [-20,-10,-10, -5, -5,-10,-10,-20]]

king_table = [[-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
			  [-30,-40,-40,-50,-50,-40,-40,-30],
              [-20,-30,-30,-40,-40,-30,-30,-20],
			  [-10,-20,-20,-20,-20,-20,-20,-10],
 			  [20, 20,  0,  0,  0,  0, 20, 20],
 			  [20, 30, 10,  0,  0, 10, 30, 20]]



# This function generates mirror versions of white's square tables for black player
def generate_mirror_table(table):

	mirror_table = []
	
	for i in range(0,8):
		mirror_table.append(table[7-i])
	
	return mirror_table

# Generating mirror piece square tables for black player
mirror_pawn_table = generate_mirror_table(pawn_table)
mirror_knight_table = generate_mirror_table(knight_table)
mirror_bishop_table = generate_mirror_table(bishop_table)
mirror_rook_table = generate_mirror_table(rook_table)
mirror_queen_table = generate_mirror_table(queen_table)
mirror_king_table = generate_mirror_table(king_table)

# Adding these tables into lists for black and white players for easiness about rest of the code in loops
white_square_tables = [pawn_table, knight_table, bishop_table, rook_table, queen_table, queen_table, king_table]

black_square_tables = [mirror_pawn_table, mirror_knight_table, mirror_bishop_table, mirror_rook_table, 
								mirror_queen_table, mirror_queen_table, mirror_king_table]


# This function evaluates the given piece positions according to corresponding piece sqaure table
def evaluate_piece_square(table, piece_positions):
	point = 0

	for i in piece_positions:
		index = i // 8
		offset = i % 8
		point += table[7-index][offset] # I substracted the index from 7, because of the board placement from the point of view below of the board

	return point

# This function calculates the piece square score for each pieces in the board for given color
def get_piece_square_score(board, color):
	
	score = 0
	
	for i in range(1,7):
		if color == chess.WHITE:
			score += evaluate_piece_square(white_square_tables[i-1], list(board.pieces(i, color)))
		else:
			score += evaluate_piece_square(black_square_tables[i-1], list(board.pieces(i, color)))

	return score

# This function simply gives the material score by multiplying the piece counts with the weights of pieces for given color
def get_material_score(board, color):
	pawn_count = len(list(board.pieces(chess.PAWN, color)))
	bishop_count = len(list(board.pieces(chess.BISHOP, color)))
	knight_count = len(list(board.pieces(chess.KNIGHT, color)))
	rook_count = len(list(board.pieces(chess.ROOK, color)))
	queen_count = len(list(board.pieces(chess.QUEEN, color)))
	king_count = len(list(board.pieces(chess.KING, color)))
	return (pawn_point * pawn_count + bishop_point * bishop_count + knight_point * knight_count +
			rook_point * rook_count + queen_point * queen_count + king_point * king_count)


# This function returns the possible legal move count for the given player
def get_mobility_score(board, color):
	if board.turn == color:
		mobility = len(list(board.legal_moves))
		return mobility
	else:
		# Turn is switched to find mobility, even if it is not given color's turn
		board.turn = color
		mobility = len(list(board.legal_moves))
		board.turn = not color  # Turn is setted to old value
		return mobility

def detect_checkmate_attack(board, color):
	board.turn = not color
	checkmate = board.is_checkmate()
	board.turn = color
	return checkmate

# This function detects the doubled pawn count for the given player
# Doubled pawn is the pawn that is placed at the same file with any other pawn
def detect_doubled_pawns(board, color):
	
	doubled_pawn_count = 0

	files_of_pawns = []

	# Adding file values of pawns into a list
	for i in list(board.pieces(chess.PAWN, color)):
		files_of_pawns.append(chess.square_file(i))	

	# If there are two or more pawn in the same file, then increment doubled pawn count
	for i in files_of_pawns:
		if files_of_pawns.count(i) > 1:
			doubled_pawn_count += 1

	return doubled_pawn_count

# This function detects the backward pawns which have no any other pawn behind them
def detect_backward_pawns(board, color):
	
	backward_pawn_count = 0

	pawns = list(board.pieces(chess.PAWN, color))

	for i in pawns:
		is_backward = True
		for j in pawns:
			if i == j:
				continue
			else:
				# If any other pawn is found at the behind of this pawn, then is_backward value is setted as False 
				# For white and black players, procedure is reversed
				if color == chess.WHITE and chess.square_rank(i) > chess.square_rank(j):
					is_backward = False
					break
				elif color == chess.BLACK and chess.square_rank(i) < chess.square_rank(j):
					is_backward = False
					break
		if is_backward == True:
			backward_pawn_count += 1
		
	return backward_pawn_count

# This function creates a matrix by using pawn locations for the pawn visualization as matrix
# Returned matrix facilitates the process for looking pawn is passed or not
def create_matrix_for_pawns(pawn_positions):
	pawn_matrix = [[0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0],
				   [0,0,0,0,0,0,0,0]]
	for i in pawn_positions:
		index = chess.square_rank(i)
		offset = chess.square_file(i)
		pawn_matrix[7-index][offset] = 1
	return pawn_matrix

# This function cheks the given position is in the board boundary or not
def is_valid_value(position):
	if position < 0 or position > 7:
		return False
	return True

# This function detects the passed pawns which protect each other
def detect_passed_pawns(board, color):
	passed_pawn_count = 0
	pawns = list(board.pieces(chess.PAWN, color))
	# Pawn matrix is created for easy calculation of passed pawns
	pawn_matrix = create_matrix_for_pawns(pawns)

	for i in range(0,len(pawn_matrix)):
		for j in range(0,len(pawn_matrix[i])):
			if pawn_matrix[i][j] == 1: # Pawn is found
				previous_row = 0 # Previous row is the row that we look for protector pawn
				# Because of point of view, previous row is taking a different value for each color
				if color == chess.WHITE:
					previous_row = i+1
				else:
					previous_row = i-1
				# Two possible squares are initialized here for possible protector pawn positions
				possible_position_left = j - 1
				possible_position_right = j + 1
				# If previous row is outside of the board range, then don't evaluate the rest
				if is_valid_value(previous_row) == False:
					continue
				else:
					# Looking if there is a pawn in the possible squares
					if is_valid_value(possible_position_right) and pawn_matrix[previous_row][possible_position_right] == 1:
						passed_pawn_count += 1
					elif is_valid_value(possible_position_left) and pawn_matrix[previous_row][possible_position_left] == 1:
						passed_pawn_count += 1
					else:
						continue
	return passed_pawn_count

# This function faciliates the detecting isolated pawn procedure by finding environment squares of the given pawn position that we look
# to understand this pawn is isolated or not
def get_environment_squares(pawn_position):
	environment_squares = []
	# Converting pawn_position into 8x8 matrix format for providing easiness to check board boundary 
	index = pawn_position // 8
	offset = pawn_position % 8
	for i in range(-1,2): # -1 for below rank, 0 for current rank, 1 for upper rank
		control_index = index + i
		if is_valid_value(control_index) == True:
			for j in range(-1,2):  # -1 for left file, 0 for current file, 1 for right file
				control_offset = offset + j
				if index == control_index and offset == control_offset: # This square belongs to this pawn, we ignore this square
					continue
				# If offset in the board boundary, then add it to the list with the index
				elif is_valid_value(control_offset) == True:
					environment_squares.append([control_index, control_offset])
	return environment_squares

# This function detects the isolated pawns that has no any other pawn around squares
def detect_isolated_pawns(board, color):

	isolated_pawn_count = 0
	
	pawns = list(board.pieces(chess.PAWN, color))

	for i in pawns:
		isolated_pawn = True
		environment_squares = get_environment_squares(i)
		for j in environment_squares:
			position = j[0] * 8 + j[1] #Converting matrix position into 0-63 range value
			# Pawn is found in the environment squares, then mark the pawn as not isolated and break the loop
			if position in pawns:
				isolated_pawn = False
				break
		if isolated_pawn == True:
			isolated_pawn_count += 1
	
	return isolated_pawn_count	


# This function looks for pawns that are placed in front of the king
# I didn't use this function in evaluation function because I could not be sure about weight of this feature
def is_king_safe(board, color):
	king_square = board.king(color)
	pawns = list(board.pieces(chess.PAWN, color))
	pawn_count_around_king = 0
	for i in range(7,10):
		if (king_square + i) in pawns:
			pawn_count_around_king += 1
	return pawn_count_around_king


#Evaluation function that evaluates the static score of the current board from the view of given color
#Used features:
# 1.Material Score
# 2.Piece Square Score
# 3.Isolated Pawn Score
# 4.Backward Pawn Score
# 5.Doubled Pawn Score
# 6.Passed Pawn Score
# 7.Mobility Score
# I used the Shannon's evaluation formula by multiplying the coefficients according to centipawn unit
# Passed pawn weight is according to my intuition, it is not placed in the Shannon's formula 
def eval_func(board, color):

	material_score = get_material_score(board, color) - get_material_score(board, not color)

	piece_square_score = get_piece_square_score(board, color) - get_piece_square_score(board, not color)
	
	# These followings are the features that give penalty
	pawn_position_score = (( detect_backward_pawns(board, color) - detect_backward_pawns(board, not color) ) 
							+ ( detect_doubled_pawns(board, color) - detect_doubled_pawns(board, not color))
							+ ( detect_isolated_pawns(board, color) - detect_isolated_pawns(board, not color)) )

	passed_pawn_score = detect_passed_pawns(board, color) - detect_passed_pawns(board, not color)
	
	mobility_score = get_mobility_score(board, color) - get_mobility_score(board, not color)
	
	total_score = ( material_score + piece_square_score  - 50 * pawn_position_score + 50 * passed_pawn_score 
							+ 10 * mobility_score ) 


	return total_score


# Minimax algorithm that find the best score by backtracking over the game tree
# I also applied the alpha-beta pruning, because the algorithm runs too slowly and my evaluation function
# is a little bit complicated and this increases the computing time 
def apply_minimax(board, depth, max_player, alpha, beta, color):
	# Base condition
	if depth == 0:
		# Determining ai color
		if color == chess.WHITE:
			return eval_func(board, chess.WHITE)
		else:
			return eval_func(board, chess.BLACK)
	elif max_player == True:
		# If the state is the stalemate, so the game is scoreless then return 0 
		if board.is_stalemate() == True:
			return 0
		# Since AI is the maximizer player and the board is in the checkmate situation, then AI lost the game and return too small value
		# Actually, if the state is the checkmate there will be no legal move and function won't enter into for loop and will return -100000000
		# However, to avoid confusion and to make it easy to see in the code, I wrote this situation with if branch
		elif board.is_checkmate() == True:
			return -100000000
		
		max_value = -100000000 # Given too small value for initial value
		# Looking for child nodes
		for move in board.legal_moves:
			move_to_perform = board.push(move) # Move is pushed for evaluating the board after the move is performed
			evaluation = apply_minimax(board, depth -1, False, alpha, beta, color)
			max_value = max(max_value, evaluation) 
			alpha = max(alpha, max_value) 
			board.pop() # After the evaluation, move is popped and board has come to old situation, so the other moves can be tried
			if alpha >= beta:
				break
		return max_value

	else:
		# If the state is the stalemate, so the game is scoreless then return 0
		if board.is_stalemate() == True:
			return 0
		# Since opponent is the minimizer player and the board is in the checkmate situation, then opponent lost the game and return too large value for us
		elif board.is_checkmate() == True:
			return 100000000
		
		min_value = 100000000  # Given too large value for initial value
		# Looking for child nodes
		for move in board.legal_moves:
			move_to_perform = board.push(move)	
			evaluation = apply_minimax(board, depth -1, True, alpha, beta, color)
			min_value = min(min_value, evaluation)
			beta = min(beta, min_value)
			board.pop()
			if alpha >= beta:
				break
		return min_value

# This function is created because minimax function returns the best score, not move.
# Minimax's first depth is performed in this function with for loop. Because of this, minimax function
# is called with the depth which is substracted 1. 
# As a summary, altough this function uses the minimax with the depth which is substracted 1, as a big picture
# minimax with depth 3 is performed.
def find_best_move(board, color):

	values = []

	for move in board.legal_moves:
		board.push(move)
		values.append(apply_minimax(board, 2, False, -100000000, 100000000, color))
		board.pop()
	
	#Selecting move that gives the maximum score for maximizer player
	max_value = max(values)
	list_legal_moves = list(board.legal_moves)
	move = list_legal_moves[values.index(max_value)]
	return str(move)
	

def ai_play(board):
	
	#Getting fen notation for determining which color the AI will be
	fen = board.fen()
	splitted_fen = fen.split(" ")
	ai_color = splitted_fen[1]
	best_move = ""
	
	if ai_color == "w":
		best_move = find_best_move(board, chess.WHITE)
	else:
		best_move = find_best_move(board, chess.BLACK)

	return best_move



