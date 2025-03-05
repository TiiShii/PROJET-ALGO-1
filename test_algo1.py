from copy import deepcopy
import os


# Génère un fichier '__test__.py' pour importer vos fonctions
with open("__test__.py", "w+") as init:
  for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and file not in ("__test__.py", __file__.split('/')[-1]):
      init.write(f"from {file[:-3]} import *\n")


from __test__ import *



# Différents plateaux de test

BOARD1 = [ [1,7,2,7,2,0],
           [0,3,4,2,2,5] ]

BOARD2 = [ [1,1,4,0,5,1],
           [2,5,0,0,1,3] ]

BOARD3 = [ [0,1,0,10,4,1],
           [0,2,3,0,16,0] ]

BOARD4 = [ [0,1,2,0,4,0],
           [0,0,0,0,0,0] ]

BOARD5 = [ [0,0,0,0,4,1],
           [1,0,0,0,0,0] ]



def test_move_j1_score2():
  board = deepcopy(BOARD1)
  score = play(board, 0, 3)
  assert score == 6, "Mauvais score si le joueur 1 joue 'd'"
  assert board == [ [1,7,2,0,3,1],
                    [1,4,5,0,0,5] ], "Mauvais plateau final si le joueur 1 joue 'd'"


def test_move_j2_nopass():
  board = deepcopy(BOARD1)
  score = play(board, 1, 1)
  assert score == 0, "Mauvais score si le joueur 2 joue 'h'"
  assert board == [ [1,7,2,7,2,0],
                    [0,0,5,3,3,5] ], "Mauvais plateau final si le joueur 2 joue 'h'"


def test_move_j1_noscore():
  board = deepcopy(BOARD1)
  score = play(board, 0, 4)
  assert score == 0, "Mauvais score si le joueur 1 joue 'e'"
  assert board == [ [1,7,2,7,0,1],
                    [1,3,4,2,2,5] ], "Mauvais plateau final si le joueur 1 joue 'e'"


def test_move_j1_nopass():
  board = deepcopy(BOARD2)
  score = play(board, 0, 0)
  assert score == 0, "Mauvais score si le joueur 1 joue 'a' sur le 2e plateau"
  assert board == [ [0,2,4,0,5,1],
                    [2,5,0,0,1,3] ], "Mauvais plateau final si le joueur 1 joue 'd' sur le 2e plateau"


def test_move_j2_score1():
  board = deepcopy(BOARD2)
  score = play(board, 1, 1)
  assert score == 2, "Mauvais score si le joueur 2 joue 'h' sur le 2e plateau"
  assert board == [ [0,1,4,0,5,1],
                    [2,0,1,1,2,4] ], "Mauvais plateau final si le joueur 2 joue 'h' sur le 2e plateau"


def test_move_j2_noscore():
  board = deepcopy(BOARD2)
  score = play(board, 1, 5)
  assert score == 0, "Mauvais score si le joueur 2 joue 'g' sur le 2e plateau"
  assert board == [ [2,2,5,0,5,1],
                    [2,5,0,0,1,0] ], "Mauvais plateau final si le joueur 2 joue 'g' sur le 2e plateau"


def test_move_j1_noscore_row1():
  board = deepcopy(BOARD3)
  score = play(board, 0, 3)
  assert score == 0, "Mauvais score si le joueur 1 joue 'd' sur le 3e plateau"
  assert board == [ [1,2,0,0,5,2],
                    [1,3,4,1,17,1] ], "Mauvais plateau final si le joueur 1 joue 'd' sur le 3e plateau"


def test_move_j2_score3_row2():
  board = deepcopy(BOARD3)
  score = play(board, 1, 4)
  assert score == 7, "Mauvais score si le joueur 2 joue 'e' sur le 3e plateau"
  assert board == [ [0,0,0,11,5,2],
                    [1,3,4,1,1,2] ], "Mauvais plateau final si le joueur 2 joue 'e' sur le 3e plateau"



def test_end_j1_false():
  board = deepcopy(BOARD1)
  assert not is_end(board, 0), "Le 1er plateau n'est pas une fin de partie"


def test_end_j1_false_starving():
  board = deepcopy(BOARD4)
  assert not is_end(board, 0), "Le 4e plateau n'est pas une fin de partie si c'est le tour du joueur 1"


def test_end_j2_true():
  board = deepcopy(BOARD4)
  assert is_end(board, 1), "Le 4e plateau est une fin de partie si c'est le tour du joueur 2"


def test_end_j2_false_starving():
  board = deepcopy(BOARD4[::-1])
  assert not is_end(board, 1), "Le 4e plateau (inversé) n'est pas une fin de partie si c'est le tour du joueur 2"


def test_end_j1_true():
  board = deepcopy(BOARD4[::-1])
  assert is_end(board, 0), "Le 4e plateau (inversé) est une fin de partie si c'est le tour du joueur 1"



def enum_to_dict(seqs):
  return { tuple(moves): score for (moves, score) in seqs }



def test_enum_p1_depth1():
  board = deepcopy(BOARD1)
  seqs = enum(board, 0, 1)
  assert sorted(seqs) == [([0], 0), ([1], 0), ([2], 0), ([3], 6), ([4], 0)], "Un ou plusieurs des coups énumérés et leurs scores sont erronés"


