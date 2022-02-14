# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 23:21:16 2020

@author: Huitian, YU
"""

import unittest
from unittest.mock import patch
import random
import yahtzee
yahtzee.is_write_to_console = False
yahtzee.is_write_to_file = False

class NewMemo(yahtzee.Memo):
    def __init__(self):
        super().__init__()
        self._category_list.append("Two of a kind")
        self._category_list.append("Doubled two of a kind")
        self._score_list = [None] * len(self._category_list)
        self._possible_list = [0] * len(self._category_list)
        
    def refresh_possible_list(self, dice_list_ref):
        super().refresh_possible_list(dice_list_ref)
        dice_quantity_list = list(map(lambda dice_num: 
            dice_list_ref.count(dice_num), list(range(1,7))))
            
         # 13: Two of a kind
        self._possible_list[13] = [0, max(map(lambda i, x: i if x >= 2 else 0, 
            range(1,7), dice_quantity_list)) 
          * dice_list_ref.count(max(map(lambda i, x: i if x >= 2 else 0, 
            range(1,7), dice_quantity_list)))][
          int(any(map(lambda x: x >= 2, dice_quantity_list)))]
                
        # 14: Doubled two of a kind
        self._possible_list[14] = [0, sum(map(lambda x, y: x * y, 
            map(lambda x: x if x >= 2 else 0, dice_quantity_list), 
            range(1, 7)))][int(len(list(filter(lambda x: x >= 2, 
            dice_quantity_list)))) == 2]
        

class TestYahtzee(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('\nsetUpClass')
    
    @classmethod
    def tearDownClass(cls):
        print('\ntearDownClass')
    
    def setUp(self):    # initialize variables
        print('\nsetUp')
    
    def tearDown(self):    # delete variables
        print('\ntearDown')
        
    """
    def test_method(self):
        self.assertEqual(classObject.method(*args, **kwargs), value)
        
        with self.assertRaises(TypeError):
            classObject.method(*args, **kwargs)
    """
        
    # mocking ...
    
    # Test 1
    def test_memo_refresh_possible_list(self):
        memo = yahtzee.Memo()
        dice_list = [1, 1, 2, 2, 2]
        memo.refresh_possible_list(dice_list)
        result_possible_list = [2, 6, 0, 0, 0, 0, 8, 0, 25, 0, 0, 8, 0]
        for category_id in range(len(memo.category_list)):
            self.assertEqual(memo.possible_list[category_id],
                             result_possible_list[category_id])
    
    # Test 2
    def test_memo_refresh_score_list(self):
        memo = yahtzee.Memo()
        category_id = 3
        memo._score_list = [2, None, None, None, 10, None, 12, None, None, 
                            30, None, 50, None]
        memo._possible_list = [2, 6, 0, 8, 0, 0, 8, 0, 25, 0, 0, 8, 0]
        memo.refresh_score_list(category_id)
        result_score_list = [2, None, None, 8, 10, None, 12, None, None, 
                             30, None, 50, None]
        for category_nr in range(len(memo.category_list)):
            self.assertEqual(memo.score_list[category_nr],
                             result_score_list[category_nr])
        
    # Test 3
    def test_memo_refresh_bonus_and_total(self):
        memo = yahtzee.Memo()
        memo._bonus = 0
        memo._total = 122
        memo._score_list = [3, 16, 15, 12, 10, 24, 12, None, None, 30, None, 
                            50, None]
        memo.refresh_bonus_and_total()
        result_bonus = 35
        result_total = 207
        self.assertEqual(memo.total,result_total)
        self.assertEqual(memo.bonus,result_bonus)
        
        memo._bonus = 35
        memo._total = 122
        memo._score_list = [3, 16, 15, 12, 10, 24, 12, None, None, 30, None, 
                            50, None]
        memo.refresh_bonus_and_total()
        result_bonus = 35
        result_total = 207
        self.assertEqual(memo.total,result_total)
        self.assertEqual(memo.bonus,result_bonus)
        
    # Test 4
    def test_player_reverse_status(self):
        player = yahtzee.Player("Anna")
        status_list = [True,True,True,False,True]
        dice_id = 2
        player.reverse_status(status_list, dice_id)
        result_status_list = [True,True,False,False,True]
        self.assertEqual(status_list,result_status_list)
    
    # Test 5
    def test_player_roll_dice(self):
        player = yahtzee.Player("Dacy")
        dice_list = list(range(1,6))
        status_list_list = [[True, False, False, False, False],
                            [False, True, False, False, False],
                            [False, False, True, False, False],
                            [False, False, False, True, False],
                            [False, False, False, False, True]]
        for status_list in status_list_list:
            dice_list_old = dice_list
            player.roll_dice(dice_list, status_list)
            self.assertEqual(
                [dice for i, dice in enumerate(dice_list) if status_list[i]],
                [dice for i, dice in enumerate(dice_list_old) 
                 if status_list[i]])
    
    # Test 6
    def test_player_choose_category(self):
        player = yahtzee.Player("Anna")
        category_id = 5
        player._score = 104
        player.memo._bonus = 0
        player.memo._score_list = [2, None, None, None, 10, None, 12, None, 
                                   None, 30, None, 50, None]
        player.memo._possible_list = [2, 6, 0, 8, 0, 18, 8, 0, 25, 0, 0, 8, 0]
        player.choose_category(category_id)
        result_score_list = [2, None, None, None, 10, 18, 12, None, None, 30, 
                             None, 50, None]
        result_score = 122
        result_bonus = 0
        self.assertEqual(player.memo.score_list,result_score_list)
        self.assertEqual(player.score,result_score)
        self.assertEqual(player.memo.bonus,result_bonus)
        
    # Test 7
    def test_arena_add_player(self):
        arena = yahtzee.Arena()
        arena._player_list = [yahtzee.Player("Square"), 
                              yahtzee.Player("Sky")]
        arena.add_player("Chess")
        result_player_name_list = ["Square", "Sky","Chess"]
        self.assertEqual([player.name for player in arena.player_list], 
                         result_player_name_list)

    # Test 8
    def test_arena_decide_winner_list(self):
        arena = yahtzee.Arena()
        arena._player_list = [yahtzee.Player("Square"),
              yahtzee.Player("Sky"), yahtzee.Player("Chess")]
        player1 = arena.player_list[0]
        player2 = arena.player_list[1]
        player3 = arena.player_list[2]
        player1._score = 157
        player2._score = 157
        player3._score = 156
        arena.decide_winner_list()
        self.assertIn(player1, arena.winner_list)
        self.assertIn(player2, arena.winner_list)
        
    # Test 9
    def test_arena_execute(self):
        arena = yahtzee.Arena()
        name_list = ["Dacy", "Daniel", "David"]
        for name in name_list:
            arena.add_player(name)
        arena.start()
        
        arena._status_list = [True, True, True, True, True]
        arena._chance = 1
        arena.execute(0, 1)
        self.assertEqual(arena.status_list, [True, False, True, True, True])
        
        arena._status_list = [True, True, True, True, True]
        arena._chance = 0
        arena.execute(0, 1)
        self.assertEqual(arena.status_list, [True, True, True, True, True])    
        
        arena._dice_list = list(range(1, 6))
        arena._status_list = [False, False, True, False, True]
        arena._chance = 0
        arena._player_id = 0
        dice_list_old  = arena.dice_list
        arena.execute(1)
        self.assertEqual([dice for i, dice in enumerate(arena.dice_list) 
                          if arena.status_list[i]], 
                         [dice for i, dice in enumerate(dice_list_old) 
                          if arena.status_list[i]])
        
        arena._dice_list = list(range(1, 6))
        arena._status_list = [False, False, True, False, True]
        arena._chance = 3
        arena._player_id = 0
        dice_list_old  = arena.dice_list
        arena.execute(1)
        self.assertEqual(dice_list_old, arena.dice_list)
        
        arena._dice_list = list(range(1, 6))
        arena._status_list = [False, False, False, False, False]
        arena._chance = 2
        arena._player_id = 0
        dice_list_old  = arena.dice_list
        arena.execute(1)
        self.assertEqual(dice_list_old, arena.dice_list)
        
        arena._chance = 1
        arena._player_id = 0
        arena.player_list[arena.player_id].memo._possible_list[1] = 8
        arena.execute(2, 1)
        self.assertEqual(arena.player_list[0].memo.score_list[1], 8)
        
        arena._chance = 0
        arena._player_id = 0
        arena.player_list[arena.player_id].memo._score_list[1] = None
        arena.execute(2, 1)
        self.assertEqual(arena.player_list[0].memo.score_list[1], None)
        
        arena._chance = 3
        arena._player_id = 0
        arena.player_list[arena.player_id].memo._score_list[1] = 1
        arena.execute(2, 1)
        self.assertEqual(arena.player_list[0].memo.score_list[1], 1)
        
    
    # Test
    @patch("yahtzee.Memo", NewMemo)
    def test_additional_category(self):
        arena = yahtzee.Arena()
        arena.add_player("Dacy")
        dice_list = [1, 1, 1, 2, 2]
        arena.player_list[0].memo.refresh_possible_list(dice_list)
        self.assertEqual(arena.player_list[0].memo.possible_list[13], 4)
        self.assertEqual(arena.player_list[0].memo.possible_list[14], 7)
    
    

if __name__ == "__main__":
    unittest.main()
