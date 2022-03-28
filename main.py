import os, sys, pygame, time, random, json
from unicodedata import name

version = "a0.1.0"
minFrameLength = 1 / 60 # reciprocral of maximum framerate
delayedAutoShift = .3
autoRepeat = .06

defaultLang = {
    "title"        : "pygame-tetrominoes",
    "version"      : "version",
    "blockOut"     : "Block Out",
    "lockOut"      : "Lock Out",
    "classic"      : "classic",
    "endurance"    : "endurance",
    "extreme"      : "extreme",
    "40line"       : "40 lines",
    "3min"         : "3 minutes",
    "back"         : "back",
    "startGame"    : "start game",
    "startingLevel": "starting level",
    "endless"      : "endless",
    "off"          : "off",
    "on"           : "on",
    "pressAnyKey"  : "press any key",
    "next"         : "NEXT",
    "hold"         : "HOLD",
    "score"        : "score",
    "lines"        : "lines",
    "time"         : "time",
    "level"        : "level",
    "remaining"    : "left",
    "exclLCD1"     : "excluding line",
    "exclLCD2"     : "clear delay",
    "gameOver"     : "Game Over",
    "fps"          : "frames per second",
    "tSpin"        : "{ t-spin }",
    "miniTSpin"    : "{ mini t-spin }",
    "backToBack"   : "{ back-to-back }",
    "allClear"     : "{ all clear }",
    "combo"        : "combo",
    "excellent"    : "Excellent!",
    "paused"       : "paused",
    "continue"     : "continue",
    "retry"        : "retry",
    "exit"         : "exit",
    "settings"     : "settings",
    "handling"     : "handling",
    "DAS"          : "DAS delay",
    "ARR"          : "DAS speed (ARR)",
    "langSelect"   : "language select",
    "pwinfo"       : "protestware info",
    "pwinfotxt"    : [
        "The Russian language option has been",
        "removed because:",
        "- some of the translations came from Google",
        "  Translate (such as the ones for this",
        "  message), which can sometimes be",
        "  unreliable",
        "- of Russia's invasion of Ukraine"
    ],
    "pwfputin"     : "F**k You, Putin!",
    "pwexit"       : "Press Enter To Exit"
}
langDirectory = os.path.join(os.path.dirname(__file__), "lang")
def refreshLangList():
    global langList
    langList = [f for f in os.listdir(langDirectory) if os.path.isfile(os.path.join(langDirectory, f))]
    langList = ["english"] + [i[: -5] for i in langList if i[-5 :] == ".json"]
    return langList
    ## legacy language input code
    #print("\n1 english")
    #for i in range(len(langList)): print(i + 2, langList[i][: -5])
    #langNum = int(input("\n🌐 --> ")) - 2

def getLangTxt(key):
    global lang
    try:
        return lang[key]
    except KeyError:
        return key

def updateLang(aLangNum):
    global langList, lang, langNum
    langNum = aLangNum
    try:
        if langList[langNum] == "english":
            lang = defaultLang
        else:
            langFile = open(os.path.join(langDirectory, langList[langNum] + ".json"))
            lang = json.load(langFile)
            langFile.close()
    except Exception as e:
        print("\n", e, "\n")
        lang = defaultLang
    pygame.display.set_caption(getLangTxt("title"))
    return lang
refreshLangList()
updateLang(0)

# Initialize pygame and start and rename the window
pygame.init()
size = width, height = 320, 240
flags = pygame.RESIZABLE
window = pygame.display.set_mode(size, flags)
screen = pygame.Surface(size)
pygame.display.set_caption(getLangTxt("title"))

# Tetromino color data
tetrominoColors = [
    pygame.Color(255,   0,   0), # Z is red
    pygame.Color(255, 128,   0), # L is orange
    pygame.Color(255, 255,   0), # O is yellow
    pygame.Color(  0, 255,   0), # S is green
    pygame.Color(  0, 255, 255), # I is cyan (light blue)
    pygame.Color(  0,   0, 255), # J is blue
    pygame.Color(255,   0, 255), # T is purple
    pygame.Color(128, 128, 128)  # Gray for already-held tetrominoes
]
# Tetromino shape data
tetrominoes = [
    [ # Z
        [(0, 2), (1, 2), (1, 1), (2, 1)],
        [(2, 2), (2, 1), (1, 1), (1, 0)],
        [(2, 0), (1, 0), (1, 1), (0, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],
    [ # L
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 2), (1, 1), (1, 0), (2, 0)],
        [(2, 1), (1, 1), (0, 1), (0, 0)],
        [(1, 0), (1, 1), (1, 2), (0, 2)]
    ],
    [ # O
        [(1, 2), (2, 2), (2, 1), (1, 1)],
        [(2, 2), (2, 1), (1, 1), (1, 2)],
        [(2, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 1), (1, 2), (2, 2), (2, 1)],
    ],
    [ # S
        [(2, 2), (1, 2), (1, 1), (0, 1)],
        [(1, 2), (1, 1), (2, 1), (2, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 2), (0, 1), (1, 1), (1, 0)]
    ],
    [ # I
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(2, 3), (2, 2), (2, 1), (2, 0)],
        [(3, 1), (2, 1), (1, 1), (0, 1)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ],
    [ # J
        [(2, 1), (1, 1), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 0)],
        [(1, 2), (1, 1), (1, 0), (0, 0)]
    ],
    [ # T
        [(2, 1), (1, 1), (0, 1), (1, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (1, 0)],
        [(1, 2), (1, 1), (1, 0), (0, 1)]
    ]
]
# SRS (Super Rotation System) wall kick data
srsWallKickData = [
    [ # Clockwise rotations
        [ # Z, J, L, S, and T
            [( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)],
            [( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)],
            [( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)],
            [( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)]
        ],
        [ # O
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)]
        ],
        [ # I
            [( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)],
            [( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)],
            [( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1)],
            [( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)]
        ]
    ],
    [ # Counterclockwise rotations
        [ # Z, J, L, S, and T
            [( 0, 0), ( 1, 0), ( 1,-1), ( 0, 2), ( 1, 2)],
            [( 0, 0), (-1, 0), (-1, 1), ( 0,-2), (-1,-2)],
            [( 0, 0), (-1, 0), (-1,-1), ( 0, 2), (-1, 2)],
            [( 0, 0), ( 1, 0), ( 1, 1), ( 0,-2), ( 1,-2)]
        ],
        [ # O
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)],
            [( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0), ( 0, 0)]
        ],
        [ # I
            [( 0, 0), ( 2, 0), (-1, 0), ( 2, 1), (-1,-2)],
            [( 0, 0), ( 1, 0), (-2, 0), ( 1,-2), (-2, 1)],
            [( 0, 0), (-2, 0), ( 1, 0), (-2,-1), ( 1, 2)],
            [( 0, 0), (-1, 0), ( 2, 0), (-1, 2), ( 2,-1)]
        ]
    ]
]
# Gravity function takes in level as input and outputs tetromino fall speed in seconds per row
gravity = lambda level: (0.8 - ((level - 1) * 0.007)) ** (level - 1)

