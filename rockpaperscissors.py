#!/usr/bin/python3
from random import *
from tkinter import *
from learner import *

########################
PLAYER_SCORE_INDEX = 0
COMPUTER_SCORE_INDEX = 1


########################

class GamePlay:
    scores = [0, 0]
    history = []
    file = None

    def __init__(self, agent=RandomAgent()):
        self.agent = agent
        self.next_move = self.agent.predict(self.history).best_counter()

        # main program
        self.mainWindow = Tk()
        self.scores_text = "SCORE:\nYou: {}\nComputer: {}"
        self.write_mode = BooleanVar()
        self.mainWindow.title("Rock-Paper-Scissors by Nahaliel")

        # images
        self.emptyImage = PhotoImage()
        self.rockImage_player = PhotoImage(file="images"+os.path.sep+"rockPlayer.png")
        self.rockImage_computer = PhotoImage(file="images"+os.path.sep+"rockComputer.png")
        self.paperImage_player = PhotoImage(file="images"+os.path.sep+"paperPlayer.png")
        self.paperImage_computer = PhotoImage(file="images"+os.path.sep+"paperComputer.png")
        self.scissorsImage_player = PhotoImage(file="images"+os.path.sep+"scissorsPlayer.png")
        self.scissorsImage_computer = PhotoImage(file="images"+os.path.sep+"scissorsComputer.png")
        self.rockButtonImage = PhotoImage(file="images"+os.path.sep+"rockButton.png")
        self.paperButtonImage = PhotoImage(file="images"+os.path.sep+"paperButton.png")
        self.scissorsButtonImage = PhotoImage(file="images"+os.path.sep+"scissorsButton.png")
        self.random_button_image = PhotoImage(file="images"+os.path.sep+"RAND_button.png")
        self.reflex_button_image = PhotoImage(file="images"+os.path.sep+"REFLEX_button.png")
        self.ai_button_image = PhotoImage(file="images"+os.path.sep+"AI_button.png")

        self.userImage = Label(image=self.emptyImage)
        self.userImage.image = self.emptyImage
        self.opponentImage = Label(image=self.emptyImage)
        self.opponentImage.image = self.emptyImage

        self.turnResult = Label(self.mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
        self.your_choice = Label(self.mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
        self.ai_choice = Label(self.mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
        self.scores_textbox = Label(self.mainWindow, width=20,
                                    text=self.scores_text.format(self.scores[0], self.scores[1]), justify=CENTER,
                                    font=("Helvetica", 20), fg="blue")

        self.rockButton = Button(self.mainWindow, image=self.rockButtonImage, command=self.user_choice_rock)
        self.paperButton = Button(self.mainWindow, image=self.paperButtonImage, command=self.user_choice_paper)
        self.scissorsButton = Button(self.mainWindow, image=self.scissorsButtonImage, command=self.user_choice_scissors)
        self.random_agent_button = Button(self.mainWindow, image=self.random_button_image,
                                          command=self.random_agent_chosen)
        self.reflex_agent_button = Button(self.mainWindow, image=self.reflex_button_image,
                                          command=self.reflex_agent_chosen)
        self.ai_agent_button = Button(self.mainWindow, image=self.ai_button_image, command=self.ai_agent_chosen)
        self.write_mode_button = Checkbutton(self.mainWindow, text="Write episode to examples",
                                             variable=self.write_mode)
        self.locate_agent_buttons()

    def random_agent_chosen(self):
        if self.write_mode.get():
            self.file = open("examples"+os.path.sep+"random_examples.txt", 'a')
        self.agent_chosen(RandomAgent())

    def reflex_agent_chosen(self):
        if self.write_mode.get():
            self.file = open("examples"+os.path.sep+"reflex_examples.txt", 'a')
        self.agent_chosen(ReflexAgent())

    def ai_agent_chosen(self):
        if self.write_mode.get():
            self.file = open("examples"+os.path.sep+"ai_examples.txt", 'a')
        self.agent_chosen(AI_agent())

    def agent_chosen(self, agent):
        if self.write_mode.get() and self.file.read():
            self.file.write('\n')
        self.agent = agent
        self.ai_agent_button.grid_remove()
        self.reflex_agent_button.grid_remove()
        self.random_agent_button.grid_remove()
        self.write_mode_button.grid_remove()
        self.locate_play_table()

    def locate_agent_buttons(self):
        self.ai_agent_button.grid(row=2, column=1)
        self.reflex_agent_button.grid(row=2, column=2)
        self.random_agent_button.grid(row=2, column=3)
        self.write_mode_button.grid(row=3, column=1)

    def locate_play_table(self):
        # Tk GUI grid
        self.rockButton.grid(row=2, column=1)
        self.paperButton.grid(row=2, column=2)
        self.scissorsButton.grid(row=2, column=3)
        self.userImage.grid(row=3, column=1)
        self.opponentImage.grid(row=3, column=3)
        self.turnResult.grid(row=3, column=2)
        self.ai_choice.grid(row=4, column=3)
        self.your_choice.grid(row=4, column=1)
        self.scores_textbox.grid(row=4, column=2)

    # choice section
    def user_choice_rock(self):
        self.history.append(Rock)
        userChoice = Rock
        self.turn(userChoice)
        self.userImage.configure(image=self.rockImage_player)
        self.next_move = self.agent.predict(self.history).best_counter()

    def user_choice_paper(self):
        self.history.append(Paper)
        userChoice = Paper
        self.turn(userChoice)
        self.userImage.configure(image=self.paperImage_player)
        self.next_move = self.agent.predict(self.history).best_counter()

    def user_choice_scissors(self):
        self.history.append(Scissors)
        userChoice = Scissors
        self.turn(userChoice)
        self.userImage.configure(image=self.scissorsImage_player)
        self.next_move = self.agent.predict(self.history).best_counter()

    # gameplay section
    def turn(self, user_choice):
        to_write = user_choice
        opponent_choice = self.next_move
        self.your_choice.configure(text="Your Choice")
        self.ai_choice.configure(text="Computer Choice")
        if opponent_choice == Rock:
            self.opponentImage.configure(image=self.rockImage_computer)
        elif opponent_choice == Paper:
            self.opponentImage.configure(image=self.paperImage_computer)
        else:
            self.opponentImage.configure(image=self.scissorsImage_computer)

        if opponent_choice == user_choice:
            self.turnResult.configure(text="It's a draw.", fg="gray")
            to_write += 'D'
        elif ((opponent_choice == Rock and user_choice == Scissors) or (
                opponent_choice == Paper and user_choice == Rock) or (
                      opponent_choice == Scissors and user_choice == Paper)):
            self.turnResult.configure(text="You lose!", fg="red")
            self.scores[COMPUTER_SCORE_INDEX] += 1
            to_write += 'L'

        else:
            self.turnResult.configure(text="You win!", fg="green")
            self.scores[PLAYER_SCORE_INDEX] += 1
            to_write += 'W'
        self.scores_textbox.configure(text=self.scores_text.format(self.scores[0], self.scores[1]))
        if self.write_mode.get():
            self.file.write(to_write + ' ')

    def play(self):
        self.mainWindow.mainloop()
        if self.write_mode.get():
            self.file.close()


game = GamePlay()
game.play()
