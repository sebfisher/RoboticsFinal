from time import sleep

#Command Line Interpreter
#User enters one of 4 colors to assign as target
def command_lines(memory={}):

    target_colors = ["Red", "Blue", "Yellow", "Green"]

    while memory.get("running"):
        new_target = input("Target color: ")
        if new_target in target_colors:
            memory["cut_flag"] = False
            memory["target"] = new_target
            sleep(13)