# Simple function for rendering text onto the screen
def render_text(text, pos = (0, 0), color = pygame.Color(255, 255, 255), size = 12, fontPath = pygame.font.get_default_font(), background = None, antialias = True):
    textSurface = pygame.font.Font(fontPath, size).render(text, antialias, color, background)
    screen.blit(textSurface, textSurface.get_rect().move(pos[0], pos[1]))

# Simple function for rendering a single mino to the screen
def render_mino(color, pos, borderWidth = 0):
    pygame.draw.rect(screen, tetrominoColors[color], pygame.Rect(110 + 10 * pos[0] + borderWidth, 210 - 10 * pos[1] + borderWidth, 10 - borderWidth * 2, 10 - borderWidth * 2), borderWidth)

defaultKeys = {
    "rotateLeft" : [pygame.constants.K_LCTRL,  pygame.constants.K_RCTRL,  pygame.constants.K_z,   pygame.constants.K_KP3, pygame.constants.K_KP7],
    "rotateRight": [pygame.constants.K_UP,     pygame.constants.K_x,      pygame.constants.K_KP1, pygame.constants.K_KP5, pygame.constants.K_KP9],
    "hold"       : [pygame.constants.K_LSHIFT, pygame.constants.K_RSHIFT, pygame.constants.K_c,   pygame.constants.K_KP0],
    "hardDrop"   : [pygame.constants.K_SPACE,  pygame.constants.K_KP8],
    "shiftLeft"  : [pygame.constants.K_LEFT,   pygame.constants.K_KP4],
    "softDrop"   : [pygame.constants.K_DOWN,   pygame.constants.K_KP2],
    "shiftRight" : [pygame.constants.K_RIGHT,  pygame.constants.K_KP6],
    "menuSelect" : [pygame.constants.K_RETURN],
    "menuDown"   : [pygame.constants.K_DOWN,   pygame.constants.K_s],
    "menuUp"     : [pygame.constants.K_UP,     pygame.constants.K_w],
    "menuRight"  : [pygame.constants.K_RIGHT,  pygame.constants.K_d],
    "menuLeft"   : [pygame.constants.K_LEFT,   pygame.constants.K_a],
    "pause"      : [pygame.constants.K_ESCAPE]
}

def checkKeys(keys, keyData = None):
    global pressedKeys
    if keyData == None:
        keyData = pressedKeys
    for i in keys:
        if keyData[i]: # 0 <= i < len(pressedKeys) and
            return True
    return False

# Function that initializes a brand new game
def initializeNewGame():

    global stack, tetrominoPosition, currentTetromino, nextTetrominoes, holdQueue, tetrominoAlreadyHeld, tetrominoBag, tetrominoRotation, fallTimer, lockDelay, lockTimer, inputsUntilLock, lowestTetrominoYPosition, score, lineClears, level, currentGravity, lineClearTimer, linesToClear, backToBack, combo, tSpin, allClear, isDASCharged, autoRepeatTimer, leftRotatePressedLastFrame, rightRotatePressedLastFrame, holdPressedLastFrame, hardDropPressedLastFrame, tetrominoRotatedDirectlyBeforeLock

    # Variables related to the current state of the board

    stack = []
    for i in range(40):
        stack += [[-1] * 10]
    tetrominoPosition = (3, 19)
    currentTetromino = -1
    nextTetrominoes = [-1]*5
    tetrominoBag = []
    # while nextTetrominoes[0] == -1:
    #     nextTetrominoes += [randomGenerator()]
    #     del nextTetrominoes[0]
    holdQueue = -1
    tetrominoAlreadyHeld = False
    tetrominoBag = []
    tetrominoRotation = 0
    fallTimer = 0
    lockDelay = .5
    lockTimer = lockDelay
    inputsUntilLock = 15
    lowestTetrominoYPosition = 19
    score = 0
    lineClears = 0
    level = 1
    currentGravity = 1.0
    lineClearTimer = 0
    linesToClear = []
    backToBack = 0
    combo = -1
    tSpin = 0
    allClear = False

    if nextTetrominoes[0] == -1:
        while nextTetrominoes[0] == -1:
            nextTetrominoes += [randomGenerator()]
            del nextTetrominoes[0]

    # Variables related to tetromino manipulation

    isDASCharged = False
    autoRepeatTimer = 1
    tetrominoRotatedDirectlyBeforeLock = 0

