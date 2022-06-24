# Wall OBS-Builder

A tool that builds a basic scene collection for the wall with any specifications.

## Instructions

- First, you need Python installed, then run the buildObs.py script
- Enter in data that it asks for:
  - Note, for screen width & height, enter the numbers for the "Base (Canvas) Resolution" in OBS settings -> Video
  - The bigger number will be the width (unless youre streaming to like tiktok or some shit lul dubz)
- A sceneCollection.json file will be made. Go to OBS and select Scene Collection -> Import, then select this json file and hit "Import"
- In the new scene collection you can add your universal sources like audios to the Main Overlay and they will be carried over to each scene
- Finally, this doesnt set up Source Record for you, so just add that filter to the Wall scene and youll be set!