def test_enum_p2_depth1():
  board = deepcopy(BOARD1)
  seqs = enum(board, 1, 1)
  assert sorted(seqs) == [([1], 0), ([2], -2), ([3], 0), ([4], -2), ([5], -3)], "Un ou plusieurs des coups énumérés et leurs scores sont erronés"


def test_enum_p1_depth1_starving1():
  board = deepcopy(BOARD4)
  seqs = enum(board, 0, 1)
  assert sorted(seqs) == [([4], 0)], "Seul le coup 'e' est valide pour ne pas affamer le joueur 2"


def test_enum_p1_depth1_starving2():
  board = deepcopy(BOARD5)
  seqs = enum(board, 0, 1)
  assert sorted(seqs) == [([4], 0)], "Le coup 'f' est invalide car il affamerait le joueur 2"


def test_enum_p2_depth1_starving1():
  board = deepcopy(BOARD4[::-1])
  seqs = enum(board, 1, 1)
  assert sorted(seqs) == [([4], 0)], "Seul le coup 'k' est valide pour ne pas affamer le joueur 1"


def test_enum_p2_depth1_starving2():
  board = deepcopy(BOARD5[::-1])
  seqs = enum(board, 1, 1)
  assert sorted(seqs) == [([4], 0)], "Le coup 'l' est invalide car il affamerait le joueur 1"


def test_enum_p1_depth2():
  board = deepcopy(BOARD2)
  seqs = enum(board, 0, 2)
  assert sorted(seqs) == [([0, 0], 0), ([0, 1], 0), ([0, 4], 0), ([0, 5], 0), ([1, 0], 0), ([1, 1], -2), ([1, 4], 0), ([1, 5], 0), ([2, 1], 1), ([2, 4], 3), ([2, 5], 3), ([4, 0], 0), ([4, 1], -4), ([4, 2], 0), ([4, 3], 0), ([4, 4], 0), ([4, 5], 0), ([5, 1], 1), ([5, 4], 3), ([5, 5], 3)], "Un ou plusieurs des coups énumérés et leurs scores sont erronés"


def test_enum_p2_depth2():
  board = deepcopy(BOARD2)
  seqs = enum(board, 1, 2)
  assert sorted(seqs) == [([0, 0], 0), ([0, 1], 0), ([0, 2], 0), ([0, 4], 0), ([0, 5], 0), ([1, 1], -2), ([1, 2], 1), ([1, 4], 2), ([1, 5], 1), ([4, 0], 0), ([4, 1], 0), ([4, 2], 3), ([4, 4], 0), ([4, 5], 3), ([5, 0], 0), ([5, 1], 0), ([5, 2], 0), ([5, 4], 0), ([5, 5], 3)], "Un ou plusieurs des coups énumérés et leurs scores sont erronés"


def test_enum_p1_depth4():
  board = deepcopy(BOARD1)
  seqs = enum(board, 0, 4)
  assert len(seqs) == 596, "Tous les coups n'ont pas été énumérés."
  seqs = enum_to_dict(seqs)
  assert seqs[(3,1,5,2)] == 5, "Le score du chemin (3,1,5,2) n'est pas correct"
  assert seqs[(0, 1, 1, 0)] == 0, "Le score du chemin (0,1,1,0) n'est pas correct"
  assert seqs[(0, 1, 3, 2)] == -3, "Le score du chemin (0,1,3,2) n'est pas correct"
  assert seqs[(1, 0, 4, 4)] == -2, "Le score du chemin (1,0,4,4) n'est pas correct"
  assert seqs[(4, 1, 0, 4)] == 0, "Le score du chemin (4,1,0,4) n'est pas correct"



def test_suggest_p1_depth1():
  board = deepcopy(BOARD1)
  assert suggest(board, 0, 1) == 3, "Le meilleur coup pour le joueur 1 est la case 'c'"


def test_suggest_p1_depth1_starving1():
  board = deepcopy(BOARD4)
  assert suggest(board, 0, 1) == 4, "Seul le coup 'e' est valide pour ne pas affamer le joueur 2"


def test_suggest_p1_depth1_starving2():
  board = deepcopy(BOARD5)
  assert suggest(board, 0, 1) == 4, "Le coup 'f' est invalide car il affamerait le joueur 2"


def test_suggest_p1_depth2():
  board = deepcopy(BOARD3)
  assert suggest(board, 0, 2) == 3, "Le coup le moins pire pour le joueur 1 est 'd'"


def test_suggest_p1_depth4():
  board = deepcopy(BOARD1)
  assert suggest(board, 0, 4) == 3, "Le meilleur coup pour le joueur 1 est 'd'"


def test_suggest_p1_depth8():
  board = deepcopy(BOARD3)
  assert suggest(board, 0, 4) == 3, "Le meilleur coup pour le joueur 1 est 'd' pour une profondeur de 4"
  assert suggest(board, 0, 8) == 5, "Le meilleur coup pour le joueur 1 est 'f' pour une profondeur de 8"
