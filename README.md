# Honkai: Star Rail - `starrail`

   



<p align="center">
  <img src="https://i.imgur.com/lE9hrlV.png" height="auto" alt="Centered Image"/>
</p>

![badge](https://img.shields.io/pypi/dm/starrail) ![GitHub License](https://img.shields.io/github/license/rezeroe/starrail) ![support](https://img.shields.io/badge/support-Python_3.7%2B-blue) ![size](https://img.shields.io/github/repo-size/rezeroe/starrail)


## Overview


The `starrail` package is a CLI (command-line interface) tool designed for managing and interacting with the game, Honkai: Star Rail, directly from your terminal. 



### Key Features:
- **Game Launch Control**
   - Start/Stop the game application directory from the terminal (skips launcher).
   - Schedule the game to start/stop at any given time (i.e. 10:30AM).

     
- **Simple Automation**
   - Custom Macros: Record and playback recorded mouse + keyboard click sequences in-game.
   - Uniform Click: Allows automatic uniform-interval mouse clicking (duration can be randomized).

     
- **Binary Decoding**
   - Web Cache: Access decoded web cache URLs containing information about pulls, events, and announcements.
   - Streaming Assets: Access detailed client streaming asset information (read-only).
   - Supplement Binary Decoder: Provides supplementary tools to decode any ASCII-based binary file.

     
- **Other Features**
   - Screenshots: Open the screenshots directory from the CLI without the game launcher. 
   - Official Pages: Open the official HoyoVerse web pages easily from the CLI.

<br/>





> [!NOTE]  
> **Installation Requirements**
>  - Windows 10 or later
>  - Python 3.7 or later
>  - Official Honkai: Star Rail Installation

<br/>

Please review the CHANGELOG for the latest project updates and the [developer's note](https://github.com/ReZeroE/StarRail/wiki/99.-Developer's-Note) for more information regarding the project overhaul.

<br/>



***

<br/>

![CLI](https://i.imgur.com/882zWGf.png)

# Installation / Setup




**STEP 1 - To Install** the `starrail` package, run with **admin permissions**:
```shell
> pip install starrail==1.0.5

OR

> git clone https://github.com/ReZeroE/StarRail.git
> cd StarRail/
> pip install -e .
```

<br/>

**STEP 2 - To configure** the `starrail` module after installing, run:
```shell
> starrail configure
```

<br/>

**STEP 3 - To verify** that the installation was successful, run:
```shell
> starrail config
```

<br/>

> [!NOTE]
> If you encounter any issues during the installation/setup process, visit [this page](https://github.com/ReZeroE/StarRail/wiki/99.-Common-Setup-Issues) for more help!


<br/>

***

<br/>


# Start CLI

The `starrail` package provides its own standalone CLI environment. You may access the CLI by running:
```shell
> starrail
```
This will bring up the StarRail CLI environment where all the commands can be executed without the `starrail` prefix.

![ABC](https://i.imgur.com/cFKRjFV.png)

The StarRail CLI environment facilitates efficient execution of the package's supported commands (see Usage Guide section below). Although all commands can be executed directly outside of the CLI environment in any terminal, activating the StarRail CLI allows you to run commands without the `starrail` prefix.

> [!NOTE]
> 
> Inside of the StarRail CLI:
> ```shell
> > about
> ```
> 
> Outside of the StarRail CLI (any terminal):
> ```shell
> > starrail about
> ```


For this guide, all following commands will be shown as if the CLI environment has not been activated.

<br/>

***

<br/>



# Usage Guide

Below is a brief overview of all the features supported by the `starrail` package. Each section includes a link to a full documentation page where each function is detailed comprehensively.

- [Package Info](https://github.com/ReZeroE/StarRail/wiki/3.-Package-Information)
   - About Package
   - Version
   - Author
   - Repository

- [CLI Launcher & Scheduler](https://github.com/ReZeroE/StarRail/wiki/4.-Start-Stop-&-Schedule-Game)
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

For the entire list of commands available in the `starrail` package, run:
```shell
> starrail help
```

<br/>


## 1. Package Info
To see the general information about the `starrail` package, run:
```shell
> starrail about                # Shows all information about the package

OR

> starrail version              # Shows HSR and SR-CLI package version
> starrail author               # Shows author information
> starrail repo [--open]        # Shows repository link
```

<br/>

***

<br/>


## 2. Start/Stop & Schedule Game
To start, stop, or schedule the start or stop of Honkai: Star Rail, the following commands are provided.

### ☆ Start Game
To start Honkai: Star Rail, run:
```shell
> starrail start
```

<br/>

### ☆ Stop Game
To stop Honkai: Star Rail, run:
```shell
> starrail stop
```

<br/>

### ☆ Schedule Start/Stop
To schedule the start/stop of Honkai: Star Rail at a given time, you may use the scheduler supplied in the `starrail` package.

To view the scheduler's help panel, run:
```shell
> starrail schedule
```

**Supported Scheduler Commands** (see usage below)
1. Show Schedule
2. Add Schedule
3. Remove Schedule
4. Clear (remove all) Schedules

```
Example Command                                    Description
----------------------------------------           ----------------------------------------------
starrail schedule add --time 10:30 --action start  Schedule Honkai Star Rail to START at 10:30 AM
starrail schedule add --time 15:30 --action stop   Schedule Honkai Star Rail to STOP  at 3:30 PM
starrail schedule remove                           Remove an existing scheduled job
starrail schedule show                             Show all scheduled jobs and their details
starrail schedule clear                            Cancel all scheduled jobs (irreversible)
```


> [!NOTE]
> **For the full documentation on scheduling**, visit [this page](https://github.com/ReZeroE/StarRail/wiki/4.-CLI-Launcher-&-Scheduler).

<br/>

***

<br/>

## 3. Game Configuration

To view Honkai: Star Rail's configuration as well as its detailed client information, several commands are provided.

### ☆ Real-time Game Status
To show the real-time status of the game while it's running, run:
```shell
> starrail status
```
```
               HSR Status Details
-------------  -------------------------------------
Status         ✓ Running
Process ID     59420
Started On     2024-0x-xx 15:11:04
CPU Percent    1.3%
CPU Affinity   0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
IO Operations  Writes: 247728, Reads: 580093
```
To show live game status non-stop, run with argument `-l` or `--live`:
```shell
> starrail status [-l|--live]
```

<br/>

### ☆ Base Game Information
To view the game's basic information configured under the `starrail` package listed below, run:
- Game Version
- Game Executable Location
- Game Screenshots Directory
- Game Logs Directory
- Game Executable SHA256

```shell
> starrail config
```
```
Title               Details                                           Related Command
------------------  ------------------------------------------------  --------------------
Game Version        2.3.0                                             starrail version
Game Executable     E:\Star Rail\Game\StarRail.exe                    starrail start/stop
Game Screenshots    E:\Star Rail\Game\StarRail_Data\ScreenShots       starrail screenshots
Game Logs           E:\Star Rail\logs                                 starrail game-logs
Game (.exe) SHA256  2axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx2c
```

<br/>

### ☆ Detailed Client Information
To view detailed information about Honkai: Star Rail, run:
- Client Version
- Client Datetime
- Client Detailed Version
- Application Identifier
- Service Entrypoint(s)
- Client Engine Version
- Other Information

```shell
> starrail details
```
```
Title                   Details (binary)
----------------------  --------------------------------------------------------
Version                 V2.3Live
Datetime String         20240607-2202
Detailed Version        7x02406xx-2xx2-V2.3Live-7xxxxx5-CNPRODWin2.3.0-CnLive-v2
Application Identifier  com.miHoYo.hkrpg
Service Endpoints       https://globaldp-prod-cn0x.bhsr.com/query_dispatch
Engine Version          EngineReleaseV2.3
Other                   StartAsset
                        StartDesignData
                        dxxxxxxxxb
                        f4xxxxxxxxxxxxxxxxxxxxxxa7
```

<br/>

***

<br/>


## 4. Simple Automation
The `starrail` package supports two automation features to assist with the gameplay of Honkai: Star Rail.

### ☆ Custom Automation
This feature enables users to record a sequence of keyboard and mouse actions and replay them within the game. It is specifically optimized for Honkai: Star Rail, ensuring that all actions are only recorded and executed when the game is in focus, thereby preventing unintentional interactions with other applications.

To start, enter the following to bring up the help panel for automation:
```shell
> starrail automation
```

```
Example Command             Description
--------------------------  ----------------------------------------------------
starrail automation record  Create and record a new automation sequence (macros)
starrail automation show    List all recorded automation sequences
starrail automation run     Run a recorded automation sequence
starrail automation remove  Delete a recorded automation sequence
starrail automation clear   Delete all recorded automation sequences
```
> [!NOTE]
> **For a full documentation / guide on custom automation**, visit [this page](https://github.com/ReZeroE/StarRail/wiki/6.-Simple-Automation). 


<br/>


### ☆ Uniform Clicks
This feature assists with repetitive mouse clicking (such as for "Start Again" after completing a stage in HSR).

To use this feature, run:
```shell
> starrail click
```

<br/>

**For example**, to control the mouse to click:
1. Once every 5 seconds and
2. Hold for 2 seconds each click
```shell
> starrail click --interval 5 --randomize 1 --hold 2
```

<br/>

***

<br/>


## 5. Official Pages

The `starrail` package supports the following simple commands to access Honkai: Star Rail's official pages.

### ☆ Offical Homepage
To start Honkai: Star Rail's Official Home Page, run:
```shell
> starrail homepage
OR
> starrail homepage -cn # CN Homepage
```


<br/>

### ☆ Official HoyoLab Page
To start Honkai: Star Rail's Official HoyoLab Page, run:
```shell
> starrail hoyolab
```

<br/>

### ☆ Offical Youtube Page
To start Honkai: Star Rail's Official Youtube Page, run:
```shell
> starrail youtube
```

<br/>

### ☆ Offical BiliBili Page (CN)
To start Honkai: Star Rail's Official BiliBili Page, run:
```shell
> starrail bilibili
```

<br/>

***

<br/>

## 6. Binary Utilities

The `starrail` package supports a list of binary-related utility commands for web cache and streaming assets decoding.

### ☆ Web Cache
Honkai: Star Rail's web cache stores recent web data. To access the decoded web cache URLs containing cached information about events, pulls, and announcements without loading into the game, run:
```shell
> starrail webcache
```
The results will be listed in two sections:
1. Events/Pulls Web Cache
2. Announcements Web Cache


<br/>

### ☆ Cached Pulls
To access your Honkai: Star Rail's cached pulls information without logging in to the game, run:
```shell
> starrail pulls
```
Web view of all the pull information will open in the default browser.

<br/>

### ☆ Supplement Binary Decoder
The package provides this supplementary tools to decode any ASCII-based binary file.
```shell
> starrail decode --path <path_to_file>
```
All ASCII-based information will be outputted into a table with index listings as following:
```
  Index  Content
-------  --------------
      0  This is a test
      1  /Root xxxx 0 R
      2  /Info 1 0 R>>
      3  start ref
    ...  .....
```

<br/>

***

<br/>


## 7. Misc Utilities

The `starrail` package provides the following quality-of-life utility features to quickly access key game information.

### ☆ Access Screenshots
To access the screenshots without the client or searching through the directory, run:
```shell
> starrail screenshots
```

<br/>

### ☆ Access Game Logs
To access the game's log files, run:
```shell
> starrail game-logs
```

<br/>


### ☆ Session runtime
To get the runtime of the current Honkai: Star Rail session (how long the game has been running since it started), run:
```shell
> starrail runtime
```

<br/>

***

<br/>

## Disclaimer

The "starrail" Python 3 module is an external CLI tool
designed to automate the gameplay of Honkai Star Rail. It is designed
solely interacts with the game through the existing user interface,
and it abides by the Fair Gaming Declaration set forth by COGNOSPHERE
PTE. LTD. The package is designed to provide a streamlined and
efficient way for users to interact with the game through features
already provided within the game, and it does not, in any way, intend 
to damage the balance of the game or provide any unfair advantages. 
The package does NOT modify any files in any way.

The creator(s) of this package has no relationship with MiHoYo, the
game's developer. The use of this package is entirely at the user's
own risk, and the creator accepts no responsibility for any damage or
loss caused by the package's use. It is the user's responsibility to
ensure that they use the package according to Honkai Star Rail's Fair
Gaming Declaration, and the creator accepts no responsibility for any
consequences resulting from its misuse, including game account
penalties, suspension, or bans.

By using this package, the user agrees to ALL terms and conditions
and acknowledges that the creator will not be held liable for any
negative outcomes that may occur as a result of its use.


<br/>

***

<br/>

## Repository Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ReZeroE/StarRail&type=Date)](https://star-history.com/#ReZeroE/StarRail&Date)


<br/>

***

<br/>

## License

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/220px-MIT_logo.svg.png" align="left" width="150"/>

<ul>
 - MIT Licensed
</ul>

<br clear="left"/>

