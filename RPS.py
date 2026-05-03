# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[]):
    # Clear opponent's last move and mine
    if prev_play == "":
        opponent_history.clear()
        my_history.clear()

    if prev_play:
        opponent_history.append(prev_play)

    if is_quincy(opponent_history):
        move = counter_quincy(opponent_history)
    elif is_kris(opponent_history, my_history):
        move = counter_kris(my_history)
    elif is_mrugesh(opponent_history, my_history):
        move = counter_mrugesh(my_history)
    elif len(opponent_history) >= 2:
        move = anti_abbey_move(my_history)
    else:
        move = predict_next_move(opponent_history)

    my_history.append(move)
    return move

def is_quincy(opponent_history):
    if len(opponent_history) < 5:
        return False
    
    recent = "".join(opponent_history[-5:])

    quincy_patterns = [
        "RRPPS",
        "RPPSR",
        "PPSRR",
        "PSRRP",
        "SRRPP"
    ]

    return recent in quincy_patterns

def is_kris(opponent_history, my_history):
    if len(opponent_history) < 10 or len(my_history) < 10:
        return False
    
    correct = 0

    for i in range(1, len(opponent_history)):
        if opponent_history[i] == counter_move(my_history[i - 1]):
            correct += 1
    
    return correct / (len(opponent_history) - 1) > 0.8

def is_mrugesh(opponent_history, my_history):
    if len(my_history) < 10 or len(opponent_history) < 10:
        return False
    
    correct = 0

    for i in range(10, len(opponent_history)):
        recent_my_moves = my_history[i - 10:i]

        most_frequent = max(["R", "P", "S"], key=recent_my_moves.count)

        predicted_mrugesh_move = counter_move(most_frequent)

        if opponent_history[i] == predicted_mrugesh_move:
            correct += 1
        
    return correct / (len(opponent_history) - 1) > 0.7

def predict_next_move(opponent_history):
    if len(opponent_history) == 0:
        return "R"

    if len(opponent_history) < 4:
        return counter_move(opponent_history[-1])

    pattern_length = 3
    history_string = "".join(opponent_history)
    recent_pattern = history_string[-pattern_length:]

    possible_next_moves = {
        "R": 0,
        "P": 0,
        "S": 0
    }

    # Look through history for the same pattern
    for i in range(len(history_string) - pattern_length):
        pattern = history_string[i:i + pattern_length]

        if pattern == recent_pattern:
            next_move = history_string[i + pattern_length]
            possible_next_moves[next_move] += 1
    
    # Pick the move that most often followed this pattern
    prediction = max(possible_next_moves, key=possible_next_moves.get)

    # Fallback if the pattern was never seen before
    if possible_next_moves[prediction] == 0:
        prediction = opponent_history[-1]
    
    return prediction

def counter_move(move):
    counters = {
        "R": "P",
        "P": "S",
        "S": "R"
    }
    return counters[move]


def counter_quincy(opponent_history):
    recent = "".join(opponent_history[-5:])

    next_move_lookup = {
        "RRPPS": "R",
        "RPPSR": "R",
        "PPSRR": "P",
        "PSRRP": "P",
        "SRRPP": "S"
    }

    
    predicted_next = next_move_lookup[recent]

    return counter_move(predicted_next)

def counter_kris(my_history):
    if len(my_history) == 0:
        return "R"
    
    kris_prediction = counter_move(my_history[-1])
    return counter_move(kris_prediction)

def anti_abbey_move(my_history):
    play_order = { 
        "RR": 0,
        "RP": 0,
        "RS": 0,
        "PR": 0,
        "PP": 0,
        "PS": 0,
        "SR": 0,
        "SP": 0,
        "SS": 0,
    }

    # Build the same pair cunters Abbey builds from our history
    for i in range(len(my_history) - 1):
        pair = my_history[i] + my_history[i + 1]
        play_order[pair] += 1
    
    last_move = my_history[-1]

    potential_plays = [
        last_move + "R",
        last_move + "P",
        last_move + "S",
    ]

    sub_order = {
        k: play_order[k]
        for k in potential_plays
    }

    abbey_prediction = max(sub_order, key=sub_order.get)[-1]

    # Abbey will counter this prediction
    abbey_response = counter_move(abbey_prediction)

    # Counter Abbey's response to the prediction
    return counter_move(abbey_response)

def counter_mrugesh(my_history):
    if len(my_history) < 10:
        return "S"

    recent_my_moves = my_history[-10:]

    most_frequent = max(["R", "P", "S"], key=recent_my_moves.count)

    mrugesh_next_move = counter_move(most_frequent)

    return counter_move(mrugesh_next_move)

