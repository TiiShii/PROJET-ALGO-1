import copy  # Importe le module copy pour la copie profonde

def play(board, player: int, cell: int) -> int:
    """
    Joue un coup pour le joueur à partir de la case donnée.
    
    Paramètres:
    board (list de list de int): Le plateau de jeu.
    player (int): Le joueur actuel (0 ou 1).
    cell (int): La case à partir de laquelle jouer (0 à 5).
    
    Retourne:
    int: Le nombre de graines capturées par le joueur.
    """
    if board[player][cell] == 0:
        return 0  # Si la case est vide, aucun coup ne peut être joué
    
    board_copy = copy.deepcopy(board)  # Crée une copie du plateau pour éviter de modifier l'original
    graines = board_copy[player][cell]  # Nombre de graines dans la case choisie
    board_copy[player][cell] = 0  # Vide la case choisie
    
    current_player, current_cell = player, cell  # Initialise le joueur et la case courante
    board_size = len(board[player])  # Taille du côté du plateau du joueur
    
    # Distribue les graines dans les cases suivantes
    while graines > 0:
        current_cell += 1  # Passe à la case suivante
        if current_cell == board_size:  # Si on atteint la fin du côté du joueur
            current_player = 1 - current_player  # Change de côté
            current_cell = 0  # Recommence à la première case
        
        board_copy[current_player][current_cell] += 1  # Ajoute une graine à la case courante
        graines -= 1  # Réduit le nombre de graines à distribuer
    
    captured_seeds = 0  # Initialise le nombre de graines capturées
    # Capture les graines de l'adversaire si les conditions sont remplies
    while current_player != player and 0 <= current_cell < board_size and board_copy[current_player][current_cell] in (2, 3):
        captured_seeds += board_copy[current_player][current_cell]  # Ajoute les graines capturées
        board_copy[current_player][current_cell] = 0  # Vide la case capturée
        current_cell -= 1  # Passe à la case précédente
    
    # Met à jour le plateau original avec les modifications
    board[:] = board_copy
    
    return captured_seeds  # Retourne le nombre de graines capturées

def is_end(board, player: int) -> bool:
    """
    Vérifie si la partie est terminée pour le joueur.
    
    Paramètres:
    board (list de list de int): Le plateau de jeu.
    player (int): Le joueur actuel (0 ou 1).
    
    Retourne:
    bool: True si la partie est terminée, False sinon.
    """
    if sum(board[player]) == 0:  # Si le joueur n'a plus de graines
        return True
    
    opponent_player = 1 - player  # Identifie l'adversaire
    for cell in range(len(board[player])):  # Parcourt les cases du joueur
        if board[player][cell] > 0:  # Si le joueur peut encore jouer
            board_copy = copy.deepcopy(board)  # Crée une copie du plateau
            play(board_copy, player, cell)  # Joue un coup hypothétique
            if sum(board_copy[opponent_player]) > 0:  # Si l'adversaire peut encore jouer
                return False
    
    return True  # La partie est terminée si aucune condition précédente n'est remplie

def recursive_enum(current_board, current_player, current_depth, current_moves):
    """
    Énumère récursivement toutes les suites de coups possibles.
    
    Paramètres:
    current_board (list de list de int): Le plateau de jeu actuel.
    current_player (int): Le joueur actuel (0 ou 1).
    current_depth (int): La profondeur actuelle de la recherche.
    current_moves (list de int): La liste des coups joués jusqu'à présent.
    
    Retourne:
    list de tuple: Une liste de tuples contenant les séquences de coups et les scores associés.
    """
    valid_moves = [cell for cell in range(6) if current_board[current_player][cell] > 0]  # Liste des coups valides
    
    filtered_moves = []
    for cell in valid_moves:
        board_copy = copy.deepcopy(current_board)  # Crée une copie du plateau
        play(board_copy, current_player, cell)  # Joue un coup hypothétique
        if not is_end(board_copy, 1 - current_player):  # Filtre les coups qui ne terminent pas la partie
            filtered_moves.append(cell)
    
    if not filtered_moves:
        return [(current_moves, 0)]  # Aucun coup valide, retourne la séquence actuelle
    
    if current_depth == 0:
        return [(current_moves, 0)]  # Profondeur maximale atteinte, retourne la séquence actuelle
    
    sequences = []
    for cell in filtered_moves:
        board_copy = copy.deepcopy(current_board)  # Crée une copie du plateau
        score_captured = play(board_copy, current_player, cell)  # Joue un coup hypothétique et capture les graines
        adjusted_score = score_captured if current_player == 0 else -score_captured  # Ajuste le score en fonction du joueur
        sub_sequences = recursive_enum(board_copy, 1 - current_player, current_depth - 1, current_moves + [cell])  # Énumère récursivement les sous-séquences
        adjusted_sub_sequences = [(seq, score + adjusted_score) for seq, score in sub_sequences]  # Ajuste les scores des sous-séquences
        sequences.extend(adjusted_sub_sequences)  # Ajoute les sous-séquences à la liste des séquences
    
    return sequences

