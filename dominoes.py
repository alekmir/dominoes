# Осталось дописать:
# 1. Надо дописать условия ничьей, которые должны учитывать, какое количество раз встречается в змее это число.
#    Если 8 раз, то больше такой цифры нет. Если нет обеих - ничья. Конечно с условием, что у игроков остались
#    доминошки.


from random import shuffle
from string import ascii_letters
from string import punctuation
from random import choice

computer_pieces = []
player_pieces = []
stock_remains = []
domino_snake = []
game_continue = True
current_player = ""
player_legal_pieces = []


# Generating stock dominoes - 28 pieces
def generate_stock():
    stock_dominoes = []
    for i in range(0, 7):
        for k in range(0, 7):
            domino_piece = [i, k]
            if k >= i:
                stock_dominoes.append(domino_piece)
    return stock_dominoes


# Distributing stock dominoes between players (one of them is a computer).
# In result is three global variables: computer hand, player hand, remaining stock.
# Distribution is quite simple; it is division shuffled stock to three parts
def dealing():
    stock_dominoes = generate_stock()
    global computer_pieces
    global player_pieces
    global stock_remains

    shuffle(stock_dominoes)
    computer_pieces = stock_dominoes[0:7]
    player_pieces = stock_dominoes[7:14]
    stock_remains = stock_dominoes[14:]


# Defining another one global - domino_snake, and starting piece by comparing max double on players hands.
# If no doubles on hands - restarting game until double appear in hands
def first_move():
    global domino_snake
    global current_player

    # Check is there a double on hands? If not - deal again
    double_in_hand = False
    players_pieces = computer_pieces + player_pieces
    for piece in players_pieces:
        if piece[0] == piece[1]:
            double_in_hand = True
            break
    if double_in_hand:
        pass
    else:
        first_move()

    # Defining max double in computer's hand
    computer_max = [-1, -1]
    for piece in computer_pieces:
        piece.sort(reverse=True)
        if piece[0] == piece[1]:
            if piece[0] > computer_max[0]:
                computer_max = piece

    # Defining max double in player's hand
    player_max = [-1, -1]
    for piece in player_pieces:
        piece.sort(reverse=True)
        if piece[0] == piece[1]:
            if piece[0] > player_max[0]:
                player_max = piece

    # Comparing players hands and define first player to move
    if computer_max[0] > player_max[0]:
        domino_snake.append(computer_max)
        computer_pieces.remove(computer_max)
        current_player = 'player'
    else:
        domino_snake.append(player_max)
        player_pieces.remove(player_max)
        current_player = 'computer'


# This function draw a table with pieces amount on each side
def display_table():
    print('=' * 70)
    print('Stock size:', len(stock_remains))
    print('Computer pieces:', len(computer_pieces))
    domino_snake_visualization()
    print("Your pieces:")
    piece_num = 1
    for piece in player_pieces:
        print(f'{piece_num}:{piece}')
        piece_num += 1
    print("")


