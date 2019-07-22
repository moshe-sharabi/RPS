#!/usr/bin/python3
from random import *
from tkinter import *

########################
# our code here:
scores = [0, 0]
PLAYER_SCORE_INDEX = 0
COMPUTER_SCORE_INDEX = 1
scores_text = "SCORE:\nyou: {}\ncomputer: {}"
# done
########################

# choice section
def userChoiceRock():
    userChoice = "rock"
    turn(userChoice)
    userImage.configure(image=rockImage_player)


def userChoicePaper():
    userChoice = "paper"
    turn(userChoice)
    userImage.configure(image=paperImage_player)


def userChoiceScissors():
    userChoice = "scissors"
    turn(userChoice)
    userImage.configure(image=scissorsImage_player)


# gameplay section
def turn(userChoice):
    opponent = ['rock', 'paper', 'scissors']
    opponent_choice = opponent[randint(0, 2)]
    your_choice.configure(text="Your Choice")
    ai_choice.configure(text="Computer Choice")
    if opponent_choice == 'rock':
        opponentImage.configure(image=rockImage_computer)
    elif opponent_choice == 'paper':
        opponentImage.configure(image=paperImage_computer)
    else:
        opponentImage.configure(image=scissorsImage_computer)

    if opponent_choice == userChoice:
        turnResult.configure(text="It's a draw.", fg="gray")
    elif ((opponent_choice == 'rock' and userChoice == 'scissors') or (
            opponent_choice == 'paper' and userChoice == 'rock') or (
                  opponent_choice == 'scissors' and userChoice == 'paper')):
        turnResult.configure(text="You lose!", fg="red")
        scores[COMPUTER_SCORE_INDEX] += 1
    else:
        turnResult.configure(text="You win!", fg="green")
        scores[PLAYER_SCORE_INDEX] += 1
    scores_textbox.configure(text=scores_text.format(scores[0], scores[1]))



# main program
mainWindow = Tk()
mainWindow.title("Rock-Paper-Scissors by Nahaliel")
rockButtonImage = PhotoImage(file="images/rockButton.png")
rockButton = Button(mainWindow, image=rockButtonImage, command=userChoiceRock)
paperButtonImage = PhotoImage(file="images/paperButton.png")
paperButton = Button(mainWindow, image=paperButtonImage, command=userChoicePaper)
scissorsButtonImage = PhotoImage(file="images/scissorsButton.png")
scissorsButton = Button(mainWindow, image=scissorsButtonImage, command=userChoiceScissors)

# images
# emptyImage = PhotoImage(file="images/empty.gif")
emptyImage = PhotoImage()
rockImage_player = PhotoImage(file="images/rockPlayer.png")
rockImage_computer = PhotoImage(file="images/rockComputer.png")
paperImage_player = PhotoImage(file="images/paperPlayer.png")
paperImage_computer = PhotoImage(file="images/paperComputer.png")
scissorsImage_player = PhotoImage(file="images/scissorsPlayer.png")
scissorsImage_computer = PhotoImage(file="images/scissorsComputer.png")

userImage = Label(image=emptyImage)
userImage.image = emptyImage
opponentImage = Label(image=emptyImage)
opponentImage.image = emptyImage

turnResult = Label(mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
your_choice = Label(mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
ai_choice = Label(mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
ai_choice = Label(mainWindow, width=20, justify=CENTER, font=("Helvetica", 20))
scores_textbox = Label(mainWindow, width=20, text=scores_text.format(scores[0], scores[1]), justify=CENTER, font=("Helvetica", 20), fg="blue")

# Tk GUI grid
rockButton.grid(row=2, column=1)
paperButton.grid(row=2, column=2)
scissorsButton.grid(row=2, column=3)
userImage.grid(row=3, column=1)
opponentImage.grid(row=3, column=3)
turnResult.grid(row=3, column=2)
ai_choice.grid(row=4, column=3)
your_choice.grid(row=4, column=1)
scores_textbox.grid(row=4, column=2)

# mainloop
mainWindow.mainloop()