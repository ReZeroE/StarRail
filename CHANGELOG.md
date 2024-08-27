# Change Log

### Version 1.0.2 - [8/27/2024]
- Resolved issue with auto-detecting the game's executable's path.
    - New HoyoPlay launcher introduced a new game directory structure that broke old game detecting system. Package now matches:
        1. `.../Star Rail/Game/StarRail.exe`
        2. `.../Star Rail Games/StarRail.exe`
    - Implemented new "weak match" feature to future-proof another change in game directory structure. 
    - Added new error message if package is unable to locate the game.

### Version 1.0.1 - [8/26/2024]
- Resolved version support issues (now supports Python 3.7 and later).

### Version 1.0.0 - [8/1/2024]
1. Complete redesign of the entire project.
    - [Package Info](https://github.com/ReZeroE/StarRail/wiki/3.-Package-Information)
        - About Package
        - Version
        - Author
        - Repository

    - [CLI Launcher & Scheduler](https://github.com/ReZeroE/StarRail/wiki/4.-CLI-Launcher-&-Scheduler)
        - Start Game
        - Stop Game
        - Schedule Start/Stop

    - [Game Configuration](https://github.com/ReZeroE/StarRail/wiki/5.-Game-Configurations)
        - Real-time Game Status
        - Base Game Information
        - Detailed Client Information

    - [Simple Automation](https://github.com/ReZeroE/StarRail/wiki/6.-Simple-Automation)
        - Custom Automation
        - Uniform Clicks

    - [Official Page Access](https://github.com/ReZeroE/StarRail/wiki/7.-Official-Page-Access)
        - Official Homepage
        - Official Youtube Page
        - Official HoyoLab Page

    - [Binary Utilities](https://github.com/ReZeroE/StarRail/wiki/8.-Binary-Utilities)
        - Decoded Web Cache (events, pulls, announcements)
        - Cached Pull History
        - Supplementary Binary Decoder

    - [Misc Utilities](https://github.com/ReZeroE/StarRail/wiki/9.-Misc-Utilities)
        - View Screenshots
        - View Game Logs

<br/>

Please view the [developer's note](https://github.com/ReZeroE/StarRail/wiki/99.-Developer's-Note) for more information regarding the project overhaul.

<br/>

***

<br/>

## Legacy Version Logs

### Version 0.0.3 - [6/7/2023]
1. Optimized `starrail configure` to use multiprocessing Managers (speedup in local game search). 
2. Added feature to downscale screen feature matching threshold based on the native screen resolution.
    - Enabled `starrail` to support 4K, 2K, 1080P or lower resolution screens.
3. Added logout feature. 

### Version 0.0.3 - [6/4/2023]
1. Added new rewards logic maps (Daily Training, Assignments)
2. Restructured the code framework of logic maps for better optimization.
3. The starrail show-config command now displays the absolute path of the game executable after configuration.
4. Adjusted image feature matching values to allow for less accurate matches in specific circumstances.
5. The time delay following a simulated mouse or keyboard key click has been extended.

### Version 0.0.3 - [6/3/2023]
1. Added Logic Map for Calyx Golden (bud_of_memories, bud_of_aether, bud_of_threasures)
2. Tested automation features for login, reward collection, and Calyx Golden.
3. Implemented "secondary image detection" with SIFT and FLANN for non-centered buttons (non-centered buttons were previously tracked with pixels offsets (x, y)).   

### Version 0.0.3 - [6/1/2023]
1. Implemented "Logic Maps" structures (process sequence maps for automation).
2. Implemented base wrapper classes for auto grind(Calyx), reward collection, and login that utilizes the Logic Maps for automation.
3. Added Logic Maps for login and reward collection.
4. Updated project code structure.

### Version 0.0.3 - [5/21/2023]
1. Implemented SIFT (Scale Invariant Feature Transform) algorithm for feature detection and description, and FLANN (Fast Library for Approximate Nearest Neighbors) for feature matching. This is used to auto-detect buttons on-screen for executing process sequences. 
2. Implemented RANSAC for finding homography to account for any scale, rotation or translation between the images to support various game window sizes (4k, 2k, 1080p, etc).

### Version 0.0.3 - [5/10/2023]
1. Optimized the `starrail configure` process to use multithreading when searching for the local game instance (Honkai: Star Rail) for a decrease in runtime.

### Version 0.0.3 - [5/1/2023]
1. Removed faulty dependencies that cannot be properly installed from PyPI
2. Resolved game path auto-detection issue

### Version 0.0.2 - [4/30/2023]
1. Stablized commandline features for start, stop, configure
2. Added commandline feature for overwriting previous path configurations:
```shell
$ starrail set-path
```
3. And other efficiency and maintainability related optimizations

### Version 0.0.2 - [4/29/2023]
Added commandline support for the following operations (**UNSTABLE**):

1. Configure `starrail` (only once after download):
```shell
$ starrail configure
```
2. Starting Honkai: Star Rail from the commandline
```shell
$ starrail start
```
3. Terminating Honkai: Star Rail from the commandline (started from `starrail`)
```shell
$ starrail stop
```

### Version 0.0.1 - [4/26/2023]
Initial Release
