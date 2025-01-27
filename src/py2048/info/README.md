# 中文版 Chinese(Simplified)

# Py2048 说明

## 特别说明

此Python包仅支持Python3.10及以上的版本，因为它在源代码中使用了match语句（参见PEP 634，PEP 635，PEP 636）

## 项目名称

- Python 2048

## 项目信息

- 此项目旨在将2048游戏移植到Python上
- 联系邮箱&问题反馈：kill114514251@outlook.com
- testPyPI：同名
- 哔哩哔哩：GQX编程

## 版本
- 1.0.0b1 (Pre Release)

## 开发环境
- Ubuntu Linux 22.04
- Python 3.12.8
- Pygame 2.6.1

## 使用语言
- Python
- json

## 改动说明
- 无（此版本为第一个版本）

## 未来计划

### v1.1
- 提供更加流畅的窗口缩放功能

### v1.2
- 增加远程控制功能

## 修复中BUG
- 按住方向键后持续移动

## 项目说明

### 项目结构
```
/
    assets/
        |_素材（BGM/图片等）若干
    info/
        |_游戏说明文档
        README.md
        LICENSE
    data/
        |_游戏数据
        scoreList.json
    __init__.py
    data.py
        |_各种常量
    error.py
        |_自定义错误类型
        class CommandError
        class ShellError
        class TaskScheduleError
    game.py（和 game.pyi）
        |_游戏主文件
        class Py2048
            |_
            def __init__(
                self,
                operateAPI : Queue = ...,
                getPuzzleAPI : Queue = ...,
                endless : bool = ...,
                debug : bool = ...
            ) -> None: ...
            
            def __main(
                self,
                size : int = ...,
                operateAPI : Queue = ...,
                getPuzzleAPI : Queue = ...,
                endless : bool = ...,
                debug : bool = ...
            ) -> None: ...
            def __drawRestartButton(self) -> None: ...
            def __drawScoreList(self) -> None: ...
            def __drawTitleWhenFailed(self) -> None: ...
            def __randAddBlock(self) -> None: ...
            def __drawBackGround(self) -> None: ...
            def __blitBlocks(self) -> None: ...
            def __moveBlocks(self) -> None: ...
            def __updateStatus(self) -> None: ...
            def __drawBottomBar(self) -> None: ...
            def __updateWindowInfo(self) -> None: ...
            def __updatePictures(self) -> None: ...
            def __reInitialize(self) -> None: ...
            def __startGame(self) -> None: ...
            def __quit(self) -> None: ...
            def __print(self, text : str) -> None: ...
            def __call__(self) -> None: ...
            def __getattr__(self, name : str) -> None: ...
            def __str__(self) -> str: ...
            def __hash__(self) -> int: ...
    info.py（和 info.pyi）
        |_包信息
    def readme() -> None: ...
    def license() -> None: ...

```

### 安装方法
>>> python3 -m pip installl py2048  

### 项目介绍
此版本无法显示4096，意味着您无法合成4096，我保证这个错误将在此版本发布后的2周内被1.1.0pre1版本修复
用户可以通过初始化 py2048.game.Py2048 类开始游戏  
也可以调用 py2048.info.readme 函数获取本文档  
或者调用 py2048.info.license 函数获取本Python包使用的MIT协议的详细内容  

#### Py2048类 详细介绍
本类是 multiprocessing.Process 类的子类，所以游戏并不会阻塞您的程序
本类支持程序控制游戏（这个功能或许可以用来训练玩2048的人工智能）
支持存储分数前八名的名字及分数（在游戏开始时的菜单输入的名字），这个功能称为scoreList

##### __init__参数：
- name : str = ""  
设定名字（默认为""），用于存储在scoreList中。  
注意：如果未设定API，则游戏会显示菜单，name的设定以用户在菜单的输入为准。这意味着如果您未设定API参数，我们建议您同样不要设置name参数。  

