# CAP4621 Final Project - Ultimate Tic Tac Toe Game
# Authors - Vraj Patel and Daishak Patel

# CAP4621 AI Final Project
# Ultimate Tic Tac Toe AI Player
# Authors - Vraj Patel, Daishak Patel
# Description - This program allows a user to play a game of
#               Ultimate Tic Tac Toe. The program implements
#               an AI agent that uses Minimax Search with
#               alpha beta pruning along with evaluation functions
#               to determine the best move.

import os, time, shutil, copy, random

# Class UltimateTicTacToe encapsulates all methods needed to execute one game of Ultimate Tic Tac Toe
class UltimateTicTacToe:
    # initialize game variables
    def __init__(self,width,human):
        self.humanPlayer = human # stores which player is the human
        self.ultimateBoard = [[' '] * 9 for _ in range(9)]  # Represents the current board, ' ' means no mark
        self.largeBoard = [' ']*9
        # game finishes when large board is full (tie) or one player forms a row, column, or diagonal
        self.move_counter = 0
        self.width = width  # for printing purposes
        self.print = True
        self.lastSmallBoard = 9 # keeps track of which region the next player must move in
        self.nodesSearched = 0 # for performance evaluation of to compare alpha beta pruning

    # determines the minimax depth to be searched based on progression of the game - avoid unneceessarily intensive work at start
    def determine_depth(self):
        if self.move_counter <= 1:
            return 0
        elif 2 <= self.move_counter <= 8:
            return 3
        elif 9 <= self.move_counter <= 60:
            return 5
        else:
            return 7
        
        
    # displays the game board in a neat manner on the center of the console
    def display_board(self,player):
        clearConsole()
        print()
        printCentered("Ultimate Tic Tac Toe Board",self.width)
        print()
        for i in range(3):
            for j in range(3):
                print(" ",end="")
                for k in range(3):
                    if k == 2:
                        print(" " + self.ultimateBoard[i * 3 + k][j * 3 + 0] + " " + "|" +
                          " " + self.ultimateBoard[i * 3 + k][j * 3 + 1] + " " + "|" +
                          " " + self.ultimateBoard[i * 3 + k][j * 3 + 2] + " ", end="")
                    elif k == 0:
                        print(" "*((self.width-37)//2),end="")
                        print(" " + self.ultimateBoard[i * 3 + k][j * 3 + 0] + " " + "|" +
                          " " + self.ultimateBoard[i * 3 + k][j * 3 + 1] + " " + "|" +
                          " " + self.ultimateBoard[i * 3 + k][j * 3 + 2] + " ", end="║")
                    else:
                        print(" " + self.ultimateBoard[i * 3 + k][j * 3 + 0] + " " + "|" +
                              " " + self.ultimateBoard[i * 3 + k][j * 3 + 1] + " " + "|" +
                              " " + self.ultimateBoard[i * 3 + k][j * 3 + 2] + " ", end="║")
                print()
                if i < 2 or j < 2:
                    if j == 2:
                        print(" "*((self.width-37)//2) + "══"*19)
                    else:
                        print(" "*((self.width-37)//2) + " ---+---+---║---+---+---║---+---+---")
                        
        print()

    # Updates the game board with a particular move made by a player. Also, checks for regions captured.
    def make_move(self, move, player):
        if self.ultimateBoard[move[0]][move[1]] != ' ':
            print("Invalid move. Box already marked.")
            return False
        elif self.largeBoard[move[0]] != ' ':
            print('Invalid move. This region is already decided.')
        elif self.lastSmallBoard != 9 and move[0] != self.lastSmallBoard and self.largeBoard[self.lastSmallBoard] == ' ':
            print(f"Invalid move. Region index must be {self.lastSmallBoard+1} per the rules of the game.")   
        else:   # mark box as taken, 'X' for (P1) and 'O' for (P2)
            self.move_counter += 1
            if player == 1:
                self.ultimateBoard[move[0]][move[1]] = 'X'
            else:
                self.ultimateBoard[move[0]][move[1]] = 'O'
            self.check_smaller_board(move[0])   # check status of the smaller box just marked to see intermediate win
            self.lastSmallBoard = move[1]
            return True

    # If a region is captured or tied, marks it as such in the largeBoard variable
    def annotate(self,winner,boardRegion):
        if winner == 'X':   # If winner of the region is the 'X' player
            if self.print:
                print("Player 1 captured a region!")
            for box in range(9):
                if box not in [1,3,5,7]:
                    self.ultimateBoard[boardRegion][box] = 'X'
                else:
                    self.ultimateBoard[boardRegion][box] = '-'
        elif winner == 'O': # If winner of the region is the 'O' player
            if self.print:
                print("Player 2 captured a region!")
            for box in range(9):
                if box == 4:
                    self.ultimateBoard[boardRegion][box] = '-'
                else:
                    self.ultimateBoard[boardRegion][box] = 'O'
        else:   # If the region has reached capacity and has tied
            if self.print:
                print("A region was tied!")
            self.ultimateBoard[boardRegion][3] = 'T'
            self.ultimateBoard[boardRegion][4] = 'I'
            self.ultimateBoard[boardRegion][5] = 'E'
            for box in [0,1,2,6,7,8]:
                self.ultimateBoard[boardRegion][box] = '-'
                
    # checks if one of the nine smaller boards are taken or available
    def check_smaller_board(self,boardIndex):
        self.ultimateBoard[boardIndex]
        # Check rows
        for i in [0,3,6]:
            if self.ultimateBoard[boardIndex][i] == self.ultimateBoard[boardIndex][i+1] == self.ultimateBoard[boardIndex][i+2] != ' ':
                self.largeBoard[boardIndex] = self.ultimateBoard[boardIndex][i]
                self.annotate('X',boardIndex) if self.largeBoard[boardIndex] == 'X' else self.annotate('O',boardIndex)
                return
        # Check columns
        for i in [0,1,2]:
            if self.ultimateBoard[boardIndex][i] == self.ultimateBoard[boardIndex][i+3] == self.ultimateBoard[boardIndex][i+6] != ' ':
                self.largeBoard[boardIndex] = self.ultimateBoard[boardIndex][i]
                self.annotate('X',boardIndex) if self.largeBoard[boardIndex] == 'X' else self.annotate('O',boardIndex)
                return
        # Check diagonals
        if self.ultimateBoard[boardIndex][0] == self.ultimateBoard[boardIndex][4] == self.ultimateBoard[boardIndex][8] != ' ':
            self.largeBoard[boardIndex] = self.ultimateBoard[boardIndex][0]
            self.annotate('X',boardIndex) if self.largeBoard[boardIndex] == 'X' else self.annotate('O',boardIndex)
            return
        if self.ultimateBoard[boardIndex][2] == self.ultimateBoard[boardIndex][4] == self.ultimateBoard[boardIndex][6] != ' ':
            self.largeBoard[boardIndex] = self.ultimateBoard[boardIndex][2]
            self.annotate('X',boardIndex) if self.largeBoard[boardIndex] == 'X' else self.annotate('O',boardIndex)
            return
        # Check for a tie
        if ' ' not in self.ultimateBoard[boardIndex]:
            self.largeBoard[boardIndex] = '-'
            self.annotate('T',boardIndex)
            return
        # this small board is still available
        
    
    # Returns 1 if Player 1 has won, returns 2 if Player 2 has won, returns 0 if game still on
    def check_winner(self):
        # Check rows
        for i in [0,3,6]:
            if self.largeBoard[i] == self.largeBoard[i+1] == self.largeBoard[i+2] != ' ':
                return 1 if self.largeBoard[i] == 'X' else 2
        # Check columns
        for i in [0,1,2]:
            if self.largeBoard[i] == self.largeBoard[i+3] == self.largeBoard[i+6] != ' ':
                return 1 if self.largeBoard[i] == 'X' else 2
        # Check diagonals
        if self.largeBoard[0] == self.largeBoard[4] == self.largeBoard[8] != ' ':
            return 1 if self.largeBoard[i] == 'X' else 2
        if self.largeBoard[2] == self.largeBoard[4] == self.largeBoard[6] != ' ':
            return 1 if self.largeBoard[i] == 'X' else 2
        # Check for tie
        if ' ' not in self.largeBoard:
            if self.largeBoard.count('X') > self.largeBoard.count('O'):
                return 1
            elif self.largeBoard.count('X') < self.largeBoard.count('O'):
                return 2
            else:
                return 0.5
        # Game is still ongoing
        return 0

    # Determines all legal next moves, returns a list of tuples of moves
    def determine_legal_moves(self, player):
        legalMoves = []
        if self.lastSmallBoard == 9: # the game has just started, all boxes available
            legalMoves = [(i, j) for i in range(9) for j in range(9)]
        elif self.largeBoard[self.lastSmallBoard] == ' ':
            for box in range(9):
                if self.ultimateBoard[self.lastSmallBoard][box] == ' ':
                    legalMoves.append((self.lastSmallBoard,box))
        else:
            for smallBoard in range(9):
                if self.largeBoard[smallBoard] == ' ':
                    for box in range(9):
                        if self.ultimateBoard[smallBoard][box] == ' ':
                            legalMoves.append((smallBoard,box))
        return legalMoves

    # Randomly makes a choice from the legal moves
    def choose_move(self,player):
        return random.choice(self.determine_legal_moves(player))
    
    # Iterates over all possible moves and performs minimax on each
    def find_best_move(self, player):
        alpha = float('-inf')
        beta = float('inf')
        depth = self.determine_depth()
        nodesSearched = 0
        best_val = float('-inf')
        best_moves = []
        legal_moves = self.determine_legal_moves(player)
        # find the best move
        for move in legal_moves:
            temp_board = copy.deepcopy(self)    # makes a copy of the board to simulate a search
            temp_board.print = False            # disable printing to output for copies
            temp_board.make_move(move, player)  # marks on that copy
            move_val, nodes = temp_board.evaluate_move(depth, False, player, alpha, beta)  # Adjust depth as needed
            nodesSearched += nodes
            #print("Move:",move[0]+1,move[1]+1,"Value:",move_val)   #uncomment to display move scores
            if move_val > best_val:
                best_val = move_val
                best_moves.clear()
                best_moves.append(move)
            elif move_val == best_val:
                best_moves.append(move)
            alpha = max(alpha, move_val)
            if beta <= alpha:
                break  # Beta cut-off
        best_move = random.choice(best_moves)
        #print("Best move:",best_move[0]+1,best_move[1]+1,"Best move value:",best_val)  #uncomment to display best move's score
##        print(f"Nodes searched at depth {depth}: {nodesSearched}")
        self.nodesSearched += nodesSearched
        return best_move

    # Given a triple, checks whether a player can win a region with one more mark
    def is_opportunity(self, triple):
        if triple.count('O') == 0 and triple.count('X') == 2:
            return 'X'
        elif triple.count('X') == 0 and triple.count('O') == 2:
            return 'O'
        else:
            return ' '
        
    # Counts the number of opportunities for both players in a particular board        
    def count_opportunities(self):
        opportunities = []
        for boardIndex in range(9):
            if self.largeBoard[boardIndex] != ' ':
                continue
            # Check rows
            for i in [0,3,6]:
                opportunities.append(self.is_opportunity([self.ultimateBoard[boardIndex][i],self.ultimateBoard[boardIndex][i+1],self.ultimateBoard[boardIndex][i+2]]))      
            # Check columns
            for i in [0,1,2]:
                opportunities.append(self.is_opportunity([self.ultimateBoard[boardIndex][i],self.ultimateBoard[boardIndex][i+3],self.ultimateBoard[boardIndex][i+6]]))   
            # Check diagonals
            opportunities.append(self.is_opportunity([self.ultimateBoard[boardIndex][0],self.ultimateBoard[boardIndex][4],self.ultimateBoard[boardIndex][8]]))
            opportunities.append(self.is_opportunity([self.ultimateBoard[boardIndex][2],self.ultimateBoard[boardIndex][4],self.ultimateBoard[boardIndex][6]]))

        return opportunities.count('X'),opportunities.count('O')
        
        
    # The evaluation function used to evaluate a board configuration once depth limit is reached
    def evaluate_board(self,player,is_maximizing):
        score = 0     
        # determine which player the computer is
        if player == 1: # computer is player 1 ('X')
            # Regions Heuristic - count # of regions captured by computer/human
            if is_maximizing:
                score += self.largeBoard.count('X')*5.75
                score -= self.largeBoard.count('O')*8.25
            else:
                score += self.largeBoard.count('X')*8.25
                score -= self.largeBoard.count('O')*5.75
            # Positions Heuristic - number of opportunities
            opportunities_X, opportunities_O = self.count_opportunities()
            if is_maximizing:
                score += opportunities_X*0.75
                score -= opportunities_O*1.75
            else:
                score += opportunities_X*1.75
                score -= opportunities_O*0.75
            
        else:   # computer is player 2 ('O')
            # Regions Heuristic - reward/penalize based on count of number of regions captured by computer/human
            if is_maximizing:
                score += self.largeBoard.count('O')*5.75
                score -= self.largeBoard.count('X')*8.25
            else:
                score += self.largeBoard.count('O')*8.25
                score -= self.largeBoard.count('X')*5.75
            # Position Heuristic - number of opportunities
            opportunities_X, opportunities_O = self.count_opportunities()
            if is_maximizing:
                score += opportunities_O*0.75
                score -= opportunities_X*1.75
            else:
                score += opportunities_O*1.75
                score -= opportunities_X*0.75
            
        return score
            

    # Actual minimax implementation -
    # Finds utility of a move, 'player' is always the computer and is maximizing
    def evaluate_move(self, depth, is_maximizing, player, alpha, beta, nodesSearched=0):
        nodesSearched += 1
        winner = self.check_winner()
        if winner == 1:
            return (50, nodesSearched) if player == 1 else (-50, nodesSearched)
        elif winner == 2:
            return (50, nodesSearched) if player == 2 else (-50, nodesSearched)
        elif winner == 0.5:
            return (0, nodesSearched)
        
        if depth == 0:     
            return self.evaluate_board(player, is_maximizing), nodesSearched

        # implements minimax with alpha beta pruning depending on if the current player is maximizing or minimizing 
        if is_maximizing:
            max_eval = float('-inf')
            legal_moves = self.determine_legal_moves(player)
            for move in legal_moves:
                temp_board = copy.deepcopy(self)
                temp_board.make_move(move, player)
                eval, nodesSearched = temp_board.evaluate_move(depth - 1, False, player, alpha, beta, nodesSearched)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval, nodesSearched
        else:
            min_eval = float('inf')
            legal_moves = self.determine_legal_moves(player)
            for move in legal_moves:
                temp_board = copy.deepcopy(self)
                temp_board.make_move(move, 3 - player)
                eval, nodesSearched = temp_board.evaluate_move(depth - 1, True, player, alpha, beta, nodesSearched)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval, nodesSearched

    # Utility function to display message depending on winner    
    def gameFinishedMessage(self,winner):
        if winner == 0.5:
            print("""
  ____                           _____  _            _ 
 / ___|  __ _  _ __ ___    ___  |_   _|(_)  ___   __| |
| |  _  / _` || '_ ` _ \  / _ \   | |  | | / _ \ / _` |
| |_| || (_| || | | | | ||  __/   | |  | ||  __/| (_| |
 \____| \__,_||_| |_| |_| \___|   |_|  |_| \___| \__,_|""")
            
        elif winner == self.humanPlayer:
            print("""
__   __               __        __ _        
\ \ / /  ___   _   _  \ \      / /(_) _ __  
 \ V /  / _ \ | | | |  \ \ /\ / / | || '_ \ 
  | |  | (_) || |_| |   \ V  V /  | || | | |
  |_|   \___/  \__,_|    \_/\_/   |_||_| |_|""")
        else:
            print("""
__   __                _                        _ 
\ \ / /  ___   _   _  | |      ___   ___   ___ | |
 \ V /  / _ \ | | | | | |     / _ \ / __| / _ \| |
  | |  | (_) || |_| | | |___ | (_) |\__ \|  __/|_|
  |_|   \___/  \__,_| |_____| \___/ |___/ \___|(_)""")
            
 
    # Carries out the logistics of the play alternating between human and computer depending on human's choice
    def play(self, player_choice):
        print(f"You are Player {player_choice}")
        if player_choice == 1:
            while self.check_winner() == 0:
                print()
                print(f"Player {player_choice}'s turn".center(self.width,"="))
                print()
                if player_choice == 1:
                    try:
                        print(f"Select from region #{self.lastSmallBoard+1}" if self.lastSmallBoard != 9 and \
                              self.largeBoard[self.lastSmallBoard] == ' ' else "You have a Free Go!")
                        b1, b2 = map(int, input("Enter the region/square indices to place an 'X' (1 to 9): ").split())
                        if not (1 <= b1 <= 9 and 1 <= b2 <= 9):
                            raise ValueError
                        message = f"\nYou placed an 'X' at region {b1} square {b2}\n"
                        if not self.make_move((b1-1, b2-1), player_choice):
                            continue
                    except ValueError:
                        print("Invalid input. Please enter two integers in the range 1-9 separated by a space.")
                        continue
                else:
                    bestMove = self.find_best_move(player_choice)
                    #bestMove = self.choose_move(player_choice)    #Uncomment to choose a legal move at random
                    self.make_move(bestMove, player_choice)
                    message = f"\nComputer placed an 'O' at region {bestMove[0]+1} square {bestMove[1]+1}\n"
                player_choice = 3 - player_choice  # Switch players
                self.display_board(player_choice)
                print(message)
                     
        else:
            player_choice = 1
            while self.check_winner() == 0:
                print()
                print(f"Player {player_choice}'s turn".center(self.width,"="))
                print()
                if player_choice == 2:
                    try:
                        print(f"Select from region #{self.lastSmallBoard+1}" if self.largeBoard[self.lastSmallBoard] == ' ' else "You have a Free Go!")
                        b1, b2 = map(int, input("Enter the region/square indices to place an 'O' (1 to 9): ").split())
                        if not (1 <= b1 <= 9 and 1 <= b2 <= 9):
                            raise ValueError
                        message = f"\nYou placed an 'O' at region {b1} square {b2}\n"
                        if not self.make_move((b1-1, b2-1), player_choice):
                            continue
                    except ValueError:
                        print("Invalid input. Please enter two integers in the range 1-9 separated by space.")
                        continue
                else:
                    bestMove = self.find_best_move(player_choice)
                    #bestMove = self.choose_move(player_choice)   #Uncomment to choose a legal move at random
                    self.make_move(bestMove, player_choice)
                    message = f"\nComputer placed an 'X' at region {bestMove[0]+1} square {bestMove[1]+1}\n"
                player_choice = 3 - player_choice  # Switch players
                self.display_board(player_choice)
                print(message)

        # Once play loop terminates, check for result
        winner = self.check_winner()
        print(f"The computer searched a total of {self.nodesSearched} nodes in the game.")
        if winner == 0.5:
            print(f"\nGame Tied")
        self.gameFinishedMessage(winner)
        print(f"\nPlayer {winner} wins!")

# Halts execution until user presses enter
def waitForKeyPress(width,message=""):
    printCentered(message,width,fill="=")
    print("Press enter to continue ... ",end="")
    input()

# Clears the console screen
def clearConsole():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

# Returns the concole width for centering purposes
def getConsoleWidth():
    if os.name == 'posix':
        try:
            columns, _ = os.get_terminal_size(0)
            return columns
        except OSError:
            return None
    else:
        try:
            columns, _ = shutil.get_terminal_size()
            return columns
        except OSError:
            return None

# Displays a board with region indices markings
def printRegionBoard(width,offset):
    print()
    print("Region indices:".center(width))
    board = [[' ',' ',' ',' ',str(i),' ',' ',' ',' '] for i in range(1,10)]
    printUltimateBoard(board,offset)

# Displays a board with square indices markings
def printSquaresBoard(width,offset):
    print()
    print("Square indices within regions:".center(width))
    board = [['1','2','3','4','5','6','7','8','9'] for i in range(1,10)]
    printUltimateBoard(board,offset)

# Displays the board used as an example of how to enter region/square indices
def printExampleBoard(width,offset):
    print()
    print("Example:".center(width))
    board = [[' '] * 9 for _ in range(9)]
    board[2][7], board[7][5] = 'O', 'X'
    printUltimateBoard(board,offset)
    print("For example, the 'O' is at location 3 8 because it is in region 3, at square 8.")
    print("Similarly, the 'X' is at 8 6")

# Prints instructions of how to play   
def printInstructions():
    print("Welcome to Ultimate Tic Tac Toe!")
    print("\nInstructions:")
    print("1.  Ultimate Tic Tac Toe is played on a 3x3 grid of 3x3 Tic Tac Toe boards called regions.")
    print("2.  Player 1 ('X') begins with a free go, which means they can place an 'X' in any square.")
    print("3.  The relative square where a player places their symbol determines the region the next player must play in.")
    print("4.  If a player plays in a square that has an unavailable region, the opponent has a free go the next turn.")
    print("5.  The objective is to win each individual board and ultimately the larger Tic Tac Toe grid.")
    print("6.  To win a region, a player must get three of their symbols in a row, column, or diagonal.")
    print("7.  Once a region is won or full, the corresponding cell on the larger grid is marked.")
    print("8.  The first player to win three boards in a row, column, or diagonal wins the game.")
    print("9.  If the board is entirely full and no player has an overall row, column, or diagonal, the player with the most regions wins.")
    print("10. With a full board, if both players have the same number of regions, then the game is tied.")
    print("11. The next couple of menues describe what is meant by region and square, and how to take a turn.")
    print("12. Have fun and may the best player win!\n")

# Given a string, prints a message centered within provided width    
def printCentered(text, width=90,fill=" ",endChar='\n'):
    print(text.center(width,fill),end=endChar)

# Displays the welcome message and introduction    
def printWelcomeMessage(width):
    if width > 80:
        print("""
 _   _  _  _    _                    _           _____  _         _____                _____              
| | | || || |_ (_) _ __ ___    __ _ | |_   ___  |_   _|(_)  ___  |_   _|  __ _   ___  |_   _|  ___    ___ 
| | | || || __|| || '_ ` _ \\  / _` || __| / _ \   | |  | | / __|   | |   / _` | / __|   | |   / _ \\  / _ \\
| |_| || || |_ | || | | | | || (_| || |_ |  __/   | |  | || (__    | |  | (_| || (__    | |  | (_) ||  __/
 \___/ |_| \__||_||_| |_| |_| \__,_| \__| \___|   |_|  |_| \___|   |_|   \__,_| \___|   |_|   \___/  \___|""")
    printCentered("",width,"=")
    printCentered(" Welcome to the game of Ultimate Tic Tac Toe! ",width,fill="=")
    printCentered("",width,fill="=")
    print("\n")
    printCentered("Ultimate Tic Tac Toe is a variation of the classic Tic Tac Toe game, where each",width)
    printCentered("cell in the board contains a smaller Tic Tac Toe board.",width)
    printCentered("The objective is to win three smaller Tic Tac Toe boards in a row.",width)
    printCentered("Players take turns selecting a board and making a move within that board.",width)
    printCentered("To make a move, enter the position you want to place your mark (X or O).",width)
    printCentered("The first player to win three boards in a row, vertically, horizontally, or diagonally, wins!",width)
    print("\n")
    printCentered("",width,fill="=")
    printCentered(" Let's begin! Have fun playing! ",width,fill="=")
    printCentered("",width,fill="=")

# Prints the initial blank board
def printUltimateBoard(board,offset):
    print()
    for i in range(3):
        for j in range(3):
            print(" ",end="")
            for k in range(3):
                if k == 2:
                    print(" " + board[i * 3 + k][j * 3 + 0] + " " + "|" +
                      " " + board[i * 3 + k][j * 3 + 1] + " " + "|" +
                      " " + board[i * 3 + k][j * 3 + 2] + " ", end="")
                elif k == 0:
                    print(" "*offset,end="")
                    print(" " + board[i * 3 + k][j * 3 + 0] + " " + "|" +
                      " " + board[i * 3 + k][j * 3 + 1] + " " + "|" +
                      " " + board[i * 3 + k][j * 3 + 2] + " ", end="║")
                else:
                    print(" " + board[i * 3 + k][j * 3 + 0] + " " + "|" +
                          " " + board[i * 3 + k][j * 3 + 1] + " " + "|" +
                          " " + board[i * 3 + k][j * 3 + 2] + " ", end="║")
            print()
            if i < 2 or j < 2:
                if j == 2:
                    print(" "*offset + "══"*19)
                else:
                    print(" "*offset + " ---+---+---║---+---+---║---+---+---")
                    
    print()


# Determine console width and feeds it into all subsequent print functions
consoleWidth = getConsoleWidth() - 1
printWelcomeMessage(consoleWidth)


# Call the function to wait for any key press, clear afterwards
waitForKeyPress(consoleWidth)
clearConsole()

# Guide the user through pre-game instructions
printCentered("Ultimate Tic Tac Toe Board",consoleWidth)
ultimateBoard = [[' '] * 9 for _ in range(9)]
printUltimateBoard(ultimateBoard,(consoleWidth-37)//2)
print()
waitForKeyPress(consoleWidth)
printInstructions()
waitForKeyPress(consoleWidth)
clearConsole()
printRegionBoard(consoleWidth,(consoleWidth-37)//2)
waitForKeyPress(consoleWidth)
clearConsole()
printSquaresBoard(consoleWidth,(consoleWidth-37)//2)
waitForKeyPress(consoleWidth)
clearConsole()
printExampleBoard(consoleWidth,(consoleWidth-37)//2)
waitForKeyPress(consoleWidth)
clearConsole()
waitForKeyPress(consoleWidth-1,'Time to begin playing!')
printUltimateBoard(ultimateBoard,(consoleWidth-37)//2)


# Ask for the user's choice of 'X' or 'O' and call the UltimateTicTacToe object to begin playing
player_choice = input("\n\nDo you wish to be Player 1 ('X') or Player 2 ('O')? \nEnter 1 or 2: ")
while player_choice not in ['1', '2', 'q']:
    player_choice = input("Do you wish to be Player 1 ('X') or Player 2 ('O')? \nEnter 1 or 2 or 'q' to quit: ")
if player_choice == 'q':
    pass
else:
    game = UltimateTicTacToe(consoleWidth,int(player_choice))
    game.play(int(player_choice))
    input("\n\nPress enter to quit...")