# Complex function which operate with the user input, adding selected piece to snake
def player_move():
    global game_continue
    global current_player
    # First test: is user input contains something? If empty - asking another input
    player_choice = input()
    if len(player_choice) == 0:
        print('Invalid input. Please try again.')
        current_player = "error"
        return current_player
    # Second test: if user input contains any symbols except digits. If so - asking another input
    for symbol in player_choice:
        if symbol in punctuation:
            if symbol == "-":
                continue
            else:
                print('Invalid input. Please try again.')
                current_player = "error"
                return current_player
        if symbol in ascii_letters:
            print('Invalid input. Please try again.')
            current_player = "error"
            return current_player
    # Third and last test: is user input more than pieces? If so - asking another input
    if abs(int(player_choice)) > len(player_pieces):
        print('Invalid input. Please try again.')
        current_player = "error"
        return current_player
    else:
        # It seems all test are passed. So what exactly user want?
        if int(player_choice) == 0:
            # User wants to pick from stock. Is there enough pieces?
            if len(stock_remains) > 0:
                # Selecting random piece from stock and adding to user hand
                random_piece = choice(stock_remains)
                player_pieces.append(random_piece)
                # Removing this piece from stock
                stock_remains.remove(random_piece)
                # Drawing table, passing move to the computer
                current_player = "computer"
                return current_player
            else:
                if legal_moves(player_pieces):
                    # No pieces left in stock. Asking player to choose appropriate piece from his hand
                    print('Invalid input. Please try again.')
                    current_player = "error"
                    return current_player
                else:
                    # No pieces left in stock. Player have no legal moves. Skipping move
                    current_player = "computer"
                    return current_player

        # Checking if player choice is a legal piece to move. If not - showing error
        else:
            if legal_moves(player_pieces):
                if int(player_choice) < 0:
                    # Player wants to add piece to left side of snake
                    # Checking is piece fit to snake?
                    if player_pieces[abs(int(player_choice)) - 1][0] == domino_snake[0][0]:
                        # First piece number is the same as first piece number in snake on the left side.
                        # Reversing and adding.
                        player_pieces[abs(int(player_choice)) - 1].reverse()
                        domino_snake.insert(0, player_pieces[abs(int(player_choice)) - 1])
                    elif player_pieces[abs(int(player_choice)) - 1][1] == domino_snake[0][0]:
                        # Second piece number is the same as first number in snake on the left side.
                        # Adding as it is.
                        domino_snake.insert(0, player_pieces[abs(int(player_choice)) - 1])
                    else:
                        # Player has legal piece but done wrong choice
                        print('Illegal move. Please try again.')
                        current_player = "error"
                        return current_player
                    # Removing selected piece from players hand
                    player_pieces.remove(player_pieces[abs(int(player_choice)) - 1])
                else:
                    # Player wants to add piece to right side of snake. Inserting selected piece there
                    # Its necessary to place piece to stock by the right side
                    if player_pieces[abs(int(player_choice)) - 1][0] == domino_snake[-1][1]:
                        # First piece number is the same as second piece number in snake on the right side.
                        # Adding as it is.
                        domino_snake.insert(len(domino_snake), player_pieces[abs(int(player_choice)) - 1])
                    elif player_pieces[abs(int(player_choice)) - 1][1] == domino_snake[-1][1]:
                        # Second piece number is the same as second piece number in snake on the right side.
                        # Reversing and adding.
                        player_pieces[abs(int(player_choice)) - 1].reverse()
                        domino_snake.insert(len(domino_snake), player_pieces[abs(int(player_choice)) - 1])
                    else:
                        # Player has legal piece but done wrong choice
                        print('Illegal move. Please try again.')
                        current_player = "error"
                        return current_player
                    # Removing selected piece from players hand
                    player_pieces.remove(player_pieces[abs(int(player_choice)) - 1])
            else:
                if int(player_choice) != 0:
                    # Player hasn't legal piece but doesn't choose 0 (taking from stock)
                    print('Illegal move. Please try again.')
                    current_player = "error"
                    return current_player

    if len(player_pieces) > 0:
        # If player has more than 0 pieces in hand - game will continue on next loop turn by computer's move
        current_player = "computer"
    else:
        # If player has no pieces - he won. Redrawing table, announcing winner. Stopping loop
        display_table()
        print("\nStatus: The game is over. You won!")
        game_continue = False