# Function that manages the "7-bag" Random Generator that is standard with modern versions of this classic game
def randomGenerator():
    global tetrominoBag
    if tetrominoBag == []:
        tetrominoBag = [0, 1, 2, 3, 4, 5, 6]
    i = random.randint(0, len(tetrominoBag) - 1)
    generatedTetromino = tetrominoBag[i]
    del tetrominoBag[i]
    return generatedTetromino

# Function that initializes new tetrominoes
def initializeNewTetromino(tetromino):
    global currentTetromino, tetrominoPosition, tetrominoRotation, fallTimer, lockTimer, inputsUntilLock, lowestTetrominoYPosition, tetrominoRotatedDirectlyBeforeLock
    currentTetromino = tetromino
    if currentTetromino == 4:
        tetrominoPosition = (3, 18)
    else:
        tetrominoPosition = (3, 19)
    tetrominoRotation = 0
    fallTimer = 0
    lockTimer = lockDelay
    inputsUntilLock = 15
    lowestTetrominoYPosition = 19
    tetrominoRotatedDirectlyBeforeLock = 0

# Function that shifts a tetromino left if direction is -1 or right if it is 1
def shiftTetromino(direction):
    global tetrominoPosition, tetrominoRotation, lockTimer, inputsUntilLock, tetrominoRotatedDirectlyBeforeLock
    canShift = True
    for i in tetrominoes[currentTetromino][tetrominoRotation]:
        if tetrominoPosition[0] + i[0] + direction < 0 or tetrominoPosition[0] + i[0] + direction >= 10 or stack[tetrominoPosition[1] + i[1]][tetrominoPosition[0] + i[0] + direction] != -1:
            canShift = False
    if canShift:
        tetrominoPosition = (tetrominoPosition[0] + direction, tetrominoPosition[1])
        lockTimer = lockDelay
        inputsUntilLock -= 1
        tetrominoRotatedDirectlyBeforeLock = 0
    return canShift