- operateAPI : multiprocessing.Queue = None  
操作API（默认为None），您可以通过设置这个参数来操作游戏  
当您设定了这个参数时，您就可以向这个Queue输入操作（字符串）  
有效的操作："exit", "up", "left", "right", "down"  
顾名思义，exit用来退出游戏，其余操作用来操控游戏下一步的方向  
如果您输入的操作不属于这五个中的任意一个，程序会触发自定义错误：CommandError  
当您设定了这个参数时，游戏不会显示菜单，否则反之  
注意 ：当您设定了这个参数时，您必须同时设置getPuzzleAPI参数，否则会触发TypeError  

- getPuzzleAPI : Queue = None  
回溯API（默认为None），当您向operateAPI输入一个操作后，getPuzzleAPI会输出一个4元组，内容为：（状态（str类|playing, failed, display等，若此项不为playing那么游戏已经失败，请通过terminate或kill方法杀死此进程，或者点击屏幕上的RETRY按钮进入菜单）, 已经走过的步数（int类）, 总得分（int类）, 目前的局面（二维list类|4x4阵列））  

- endless : bool = False  
合成出2048块后是否结束（默认为False），如果为True，那么不结束，否则反之  
注意：如果未设定API，则游戏会显示菜单，endless的设定以用户在菜单的选择为准。这意味着如果您未设定API参数，我们建议您同样不要设置endless参数。  

- debug : bool = False  
是否打印debug信息（默认为False）。  

##### 运行方式
假设您初始化此类为py2048inst:  
>>> from py2048.game import Py2048  
>>> py2048inst = Py2048()  
注意，此时仅仅创建了游戏进程，还未创建游戏窗口（通俗点说就是游戏还未开始）  
要开始游戏，执行：  
>>> py2048inst.start()  
或者调用魔术方法__call__：  
>>> py2048inst()  

##### 终止方式
要终止游戏，可以调用  
>>> py2048inst.terminate()  
或  
>>> py2048inst.kill()  
然后执行  
>>> py2048inst.close()  

## 感谢阅读和下载！
- 您的支持是我更新的最大动力！  

# English Version

