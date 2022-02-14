import random
#import win32api,win32gui,win32con #鼠标操作

# ------- START my_print ------
import os
import sys  
from datetime import datetime
str_now = None
is_write_to_console = True
is_write_to_file = True
# ------------------------------
def my_print(*args, **kwargs):
    global is_write_to_console
    if is_write_to_console:
        print(*args, **kwargs)
    global is_write_to_file
    if is_write_to_file:
        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')
            orig_stdout = sys.stdout
            global str_now
            if str_now is None:
                now = datetime.now()
                str_now = "_".join([str(now.year), str(now.month), 
                        str(now.day), str(now.hour), str(now.minute), 
                        str(now.second)])
            f = open("".join(
                ["logs/", "_".join(["log", str_now]), ".txt"]), "a")
            sys.stdout = f
            print(*args, **kwargs)
            sys.stdout = orig_stdout
            f.close()
        except:
            pass
# ------- END   my_print ------
class Memo:
    def __init__(self):
        self._category_list = ["Ones", "Twos", "Threes", "Fours", "Fives", 
                           "Sixs","Three of a kind", "Four of a kind", 
                           "Full House", "Small Straight", "Large Straight", 
                           "Chance", "Yahtzee"]
        self._possible_list = [0] * 13
        self._score_list = [None] * 13
        self._bonus = 0
        self._total = 0

    @property
    def category_list(self):
        return self._category_list

    @property
    def possible_list(self):
        return self._possible_list
    
    @property
    def score_list(self):
        return self._score_list

    @property
    def bonus(self):
        return self._bonus
    
    @property
    def total(self):
        return self._total
    
    def refresh_possible_list(self, dice_list):
        dice_count_list = list(map(lambda dice_num: 
           dice_list.count(dice_num), list(range(1,7))))
        # UPPER SCORE
        # 0 - 5: Ones, Twos, Threes, Fours, Fives, Sixs
        for category_id in range(0,6):
            self._possible_list[category_id] = dice_count_list[category_id
               ] * (category_id + 1)
            
        # LOWER SCORE
        # 6: Three of a kind
        self._possible_list[6] = [0, sum(dice_list)][int(
            max(dice_count_list)>=3)]
            
        # 7: Four of a kind
        self._possible_list[7] = [0, sum(dice_list)][int(
            max(dice_count_list)>=4)]
            
        # 8: Full house
        self._possible_list[8] = [0, 25][int(
            sorted(dice_count_list, reverse=True)[0:2] == [3,2])]
            
        # 9: Small straight
        self._possible_list[9] = [0, 30][int(
            any(list(map(lambda straight_set: 
                            straight_set.issubset(set(dice_list)), 
                        [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}])))
                )]
        # 10: Large stright
        self._possible_list[10] = [0, 40][int(
            any(list(map(lambda straight_set: 
                            straight_set.issubset(set(dice_list)), 
                        [{1,2,3,4,5}, {2,3,4,5,6}])))
                )]
        # 11: Chance
        self._possible_list[11] = sum(dice_list)
        
        # 12: Yahtzee
        self._possible_list[12] = [0, 50][int(
            max(dice_count_list)== 5)]
    
    def refresh_score_list(self, category_id): # including yahtzee bonus
        if self._possible_list[12] and self._score_list [12] == 50: # Additional yahtzee
            self._score_list[12] += 100
        self._score_list[category_id] = self._possible_list[category_id]
        self._possible_list = [0] * len(self._category_list)
    
    def refresh_bonus_and_total(self):# 加总和的时候注意None, 可以用list comprehension + lambda表达式完成 
        upperscore = sum(filter(None,self._score_list[0:6]))
        self._bonus = 35 if upperscore >=63 else 0
        self._total = sum(filter(None, self._score_list)) + self._bonus
        
    def reset(self):
        self._possible_list = [0] * len(self._category_list)
        self._score_list = [None] * len(self._category_list)
        self._bonus = 0
        self._total = 0


