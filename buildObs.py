import json
from copy import deepcopy


def run_build_obs(config, ss_config):
    cols, rows = config["cols"], config["rows"]
    width, height = config["width"], config["height"]
    fullscreen = config["fullscreen"]
    mcdirs = config["mcdirs"]

    if rows*cols > len(mcdirs):
        raise Exception(
            "mcdirs.txt either empty or not doesnt have enough to support instance count")
    # Generate sources
    sources = []
    for i in range(cols*rows):
        with open("../data/defaults/default-instance-source.json") as f:
            base = json.load(f)
            base["settings"]["window"] = f"Minecraft* - Instance {i+1}:GLFW30:javaw.exe"
            base["name"] = f"mc {i+1}"
            base["id"] = "window_capture"
            base["versioned_id"] = "window_capture"
            sources.append(base)
            new_base = deepcopy(base)
            new_base["name"] = f"t-mc {i+1}"
            sources.append(new_base)
        with open("../data/defaults/default-lock.json") as f:
            base = json.load(f)
            base["name"] = f"lock {i+1}"
            base["settings"]["file"] = f"{mcdirs[i]}lock.png"
            sources.append(base)
    if fullscreen:
        for i in range(cols*rows):
            with open("../data/defaults/default-instance-source.json") as f:
                base = json.load(f)
                base["settings"]["window"] = f"Minecraft* - Instance {i+1}:GLFW30:javaw.exe"
                base["name"] = f"gc-mc {i+1}"
                base["settings"]["capture_mode"] = "window"
                base["settings"]["priority"] = 0
                base["settings"]["hook_rate"] = 3
                base["id"] = "game_capture"
                base["versioned_id"] = "game_capture"
                sources.append(base)

    # Generate wall
    wall_insts = []
    wall_locks = []
    for i in range(cols*rows):
        bounds = (width / cols, height / rows)
        with open("../data/defaults/default-wall-instance.json") as f:
            base = json.load(f)
            base["name"] = f"mc {i+1}"
            base["bounds"]["x"] = bounds[0]
            base["bounds"]["y"] = bounds[1]
            base["id"] = i + 2
            x, y = i % cols, i // cols
            base["pos"]["x"] = bounds[0] * x
            base["pos"]["y"] = bounds[1] * y
            wall_insts.append(base)
            new_base = deepcopy(base)
            new_base["name"] = f"lock {i+1}"
            new_base["bounds"]["x"] = height * 0.1
            new_base["bounds"]["y"] = height * 0.1
            new_base["pos"]["x"] += 10
            new_base["pos"]["y"] += 10
            wall_insts.append(new_base)

    wall = {}
    with open("../data/defaults/default-wall.json") as f:
        wall = json.load(f)
        wall["settings"]["items"] = wall_insts + \
            wall_locks + wall["settings"]["items"]

    # Generate instance scenes
    inst_scenes = []
    for i in range(cols*rows):
        with open("../data/defaults/default-instance-scene.json") as f:
            base = json.load(f)
            base["name"] = f"MultiMC-{i+1}"
            base["hotkeys"]["OBSBasic.SelectScene"][0]["key"] = f"OBS_KEY_NUM{i+1}"
            base["settings"]["id_counter"] = i + 2
            base["settings"]["items"][0]["bounds"]["x"] = width
            base["settings"]["items"][0]["bounds"]["y"] = height
            base["settings"]["items"][0]["name"] = f"gc-mc {i+1}" if fullscreen else f"mc {i+1}"
            inst_scenes.append(base)

    # Generate Tinder scene
    tinder_details = []
    for i in range(cols*rows):
        with open("../data/defaults/default-wall-instance.json") as f:
            base = json.load(f)
            base["name"] = f"t-mc {i+1}"
            base["bounds"]["x"] = width
            base["bounds"]["y"] = height
            base["id"] = (i**2) + 2
            tinder_details.append(base)

    with open("../data/defaults/default-instance-scene.json") as f:
        base = json.load(f)
        base["name"] = f"Tinder"
        base["settings"]["id_counter"] = i + 2
        base["settings"]["items"] = tinder_details
        inst_scenes.append(base)

    full_obs = {}
    with open("../data/defaults/default-base.json") as f:
        full_obs = json.load(f)
        full_obs["scene_order"].append({"name": "Wall"})
        for i in range(len(inst_scenes)):
            full_obs["scene_order"].append({"name": f"MultiMC-{i+1}"})
        full_obs["sources"] += sources
        full_obs["sources"].append(wall)
        full_obs["sources"] += inst_scenes
    full_obs["modules"]["advanced-scene-switcher"] = ss_config

    with open("../data/sceneCollection.json", "w") as f:
        json.dump(full_obs, f, indent=2)
