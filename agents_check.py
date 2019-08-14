from learner import *
import multiprocessing as mp

folder = AI_agent.example_folder_name
file1 = os.path.join(folder, "ai_examples.txt")
file2 = os.path.join(folder, "epoch_examples.txt")

save_to = open(os.path.join('.', 'agent_scores_plus_prob.txt'), 'w')

histories = read_histories(file1)
histories += read_histories(file2)


def get_scores_for_params(params):
    epoch, _gamma = params
    gamma = 0.1 * _gamma
    score1 = 0
    score2 = 0
    score1_prob = 0
    count = 0
    for match in histories:
        agent1 = Ai2(epoch, 5, gamma)
        # agent2 = OnlineEpochAgent(epoch,5,gamma)
        for i in range(len(match) - 2):
            count += 1
            cur_hist = match[:i]
            played = match[i][INDEX_OF_PLAY]

            prediction = agent1.predict(cur_hist)
            comp_move = prediction.best_counter()
            game = PAIR_TRANSLATOR[played + comp_move]
            comp_result = neg[game][INDEX_OF_RESULT]
            score1 += points[comp_result]

            comp_move = prediction.best_counter_probabilistic()
            game = PAIR_TRANSLATOR[played + comp_move]
            comp_result = neg[game][INDEX_OF_RESULT]
            score1_prob += points[comp_result]

            # comp_move = agent2.predict(cur_hist).best_counter()
            # game = PAIR_TRANSLATOR[played + comp_move]
            # comp_result = neg[game][INDEX_OF_RESULT]
            # score2 += points[comp_result]
    norm1 = score1 / count
    norm_prob1 = score1_prob / count
    norm2 = score2 / count
    print(f"Ai2({epoch},5,{gamma}) score: {score1}, normalized: {norm1}")
    # save_to.write(f"Ai2({epoch},5,{gamma}) score: {score1}, normalized: {norm1}\n\n")
    print(f"Ai2_probapilistic({epoch},5,{gamma}) score: {score1_prob}, normalized: {norm_prob1}")
    # save_to.write(f"Ai2_probapilistic({epoch},5,{gamma}) score: {score1_prob}, normalized: {norm_prob1}\n\n")
    # print(f"OnlineEpochAgent({epoch},5,{gamma}) score: {score2}, normalized: {norm2}")
    # save_to.write(f"OnlineEpochAgent({epoch},5,{gamma}) score: {score2}, normalized: {norm2}\n\n")
    dict_ret = {"Ai2": score1, "ai2_prob": score1_prob}
    return dict_ret

arr = np.arange(6*11)
arr = arr.tolist()
for epoch in range(5,11):
    for _gamma in range(11):
        arr[(epoch-5)*11 + _gamma] = (epoch, _gamma)
pool = mp.Pool(mp.cpu_count())
res = pool.map(get_scores_for_params, arr)


for epoch in range(5,11):
    for _gamma in range(11):
        score1 = res[(epoch-5)*11 + _gamma]["Ai2"]
        score1_prob = res[(epoch-5)*11 + _gamma]["Ai2_prob"]
        print(f"Ai2({epoch},5,{gamma}) score: {score1}")
        save_to.write(f"Ai2({epoch},5,{gamma}) score: {score1}\n\n")
        print(f"Ai2_probapilistic({epoch},5,{gamma}) score: {score1_prob}")
        save_to.write(f"Ai2_probapilistic({epoch},5,{gamma}) score: {score1_prob}\n\n")