def enum(board, player: int, depth: int) -> list[tuple[list[int], int]]:
    """
    Énumère récursivement toutes les suites de coups possibles.
    
    Paramètres:
    board (list de list de int): Le plateau de jeu.
    player (int): Le joueur actuel (0 ou 1).
    depth (int): La profondeur maximale de la recherche.
    
    Retourne:
    list de tuple: Une liste de tuples contenant les séquences de coups et les scores associés.
    """
    return recursive_enum(board, player, depth, [])  # Appelle la fonction récursive avec les paramètres initiaux

def suggest(board, player: int, depth: int) -> int:
    """
    Suggère le meilleur coup pour le joueur en utilisant MinMax.
    
    Paramètres:
    board (list de list de int): Le plateau de jeu.
    player (int): Le joueur actuel (0 ou 1).
    depth (int): La profondeur maximale de la recherche.
    
    Retourne:
    int: Le meilleur coup suggéré (0 à 5), ou -1 si aucun coup valide n'est disponible.
    """
    def minmax(board, player, depth, maximizing_player):
        if depth == 0 or is_end(board, player):
            return 0  # Retourne 0 comme score neutre pour les nœuds terminaux
        
        valid_moves = [cell for cell in range(6) if board[player][cell] > 0]  # Liste des coups valides
        if not valid_moves:
            return 0  # Aucun coup valide disponible
        
        if maximizing_player:
            max_eval = float('-inf')  # Initialise l'évaluation maximale
            for move in valid_moves:
                board_copy = copy.deepcopy(board)  # Crée une copie du plateau
                captured = play(board_copy, player, move)  # Joue un coup hypothétique et capture les graines
                if sum(board_copy[1 - player]) == 0:  # Vérifie la famine
                    continue  # Ignore ce coup s'il affame l'adversaire
                eval = captured + minmax(board_copy, 1 - player, depth - 1, False)  # Évalue le coup en appelant récursivement minmax
                max_eval = max(max_eval, eval)  # Met à jour l'évaluation maximale
            return max_eval
        else:
            min_eval = float('inf')  # Initialise l'évaluation minimale
            for move in valid_moves:
                board_copy = copy.deepcopy(board)  # Crée une copie du plateau
                captured = play(board_copy, player, move)  # Joue un coup hypothétique et capture les graines
                if sum(board_copy[1 - player]) == 0:  # Vérifie la famine
                    continue  # Ignore ce coup s'il affame l'adversaire
                eval = -captured + minmax(board_copy, 1 - player, depth - 1, True)  # Évalue le coup en appelant récursivement minmax
                min_eval = min(min_eval, eval)  # Met à jour l'évaluation minimale
            return min_eval

    best_move = -1  # Initialise le meilleur coup
    best_score = float('-inf') if player == 0 else float('inf')  # Initialise le meilleur score en fonction du joueur
    valid_moves = [cell for cell in range(6) if board[player][cell] > 0]  # Liste des coups valides

    for move in valid_moves:
        board_copy = copy.deepcopy(board)  # Crée une copie du plateau
        captured = play(board_copy, player, move)  # Joue un coup hypothétique et capture les graines
        if sum(board_copy[1 - player]) == 0:  # Vérifie la famine
            continue  # Ignore ce coup s'il affame l'adversaire
        score = captured + minmax(board_copy, 1 - player, depth - 1, player == 1)  # Évalue le coup en appelant minmax
        
        if (player == 0 and score > best_score) or (player == 1 and score < best_score):  # Met à jour le meilleur coup et le meilleur score
            best_score = score
            best_move = move

    return best_move  # Retourne le meilleur coup suggéré

