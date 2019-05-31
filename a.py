"""
@author Farzaneh.Tlb
5/26/19 5:24 PM
Implementation of psychophysics experiment(Fill this line)
"""

id = 1

import os
import random

import numpy as np
from psychopy import visual, event, core, monitors

response = []
temp_response = []

my_monitor = monitors.Monitor(name='zenbook')
my_monitor.setSizePix((1276, 886))
my_monitor.setWidth(32.4)
my_monitor.setDistance(57)
my_monitor.saveMon()

win = visual.Window(
    units="pix",
    monitor=my_monitor,
    color="black",
    fullscr=True
)

instructions = visual.TextStim(
    win=win,
)

instructions.text = """
Press the left arrow key when you see the male.\n
Press the right arrow key when you see the female.\n
Press any key to begin.
"""

instructions.draw()
win.flip()
event.waitKeys()
clock = core.Clock()
performance = 0
stim_duration_s = 0.05
interval1 = 0.45
interval2 = 0.05


def create_test_choice():
    trial_test_folder = ["-10", "-20", "-30", "-40", "0", "10", "20", "30", "40"]
    trial_test_file = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    test_list = [x + "/" + y for x in trial_test_folder for y in trial_test_file]
    test_list = test_list + test_list
    print(len(test_list))
    return test_list


def task_train():
    trial_number = 0
    performance = 0
    temp_response = []
    circle = visual.Circle(
        win=win,
        units="pix",
        radius=2,
        fillColor="red",
        lineColor="red"

    )
    while clock.getTime() < 1.5:
        circle.draw()
        win.flip()

    while performance < 0.1:
        trial_number += 1
        clock.reset()
        while clock.getTime() < stim_duration_s:
            file = random.choice(np.arange(1, 81, 1))
            img = visual.ImageStim(
                win=win,
                image="train/" + str(file) + ".png",
                units="deg",
                size=2,
            )
            img.draw()
            win.flip()
        win.flip()
        keys = event.waitKeys(
            keyList=["left", "right", "q"],
            timeStamped=clock
        )
        if (keys[0][0] == "q"):
            core.quit()
        if (keys[0][0] == "left" and file <= 40) or (
                keys[0][0] == "right" and (file > 41)):
            ans = True
            message = visual.TextStim(win, text="Correct", color="green", bold=True, height=50)
        else:
            ans = False
            message = visual.TextStim(win, text="Not Correct", color="red", bold=True, height=50)
        clock.reset()
        while clock.getTime() < interval1:
            message.draw()
            win.flip()

            # trial_data = [trial_number, folder, file, keys[0][0], keys[0][1]]
        while clock.getTime() < interval2:
            win.flip()
        temp_response.append(ans)
        if trial_number % 20 == 0:
            performance = sum(temp_response) / 20
            temp_response = []
            print(performance)
    return performance, trial_number


def task_test():
    trial_number = 0
    random.shuffle(test_list)
    circle = visual.Circle(
        win=win,
        units="pix",
        radius=2,
        fillColor="red",
        lineColor="red"

    )
    for image in test_list:
        trial_number += 1
        clock.reset()
        position = random.choice([1, 2])
        if position == 1:
            img = visual.ImageStim(
                win=win,
                image="test/" + image + ".png",
                units="deg",
                size=2,
                pos=(0, 3)

            )
        else:
            img = visual.ImageStim(
                win=win,
                image="test/" + image + ".png",
                units="deg",
                size=2,
                pos=(-3, 0)

            )

        clock.reset()
        while clock.getTime() < stim_duration_s:
            img.draw()
            circle.draw()
            win.flip()
        circle.draw()
        win.flip()
        keys = event.waitKeys(keyList=["left", "right", "q"], timeStamped=clock)
        clock.reset()
        # win.flip()
        while clock.getTime() < 0.5:
            circle.draw()
            win.flip()
        if position == 1:
            morph = 90
        else:
            morph = 180
        if (keys[0][0] == "q"):
            core.quit()
        elif (keys[0][0] == "left"):
            gender = "male"
        else:
            gender = "female"
        trial_data = [trial_number, image, gender, keys[0][1], morph]
        response.append(trial_data)
    return response


def rest():
    instructions = visual.TextStim(
        win=win,
    )

    instructions.text = """
    GREAT!\n
    Press any key to continue.. .
    """

    instructions.draw()
    win.flip()

    event.waitKeys()


test_list = create_test_choice()
performance, i = task_train()
event.clearEvents()
rest()
event.clearEvents()
trial_data = task_test()
trial_data.append([performance, i])

data_path = str(id) + ".csv"

#

#
data_path = str(id) + ".csv"
while (os.path.isfile(data_path)):
    id = id + 1
    data_path = str(id) + ".csv"
    if (id == 1000):
        break

np.savetxt(data_path, trial_data, fmt="%s")
win.close()
