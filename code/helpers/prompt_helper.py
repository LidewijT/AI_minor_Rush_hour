"""
Prompt helper consists of functions of prompts to be asked for in the main.py
prompt toolkit is used for this with the function WordCompleter, which is for
instance used to fill out the board and algorithm
"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# ------------------- initiate list of algorithms and boards -------------------
algorithm_list = ["randomise.random_car_move",
"priority_red_car.move_priority_red_car",
"breadth_first.Breadth_First_Search",
"depth_first.Depth_First_Search",
"depth_limited.Depth_Limited_Search",
"depth_hill_climber.DFS_Hill_Climber",
"depth_priority_children.PriorityChildren"]

board_list = ["Rushhour6x6_1", "Rushhour6x6_2", "Rushhour6x6_3",
"Rushhour9x9_4", "Rushhour9x9_5", "Rushhour9x9_6", "Rushhour12x12_7"]

# ------------------------- initiate word completers ---------------------------
board_completer = WordCompleter(board_list)

algorithm_completer = WordCompleter(algorithm_list)

yes_no_completer = WordCompleter(["yes", "no"])

# ------------------------- initiate prompt functions --------------------------
def get_yes_or_no(input):
    """
    Ensures an anwer can only be yes or no
    """
    answer = prompt(input, completer = yes_no_completer).lower()

    # failsave to ensure answer is yes or no
    while answer not in {"yes", "y", "no", "n"}:
        answer = prompt("Please respond with yes/no: ", completer = yes_no_completer)

    return answer

def experiment_bool_prompt():
    return get_yes_or_no("Do you want to run an experiment? (yes/no): ")

def visualisation_bool_prompt():
    return get_yes_or_no("Would you like to visualise a csv of moves? (yes/no): ")

def board_prompt():
    return prompt("What board do you want to run?\n(Hint: type an 'R'): ", \
    completer = board_completer) + ".csv"

def moves_input_prompt():
    return prompt("What csv file would you like to visualise?: ") + ".csv"

def algorithm_prompt():
    question = "What algorithm would you like to run? \
choose from: \nrandom, priority random, breath first search, depth first search\
depth limited search, depth hill climber or depth priority children: "

    answer = prompt(question, completer = algorithm_completer)

    # check if it is a valid algorithm
    while answer not in set(algorithm_list):
        print("please choose one of the autocomplete options")
        answer = prompt(question, completer = algorithm_completer)

    return answer


    return prompt("What algorithm would you like to run? \
choose from: \nrandom, priority random, breath first or depth first: "\
    , completer = algorithm_completer)

def branch_prompt():
    return get_yes_or_no("Would you like to add a branch and bound heuristic \
to your algorithm? (yes/no): ")

def runs_prompt():
    while True:
        try:
            answer = int(input("how many iterations do you want to run?: "))
            break

        except ValueError:
            print("Invalid input. Please enter an integer.")

    return answer

def max_depth_prompt():
    while True:
        try:
            answer = int(input("Give a max depth you'd like to run the \
algorithm to: "))
            break

        except ValueError:
            print("Invalid input. Please enter an integer.")

    return answer

def graph_bool_prompt():
    return get_yes_or_no("Would you like to test...: (yes/no)")

def png_output_prompt():
    return input("Give a file name to save the graph to: ") + ".png"

def graph_csv_output_prompt():
    return input("Give a file name to save the amount of moves to: ") + ".csv"

def csv_output_prompt():
    return input("Give a file name to save the made moves to: ") + ".csv"
