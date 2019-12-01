from threading import Thread

from display_image import display_image
from grab_image import grab_image
from motor_control import motor_control
from process_image import process_image
from command_lines import command_lines

#Main program runs all threads
def main():
    memory = {
        "running": True,
        "raw_image": None,
        "centroid": None,
        "image": None,
        "target": None,
        "cut_flag": False,
    }
    threads = [
        Thread(target=grab_image, args=(memory, )),
        Thread(target=process_image, args=(memory, )),
        Thread(target=display_image, args=(memory, )),
        Thread(target=motor_control, args=(memory, )),
        Thread(target=command_lines, args=(memory, ))
    ]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == "__main__":
    main()
