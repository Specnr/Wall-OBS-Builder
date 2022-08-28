from buildObs import run_build_obs
from buildSceneSwitcher import run_build_scene_switcher
import os


def get_valid_input(ask, validity_check):
    ret = None
    while ret is None:
        got = input(ask)
        if (validity_check(got)):
            ret = got
        else:
            print("Didn't like that answer, try again.")
    return ret


# Inputs
config = {}
config["fullscreen"] = get_valid_input(
    "Do you play in Fullscreen? (y/n) ", lambda x: x in {"y", "n"}) == "y"
config["cols"] = int(get_valid_input("Number of columns: ",
                                     lambda x: x.isdigit() and int(x) > 0))
config["rows"] = int(get_valid_input(
    "Number of rows: ", lambda x: x.isdigit() and int(x) > 0))
# Specifically for obs
config["width"] = float(get_valid_input(
    "Screen width (OBS base resolution): ", lambda x: x.isdigit() and int(x) > 0))
config["height"] = float(get_valid_input(
    "Screen height (OBS base resolution): ", lambda x: x.isdigit() and int(x) > 0))
config["format"] = get_valid_input(
    "Current window/game capture naming format (leave blank if setting up new scene collection): ", lambda x: x.strip() != "")

if not os.path.exists("../data/mcdirs.txt"):
    print("Missing mcdirs.txt, please run TheWall.ahk with instances open first.")
    input("Exiting, press enter to continue...")
else:
    raw_mcdirs = {}
    with open("../data/mcdirs.txt") as f:
        for line in f:
            inst_num, path = line.strip().split("~")
            raw_mcdirs[int(inst_num)] = path
    config["mcdirs"] = [raw_mcdirs[i+1] for i in range(len(raw_mcdirs))]
    try:
        ss_config = run_build_scene_switcher(config)
        run_build_obs(config, ss_config)
        input("Complete, press enter to continue...")
    except Exception as e:
        print(e)
        input("An error has occurred, please try again...")
