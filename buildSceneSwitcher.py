import json
import os


def run_build_scene_switcher(config):
    cols, rows = config["cols"], config["rows"]
    all_macros = []
    inst_file = os.getcwd() + "\\data\\instance.txt"
    bg_file = os.getcwd() + "\\data\\bg.txt"
    # Generate instance switcher macros
    for i in range(cols*rows):
        with open("./defaults/default-ss-instance.json") as f:
            base = json.load(f)
            base["actions"][0]["scene"] = f"MultiMC-{i+1}"
            base["conditions"][0]["file"] = inst_file
            base["conditions"][0]["text"] = str(i+1)
            base["name"] = f"Instance {i+1} switch"
            all_macros.append(base)

    # Generate wall switcher macro
    with open("./defaults/default-ss-wall.json") as f:
        base = json.load(f)
        base["conditions"][0]["file"] = inst_file
        all_macros.append(base)

    # Generate tinder switcher macros
    for i in range(cols*rows):
        # Generate tinder actions
        actions = []
        for j in range(cols*rows):
            with open("./defaults/default-ss-tinder-action.json") as f:
                base = json.load(f)
                base["action"] = int(i != j)
                base["settings"] = '{\n    \\"client_area\\": true,\n    \\"compatibility\\": false,\n    \\"cursor\\": true,\n    \\"method\\": 0,\n    \\"priority\\": 2,\n    \\"window\\": \\"Minecraft* - Instance 1:GLFW30:javaw.exe\\"\n}\n'
                base["source"] = f"t-mc {j+1}"
                actions.append(base)
        with open("./defaults/default-ss-tinder.json") as f:
            base = json.load(f)
        base["conditions"][0]["file"] = bg_file
        base["conditions"][0]["text"] = str(i+1)
        base["name"] = f"Tinder {i+1}"
        base["actions"] = actions
        all_macros.append(base)

    # Generate tinder hideall macro
    # Generate tinder actions
    actions = []
    for j in range(cols*rows):
        with open("./defaults/default-ss-tinder-action.json") as f:
            base = json.load(f)
            base["action"] = 1
            base["settings"] = '{\n    \\"client_area\\": true,\n    \\"compatibility\\": false,\n    \\"cursor\\": true,\n    \\"method\\": 0,\n    \\"priority\\": 2,\n    \\"window\\": \\"Minecraft* - Instance 1:GLFW30:javaw.exe\\"\n}\n'
            base["source"] = f"t-mc {j+1}"
            actions.append(base)
    with open("./defaults/default-ss-tinder.json") as f:
        base = json.load(f)
        base["conditions"][0]["file"] = bg_file
        base["conditions"][0]["text"] = 0
        base["name"] = f"Tinder hide all"
        base["actions"] = actions
        all_macros.append(base)

    # Put all macros in scene switcher
    ss_config = {}
    with open("./defaults/default-scene-switcher.json") as f:
        ss_config = json.load(f)
        ss_config["macros"] = all_macros

    # Write to file
    with open("sceneSwitcher.txt", "w") as f:
        json.dump(ss_config, f, indent=2)
