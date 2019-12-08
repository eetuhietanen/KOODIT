# TIE-02100 Johdatus ohjelmointiin
# Ilari Hildén, ilari.hilden@tuni.fi, opiskelijanumero: 282680
# Eetu Hietanen, eetu.hietanen@tuni.fi, opiskelijanumero: 284956
# GUI_ristinolla
# TicTacToe with a graphical user interface.

from tkinter import *

NUMBER_OF_PLAYERS = 2
INFOTEXT = "This is TicTacToe. The rules are simple, there are two " \
           "players who place their mark on the board alternately. When" \
           " one of the players gets the desired amount of their mark in" \
           " a row (vertically, horizontally or diagonally) he/she wins." \
           " If the board fills up before either of the players gets to" \
           " this point its a draw. You can choose the size of the" \
           " game board (from three to ten) and the length of the straight" \
           " required to win below. The winning length must be less or" \
           " equal to the size of the board.  You can always restart the" \
           " game with the restart button and choose the variables again" \
           " and start a new game with the new game button. The Start" \
           " button starts the game and Quit button always quits the game."


class InfoWindow:
    """
    This class is for the info window. It starts on the program start up. It
    has the information about the program, for example the rules and the
    instructions about the program. It starts the game.
    """

    def __init__(self):
        self.__infowindow = Tk()
        self.__infowindow.title("TicTacToe")

        self.__scroller = Scrollbar(self.__infowindow)
        self.__scroller.grid(row=0, column=5, ipady=26)

        self.__infotext = Text(self.__infowindow, height=6, width=30,
                               yscrollcommand=self.__scroller.set, wrap=WORD,
                               padx=10)
        self.__infotext.grid(row=0, column=0, columnspan=5)
        self.__infotext.insert(END, INFOTEXT)
        self.__infotext.config(state=DISABLED)

        self.__scroller.config(command=self.__infotext.yview)

        self.__startbutton = Button(self.__infowindow, text="Start!",
                                    command=self.start_game)
        self.__startbutton.grid(row=3, column=1, rowspan=3)

        self.__quitbutton = Button(self.__infowindow, text="Quit",
                                   command=self.quit)
        self.__quitbutton.grid(row=3, column=3)

        self.__scale_entry = Entry(self.__infowindow, width=5)
        self.__scale_entry.grid(row=2, column=1)

        self.__winning_lenght = Entry(self.__infowindow, width=5)
        self.__winning_lenght.grid(row=2, column=4)

        self.__scale_label = Label(self.__infowindow, text="Board size:")
        self.__scale_label.grid(row=2, column=0)

        self.__lenght_label = Label(self.__infowindow, text="Winning length:")
        self.__lenght_label.grid(row=2, column=3)

        self.__error_label = Label(self.__infowindow, text="")
        self.__error_label.grid(row=3, column=0, columnspan=5)

    def start_game(self):
        """
        For starting the program. This methods checks for valid input and
        creates a new Board object with the specified values.
        :return:
        """
        try:
            scale = int(self.__scale_entry.get())
            winning_lenght = int(self.__winning_lenght.get())
            if winning_lenght <= scale and 10 >= scale >= 3:
                self.__infowindow.destroy()
                board = Board(scale, winning_lenght)
                board.start()
            else:
                if winning_lenght > scale:
                    self.__error_label.configure(
                        text="Winning length must be less or equal to scale!")
                else:
                    self.__error_label.configure(
                        text="Please enter integers between three and ten!")
                self.__startbutton.grid(row=4, column=1)
                self.__quitbutton.grid(row=4, column=3)
        except ValueError:
            self.__error_label.configure(
                text="Please enter integers over three!")
            self.__startbutton.grid(row=4, column=1)
            self.__quitbutton.grid(row=4, column=3)

    def quit(self):
        """
        Quits the program.
        :return:
        """
        self.__infowindow.destroy()

    def start(self):
        """
        For starting the main loop.
        :return:
        """
        self.__infowindow.mainloop()