# Function that rotates a tetromino counterclockwise if direction is -1 or clockwise if it is 1
def rotateTetromino(direction):
    global tetrominoRotation, tetrominoPosition, lockTimer, inputsUntilLock, tetrominoRotatedDirectlyBeforeLock
    tetrominoRotation = (tetrominoRotation + direction) % 4
    iindex = 0
    for i in srsWallKickData[(direction - 1) // -2][[0, 0, 1, 0, 2, 0, 0][currentTetromino]][tetrominoRotation]:
        iindex += 1
        tetrominoPosition = (tetrominoPosition[0] + i[0], tetrominoPosition[1] + i[1])
        kickRejected = False
        for j in tetrominoes[currentTetromino][tetrominoRotation]:
            if tetrominoPosition[0] + j[0] < 0 or tetrominoPosition[0] + j[0] >= 10 or tetrominoPosition[1] + j[1] < 0 or stack[tetrominoPosition[1] + j[1]][tetrominoPosition[0] + j[0]] != -1:
                kickRejected = True
                break
        if kickRejected:
            tetrominoPosition = (tetrominoPosition[0] - i[0], tetrominoPosition[1] - i[1])
            if iindex == 5:
                tetrominoRotation = (tetrominoRotation - direction) % 4
        else:
            lockTimer = lockDelay
            inputsUntilLock -= 1
            if iindex == 5 and currentTetromino == 6:
                tetrominoRotatedDirectlyBeforeLock = 2
            else:
                tetrominoRotatedDirectlyBeforeLock = 1
            break

# A small function that is essential to scoring
def linesSentFromCombo(combo):
    if combo < 11:
        return min(combo // 2, 4)
    else:
        return 5

# The master function of the game which updates the current state of the game
def gameTick(gravity = gravity):
    global allClear, autoRepeatTimer, backToBack, combo, currentGravity, fallMinoes, fallTimer, holdQueue, inputsUntilLock, isDASCharged, lastFrameTotalTime, level, lineClearTimer, lineClears, linesToClear, lockDelay, lockTimer, lowestTetrominoYPosition, nextTetrominoes, pointsScoredByLineClear, score, stack, tetrominoAlreadyHeld, tetrominoPosition, tetrominoRotatedDirectlyBeforeLock, tSpin
    
    currentGravity = gravity(level)

    # Manage line clears during line clear delay
    if lineClearTimer > 0:
        lineClearTimer -= lastFrameTotalTime
        if lineClearTimer <= 0:
            for i in reversed(linesToClear):
                del stack[i]
                stack += [[-1] * 10]
            nextTetrominoes += [randomGenerator()]
            initializeNewTetromino(nextTetrominoes[0])
            del nextTetrominoes[0]
            tetrominoAlreadyHeld = False

    # Manage hard drop
    if checkKeys(defaultKeys["hardDrop"]) and not checkKeys(defaultKeys["hardDrop"], keysPressedLastFrame) and lineClearTimer <= 0:
        ghostHeight = tetrominoPosition[1]
        ghostTouchingGround = False
        while not ghostTouchingGround:
            for i in tetrominoes[currentTetromino][tetrominoRotation]:
                if stack[ghostHeight + i[1]][tetrominoPosition[0] + i[0]] != -1 or ghostHeight + i[1] < 0:
                    ghostTouchingGround = True
                    break
            if not ghostTouchingGround:
                for i in tetrominoes[currentTetromino][tetrominoRotation]:
                    fallMinoes += [(currentTetromino, (tetrominoPosition[0] + i[0], ghostHeight + i[1]))]
                ghostHeight -= 1
        if ghostHeight < tetrominoPosition[1]:
            ghostHeight += 1
            if ghostHeight < tetrominoPosition[1]:
                tetrominoRotatedDirectlyBeforeLock = 0
        score += 2 * (tetrominoPosition[1] - ghostHeight)
        tetrominoPosition = (tetrominoPosition[0], ghostHeight)
        fallTimer = 0
        lockTimer = 0

    # Manage hold
    if checkKeys(defaultKeys["hold"]) and not (checkKeys(defaultKeys["hold"], keysPressedLastFrame) or tetrominoAlreadyHeld) and lineClearTimer <= 0:
        holdCopy = holdQueue
        holdQueue = currentTetromino
        initializeNewTetromino(holdCopy)
        tetrominoAlreadyHeld = True

    if lineClearTimer <= 0:
        # Generate new tetrominoes
        if currentTetromino == -1:
            while currentTetromino == -1:
                nextTetrominoes += [randomGenerator()]
                initializeNewTetromino(nextTetrominoes[0])
                del nextTetrominoes[0]
        else:
            
            # Handle soft drop, lock delay, locking, game over, line clearing before line clear delay, and level up

            # Check if the current tetromino is on a Surface
            
            onFloor = False
            for i in tetrominoes[currentTetromino][tetrominoRotation]:
                if stack[tetrominoPosition[1] + i[1] - 1][tetrominoPosition[0] + i[0]] != -1 or tetrominoPosition[1] + i[1] - 1 < 0:
                    onFloor = True
            
            if not onFloor:
                lockTimer = lockDelay
            if checkKeys(defaultKeys["softDrop"]):
                fallTimer -= lastFrameTotalTime * 20
            else:
                fallTimer -= lastFrameTotalTime
            while fallTimer <= 0 and lineClearTimer <= 0:
                if onFloor:
                    if checkKeys(defaultKeys["softDrop"]):
                        fallTimer += lastFrameTotalTime * 20
                    else:
                        fallTimer += lastFrameTotalTime
                    lockTimer -= lastFrameTotalTime
                    if inputsUntilLock <= 0:
                        lockTimer = 0
                    if lockTimer <= 0:
                        
                        # Lock tetromino to Matrix and check for game over conditions

                        for i in tetrominoes[currentTetromino][tetrominoRotation]:
                            if stack[tetrominoPosition[1] + i[1]][tetrominoPosition[0] + i[0]] != -1:
                                return "blockOut"
                        notLockedOut = False
                        for i in tetrominoes[currentTetromino][tetrominoRotation]:
                            stack[tetrominoPosition[1] + i[1]][tetrominoPosition[0] + i[0]] = currentTetromino
                            if tetrominoPosition[1] + i[1] < 20:
                                notLockedOut = True
                        if not notLockedOut:
                            return "lockOut"

                        # Recognize T-spins
                        tetrominoCorners = 0
                        tetrominoFrontCorners = 0
                        if tetrominoRotatedDirectlyBeforeLock > 0 and currentTetromino == 6:
                            for i in range(4):
                                if tetrominoPosition[0] + [0, 2, 2, 0][(tetrominoRotation + i) % 4] < 0 or tetrominoPosition[0] + [0, 2, 2, 0][(tetrominoRotation + i) % 4] >= 10 or tetrominoPosition[1] + [2, 2, 0, 0][(tetrominoRotation + i) % 4] < 0 or stack[tetrominoPosition[1] + [2, 2, 0, 0][(tetrominoRotation + i) % 4]][tetrominoPosition[0] + [0, 2, 2, 0][(tetrominoRotation + i) % 4]] != -1:
                                    tetrominoCorners += 1
                                    if i < 2:
                                        tetrominoFrontCorners += 1
                        if tetrominoCorners >= 3:
                            if tetrominoFrontCorners >= 2 or tetrominoRotatedDirectlyBeforeLock >= 2:
                                tSpin = 2
                            else:
                                tSpin = 1
                        else:
                            tSpin = 0
                        
                        # Check which lines need to be cleared, if there are any, and whether or not an All Clear has been performed

                        linesToClear = []
                        allClear = True
                        for i in range(len(stack)):
                            linesToClear += [i]
                            for j in stack[i]:
                                if j == -1:
                                    del linesToClear[-1]
                                    break
                            if (len(linesToClear) <= 0 or linesToClear[-1] != i) and allClear == True:
                                for j in stack[i]:
                                    if j != -1:
                                        allClear = False
                                        break
                        
                        # Manage part of back-to-back and combo

                        if 0 < len(linesToClear) < 4 and tSpin < 1:
                            backToBack = 0
                        if backToBack > 0 and len(linesToClear) > 0:
                            b2bMultiplier = 1.5
                        else:
                            b2bMultiplier = 1
                        if len(linesToClear) > 0:
                            combo += 1
                        else:
                            combo = -1
                        
                        # Increase the score by the necessary amount
                        
                        pointsScoredByLineClear = 0
                        for i in range(len(linesToClear) + tSpin // 2):
                            if allClear:
                                pointsScoredByLineClear += i * 2 - 4
                                if i < 1:
                                    pointsScoredByLineClear += 16
                                elif i < 3:
                                    pointsScoredByLineClear += 6
                            else:
                                pointsScoredByLineClear += linesSentFromCombo(i + 1) + 1
                        if tSpin >= 2:
                            pointsScoredByLineClear += min(2 * len(linesToClear) + 3, 8)
                        elif tSpin >= 1:
                            pointsScoredByLineClear += 1
                        pointsScoredByLineClear = ((int(pointsScoredByLineClear * b2bMultiplier) + max(combo, 0) - int(allClear) * 4) * 100 * level)
                        score += pointsScoredByLineClear

                        lineClears += len(linesToClear)

                        if len(linesToClear) > 0:
                            # Begin line clear delay

                            for i in reversed(linesToClear):
                                stack[i] = [-1] * 10
                            lineClearTimer = .5

                            # Manage rest of back-to-back
                            if len(linesToClear) >= 4 or tSpin >= 1:
                                backToBack += 1
                        else:
                            # Initialize the next tetromino

                            nextTetrominoes += [randomGenerator()]
                            initializeNewTetromino(nextTetrominoes[0])
                            del nextTetrominoes[0]
                            tetrominoAlreadyHeld = False
                else:

                    # Manage tetromino falling

                    fallTimer += currentGravity
                    if checkKeys(defaultKeys["softDrop"]):
                        score += 1
                    tetrominoPosition = (tetrominoPosition[0], tetrominoPosition[1] - 1)
                    for i in tetrominoes[currentTetromino][tetrominoRotation]:
                        fallMinoes += [(currentTetromino, (tetrominoPosition[0] + i[0], tetrominoPosition[1] + i[1]))]
                    
                    # Check if the current tetromino is now on a Surface after falling

                    onFloor = False
                    for i in tetrominoes[currentTetromino][tetrominoRotation]:
                        if stack[tetrominoPosition[1] + i[1] - 1][tetrominoPosition[0] + i[0]] != -1 or tetrominoPosition[1] + i[1] - 1 < 0:
                            onFloor = True
                    
                    # Reset inputsUntilLock if necessary

                    if tetrominoPosition[1] < lowestTetrominoYPosition:
                        inputsUntilLock = 15
                        lowestTetrominoYPosition = tetrominoPosition[1]
        
        # Level up if necessary

        level = max(level, lineClears // 10 + 1)

    # Manage shifting of tetrominoes

    if checkKeys(defaultKeys["shiftLeft"]) or checkKeys(defaultKeys["shiftRight"]):
        autoRepeatTimer -= lastFrameTotalTime
        tryShift = True
        while autoRepeatTimer <= 0 and tryShift:
            if isDASCharged:
                autoRepeatTimer += autoRepeat
            else:
                autoRepeatTimer += delayedAutoShift
                isDASCharged = True
            if lineClearTimer > 0 or (checkKeys(defaultKeys["shiftLeft"]) and checkKeys(defaultKeys["shiftRight"])):
                tryShift = False
            else:
                if checkKeys(defaultKeys["shiftLeft"]):
                    tryShift = shiftTetromino(-1)
                else:
                    tryShift = shiftTetromino(1)
    else:
        isDASCharged = False
        autoRepeatTimer = 0.0

    # Manage rotation of tetrominoes
    if lineClearTimer <= 0:
        if checkKeys(defaultKeys["rotateRight"]) and not checkKeys(defaultKeys["rotateRight"], keysPressedLastFrame):
            rotateTetromino(1)

        if checkKeys(defaultKeys["rotateLeft"]) and not checkKeys(defaultKeys["rotateLeft"], keysPressedLastFrame):
            rotateTetromino(-1)

    return None

# Formats number of seconds into time formatted as mm:ss.cc. For whatever reason this wasn't working as lambda function. also long-line-itis pog
def formatTime(secs):
    return str(int(secs / 600)) + str(int(secs / 60) % 10) + ":" + str(int(secs / 10) % 6) + str(int(secs) % 10) + "." + str(int(secs / .1) % 10) + str(int(secs / .01) % 10)

state = 1
gameType = 0
selectedOption = 0

startingLevel = 1
endlessGame = False
menuOptions = None
def updateMenuText():
    global menuOptions, state
    menuOptions = {
        1: langList,
        2: [getLangTxt("classic"), getLangTxt("endurance"), getLangTxt("extreme"), getLangTxt("40line"), getLangTxt("3min"), getLangTxt("settings"), getLangTxt("pwinfo")],
        5: [getLangTxt("continue"), getLangTxt("retry"), getLangTxt("exit")],
        6: [getLangTxt("back"), getLangTxt("handling"), getLangTxt("langSelect")],
        7: [getLangTxt("back"), getLangTxt("DAS") + ": " + str(int(delayedAutoShift * 1000 + .0000000001)) + "ms", getLangTxt("ARR") + ": " + str(int(autoRepeat * 1000 + .0000000001)) + "ms"],
        8: langList
    }[state]
def updateModeMenuText():
    global menuOptions, gameType
    menuOptions = [
        [getLangTxt("back"), getLangTxt("startingLevel") + ": " + str(startingLevel), getLangTxt("endless") + ": " + {False: getLangTxt("off"), True: getLangTxt("on")}[endlessGame], getLangTxt("startGame")],
        [getLangTxt("back"), getLangTxt("startGame")],
        [getLangTxt("back"), getLangTxt("startingLevel") + ": M" + str(startingLevel), getLangTxt("startGame")],
        [getLangTxt("back"), getLangTxt("startGame")],
        [getLangTxt("back"), getLangTxt("startGame")]
    ][gameType]

frameParity = 0
def flashColor(color = None):
    if color == None:
        try:
            color = [pygame.Color(255, 255, 255), pygame.Color(255, 255, 0)][int(currentGravity <= 1 / 1200)]
        except NameError:
            color = pygame.Color(255, 255, 255)
    return [pygame.Color(255, 255, 255), color][frameParity >= 2]

lastFrameTotalTime = (lastFrameTime := time.perf_counter())

# Game loop
while True:
    t = time.perf_counter()

    frameParity = (frameParity + 1) % 4
    fallMinoes = []

    # Get the state of the keyboard
    try:
        keysPressedLastFrame = pressedKeys
    except NameError:
        keysPressedLastFrame = [0] * 25
    finally:
        pressedKeys = pygame.key.get_pressed()

    # Handle events (Window resized or closed)
    windowResized = False
    windowMaximized = False
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.constants.WINDOWRESIZED:
            windowResized = True
        elif event.type == pygame.constants.WINDOWMAXIMIZED:
            windowMaximized = True
            
    # Create the black background
    screen.fill(pygame.Color(0, 0, 0))

    unpausedThisFrame = False
    if state in [0, 2]:
        render_text(getLangTxt("title"), (10, 50 - 20 * {0: 0, 2: 1}[state]), size = 24)
    if state in [0, 1, 2]:
        render_text(getLangTxt("version") + " " + version, (20, 220), size = 14)
    if state in [1, 2, 3, 5, 6, 7, 8]: # Menu states
        if state == 3:
            updateModeMenuText()
        else:
            updateMenuText()
        minMenuDispIndex = max(0, min(selectedOption - 3, len(menuOptions) - 7))
        maxMenuDispIndex = min(max(7, selectedOption + 4), len(menuOptions))
        for i in range(minMenuDispIndex, maxMenuDispIndex):
            render_text({False: "  ", True: "> "}[selectedOption == i] + menuOptions[i], (5, 70 + (i - minMenuDispIndex) * 20), size = 18, color = flashColor())
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(width - 15, 70, 6, 140), 1)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(width - 15, 70 + 140 * minMenuDispIndex / len(menuOptions), 6, 140 * (maxMenuDispIndex - minMenuDispIndex) / len(menuOptions)))
        
        if checkKeys(defaultKeys["menuSelect"]) and not checkKeys(defaultKeys["menuSelect"], keysPressedLastFrame):
            prevState = state
            prevOption = selectedOption
            if state == 3:
                state, gameType, selectedOption = [
                    [(2, 0, 0), (3, 0, 1), (3, 0, 2), (4, 0, 0)],
                    [(2, 0, 1), (4, 1, 0)],
                    [(2, 0, 2), (4, 0, 1), (4, 2, 0)],
                    [(2, 0, 3), (4, 3, 0)],
                    [(2, 0, 4), (4, 4, 0)]
                ][gameType][selectedOption]
            else:
                state, gameType, selectedOption = {
                    1: [(2, 0, 0) for i in langList],
                    2: [(3, 0, 3), (3, 1, 1), (3, 2, 2), (3, 3, 1), (3, 4, 1), (6, 0, 0), (9, 0, 0)],
                    5: [(4, gameType, 0), (4, gameType, 0), (3, gameType, 0)],
                    6: [(2, 0, 5), (7, 0, 1), (8, 0, langNum)],
                    7: [(6, 0, 1), (7, 0, 1), (7, 0, 2)],
                    8: [(6, 0, 2) for i in langList],
                }[state][selectedOption]
            if prevState in [1, 8]:
                updateLang(prevOption)
            if prevState in [5] and prevOption == 2:
                currentGravity = 1
            if state in [3] and prevState not in [3] and gameType in [0, 2]:
                startingLevel = 1
                endlessGame = False
            elif state in [4] and not (prevState == 5 and prevOption == 0):
                initializeNewGame()
                gameTime = 0
                gameTimeExclLCD = 0
                pointsScoredByLineClear = 0
                if gameType in [0, 2]:
                    level = startingLevel
                gameOver = None
        elif checkKeys(defaultKeys["pause"]) and not checkKeys(defaultKeys["pause"], keysPressedLastFrame) and state == 5:
            state = 4
            unpausedThisFrame = True
        elif checkKeys(defaultKeys["menuDown"]) and not checkKeys(defaultKeys["menuDown"], keysPressedLastFrame):
            selectedOption = (selectedOption + 1) % len(menuOptions)
        elif checkKeys(defaultKeys["menuUp"]) and not checkKeys(defaultKeys["menuUp"], keysPressedLastFrame):
            selectedOption = (selectedOption - 1) % len(menuOptions) 
        elif checkKeys(defaultKeys["menuRight"]) and not checkKeys(defaultKeys["menuRight"], keysPressedLastFrame):
            if state == 3:
                if gameType == 0:
                    if selectedOption == 1:
                        startingLevel = min(startingLevel + 1, 15)
                    elif selectedOption == 2:
                        endlessGame = not endlessGame
                if gameType == 2:
                    if selectedOption == 1:
                        startingLevel = min(startingLevel + 1, 30)
            elif state == 7:
                if selectedOption == 1:
                    delayedAutoShift = min(delayedAutoShift + .01, 1)
                elif selectedOption == 2:
                    autoRepeat = min(autoRepeat + .01, 1)
        elif checkKeys(defaultKeys["menuLeft"]) and not checkKeys(defaultKeys["menuLeft"], keysPressedLastFrame):
            if state == 3:
                if gameType == 0:
                    if selectedOption == 1:
                        startingLevel = min(startingLevel - 1, 1)
                    elif selectedOption == 2:
                        endlessGame = not endlessGame
                if gameType == 2:
                    if selectedOption == 1:
                        startingLevel = min(startingLevel - 1, 1)
            elif state == 7:
                if selectedOption == 1:
                    delayedAutoShift = max(delayedAutoShift - .01, .01)
                elif selectedOption == 2:
                    autoRepeat = max(autoRepeat - .01, 0)
    elif state == 9: # Protestware
        pwtext = [
            {
                "name": "English",
                "message": getLangTxt("pwinfotxt"),
                "fputin": getLangTxt("pwfputin")
            },
            {
                "name": "український",
                "message": [
                    "Параметр рускай мовы быў выдалены, таму",
                    "што:",
                    "- некаторыя пераклады зроблены з Google",
                    "  Translate (напрыклад, для гэтага",
                    "  паведамлення), што часам можа быць",
                    "  ненадзейным",
                    "- пра ўварванне Расеі ва Украіну"
                ],
                "fputin": "На хуй, Путін!"
            },
            {
                "name": "беларуская",
                "message": [
                    "Параметр російської мови вилучено,",
                    "оскільки:",
                    "- деякі переклади (наприклад, цей)",
                    "  надійшли з Google Translate, який іноді",
                    "  може бути ненадійним",
                    "- про вторгнення Росії в Україну"
                ],
                "fputin": "До біса, Путін!"
            },
            {
                "name": "русский",
                "message": [
                    "Опция русского языка была удалена,",
                    "потому что:",
                    "- некоторые переводы (такие как этот)",
                    "  взяты из Google Translate, что иногда",
                    "  может быть ненадежным",
                    "- о вторжении России в Украину"
                ],
                "fputin": "Иди нахуй, Путин!"
            }
        ]

        try:
            pwLangNum
        except NameError:
            pwLangNum = 0

        if checkKeys(defaultKeys["menuSelect"]) and not checkKeys(defaultKeys["menuSelect"], keysPressedLastFrame):
            state, gameType, selectedOption = 2, 0, 0
        if checkKeys(defaultKeys["menuRight"]) and not checkKeys(defaultKeys["menuRight"], keysPressedLastFrame):
            pwLangNum = (pwLangNum + 1) % len(pwtext)
        if checkKeys(defaultKeys["menuLeft"]) and not checkKeys(defaultKeys["menuLeft"], keysPressedLastFrame):
            pwLangNum = (pwLangNum - 1) % len(pwtext)
        pygame.draw.rect(screen, pygame.Color(  0,   0, 255), pygame.Rect(0,        0, width, height/2))
        pygame.draw.rect(screen, pygame.Color(255, 255,   0), pygame.Rect(0, height/2, width, height/2))
        for i in enumerate(pwtext[pwLangNum]["message"]):
            render_text(i[1], (0, 20 + 14*i[0]), size=14)
        render_text(pwtext[pwLangNum]["fputin"], (50, 20 + height/2), pygame.Color(0, 0, 0), 14)
        render_text("< " + pwtext[pwLangNum]["name"] + " >", (10, height/2 + 40), pygame.Color(0,0,0), 14)
        render_text(getLangTxt("pwexit"), (10, height/2 + 60), pygame.Color(0, 0, 0), 16)
          
    if state == 0:
        render_text(getLangTxt("pressAnyKey"), (5, 100), size = 18)
        if True in pressedKeys:
            state = 2
            selectedOption = 0
  
    if state in [4]: # Game state
    
        gameEnd = (
            (gameType == 0 and lineClears >= 150 and not endlessGame and lineClearTimer <= 0) or
            (gameType == 1 and lineClears >= 500 and lineClearTimer <= 0) or
            (gameType == 2 and lineClears >= 300 and lineClearTimer <= 0) or
            (gameType == 3 and lineClears >= 40 and lineClearTimer <= 0) or
            (gameType == 4 and gameTime >= 180)
        )
        if checkKeys(defaultKeys["pause"]) and not checkKeys(defaultKeys["pause"], keysPressedLastFrame) and not unpausedThisFrame:
            state = 5
            selectedOption = 0
        elif gameOver == None and not gameEnd:
            if gameType == 2:
                lockDelay = (31 - level) / 30 * (.5 - autoRepeat) + autoRepeat
                gameOver = gameTick(lambda level: 0)
            else:
                if gameType == 1 and level > 20:
                    lockDelay = (31 - (level - 20)) / 30 * (.5 - autoRepeat) + autoRepeat
                gameOver = gameTick()
            gameTime += lastFrameTotalTime
            if lineClearTimer <= 0:
                gameTimeExclLCD += lastFrameTotalTime
            if gameType in [3, 4]:
                level = 1
        # elif gameOver != None:
        #     i = random.randint(0, len(stack) - 1)
        #     j = random.randint(0, len(stack[i]) - 1)
        #     if stack[i][j] != -1:
        #         stack[i][j] = len(tetrominoColors) - 1

        if not gameEnd:
            for i in fallMinoes:
                render_mino(i[0], i[1])

        # Render the stack; current, next, and held tetrominoes; and the ghost piece
        for i in range(len(stack)):
            for j in range(len(stack[i])):
                if stack[i][j] >= 0:
                    render_mino(stack[i][j], (j, i))
        if lineClearTimer <= 0 and not gameEnd:
            for i in tetrominoes[currentTetromino][tetrominoRotation]:
                render_mino(currentTetromino, (tetrominoPosition[0] + i[0], tetrominoPosition[1] + i[1]))
            ghostHeight = tetrominoPosition[1]
            ghostTouchingGround = False
            while not ghostTouchingGround:
                for i in tetrominoes[currentTetromino][tetrominoRotation]:
                    if stack[ghostHeight + i[1]][tetrominoPosition[0] + i[0]] != -1 or ghostHeight + i[1] < 0:
                        ghostTouchingGround = True
                        break
                if not ghostTouchingGround:
                    ghostHeight -= 1
            if ghostHeight < tetrominoPosition[1]:
                ghostHeight += 1
            for i in tetrominoes[currentTetromino][tetrominoRotation]:
                render_mino(currentTetromino, (tetrominoPosition[0] + i[0], ghostHeight + i[1]), 1)
        for i in range(len(nextTetrominoes)):
            for j in tetrominoes[nextTetrominoes[i]][0]:
                render_mino(nextTetrominoes[i], (11 + j[0], 15 - 3 * i + j[1]))
        render_text(getLangTxt("next"), (220, 20), flashColor(), 10)
        if tetrominoAlreadyHeld:
            holdColor = 7
        else:
            holdColor = holdQueue
        if holdQueue != -1:
            for i in tetrominoes[holdQueue][0]:
                render_mino(holdColor, (-5 + i[0], 15 + i[1]))
        render_text(getLangTxt("hold"), (60, 20), flashColor(), 10)

        # Draw the playfield grid
        for i in range(30, 220, 10):
            pygame.draw.line(screen, pygame.Color(64, 64, 64, 128), (110, i), (210, i))
        for i in range(120, 210, 10):
            pygame.draw.line(screen, pygame.Color(64, 64, 64, 128), (i, 20), (i, 220))

        if len(linesToClear) > 0 and lineClearTimer > 0 and gameType != 3:
            render_text(str(pointsScoredByLineClear), (145, 210 - 10 * linesToClear[0]), flashColor(), 10)

        # Draw the "tetrion"
        pygame.draw.line(screen, pygame.Color(128, 128, 128), (110, 20), (210, 20))
        pygame.draw.lines(screen, pygame.Color(255, 255, 255), False, [(110, 20), (110, 220), (210, 220), (210, 20)])

        if gameType in [1, 2]:
            pygame.draw.line(screen, pygame.Color(255, 255, 255), (100 / .5 * lockDelay + 110, 220), (100 / .5 * lockDelay + 110, 230))

        if lockTimer >= 0:
            pygame.draw.line(screen, pygame.Color(255, 0, 0), (110, 225), (100 / .5 * lockTimer + 110, 225), 4)
        for i in range(inputsUntilLock):
            # pygame.draw.circle(screen, pygame.Color(255, 255, 255), (20 * i / 3 + 340 / 3, 235), 3) # old
            pygame.draw.polygon(screen, pygame.Color(255, 255, 255), [
                ((20 * i + 1) / 3 + 113, 232),
                ((20 * i + 1) / 3 + 116, 235),
                ((20 * i + 1) / 3 + 113, 238),
                ((20 * i + 1) / 3 + 110, 235),
            ])
        
        # Display useful information like score, lines, and time

        if gameType == 1:
            levelDisp = (str(level), "M" + str(level - 20))[int(level > 20)]
        elif gameType == 2:
            levelDisp = "M" + str(level)
        else:
            levelDisp = str(level)

        if gameType == 3:
            render_text(    getLangTxt("lines")         , (260,  24 +  12), flashColor())
            render_text(    getLangTxt("remaining")     , (260,  36 +  12), flashColor())
            render_text(    str(max(40 - lineClears, 0)), (260,  48 +  12), flashColor([None, pygame.Color(255, 192, 192)][int(len(linesToClear) > 0 and lineClearTimer > 0)]))
            render_text(    getLangTxt("time")          , (260,  72 +  12), flashColor())
            render_text(    formatTime(gameTime)        , (260,  84 +  12), flashColor())
            render_text(    getLangTxt("exclLCD1")      , (260, 108 +  12), flashColor())
            render_text(    getLangTxt("exclLCD2")      , (260, 120 +  12), flashColor())
            render_text(    formatTime(gameTimeExclLCD) , (260, 136 +  12), flashColor())

        else:
            render_text(    getLangTxt("score")         , (260,   0 +  12), flashColor())
            render_text(    str(score)                  , (260,  12 +  12), flashColor([None, pygame.Color(0, 255, 255)][int(pointsScoredByLineClear > 0 and (len(linesToClear) <= 0 or lineClearTimer > 0))]))
            render_text(    getLangTxt("lines")         , (260,  36 +  12), flashColor())
            render_text(    str(         lineClears    ), (260,  48 +  12), flashColor([None, pygame.Color(0, 255, 255)][int(len(linesToClear) > 0 and lineClearTimer > 0)]))
            if gameType == 4:
                render_text(getLangTxt("time")          , (260,  72 +  12), flashColor())
                render_text(getLangTxt("remaining")     , (260,  84 +  12), flashColor())
                render_text(formatTime(180 - gameTime)  , (260,  96 +  12), flashColor())
            else:
                render_text(getLangTxt("level")         , (260,  72 +  12), flashColor())
                render_text(levelDisp                   , (260,  84 +  12), flashColor())

        if gameType != 3:

            # Display info about whether the player achieved a T-Spin, Back-to-Back, and/or All Clear

            if tSpin >= 2:
                render_text(    getLangTxt("tSpin")                                 , (0,  80 +   0), flashColor(pygame.Color(255, 192, 255)))
            elif tSpin >= 1:
                render_text(    getLangTxt("miniTSpin")                             , (0,  80 +   0), flashColor(pygame.Color(255, 192, 255)))
            if len(linesToClear) > 0:
                if backToBack > 1:
                    render_text(getLangTxt("backToBack")                            , (0,  80 +  12), flashColor(pygame.Color(128, 255, 128)))
                if allClear:
                    render_text(getLangTxt("allClear")                              , (0,  80 +  24), flashColor(pygame.Color(128, 255, 128)))
            else:
                if tSpin > 0:
                    render_text("( +" + str(pointsScoredByLineClear) + " )"   , (0,  80 +  12), flashColor())
            if combo > 0:
                render_text(    "{ " + str(combo) + " " + getLangTxt("combo") + " }", (0,  80 +  36), flashColor(pygame.Color(192, 192, 255)))

        if gameOver != None:
            render_text(getLangTxt("gameOver") + " (" + getLangTxt(gameOver) + ")", (5, 120), flashColor(pygame.Color(255, 160, 160)), 18)
        elif gameEnd:
            render_text(getLangTxt("excellent"), (100, 120), flashColor(pygame.Color(0, 255, 255)), 18)


    render_text(getLangTxt("fps") + f" = {1 / lastFrameTime:.1f} --> {1 / lastFrameTotalTime:.1f}")

    # Update the display and FPS value and wait for the next frame to start
    if windowResized:
        if windowMaximized:
            windowWidth = max((lambda s, d: s - (s % d))(pygame.display.get_window_size()[0] - size[0], size[0]), size[0])
        else:
            windowWidth = max(pygame.display.get_window_size()[0], size[0])
        pygame.display.set_mode((windowWidth, windowWidth * 3 // 4), flags)
    pygame.transform.scale(screen, pygame.display.get_window_size(), window)
    pygame.display.flip()
    lastFrameTime = time.perf_counter() - t
    while time.perf_counter() < t + minFrameLength:
        None
    lastFrameTotalTime = time.perf_counter() - t