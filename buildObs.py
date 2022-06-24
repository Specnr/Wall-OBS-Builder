import json


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
fullscreen = get_valid_input(
    "Do you play in Fullscreen? (y/n) ", lambda x: x in {"y", "n"}) == "y"
cols = int(get_valid_input("Number of columns: ",
                           lambda x: x.isdigit() and int(x) > 0))
rows = int(get_valid_input(
    "Number of rows: ", lambda x: x.isdigit() and int(x) > 0))
# Specifically for obs
screen_width = float(get_valid_input(
    "Screen width (OBS base resolution): ", lambda x: x.isdigit() and int(x) > 0))
screen_height = float(get_valid_input(
    "Screen height (OBS base resolution): ", lambda x: x.isdigit() and int(x) > 0))

# Generate sources
sources = []
for i in range(cols*rows):
    with open("./defaults/default-instance-source.json") as f:
        base = json.load(f)
        base["settings"]["window"] = f"Minecraft* - Instance {i+1}:GLFW30:javaw.exe"
        base["name"] = f"mc {i+1}"
        base["id"] = "window_capture"
        base["versioned_id"] = "window_capture"
        sources.append(base)

if fullscreen:
    for i in range(cols*rows):
        with open("./defaults/default-instance-source.json") as f:
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
for i in range(cols*rows):
    bounds = (screen_width / cols, screen_height / rows)
    with open("./defaults/default-wall-instance.json") as f:
        base = json.load(f)
        base["name"] = f"mc {i+1}"
        base["bounds"]["x"] = bounds[0]
        base["bounds"]["y"] = bounds[1]
        base["id"] = i + 2
        x, y = i % cols, i // cols
        base["pos"]["x"] = bounds[0] * x
        base["pos"]["y"] = bounds[1] * y
        wall_insts.append(base)

wall = {}
with open("./defaults/default-wall.json") as f:
    wall = json.load(f)
    wall["settings"]["items"] = wall_insts + wall["settings"]["items"]

# Generate instance scenes
inst_scenes = []
for i in range(cols*rows):
    with open("./defaults/default-instance-scene.json") as f:
        base = json.load(f)
        base["name"] = f"MultiMC-{i+1}"
        base["hotkeys"]["OBSBasic.SelectScene"][0]["key"] = f"OBS_KEY_NUM{i+1}"
        base["settings"]["id_counter"] = i + 2
        base["settings"]["items"][0]["bounds"]["x"] = screen_width
        base["settings"]["items"][0]["bounds"]["y"] = screen_height
        base["settings"]["items"][0]["name"] = f"gc-mc {i+1}" if fullscreen else f"mc {i+1}"
        inst_scenes.append(base)

full_obs = {}
with open("./defaults/default-base.json") as f:
    full_obs = json.load(f)
    full_obs["scene_order"].append({"name": "Wall"})
    for i in range(len(inst_scenes)):
        full_obs["scene_order"].append({"name": f"MultiMC-{i+1}"})
    full_obs["sources"] += sources
    full_obs["sources"].append(wall)
    full_obs["sources"] += inst_scenes

with open("sceneCollection.json", "w") as f:
    json.dump(full_obs, f, indent=2)