class Board:
    """
    This is a class for the game board. It stores the information about the
    board and reads the users commands.
    """

    def __init__(self, board_size, winninglenght):
        self.__board_window = Tk()
        self.__board_window.title("TicTacToe")

        self.__board_size = board_size
        self.__winning_lenght = winninglenght
        self.__turn = 0
        self.__mark_x = "X"
        self.__mark_o = "O"
        self.__disabled_buttons = 0

        self.__new_game = Button(self.__board_window, text="New Game",
                                 command=self.new_game)
        self.__new_game.grid(row=0, column=0,
                             columnspan=self.__board_size // 3)

        self.__restart = Button(self.__board_window, text="Restart",
                                width=9, command=self.restart)
        self.__restart.grid(row=0,
                            column=self.__board_size - self.__board_size // 3,
                            columnspan=self.__board_size // 3)

        self.__quit = Button(self.__board_window, text="Quit", width=9,
                             command=self.quit)
        self.__quit.grid(row=board_size + 1, column=0)

        self.__turn_label = Label(self.__board_window, text="X's turn")
        if self.__board_size % 2 == 0:
            self.__turn_label.grid(row=0,
                                   column=self.__board_size - self.__board_size
                                          // 2 - 1, columnspan=2)
        else:
            self.__turn_label.grid(row=0,
                                   column=self.__board_size - self.__board_size
                                          // 2 - 1)
        self.__board_buttons = []  # Data structure of the board.
        for row in range(self.__board_size):
            self.__board_buttons.append([])
            for column in range(self.__board_size):
                new_button = Button(self.__board_window, height=3, width=9,
                                    relief="groove",
                                    command=lambda row_index=row,
                                                   column_index=column:
                                    self.place_mark(row_index, column_index))
                new_button.grid(row=row + 1, column=column, sticky=E)
                self.__board_buttons[row].append(new_button)

    def place_mark(self, row, column):
        """
        Method for placing a mark on the board and disabling the button in
        question. Starts the winner checking system.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """
        if self.__turn % NUMBER_OF_PLAYERS == 0:
            self.__board_buttons[row][column].configure(state=DISABLED,
                                                        text=self.__mark_x)
            self.__turn_label.configure(text="O's turn")
        else:
            self.__board_buttons[row][column].configure(state=DISABLED,
                                                        text=self.__mark_o)
            self.__turn_label.configure(text="X's turn")
        self.__turn += 1
        self.__disabled_buttons += 1
        self.horizontal_win_checker(row, column)

    def start(self):
        """
        For starting the main loop.
        :return:
        """
        self.__board_window.mainloop()

    def new_game(self):
        """
        This method starts a new InfoWindow object and destroys the current
        board window.
        :return:
        """
        self.__board_window.destroy()
        iw = InfoWindow()
        iw.start()

    def restart(self):
        """
        This method restarts the current board.
        :return:
        """
        for row in range(self.__board_size):
            for column in range(self.__board_size):
                self.__board_buttons[row][column].configure(state="normal",
                                                            text="")
        self.__turn = 0
        self.__disabled_buttons = 0
        self.__turn_label.configure(text="X's turn")

    def horizontal_win_checker(self, row, column):
        """
        This method checks if there are enough marks in a row for a win.
        It checks only for horizontal win and starts the checking from the
        latest placed mark. If there are no winners found starts the next
        checker.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """
        marks_in_row = -1

        # Checking for marks in row to right from pressed button.
        for i in range(self.__board_size - column):
            if self.__board_buttons[row][column + i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break

        # Checking for marks in row to left from pressed button.
        for i in range(1 + column):
            if self.__board_buttons[row][column - i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break
        if marks_in_row >= self.__winning_lenght:
            self.winner_found(row, column)
        else:
            self.vertical_win_checker(row, column)

    def vertical_win_checker(self, row, column):
        """
        This method works on same principle as horizontal_win_checker but
        checks for vertical winners instead.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """
        marks_in_row = -1

        # Checking for marks in row down from pressed button.
        for i in range(self.__board_size - row):
            if self.__board_buttons[row + i][column]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break

        # Checking for marks in row up from pressed button.
        for i in range(1 + row):
            if self.__board_buttons[row - i][column]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break
        if marks_in_row >= self.__winning_lenght:
            self.winner_found(row, column)
        else:
            self.diagonal_win_checker_sw_ne(row, column)

    def diagonal_win_checker_sw_ne(self, row, column):
        """
        This method works on same principle as horizontal_win_checker but
        checks for diagonal(from SW to NE) winners instead.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """

        column_distance = self.__board_size - column
        row_distance = row + 1
        marks_in_row = -1

        # Calculating the shortest distance from board edges.
        if column_distance > row_distance:
            nearest_edge_ne = row_distance
            nearest_edge_sw = self.__board_size - column_distance + 1
        else:
            nearest_edge_ne = column_distance
            nearest_edge_sw = self.__board_size - row_distance + 1

        # Checking for marks in row to NE from pressed button.
        for i in range(nearest_edge_ne):
            if self.__board_buttons[row - i][column + i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break

        # Checking for marks in row to SW from pressed button.
        for i in range(nearest_edge_sw):
            if self.__board_buttons[row + i][column - i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break
        if marks_in_row >= self.__winning_lenght:
            self.winner_found(row, column)
        else:
            self.diagonal_win_checker_nw_se(row, column)

    def diagonal_win_checker_nw_se(self, row, column):
        """
        This method works on same principal as horizontal_win_checker but
        check for diagonal(from NW to SE) winners instead.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """

        column_distance = self.__board_size - column
        row_distance = self.__board_size - row
        marks_in_row = -1

        # Calculating the shortest distance from board edges.
        if column_distance > row_distance:
            nearest_edge_se = row_distance
            nearest_edge_nw = self.__board_size - column_distance + 1
        else:
            nearest_edge_se = column_distance
            nearest_edge_nw = self.__board_size - row_distance + 1

        # Checking for marks in row to SE from pressed button.
        for i in range(nearest_edge_se):
            if self.__board_buttons[row + i][column + i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break

        # Checking for marks in row to NW from pressed button.
        for i in range(nearest_edge_nw):
            if self.__board_buttons[row - i][column - i]["text"] \
                    == self.__board_buttons[row][column]["text"]:
                marks_in_row += 1
            else:
                break
        if marks_in_row >= self.__winning_lenght:
            self.winner_found(row, column)
        else:
            self.draw()

    def winner_found(self, row, column):
        """
        This method displays the winner and disables the buttons in a case
        of win.
        :param row: The "row" index of the button pressed.
        :param column: The "column" index of the button pressed.
        :return:
        """
        winner = self.__board_buttons[row][column]["text"]
        self.__turn_label.configure(text=(winner, "won!"))
        for row in range(self.__board_size):
            for column in range(self.__board_size):
                self.__board_buttons[row][column].configure(state=DISABLED)

    def draw(self):
        """
        Displays "draw" if the players draw.
        :return:
        """
        if self.__disabled_buttons == self.__board_size ** 2:
            self.__turn_label.configure(text="Draw")

    def quit(self):
        """
        Quits the game
        :return:
        """
        self.__board_window.destroy()


def main():
    """
    Starts the program.
    :return:
    """
    iw = InfoWindow()
    iw.start()


main()