# Py2048 Description
## Special note
This Python package only supports versions 3.10 and above of Python because it uses match statements in the source code (see PEP 634, PEP 635, PEP 636)
## Project Name
- Python 2048
## Project Information
- This project aims to port 2048 games to Python
- Contact email&problem feedback: kill114514251@outlook.com
- TestPyPI: Same name
- Bilibili: GQX Programming
## Version
- 1.0.0b1 (Pre Release)
## Development environment
- Ubuntu Linux 22.04
- Python 3.12.8
- Pygame 2.6.1
## Using language
- Python
- json
## Change description
- None (this is the first version)
## Future plans
### v1.1
- Provide smoother window zooming function
### v1.2
- Add remote control function
## Fix bugs in progress
- Keep moving while holding down the directional keys
## Project Description
### Project Structure
```
/
    assets/
        |_Several materials (BGM/images, etc.)
    info/
        |_Game documentation
        README.md
        LICENSE
    data/
        |_Game data
        scoreList.json
    __init__.py
    data.py
        |_Various constants
    error.py
        |_Customize error types
        class CommandError
        class ShellError
        class TaskScheduleError
    Game.by (and game. pyi)
        |_Game main file
        class Py2048
            |_
            def __init__(
            self,
            operateAPI : Queue = ...,
            getPuzzleAPI : Queue = ...,
            endless : bool = ...,
            debug : bool = ...
            ) -> None: ...
                        
            def __main(
            self,
            size : int = ...,
            operateAPI : Queue = ...,
            getPuzzleAPI : Queue = ...,
            endless : bool = ...,
            debug : bool = ...
            ) -> None: ...
            def __drawRestartButton(self) -> None: ...
            def __drawScoreList(self) -> None: ...
            def __drawTitleWhenFailed(self) -> None: ...
            def __randAddBlock(self) -> None: ...
            def __drawBackGround(self) -> None: ...
            def __blitBlocks(self) -> None: ...
            def __moveBlocks(self) -> None: ...
            def __updateStatus(self) -> None: ...
            def __drawBottomBar(self) -> None: ...
            def __updateWindowInfo(self) -> None: ...
            def __updatePictures(self) -> None: ...
            def __reInitialize(self) -> None: ...
            def __startGame(self) -> None: ...
            def __quit(self) -> None: ...
            def __print(self, text : str) -> None: ...
            def __call__(self) -> None: ...
            def __getattr__(self, name : str) -> None: ...
            def __str__(self) -> str: ...
            def __hash__(self) -> int: ...
            Info. py (and info. pyi)
            |_Package information
            def readme() -> None: ...
            def license() -> None: ...
```
### Installation method
>>> python3 -m pip installl py2048  
### Project Introduction
This version cannot display 4096, which means you cannot synthesize 4096. I guarantee that this error will be fixed by version 1.1.0pre1 within 2 weeks after the release of this version  
Users can initialize py2048. game Py2048 class starts the game  
You can also call the py2048. info. readme function to obtain this document  
Alternatively, you can call the py2048. info. license function to obtain detailed information about the MIT protocol used in this Python package  
#### Py2048 class detailed introduction
This category is multiprocessing Subclass of the Process class, so the game will not block your program  
This class supports program controlled games (this feature may be used to train artificial intelligence to play 2048)  
Support storing the names and scores of the top eight scores (entered in the menu at the beginning of the game), this feature is called scoreList  
#####  __init__ parameter:
- name :  str = ""  
Set the name (default is' ') for storage in the scoreList.  
Note: If the API is not set, the game will display a menu, and the name setting is based on the user's input in the menu. This means that if you have not set API parameters, we recommend that you also do not set the name parameter.  
- operateAPI :  multiprocessing.Queue = None    
Operation API (default is None), you can operate the game by setting this parameter  
When you set this parameter, you can input operations (strings) into this queue  
Effective operation: "exit", "up", "left", "right", "down"  
As the name suggests, exit is used to exit the game, while other operations are used to control the direction of the next step in the game  
If the operation you input does not belong to any of these five, the program will trigger a custom error: CommandError  
When you set this parameter, the game will not display the menu, otherwise the opposite is true
Note: When you set this parameter, you must also set the getPuzzleAPI parameter, otherwise it will trigger a TypeError  
- getPuzzleAPI :  Queue = None  
The backtracking API (default is None), when you input an operation to the opereAPI, the getPuzzleAPI will output a 4-tuple with the content: (state (str class|playing, Failed, display, etc. If this item is not playing, the game has already failed. Please use the terminate or kill method to kill this process, or click the RETRY button on the screen to enter the menu.) The number of steps taken (int class), total score (int class), and current situation (list class| 4x4 array))  
- endless :  bool = False  
Does it end after synthesizing 2048 blocks (default is False)? If True, it does not end; otherwise, it does not end  
Note: If the API is not set, the game will display a menu, and the endless setting is based on the user's selection in the menu. This means that if you have not set API parameters, we recommend that you also do not set the endless parameter.  
- debug :  bool = False  
Whether to print debug information (default is False).  
##### How To Run
Assuming you initialize this class as py2048inst:  
>>> from py2048.game import Py2048  
>>> py2048inst = Py2048()  
Note that only the game process has been created at this point, and the game window has not yet been created (in layman's terms, the game has not yet started)  
To start the game, execute:  
>>> py2048inst.start()  
Or call the magic method __call__:  
>>> py2048inst()  
##### Termination
To terminate the game, you can call  
>>> py2048inst.terminate()  
Or  
>>> py2048inst.kill()  
Then execute  
>>> py2048inst.close()  
## Thank you for reading and downloading!
- Your support is my biggest motivation for updating!  