def computer_move():
    global game_continue
    global current_player

    input("Status: Computer is about to make a move. Press Enter to continue...\n")
    # Check if computer have appropriate piece. If not - taking from stock
    if legal_moves(computer_pieces):
        # Computer have appropriate piece. Let's find out what exactly pieces are appropriate?
        computer_legal_pieces = []
        for computer_piece in computer_pieces:
            for number in computer_piece:
                if number == domino_snake[0][0]:
                    computer_legal_pieces.append(computer_piece)
                elif number == domino_snake[-1][1]:
                    computer_legal_pieces.append(computer_piece)
                else:
                    continue
        # Variation to choose the best piece for move in terms of max weight of piece
        # best_piece = []
        # best_piece_position = 0
        # for piece in computer_legal_pieces:
        #     if sum(piece) > sum(best_piece):
        #         best_piece = piece
        # for i in range(0, len(computer_pieces)):
        #     if computer_pieces[i] == best_piece:
        #         best_piece_position = i

        # Variation to choose the best piece for move in terms of rarity of piece
        nums_count = {'1': 0,
                      '2': 0,
                      '3': 0,
                      '4': 0,
                      '5': 0,
                      '6': 0}
        for piece in computer_legal_pieces:
            for number in piece:
                if number == 1:
                    nums_count['1'] += 1
                elif number == 2:
                    nums_count['2'] += 1
                elif number == 3:
                    nums_count['3'] += 1
                elif number == 4:
                    nums_count['4'] += 1
                elif number == 5:
                    nums_count['5'] += 1
                else:
                    nums_count['6'] += 1
        for piece in domino_snake:
            for number in piece:
                if number == 1:
                    nums_count['1'] += 1
                elif number == 2:
                    nums_count['2'] += 1
                elif number == 3:
                    nums_count['3'] += 1
                elif number == 4:
                    nums_count['4'] += 1
                elif number == 5:
                    nums_count['5'] += 1
                else:
                    nums_count['6'] += 1

        best_piece = []
        best_piece_weight = 0
        best_piece_position = -1
        for piece in computer_legal_pieces:
            current_piece_weight = 0
            for number in piece:
                if number == 1:
                    current_piece_weight += nums_count['1']
                elif number == 2:
                    current_piece_weight += nums_count['2']
                elif number == 3:
                    current_piece_weight += nums_count['3']
                elif number == 4:
                    current_piece_weight += nums_count['4']
                elif number == 5:
                    current_piece_weight += nums_count['5']
                else:
                    current_piece_weight += nums_count['6']
            if current_piece_weight > best_piece_weight:
                best_piece = piece
        for i in range(len(computer_pieces)):
            if computer_pieces[i] == best_piece:
                best_piece_position = i

        # Now inserting best piece to snake
        if best_piece[0] == domino_snake[0][0]:
            best_piece.reverse()
            domino_snake.insert(0, best_piece)
            computer_pieces.remove(computer_pieces[best_piece_position])
        elif best_piece[1] == domino_snake[0][0]:
            domino_snake.insert(0, best_piece)
            computer_pieces.remove(computer_pieces[best_piece_position])
        elif best_piece[0] == domino_snake[-1][1]:
            domino_snake.insert(len(domino_snake), best_piece)
            computer_pieces.remove(computer_pieces[best_piece_position])
        else:
            best_piece.reverse()
            domino_snake.insert(len(domino_snake), best_piece)
            computer_pieces.remove(computer_pieces[best_piece_position])
    else:
        # Computer has no appropriate pieces. Taking from stock
        if len(stock_remains) > 0:
            # Selecting random piece from stock and adding to computer hand
            random_piece = choice(stock_remains)
            computer_pieces.append(random_piece)
            # Removing this piece from stock
            stock_remains.remove(random_piece)
            current_player = "player"
            return current_player
        else:
            # No pieces left in stock. Skipping move
            current_player = "player"
            return current_player

    # If computer still have pieces - game will continue. Otherwise - computer won
    if len(computer_pieces) > 0:
        current_player = "player"
    else:
        display_table()
        print("\nStatus: The game is over. The computer won!")
        game_continue = False


def is_draw():
    count_of_0 = 0
    count_of_1 = 0
    count_of_2 = 0
    count_of_3 = 0
    count_of_4 = 0
    count_of_5 = 0
    count_of_6 = 0

    for piece in domino_snake:
        for number in piece:
            if number == 0:
                count_of_0 += 1
                if count_of_0 > 7:
                    return True
            elif number == 1:
                count_of_1 += 1
                if count_of_1 > 7:
                    return True
            elif number == 2:
                count_of_2 += 1
                if count_of_2 > 7:
                    return True
            elif number == 3:
                count_of_3 += 1
                if count_of_3 > 7:
                    return True
            elif number == 4:
                count_of_4 += 1
                if count_of_4 > 7:
                    return True
            elif number == 5:
                count_of_5 += 1
                if count_of_5 > 7:
                    return True
            else:
                count_of_6 += 1
                if count_of_6 > 7:
                    return True
    return False


def domino_snake_visualization():
    domino_snake_str = "\n"
    if len(domino_snake) < 7:
        # Snake no more than a 6 pieces. Drawing as is
        for i in range(0, len(domino_snake)):
            # Setting pieces to a new variable which be drown as in samples
            domino_snake_str += str(domino_snake[i])
    else:
        # Snake contains more than 6 pieces. Cutting first 3 pieces and last 3 pieces and adding "..." in between
        snake_begins = domino_snake[:3]
        snake_ends = domino_snake[-3:]
        for i in snake_begins:
            domino_snake_str += str(i)
        domino_snake_str += "..."
        for i in snake_ends:
            domino_snake_str += str(i)
    domino_snake_str += "\n"
    print(domino_snake_str)


def legal_moves(current_player_pieces):
    global player_legal_pieces

    legal_pieces = []
    for piece in current_player_pieces:
        for number in piece:
            legal_pieces.append(number)
    legal_pieces = set(legal_pieces)
    for number in legal_pieces:
        if number == domino_snake[0][0] or number == domino_snake[-1][1]:
            return True
    return False


dealing()
first_move()

while game_continue:
    if current_player == "computer":
        display_table()
        computer_move()
    elif current_player == "error":
        player_move()
    else:
        display_table()
        print("Status: It's your turn to make a move. Enter your command.")
        player_move()
    if is_draw():
        print("Status: The game is over. It's a draw!")
        game_continue = False
