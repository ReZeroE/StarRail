# Honkai Star Rail - `starrail`


<img src="https://i.imgur.com/8Elhiqy.jpg" width="400" height="auto" align="left"/>
<ul>
  
```
Honkai: Star Rail Automation Package
- Auto Resources Grind
- Auto Daily Login and Award Collection

Supported OS Platforms:
- Windows [Official Star Rail Installation]

Android/iOS emulators are not supported.
```

| [Overview](https://github.com/ReZeroE/StarRail#installation--setup) |  -  |
[Installation / Setup](https://github.com/ReZeroE/StarRail#installation--setup) | - |
[Usage](https://github.com/ReZeroE/StarRail/tree/dev#usage) |

</ul>
<br clear="left"/>

**Note: This package is currently under development - [`Development Status :: 1 - Planning`]**

***

## Overview

The `starrail` package is a Python3-based module that facilitates the automation of various tasks pertaining to Honkai Star Rail. This package is currenly undergoing active development, and additional details will be made available in due course.

Features in development:
- `starrail` UI
- Auto Resources Grind
- Auto Daily Login and In-Game Award Collection
- Scheduler System For Schdeduling Tasks (login + grind + etc.)

***

## Installation / Setup
The install the `starrail` package, run:
```shell
pip install starrail
```
**OR**
```shell
git clone https://github.com/ReZeroE/StarRail.git
cd StarRail/
pip install .
```

After `pip` installing the module, configure the module by running:
```
starrail configure
```
and then follow the promopted steps to configure the module.

***

## Usage

**Note: The module is currently still in an early stage of development and many intended features for this package are yet to be implemented. Please refer to the [CHANGELOG.md](https://github.com/ReZeroE/StarRail/blob/dev/CHANGELOG.md) for any recent updates.**


### 1. User-Interface

The user-interface for the `starrail` package is still in development. Once completed, it will be the main source for controlling all operations supported by `starrail`.


### 2. Command-Line Commands
The `starrail` module provides a set of basic command-line commands to interact with the game. These features are intended to be integrated with the `starrail` user-interface in future updates.

1. Start Game
```
starrail start
```
2. Stop Game (started from `starrail start`)
```
starrail stop
```
3. Overwrite StarRail's Path in `starrail`:
```
starrail set-path
```
4. Configure `starrail`
```
starrail configure
```
5. Show configuration Status:
```
starrail show-config
```


## Disclaimer
The "starrail" Python3-based module is an external script/tool
designed to automate the gameplay of Honkai Star Rail. It is designed
solely interacts with the game through the existing user interface,
and it abides by the Fair Gaming Declaration set forth by COGNOSPHERE
PTE. LTD. The package is designed to provide a streamlined and
efficient way for users to interact with the game through features
already provided within the game, and it does not, in any way, intend 
to damage the balance of the game or provide any unfair advantages. 
The package does not modify any game files or game code in any way.

The creator(s) of this package has no relationship with MiHoYo, the
game's developer. The use of this package is entirely at the user's
own risk, and the creator accepts no responsibility for any damage or
loss caused by the package's use. It is the user's responsibility to
ensure that they use the package according to Honkai Star Rail's Fair
Gaming Declaration, and the creator accepts no responsibility for any
consequences resulting from its misuse, including game account
penalties, suspension, or bans.

Please note that according to MiHoYo's [Honkai: Star Rail's Fair Gaming Declaration](https://hsr.hoyoverse.com/en-us/news/111244):

    "It is strictly forbidden to use external plug-ins, game
    accelerators/boosters, scripts, or any other third-party tools
    that damage the balance of the game. Once discovered, COGNOSPHERE
    PTE. LTD. (referred to as "we" henceforth) will take appropriate
    actions depending on the severity and frequency of the offenses.
    These actions include removing rewards obtained through such
    infringements, suspending the game account, or permanently
    banning the game account. Therefore, the user of this package
    must be aware that the use of this package may result in the
    above actions being taken against their game account by MiHoYo."

By using this package, the user agrees to ALL terms and conditions
and acknowledges that the creator will not be held liable for any
negative outcomes that may occur as a result of its use.

## License

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/220px-MIT_logo.svg.png" align="left" width="150"/>

<ul>
 - MIT Licensed
</ul>

<br clear="left"/>
