import threading
from random import *
from tkinter import *
from learner import *

########################
EPOCH = 6
PLAYER_SCORE_INDEX = 0
COMPUTER_SCORE_INDEX = 1


########################

class GamePlay:
    scores = [0, 0]
    history = []
    output_file = None
    agent = None
    next_move = None

    def __init__(self):
        self.build_process = None
        self.output_file_path = None

        # main program
        self.main_window = Tk()
        self.scores_text = "SCORE:\nYou: {}\nComputer: {}"
        self.write_mode = BooleanVar(value=1)
        self.main_window.title("Rock-Paper-Scissors by Nahaliel")

        # images
        self.empty_image = PhotoImage()
        self.rock_image_user = PhotoImage(file="images" + os.path.sep + "rockPlayer.png")
        self.rock_image_computer = PhotoImage(file="images" + os.path.sep + "rockComputer.png")
        self.paper_image_user = PhotoImage(file="images" + os.path.sep + "paperPlayer.png")
        self.paper_image_computer = PhotoImage(file="images" + os.path.sep + "paperComputer.png")
        self.scissors_image_user = PhotoImage(file="images" + os.path.sep + "scissorsPlayer.png")
        self.scissors_image_computer = PhotoImage(file="images" + os.path.sep + "scissorsComputer.png")
        self.rock_button_image = PhotoImage(file="images" + os.path.sep + "rockButton.png")
        self.paper_button_image = PhotoImage(file="images" + os.path.sep + "paperButton.png")
        self.scissors_button_image = PhotoImage(file="images" + os.path.sep + "scissorsButton.png")
        self.random_button_image = PhotoImage(file="images" + os.path.sep + "RAND_button.png")
        self.reflex_button_image = PhotoImage(file="images" + os.path.sep + "REFLEX_button.png")
        self.ai_button_image = PhotoImage(file="images" + os.path.sep + "AI_button.png")
        self.epoch_button_image = PhotoImage(file="images" + os.path.sep + "Online_Forest.png")
        self.single_button_image = PhotoImage(file="images" + os.path.sep + "Online_Single_Tree.png")
        self.user_image = Label(image=self.empty_image)
        self.user_image.image = self.empty_image
        self.computer_image = Label(image=self.empty_image)
        self.computer_image.image = self.empty_image

        self.turn_result = Label(self.main_window, width=20, justify=CENTER, font=("Helvetica", 20))
        self.your_choice = Label(self.main_window, width=20, justify=CENTER, font=("Helvetica", 20))
        self.ai_choice = Label(self.main_window, width=20, justify=CENTER, font=("Helvetica", 20))
        self.scores_textbox = Label(self.main_window, width=20,
                                    text=self.scores_text.format(self.scores[0], self.scores[1]), justify=CENTER,
                                    font=("Helvetica", 20), fg="blue")

        self.rock_button = Button(self.main_window, image=self.rock_button_image, command=self.user_choice_rock)
        self.paper_button = Button(self.main_window, image=self.paper_button_image, command=self.user_choice_paper)
        self.scissors_button = Button(self.main_window, image=self.scissors_button_image,
                                      command=self.user_choice_scissors)
        self.random_agent_button = Button(self.main_window, image=self.random_button_image,
                                          command=self.random_agent_chosen)
        self.reflex_agent_button = Button(self.main_window, image=self.reflex_button_image,
                                          command=self.reflex_agent_chosen)
        self.ai_agent_button = Button(self.main_window, image=self.ai_button_image, command=self.ai_agent_chosen)
        self.epoch_agent_button = Button(self.main_window, image=self.epoch_button_image,
                                         command=self.epoch_agent_chosen)
        self.single_agent_button = Button(self.main_window, image=self.single_button_image,
                                          command=self.single_agent_chosen)
        self.write_mode_button = Checkbutton(self.main_window, text="save log to file",
                                             variable=self.write_mode)
        self.locate_agent_buttons()

    def random_agent_chosen(self):
        if self.write_mode.get():
            self.output_file_path = "examples" + os.path.sep + "random_examples.txt"
        self.agent_chosen(RandomAgent())

    def reflex_agent_chosen(self):
        if self.write_mode.get():
            self.output_file_path = "examples" + os.path.sep + "reflex_examples.txt"
        self.agent_chosen(ReflexAgent())

    def ai_agent_chosen(self):
        if self.write_mode.get():
            self.output_file_path = "final_games.txt"
        self.agent_chosen(Ai2(EPOCH, 5, 0.7))
        # running in the background
        # thread = threading.Thread(target=self.agent.basic_ai.build, args=())
        # thread.daemon = True  # Daemonize thread
        # thread.start()

    def epoch_agent_chosen(self):
        if self.write_mode.get():
            self.output_file_path = "examples" + os.path.sep + "epoch_examples.txt"
        self.agent_chosen(OnlineEpochAgent(3, 5, 0.9))

    def single_agent_chosen(self):
        if self.write_mode.get():
            self.output_file_path = "examples" + os.path.sep + "single_examples.txt"
        self.agent_chosen(OnlineSingleTreeAgent(5, 5))

    def agent_chosen(self, agent):
        self.agent = agent
        self.ai_agent_button.grid_remove()
        self.reflex_agent_button.grid_remove()
        self.random_agent_button.grid_remove()
        self.write_mode_button.grid_remove()
        # self.epoch_agent_button.grid_remove()
        # self.single_agent_button.grid_remove()
        self.next_move = self.agent.predict(self.history).best_counter_probabilistic()
        self.locate_play_table()

    def locate_agent_buttons(self):
        self.ai_agent_button.grid(row=2, column=1)
        self.reflex_agent_button.grid(row=2, column=2)
        self.random_agent_button.grid(row=2, column=3)
        # self.epoch_agent_button.grid(row=3, column=2)
        # self.single_agent_button.grid(row=3, column=3)
        self.write_mode_button.grid(row=3, column=1)

    def locate_play_table(self):
        # Tk GUI grid
        self.rock_button.grid(row=2, column=1)
        self.paper_button.grid(row=2, column=2)
        self.scissors_button.grid(row=2, column=3)
        self.user_image.grid(row=3, column=1)
        self.computer_image.grid(row=3, column=3)
        self.turn_result.grid(row=3, column=2)
        self.ai_choice.grid(row=4, column=3)
        self.your_choice.grid(row=4, column=1)
        self.scores_textbox.grid(row=4, column=2)

    # choice section
    def user_choice_rock(self):
        userChoice = Rock
        self.turn(userChoice)
        self.user_image.configure(image=self.rock_image_user)
        if len(self.history) <= EPOCH * 2:
            self.next_move = self.agent.predict(self.history).best_counter_probabilistic()
        else:
            self.next_move = self.agent.predict(self.history).best_counter()

    def user_choice_paper(self):
        userChoice = Paper
        self.turn(userChoice)
        self.user_image.configure(image=self.paper_image_user)
        if len(self.history) <= EPOCH * 2:
            self.next_move = self.agent.predict(self.history).best_counter_probabilistic()
        else:
            self.next_move = self.agent.predict(self.history).best_counter()

    def user_choice_scissors(self):
        userChoice = Scissors
        self.turn(userChoice)
        self.user_image.configure(image=self.scissors_image_user)
        if len(self.history) <= EPOCH * 2:
            self.next_move = self.agent.predict(self.history).best_counter_probabilistic()
        else:
            self.next_move = self.agent.predict(self.history).best_counter()

    # gameplay section
    def turn(self, user_choice):
        to_write = user_choice
        computer_choice = self.next_move
        self.your_choice.configure(text="Your Choice")
        self.ai_choice.configure(text="Computer Choice")
        if computer_choice == Rock:
            self.computer_image.configure(image=self.rock_image_computer)
        elif computer_choice == Paper:
            self.computer_image.configure(image=self.paper_image_computer)
        else:
            self.computer_image.configure(image=self.scissors_image_computer)

        if computer_choice == user_choice:
            self.turn_result.configure(text="It's a draw.", fg="gray")
            to_write += 'D'
        elif ((computer_choice == Rock and user_choice == Scissors) or (
                computer_choice == Paper and user_choice == Rock) or (
                      computer_choice == Scissors and user_choice == Paper)):
            self.turn_result.configure(text="You lose!", fg="red")
            self.scores[COMPUTER_SCORE_INDEX] += 1
            to_write += 'L'

        else:
            self.turn_result.configure(text="You win!", fg="green")
            self.scores[PLAYER_SCORE_INDEX] += 1
            to_write += 'W'
        self.scores_textbox.configure(text=self.scores_text.format(self.scores[0], self.scores[1]))
        self.history.append(to_write)

    def play(self):
        self.main_window.mainloop()
        if self.write_mode.get():
            #os.system('git checkout master -- ' + self.output_file_path)
            self.output_file = open(self.output_file_path, 'a')
            self.output_file.write("\n"+' '.join(self.history))

            self.output_file.close()
            #name = os.path.basename(self.output_file_path)
            #command = "git commit " + self.output_file_path + f" -m \"updated {name}\""
            #print(command)
            #os.system(command)
            #os.system('git push')
        if self.build_process:
            self.build_process.join()


game = GamePlay()
game.play()
