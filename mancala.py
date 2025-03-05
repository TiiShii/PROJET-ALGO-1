# INFO-F103 – Algorithmique 1
# Projet 1 – Backtracking
# Implémentation du jeu Awalé (Mancala)

import copy  # Importe le module copy pour la copie profonde

def play(board, player: int, cell: int) -> int:
    """
    Joue un coup pour le joueur donné à partir de la case spécifiée.
    
    Parameters:
    board (list of list of int): Le plateau de jeu, une liste de deux listes représentant les deux côtés.
    player (int): Le joueur courant (0 ou 1).
    cell (int): La case à partir de laquelle jouer (0 à 5).
    
    Returns:
    int: Le nombre de graines capturées par le joueur.
    """
    if board[player][cell] == 0:
        return 0  # Si la case est vide, aucun coup ne peut être joué
    
    board_copy = copy.deepcopy(board)  # Crée une copie du plateau pour éviter de modifier l'original
    graines = board_copy[player][cell]  # Nombre de graines dans la case choisie
    board_copy[player][cell] = 0  # Vide la case choisie
    
    current_player, current_cell = player, cell
    board_size = len(board[player])
    
    # Distribue les graines dans les cases suivantes
    while graines > 0:
        current_cell += 1
        if current_cell == board_size:  # Si on atteint la fin du côté du joueur
            current_player = 1 - current_player  # Change de côté
            current_cell = 0
        
        board_copy[current_player][current_cell] += 1
        graines -= 1
    
    captured_seeds = 0
    # Capture les graines de l'adversaire si les conditions sont remplies
    while current_player != player and 0 <= current_cell < board_size and board_copy[current_player][current_cell] in (2, 3):
        captured_seeds += board_copy[current_player][current_cell]
        board_copy[current_player][current_cell] = 0
        current_cell -= 1
    
    # Met à jour le plateau original avec les modifications
    board[:] = board_copy
    
    return captured_seeds  # Retourne le nombre de graines capturées

def is_end(board, player: int) -> bool:
    """
    Vérifie si la partie est terminée pour le joueur courant.
    
    Parameters:
    board (list of list of int): Le plateau de jeu.
    player (int): Le joueur courant (0 ou 1).
    
    Returns:
    bool: True si la partie est terminée, False sinon.
    """
    if sum(board[player]) == 0:  # Si le joueur n'a plus de graines
        return True
    
    opponent_player = 1 - player
    for cell in range(len(board[player])):
        if board[player][cell] > 0:  # Si le joueur peut encore jouer
            board_copy = copy.deepcopy(board)
            play(board_copy, player, cell)
            if sum(board_copy[opponent_player]) > 0:  # Si l'adversaire peut encore jouer
                return False
    
    return True  # La partie est terminée si aucune condition précédente n'est remplie

def recursive_enum(current_board, current_player, current_depth, current_moves):
    """
    Énumère récursivement toutes les suites de coups possibles.
    
    Parameters:
    current_board (list of list of int): Le plateau de jeu courant.
    current_player (int): Le joueur courant (0 ou 1).
    current_depth (int): La profondeur actuelle de la recherche.
    current_moves (list of int): La liste des coups joués jusqu'à présent.
    
    Returns:
    list of tuple: Une liste de tuples contenant les séquences de coups et les scores associés.
    """
    valid_moves = [cell for cell in range(6) if current_board[current_player][cell] > 0]  # Liste des coups valides
    
    filtered_moves = []
    for cell in valid_moves:
        board_copy = copy.deepcopy(current_board)
        play(board_copy, current_player, cell)
        if not is_end(board_copy, 1 - current_player):  # Filtre les coups qui ne terminent pas la partie
            filtered_moves.append(cell)
    
    if not filtered_moves:
        return [(current_moves, 0)]  # Aucun coup valide, retourne la séquence actuelle
    
    if current_depth == 0:
        return [(current_moves, 0)]  # Profondeur maximale atteinte, retourne la séquence actuelle
    
    sequences = []
    for cell in filtered_moves:
        board_copy = copy.deepcopy(current_board)
        score_captured = play(board_copy, current_player, cell)
        adjusted_score = score_captured if current_player == 0 else -score_captured
        sub_sequences = recursive_enum(board_copy, 1 - current_player, current_depth - 1, current_moves + [cell])
        adjusted_sub_sequences = [(seq, score + adjusted_score) for seq, score in sub_sequences]
        sequences.extend(adjusted_sub_sequences)
    
    return sequences

def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
    """
    Énumère récursivement toutes les suites de coups possibles.
    
    Parameters:
    board (list of list of int): Le plateau de jeu.
    player (int): Le joueur courant (0 ou 1).
    depth (int): La profondeur maximale de la recherche.
    
    Returns:
    list of tuple: Une liste de tuples contenant les séquences de coups et les scores associés.
    """
    return recursive_enum(board, player, depth, [])

def suggest(board, player: int, depth: int) -> int:
    """
    Suggère le meilleur coup pour le joueur donné en utilisant MinMax.
    
    Parameters:
    board (list of list of int): Le plateau de jeu.
    player (int): Le joueur courant (0 ou 1).
    depth (int): La profondeur maximale de la recherche.
    
    Returns:
    int: Le meilleur coup suggéré (0 à 5), ou -1 si aucun coup valide n'est disponible.
    """
    def minmax(board, player, depth, maximizing_player):
        if depth == 0 or is_end(board, player):
            return 0  # Return 0 as a neutral score for terminal nodes
        
        valid_moves = [cell for cell in range(6) if board[player][cell] > 0]
        if not valid_moves:
            return 0  # No valid moves available
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                captured = play(board_copy, player, move)
                eval = captured + minmax(board_copy, 1 - player, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_copy = copy.deepcopy(board)
                captured = play(board_copy, player, move)
                eval = -captured + minmax(board_copy, 1 - player, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    best_move = -1
    best_score = float('-inf') if player == 0 else float('inf')
    valid_moves = [cell for cell in range(6) if board[player][cell] > 0]

    for move in valid_moves:
        board_copy = copy.deepcopy(board)
        captured = play(board_copy, player, move)
        score = captured + minmax(board_copy, 1 - player, depth - 1, player == 1)
        
        if (player == 0 and score > best_score) or (player == 1 and score < best_score):
            best_score = score
            best_move = move

    return best_move
