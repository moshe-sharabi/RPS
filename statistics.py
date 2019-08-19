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
    for line in lines:
        if len(line)== 0:
            continue
        games = line.split(" ")
        player_stats = np.zeros((3,))
        if len(games) < 0:
            continue
        for game in games:
            if game == '':
                continue
            c[game[Constants.INDEX_OF_PLAY]] += 1

            player_stats[IND_RESULT_DIC[game[Constants.INDEX_OF_RESULT]]] += 1
        length_list.append(len(games))
        statist.append(player_stats)
        normal_stats.append(player_stats/len(games))
        entire_history.append(games)
    return np.array(statist), entire_history, np.array(normal_stats), c, np.array(length_list)

def calculate_distribution(local_history):
    player_stats = np.zeros((3,))
    for game in local_history:
        if game == '':
            continue
        player_stats[IND_RESULT_DIC[game[Constants.INDEX_OF_RESULT]]] += 1
    return player_stats/len(local_history)

def create_round_graph(entire_history):
    entire_history = list(filter((lambda x: len(x) > 50), entire_history))
    round_score = []
    for i in range(10):
        precentage_arr = np.zeros((3,))
        counter = 0
        for game in entire_history:
            if len(game) < (i+4)*10:
               continue
            counter += 1
            precentage_arr += calculate_distribution(game[(i+4)*10-1: (i+5)*10])
        round_score.append(precentage_arr/counter)
    return np.array(round_score)




stats, history, normal, c, length_list = parse_stats("examples/forest_examples.txt")
i = np.argmax(normal[:, 0])
print(i)
idk = history
length = float(sum(len(x) for x in idk))
print("num turns: " + str(length))
print("r: " + str(c[Constants.Rock]/length) + " " +"p:" + str(c[Constants.Paper]/length) + " "  + "s: " + str(c[Constants.Scissors]/length) + " " )
plt.plot(list(range(len(normal))), normal[:, 0], label="agent loss")
plt.plot(list(range(len(normal))), normal[:, 1], label="agent won")
plt.plot(list(range(len(normal))), normal[:, 2], label="agent draw")
plt.xlabel("players")
plt.ylabel("percentage of")
plt.legend()

round_history = create_round_graph(history)


print("agent min precentage winning"+str(np.min(normal[:, 1]))+"  "+"median rate of winning:" +
      str(np.median(normal[:, 1])) + " " + "Agent average rate of winning:" + str(np.average(normal[:, 1])) + "  " +
      "agent max precentage winning:"+str(np.max(normal[:, 1])) + "\n")
print("agent min precentage drawing"+str(np.min(normal[:, 2]))+"  "+"median rate of drawing:" +
      str(np.median(normal[:, 2])) + " " + "Agent average rate of drawing:" + str(np.average(normal[:, 2])) + "  " +
      "agent max precentage drawing:"+str(np.max(normal[:, 2])) + "\n")
print("agent min precentage lossing"+str(np.min(normal[:, 0])) + "  " + "median rate of lossing:" +
      str(np.median(normal[:, 0])) + " " + "Agent average rate of lossing:" + str(np.average(normal[:, 0])) + "  " +
      "agent max precentage lossing:"+str(np.max(normal[:, 0])) + "\n")
print("min game length"+str(np.min(length_list)) + " " + "median lenght:" +str(np.median(length_list)) + " " +
      "average game_length:" + str(np.average(length_list)) + "  " + "max length game:"+str(np.max(length_list)) + "\n")

plt.show()

plt.plot(np.array(list(range(len(round_history))))*10+40, round_history[:, 0], label="agent loss")
plt.plot(np.array(list(range(len(round_history))))*10 + 40, round_history[:, 1], label="agent won")
plt.plot(np.array(list(range(len(round_history))))*10 + 40, round_history[:, 2], label="agent draw")
plt.xlabel("num_round")
plt.ylabel("average percentage of  in round")
plt.legend()
plt.show()
idk = 0