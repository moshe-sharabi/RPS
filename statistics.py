import numpy as np
import util
import Constants
import matplotlib.pyplot as plt

WIN_IND = 0
LOSS_IND = 1
DRAW_IND = 2

IND_RESULT_DIC = {Constants.WIN : WIN_IND, Constants.LOSS : LOSS_IND, Constants.DRAW : DRAW_IND}


def parse_stats(path):
    with open(path, "r") as fp:
        file = fp.read()
    fp.close()
    lines = file.split("\n")
    statist = []
    entire_history = []
    normal_stats = []
    length_list = []
    c = util.Counter()
    for line in lines[:-1]:
        games = line.split(" ")
        player_stats = np.zeros((3,))
        if len(games) < 0:
            continue
        for game in games:
            c[game[Constants.INDEX_OF_PLAY]] += 1
            if game == '':
                continue
            player_stats[IND_RESULT_DIC[game[Constants.INDEX_OF_RESULT]]] += 1
        length_list.append(len(games))
        statist.append(player_stats)
        normal_stats.append(player_stats/len(games))
        entire_history.append(games)
    return np.array(statist), entire_history, np.array(normal_stats), c, np.array(length_list)


stats, history, normal, c, length_list = parse_stats("examples/reflex_examples.txt")
idk = history
length = float(sum(len(x) for x in idk))
print("r: " + str(c[Constants.Rock]/length) + " " +"p:" + str(c[Constants.Paper]/length) + " "  + "s: " + str(c[Constants.Scissors]/length) + " " )
plt.plot(list(range(len(normal))), normal[:, 0], label="agent loss")
plt.plot(list(range(len(normal))), normal[:, 1], label="agent won")
plt.plot(list(range(len(normal))), normal[:, 2], label="agent draw")
plt.xlabel("players")
plt.ylabel("percentage of")
plt.legend()

print("Agent average rate of winning:" + str(np.average(normal[:, 1])) + "  " + "median rate of winning:" +
      str(np.median(normal[:, 1])) + " "+"agent max precentage winning"+str(np.max(normal[:, 1])) + " "+
      "agent min precentage winning"+str(np.min(normal[:, 1]))+"\n")
print("Agent average rate of losing:" + str(np.average(normal[:, 0])) + "  " + "median rate of losing:" +
      str(np.median(normal[:, 0]))  + " "+"agent max precentage losingg:"+str(np.max(normal[:, 0])) + " "+
      "agent min precentage losing"+str(np.min(normal[:, 0])) + "\n")
print("Agent average rate of drawing:" + str(np.average(normal[:, 2])) + "  " + "median rate of drawing:" +
      str(np.median(normal[:, 2])) + " " + "agent max precentage drawing:"+str(np.max(normal[:, 2])) + " "+
      "agent min precentage drawing"+str(np.min(normal[:, 2]))+"\n")
print("average game_length:" + str(np.average(length_list)) + "  " + "median lenght:" +
      str(np.median(length_list)) + " " + "max length game:"+str(np.max(length_list)) + " "+
      "min game length"+str(np.min(length_list))+"\n")

plt.show()
idk = 0