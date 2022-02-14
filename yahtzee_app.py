# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:54:47 2020

@author: Huitian, YU
"""

import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPixmap
import yahtzee

yahtzee.is_write_to_console = False
yahtzee.is_write_to_file = False

Ui_MainWindow_login, WindowBaseClass_login = uic.loadUiType(
        "uis/login.ui")
Ui_MainWindow_play, WindowBaseClass_play = uic.loadUiType(
    "uis/play.ui")

class My_StartDialog(WindowBaseClass_login, Ui_MainWindow_login):
    
    def __init__(self, parent=None):
        WindowBaseClass_login.__init__(self, parent)
        Ui_MainWindow_login.__init__(self)
        self.setupUi(self)
                
        # set player attribute
        self._max_player_number = 5
        self._max_length_playerName = 10
        self._playerName_list = []
        self._playerIconIndex_list = []
        
        # initial style sheet of start push button
        self.pushButton_start.setEnabled(False)
        self.pushButton_start.setVisible(False)
        
        # title
        self.label_title.setPixmap(QPixmap("figures/yahtzee.png"))
        
        # set icon
        self._max_icon_number = 167
        self._current_icon_id = 1
        self._icon_file_name_root_list = ["figures/icons/icon_", ".png"]
        self._arrow_file_name_root_list = ["figures/", ".png"]
        self.setIcon(0)
        for player_id in range(0, self._max_player_number):
            eval("".join(["self.label_icon_player_", str(player_id + 1), 
              ".setVisible(False)"]))
            eval("".join(["self.label_name_player_", str(player_id + 1), 
              ".setVisible(False)"]))
        
        # set call backs
        self.pushButton_last.clicked.connect(lambda: self.setIcon(-5))
        self.pushButton_next.clicked.connect(lambda: self.setIcon(5))
        self.pushButton_icon_1.clicked.connect(lambda: self.setIcon(-2))
        self.pushButton_icon_2.clicked.connect(lambda: self.setIcon(-1))
        self.pushButton_icon_3.clicked.connect(lambda: self.setIcon(0))
        self.pushButton_icon_4.clicked.connect(lambda: self.setIcon(1))
        self.pushButton_icon_5.clicked.connect(lambda: self.setIcon(2))
        self.lineEdit_playerName.returnPressed.connect(self.addPlayer)
        self.pushButton_addPlayer.clicked.connect(self.addPlayer)
        self.pushButton_quit.clicked.connect(self.quitStartDialog)
        
    @property
    def max_player_number(self):
        return self._max_player_number
    
    @property
    def playerName_list(self):
        return self._playerName_list
    
    @property
    def playerIconIndex_list(self):
        return self._playerIconIndex_list

    def setIcon(self, setStep): # 1 or -1
        new_icon_id_list = list(map(lambda step: self._max_icon_number - (
            self._max_icon_number - ((self._current_icon_id + step) % 
            self._max_icon_number)) % self._max_icon_number, 
             list(map(lambda x, y: x + y, 5 * [setStep], 
                  list(range(-2, 3))))))
        self._current_icon_id = new_icon_id_list[2]
        self.label_icon_1.setPixmap(QPixmap(str(new_icon_id_list[0]).join(
                self._icon_file_name_root_list)))    
        self.label_icon_2.setPixmap(QPixmap(str(new_icon_id_list[1]).join(
                self._icon_file_name_root_list)))
        self.label_icon_3.setPixmap(QPixmap(str(new_icon_id_list[2]).join(
                self._icon_file_name_root_list)))
        self.label_icon_4.setPixmap(QPixmap(str(new_icon_id_list[3]).join(
                self._icon_file_name_root_list)))
        self.label_icon_5.setPixmap(QPixmap(str(new_icon_id_list[4]).join(
                self._icon_file_name_root_list)))
    
    def addPlayer(self):
        str_playerName = self.lineEdit_playerName.text()
        if (str_playerName and len(
                str_playerName) <= self._max_length_playerName 
            and not str_playerName in self._playerName_list):
            self._playerName_list.append(str_playerName)
            self._playerIconIndex_list.append(self._current_icon_id)
            self.lineEdit_playerName.clear()
            # set player icon and name and set them visible
            eval("".join(["self.label_icon_player_", 
                  str(len(self._playerName_list)), ".setPixmap(", 
                  "QPixmap(str(", str(self._playerIconIndex_list[-1]), 
                  ").join(self._icon_file_name_root_list)))"]))
            eval("".join(["self.label_name_player_", 
                  str(len(self._playerName_list)), ".setText(\"", 
                  self._playerName_list[-1], "\")"]))
            eval("".join(["self.label_icon_player_", 
                  str(len(self._playerName_list)), ".setVisible(True)"]))
            eval("".join(["self.label_name_player_", 
                  str(len(self._playerName_list)), ".setVisible(True)"]))
            
            if len(self._playerName_list) == 2:
                self.pushButton_start.setEnabled(True)
                self.pushButton_start.setVisible(True)
            if len(self._playerName_list) >= self._max_player_number:
                self.pushButton_addPlayer.setVisible(False)
                self.pushButton_addPlayer.setEnabled(False)

    def quitStartDialog(self):
        self.close()

class My_MainWindow(WindowBaseClass_play, Ui_MainWindow_play):
    
    def __init__(self, parent=None):
        WindowBaseClass_play.__init__(self, parent)
        Ui_MainWindow_play.__init__(self)
        self.setupUi(self)
        self._max_player_number = None
        self._playerName_list = None
        self._playerIconIndex_list = None
        self._arena = None
        
        self._dice_number = 5
        self._icon_file_name_root_list = ["figures/icons/icon_", ".png"]
        self._active_dice_file_name_root_list = ["figures/dices/active/dice_",
                                                 "_active.png"]
        self._inactive_dice_file_name_root_list = [
            "figures/dices/inactive/dice_","_inactive.png"]   
        
        # set figures
        # dices
        for dice_id in range(0, self._dice_number):
            eval("".join(["self.label_dice_", str(dice_id + 1), 
          ".setPixmap(QPixmap(\"figures/dices/sealed/dice_sealed.png\"))"]))
            
        # play desk
        self.label_playDesk.setPixmap(QPixmap("figures/play_desk.png"))
        
        # Set call backs
        # dices
        self.pushButton_dice_1.clicked.connect(
                lambda: self.reverseDiceStatus(0))
        self.pushButton_dice_2.clicked.connect(
                lambda: self.reverseDiceStatus(1))
        self.pushButton_dice_3.clicked.connect(
                lambda: self.reverseDiceStatus(2))
        self.pushButton_dice_4.clicked.connect(
                lambda: self.reverseDiceStatus(3))
        self.pushButton_dice_5.clicked.connect(
                lambda: self.reverseDiceStatus(4))
        
        # roll dices
        self.pushButton_rollDice.clicked.connect(self.rollDice)

        # choose category
        self.pushButton_category_1.clicked.connect(lambda: 
            self.chooseCategory(0))
        self.pushButton_category_2.clicked.connect(lambda: 
            self.chooseCategory(1))
        self.pushButton_category_3.clicked.connect(lambda: 
            self.chooseCategory(2))
        self.pushButton_category_4.clicked.connect(lambda: 
            self.chooseCategory(3))
        self.pushButton_category_5.clicked.connect(lambda: 
            self.chooseCategory(4))
        self.pushButton_category_6.clicked.connect(lambda: 
            self.chooseCategory(5))
        self.pushButton_category_7.clicked.connect(lambda: 
            self.chooseCategory(6))
        self.pushButton_category_8.clicked.connect(lambda: 
            self.chooseCategory(7))
        self.pushButton_category_9.clicked.connect(lambda: 
            self.chooseCategory(8))
        self.pushButton_category_10.clicked.connect(lambda: 
            self.chooseCategory(9))
        self.pushButton_category_11.clicked.connect(lambda: 
            self.chooseCategory(10))
        self.pushButton_category_12.clicked.connect(lambda: 
            self.chooseCategory(11))
        self.pushButton_category_13.clicked.connect(lambda: 
            self.chooseCategory(12))
            
        # quit
        self.pushButton_quit.clicked.connect(self.quitMainWindow)
        
        # restart
        self.pushButton_restart.clicked.connect(self.restartMainWindow)
    

    def startMainWindow(self, max_player_number, playerName_list, 
                       playerIconIndex_list):     
        ## set values
        self._max_player_number = max_player_number
        self._playerName_list = playerName_list
        self._playerIconIndex_list = playerIconIndex_list
        
        ## UI initialize
        # winner sign
        for winner_id in range(0, self._max_player_number):
            eval("".join(["self.label_winnerSign_", str(winner_id + 1), 
              ".setPixmap(QPixmap(\"figures/win.png\"))"]))
        # Player list
        for player_id in range(0, self._max_player_number):
            if player_id < len(self._playerName_list):
                eval("".join(["self.label_playerIcon_", str(player_id + 1), 
                     ".setPixmap(QPixmap(\"", str(playerIconIndex_list[player_id]
                    ).join(self._icon_file_name_root_list), "\"))"])) 
                eval("".join(["self.label_playerName_", str(player_id + 1), 
                     ".setText(\"", self._playerName_list[player_id], "\")"]))            
            else:
                eval("".join(["self.label_playerNumber_", str(player_id + 1), 
                     ".setVisible(False)"]))
                eval("".join(["self.label_playerName_", str(player_id + 1), 
                     ".setVisible(False)"]))
                eval("".join(["self.label_playerScore_", str(player_id + 1), 
                     ".setVisible(False)"]))
            eval("".join(["self.label_winnerSign_", str(player_id + 1), 
                     ".setVisible(False)"]))
            
        ## Initialise Arena
        self._arena = yahtzee.Arena()
        for playerName in self._playerName_list:
            self._arena.add_player(playerName)
        self._arena.start()
        self.refreshUI()
        
    def restartMainWindow(self):
        self._arena.restart()
        self.refreshUI()
        
    def quitMainWindow(self):
        self.close()
                    
    def reverseDiceStatus(self, dice_id):
        self._arena.execute(0, dice_id)
        self.refreshUI()
        
    def rollDice(self):
        self._arena.execute(1) 
        self.refreshUI()
        
    def chooseCategory(self, category_id):
        self._arena.execute(2, category_id)
        self.refreshUI()
        
    def refreshGroupBoxPlayerList(self):
        # GROUP-BOX: Player List
        # refresh player list:
        for player_id, _ in enumerate(self._arena.player_list):
            eval("".join(["self.label_playerScore_", str(player_id + 1), 
              ".setText(\"", 
              str(self._arena.player_list[player_id].score), "\")"]))
            
        # Refresh winner sign
        for player_id in range(0, self._max_player_number):
            eval("".join(["self.label_winnerSign_", str(player_id + 1), 
                     ".setVisible(False)"]))
            
    def refreshGroupBoxPlayerCenter(self, wait_arg=False):
        # GROUP-BOX: Player Center
        if not wait_arg: # wait_arg == False
            # refresh turn, chance
            self.label_turnNumber.setText(str(self._arena.max_turn - 
                                              self._arena.turn))
            self.label_leftChanceNumber.setText(str(self._arena.max_chance - 
                                                    self._arena.chance))
            # refresh dice 
            if self._arena.chance == 0:
                for dice_id in range(0, self._dice_number):
                    eval("".join(["self.label_dice_", str(dice_id + 1), 
                      ".setPixmap(QPixmap(",
                      "\"figures/dices/sealed/dice_sealed.png\"))"]))
            else:
                for dice_id in range(0, self._dice_number):
                    eval("".join(["self.label_dice_", str(dice_id + 1), 
                      ".setPixmap(QPixmap(str(", 
                      str(self._arena.dice_list[dice_id]), ").join(",
                      "self._", ["in", ""][int(self._arena.status_list[dice_id])], 
                      "active_dice_file_name_root_list)))"]))
            
            # Refresh roll dice: chance == max_chance
            self.pushButton_rollDice.setEnabled([True, False][
                int(self._arena.chance == self._arena.max_chance)])
            self.pushButton_rollDice.setText(["Roll Dice", "No chance"][
                int(self._arena.chance == self._arena.max_chance)])
        else: # wait_arg == True
            # refresh turn, chance
            self.label_turnNumber.setText(str(self._arena.max_turn - 
                  self._arena.turn + [0, 1][int(self._arena.player_id == 0)]))
            self.label_leftChanceNumber.setText("0")
            # refresh dice 
            for dice_id in range(0, self._dice_number):
                eval("".join(["self.label_dice_", str(dice_id + 1), 
                  ".setPixmap(QPixmap(str(", 
                  str(self._arena.dice_list[dice_id]), ").join(",
                  "self._", ["in", ""][int(self._arena.status_list[dice_id])], 
                  "active_dice_file_name_root_list)))"]))
            
            # Refresh roll dice: chance == max_chance
            self.pushButton_rollDice.clicked.disconnect()
            self.pushButton_rollDice.clicked.connect(lambda: 
                 {self.refreshGroupBoxPlayerCenter(False),
                  self.refreshGroupBoxCurrentPlayer(self._arena.player_id),
                  self.pushButton_rollDice.clicked.disconnect(),
                  self.pushButton_rollDice.clicked.connect(self.rollDice)})
            self.pushButton_rollDice.setEnabled(True)
            self.pushButton_rollDice.setText("Next Player")
        
    def refreshGroupBoxCurrentPlayer(self, player_id):
        # GROUP-BOX: Current Player
        # refresh current player
        # id, name and icon
        self.label_playerNumber.setText(str(player_id + 1))
        self.label_playerName.setText(self._arena.player_list[
                player_id].name)
        self.label_playerFigure.setPixmap(
                QPixmap(str(self._playerIconIndex_list[
                        player_id]).join(
                self._icon_file_name_root_list)))

        # refresh score list & possible list    
        for category_id in range(0, len(yahtzee.Memo().category_list)):
            if self._arena.chance == 0:
                eval("".join(["self.label_category_possible_", 
                  str(category_id + 1), ".setText(\"\")"])) 
            else:
                eval("".join(["self.label_category_possible_", 
                  str(category_id + 1), ".setText(\"", ["", 
                        str(self._arena.player_list[
                              player_id].memo.possible_list[
                          category_id])][int(self._arena.player_list[
                          player_id].memo.score_list[
                                  category_id] is None)], "\")"])) 
            eval("".join(["self.label_category_score_", 
              str(category_id + 1), ".setText(\"", 
                  ["", str(self._arena.player_list[
                          player_id].memo.score_list[
                      category_id])][int(not self._arena.player_list[
                      player_id].memo.score_list[
                              category_id] is None)], 
                "\")"])) 
            
        self.label_category_possible_bonus.setText("-")
        self.label_category_possible_total.setText("-")
        self.label_category_score_bonus.setText(str(self._arena.player_list[
                player_id].memo.bonus))
        self.label_category_score_total.setText(str(self._arena.player_list[
                player_id].memo.total))
        
    def refreshAfterAllTurn(self):
            self._arena.end()
           
            # turn and chance
            self.label_turnNumber.setText("-")
            self.label_leftChanceNumber.setText("-")
            
            # dices
            for dice_id in range(0, self._dice_number):
                eval("".join(["self.label_dice_", str(dice_id + 1), 
                  ".setPixmap(QPixmap(",
                  "\"figures/dices/ended/dice_ended.png\"))"]))
            
            # roll dice
            self.pushButton_rollDice.setEnabled(False)
            self.pushButton_rollDice.setText("Game Ended")
            
            # player id, name, icon
            self.label_playerNumber.setText("-")
            self.label_playerName.setText("-")
            self.label_playerFigure.setPixmap(
                    QPixmap("figures/icon_anonym.png"))
            
            # possible list
            for category_id in range(0, len(yahtzee.Memo().category_list)):
                eval("".join(["self.label_category_possible_", 
                  str(category_id + 1), ".setText(\"\")"]))
            self.label_category_possible_bonus.setText("")
            self.label_category_possible_total.setText("")
            
            # score list
            for category_id in range(0, len(yahtzee.Memo().category_list)):
                eval("".join(["self.label_category_score_", 
                  str(category_id + 1), ".setText(\"\")"]))
            self.label_category_score_bonus.setText("")
            self.label_category_score_total.setText("")#
             
            # winner sign
            for player_id, _ in enumerate(self._arena.player_list):
                for winner in self._arena.winner_list:
                    if winner.name == self._arena.player_list[player_id].name:
                        eval("".join(["self.label_winnerSign_", 
                          str(player_id + 1), ".setVisible(True)"]))
        
    def refreshUI(self):
        self.refreshGroupBoxPlayerList()
        if not (self._arena.turn == 0 and self._arena.player_id == 0
                ) and self._arena.chance == 0:
            self.refreshGroupBoxPlayerCenter(True)
            self.refreshGroupBoxCurrentPlayer((self._arena.player_id - 1
               ) % len(self._arena.player_list)) 
        else: 
            self.refreshGroupBoxPlayerCenter()
            self.refreshGroupBoxCurrentPlayer(self._arena.player_id)
                
        # Refresh after all turn
        if self._arena.turn == self._arena.max_turn:
            self.refreshAfterAllTurn()
            

if __name__ == "__main__":
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)
        
    my_startDialog = My_StartDialog()
    my_startDialog.show()
    my_mainWindow = My_MainWindow()
    my_startDialog.pushButton_start.clicked.connect(
    	lambda:{my_mainWindow.startMainWindow(my_startDialog.max_player_number, 
                     my_startDialog.playerName_list, 
                     my_startDialog.playerIconIndex_list), 
                 my_startDialog.close(),
                 my_mainWindow.show()})
    sys.exit(app.exec_())
        
        