class Player:
    def __init__(self, name):
        self._name = name
        self._memo = Memo()
        self._score = 0

    @property
    def name(self):
        return self._name

    @property
    def memo(self):
        return self._memo

    @property
    def score(self):
        return self._score
    
    
    def reverse_status(self, status_list, dice_id):
        status_list[dice_id] = not status_list[dice_id]
           
    def roll_dice(self, dice_list, status_list):
        for dice_number in range(len(dice_list)):
            if status_list[dice_number] == True:
                dice_list[dice_number] = random.randint(1,6)
        self._memo.refresh_possible_list(dice_list)
        
    def choose_category(self, category_id):
        self._memo.refresh_score_list(category_id)
        self._memo.refresh_bonus_and_total()
        self._score = self._memo.total
        
    def reset(self):
        self._memo.reset()
        self._score = 0
            
class Arena:
    def __init__(self):
        self._player_list = [] # of class Player
        self._max_turn = 13
        self._max_chance = 3
        self._dice_list = [0, 0, 0, 0, 0]
        self._status_list = [True] * 5
        self._player_id = None
        self._turn = 13
        self._chance = 3
        self._winner_list = None
        self._click = None # 
        
    @property
    def player_list(self):
        return self._player_list
    
    @property
    def dice_list(self):
        return self._dice_list
    
    @property
    def status_list(self):
        return self._status_list
    
    @property
    def click(self):
        return self._click
    
    @property
    def turn(self):
        return self._turn
    
    @property
    def player_id(self):
        return self._player_id
    
    @property
    def chance(self):
        return self._chance
    
    @property
    def max_chance(self):
        return self._max_chance
    
    @property
    def max_turn(self):
        return self._max_turn
    
    @property
    def winner_list(self):
        return self._winner_list
      
    def add_player(self, player_name):
        self._player_list.append(Player(player_name))
        my_print("Player", player_name, "added")  
        
    def start(self): #initialize all Parameters
        my_print("\n########## START YAHTZEE ##########")
        self._dice_list = list(range(1,6))
        self._status_list = [True] * len(self._dice_list)
        self._click = 0
        self._turn = 0
        self._player_id = 0
        self._chance = 0
        self._winner_list = None
        self.print_next_step_info()
                
    
    def execute(self, option, option_arg=None): 
        self._click += 1
        if self._turn == self._max_turn:
            my_print("\nNo action is available")
        else:
            my_print("\nACTION ", self._click , ": ", 
             self._player_list[self._player_id].name, " is ", 
              ["reversing dice status", "rolling dices", 
            "choosing category"][option], " --> ", sep="", end="")
            if option == 0: # 0: alter is active dice
                if self._chance == 0: # reverse dice status only after the first chance
                    my_print(
                        "Reversing dice status not possible: dices not rolled")
                else:
                    self._player_list[self._player_id].reverse_status(
                        self._status_list, option_arg)
                    self.print_dice_list(True)
            elif option == 1: # 1: roll dice
                if self._chance >= self._max_chance:
                    my_print("Rolling dices not possible: all chances used")
                else:
                    if self._status_list == [False] * len(
                            self._dice_list):
                         my_print(
                             "Rolling dices not possible: no dices is active")  
                    else:
                        self._player_list[self._player_id].roll_dice(
                                self._dice_list, self._status_list)
                        self.print_dice_list()
                        self._chance += 1
            elif option == 2: # 2: choose score
                if not self._player_list[
                    self._player_id].memo.score_list[option_arg] == None:
                    my_print("Choosing category not possible: already chosen")
                else:
                    if self.chance == 0:
                        my_print(
                            "Choosing category not possible: dices not rolled")
                    else:
                        self._player_list[self._player_id].choose_category(
                            option_arg)
                        my_print(Memo().category_list[option_arg] + " (+" + 
                          str(self._player_list[
                              self._player_id].memo.score_list[option_arg]) + 
                          ")")
                        self._status_list = [True] * len(self._dice_list)
                        if self._player_id == len(self._player_list) - 1:
                            self._turn += 1
                        self._player_id = (self._player_id + 1) % len(
                                self._player_list)
                        self._chance = 0 # reset chance
        self.print_next_step_info()
        

    def end(self):
        my_print("\n********** RESULT **********")
        self.print_all_player_information()
        self.decide_winner_list()
        winner_name_list = [winner.name + ", " for winner in self._winner_list]
        str_winner_name_list = "".join(winner_name_list)[0:-2]
        my_print("\nThe winner is", str_winner_name_list)
        my_print("\n########## END   YAHTZEE ##########")
    
    def restart(self):
        my_print("\n########## RESTART YAHTZEE ##########...")
        for player in self._player_list:
            player.reset()
        self.start()
    
    def decide_winner_list(self):
        max_player = max(
                self._player_list, key=lambda player: player.score)
        self._winner_list = [player for player in self._player_list 
                       if player.score == max_player.score]
            
    def auto_play(self, player_name_list):
        for player_name in player_name_list:
            self.add_player(player_name)
        self.start()
        while self._turn < self._max_turn:
            option = random.randrange(0, 3)
            if option == 0:
                option_id = random.randrange(0, len(self._dice_list))
            elif option == 1:
                option_id = None
            elif option == 2:
                option_id = random.randrange(0, len(Memo().category_list))
            self.execute(option, option_id)
            #import time
            #time.sleep(0.001)
        self.end()

    def print_next_step_info(self):
        if self._turn < self._max_turn:
            my_print("")
            my_print("Executed click: ", self._click, sep="")
            my_print("Current turn: ", self._turn + 1, sep="")
            my_print("Current player: ", 
                 self._player_list[self._player_id].name, 
                  " (", (self._player_id + 1),  "/", len(self._player_list) , 
                  ")", sep="")
            my_print("Left Chance: ", self._max_chance - self._chance, sep="")
            self.print_dice_list()
            self.print_dice_list(True)
            self.print_all_player_information()
            self.print_current_player_information(
                    self._player_list[self._player_id])   
    
    def print_dice_list(self, only_active=False):
        if only_active:
            dice_list = [self._dice_list[dice_num] 
                            if status else "-" 
                         for dice_num, status in 
                             enumerate(self._status_list)]
        else:
            dice_list = self._dice_list
        str_dice_list = ("[" + ", ".join([str(dice) for dice in dice_list])
            + "]")
        my_print(
            ["Current dices:", "Active dices: "][int(only_active)], 
            str_dice_list)

    def print_all_player_information(self):
        self.print_table(15, ["All score lists", 
              *[player.name for player in self._player_list]], 
            [Memo().category_list, 
             *[["None" if score is None else score 
                for score in player.memo.score_list]
            for player in self._player_list]],
            ["Bonus", *[player.memo.bonus for player in self._player_list]],
            ["Total", *[player.memo.total for player in self._player_list]])
        
    def print_current_player_information(self, player):        
        self.print_table(15, 
            [player.name, "Possible list", "Score list"], 
            [Memo().category_list, player.memo.possible_list, 
             ["None" if score is None else score 
                   for score in player.memo.score_list]],
            ["Bonus", "-", player.memo.bonus],
            ["Total", "-", player.memo.total])
        
    def print_table(self, length_name, name_column, category_column, # category_column contains many category_list
                    bonus_column, total_column):
        str_bonus = bonus_column[0]
        str_total = total_column[0]
        length_line = (length_name + 2) + (sum(map(lambda category_list: 
            len(category_list), category_column[0])) + 
            len(category_column[0])) + (len(str_bonus) + len(str_total) + 3)
        my_print("=" * length_line)
        for line in range(0,len(name_column)):
            my_print(("{:<" + str(length_name) + "}||" + 
             self.print_category_format() + "|{:>" + str(len(str_bonus)) + 
             "}||{:>" + str(len(str_total)) + "}").format(name_column[line], 
             *category_column[line], bonus_column[line], total_column[line]))
            if line == 0:
                my_print("-" * length_line)
        my_print("=" * length_line)
        
    def print_category_format(self):
        str_category_format = []
        for category in Memo().category_list:
            str_category_format.append("{:>" + str(len(category)) + "}|")
        return "".join(str_category_format)
    '''class Exceute():
        
        #鼠标的点击
        def clickLeftCur():
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|
                                 win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            
        #鼠标的移动
        def moveCurPos(x,y):
            windll.user32.SetCursorPos(x, y)
            
        #鼠标当前坐标
        def getCurPos():
            return win32gui.GetCursorPos()
        
    '''

def main():
    arena = Arena()
    arena.auto_play(["Dacy", "Daniel", "David"])
    
    
if __name__ == "__main__":
    main()    
 
    

    
    
    

