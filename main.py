import os, sys, pygame, time, random, json

version = "a0.0.1"
minFrameLength = 1 / 60 # reciprocral of maximum framerate
delayedAutoShift = .3
autoRepeat = .0625

defaultLang = {
    "title"        : "pygame-тетромино",
    "version"      : "версия",
    "blockOut"     : "блокировать",
    "lockOut"      : "Блокировка",
    "classic"      : "классическая",
    "endurance"    : "выносливость",
    "extreme"      : "экстремальная",
    "40line"       : "40 линий",
    "3min"         : "3 минуты",
    "back"         : "вернуться",
    "startGame"    : "начать игру",
    "startingLevel": "начальный уровень",
    "endless"      : "бесконечный",
    "off"          : "выключен",
    "on"           : "включен",
    "pressAnyKey"  : "нажмите любую клавишу",
    "next"         : "NEXT",
    "hold"         : "ЗАПАС",
    "score"        : "счет",
    "lines"        : "линии",
    "time"         : "время",
    "level"        : "уровень",
    "remaining"    : "остальные",
    "exclLCD1"     : "за исключением",
    "exclLCD2"     : "обрывов строк",
    "gameOver"     : "Игра окончена",
    "fps"          : "кадров в секунду",
    "tSpin"        : "{ т-поворот }",
    "miniTSpin"    : "{ мини т-поворот }",
    "backToBack"   : "{ спина к спине }",
    "allClear"     : "{ все чисто }",
    "combo"        : "комбо",
    "excellent"    : "Отлично!"
}
try:
    langDirectory = os.path.join(os.path.dirname(__file__), "lang")
    langList = [f for f in os.listdir(langDirectory) if os.path.isfile(os.path.join(langDirectory, f))]
    langList = [i for i in langList if i[-5 :] == ".json"]
    print("\n1 русский")
    for i in range(len(langList)): print(i + 2, langList[i][: -5])
    langNum = int(input("\n🌐 --> ")) - 2
    if langNum < 0: 
        lang = defaultLang
    else:
        langFile = open(os.path.join(langDirectory, langList[langNum]))
        lang = json.load(langFile)
        langFile.close()
        print()
except Exception as e:
    print("\n", e, "\n")
    lang = defaultLang

# Initialize pygame and start and rename the window
pygame.init()
size = width, height = 320, 240
flags = pygame.RESIZABLE
window = pygame.display.set_mode(size, flags)
screen = pygame.Surface(size)
pygame.display.set_caption(lang["title"])

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
    "shiftRight" : [pygame.constants.K_RIGHT,  pygame.constants.K_KP6]
}

def checkKeys(keys, keyData = None):
    global pressedKeys
    if keyData == None:
        keyData = pressedKeys
    for i in keys:
        if pressedKeys[i]: # 0 <= i < len(pressedKeys) and
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

    # Variables related to tetromino manipulation (TODO: replace "pressed last frame" variables with checkKeys(..., keysPressedLastFrame))

    isDASCharged = False
    autoRepeatTimer = 1
    leftRotatePressedLastFrame = False
    rightRotatePressedLastFrame = False
    holdPressedLastFrame = False
    hardDropPressedLastFrame = False
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
    global allClear, autoRepeatTimer, backToBack, combo, currentGravity, fallMinoes, fallTimer, hardDropPressedLastFrame, holdPressedLastFrame, holdQueue, inputsUntilLock, isDASCharged, lastFrameTotalTime, leftRotatePressedLastFrame, level, lineClearTimer, lineClears, linesToClear, lockDelay, lockTimer, lowestTetrominoYPosition, nextTetrominoes, pointsScoredByLineClear, rightRotatePressedLastFrame, score, stack, tetrominoAlreadyHeld, tetrominoPosition, tetrominoRotatedDirectlyBeforeLock, tSpin
    
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
    if checkKeys(defaultKeys["hardDrop"]) and not hardDropPressedLastFrame and lineClearTimer <= 0:
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
    hardDropPressedLastFrame = checkKeys(defaultKeys["hardDrop"])

    # Manage hold
    if checkKeys(defaultKeys["hold"]) and not (holdPressedLastFrame or tetrominoAlreadyHeld) and lineClearTimer <= 0:
        holdCopy = holdQueue
        holdQueue = currentTetromino
        initializeNewTetromino(holdCopy)
        tetrominoAlreadyHeld = True
    holdPressedLastFrame = checkKeys(defaultKeys["hold"])

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
                                return lang["blockOut"]
                        notLockedOut = False
                        for i in tetrominoes[currentTetromino][tetrominoRotation]:
                            stack[tetrominoPosition[1] + i[1]][tetrominoPosition[0] + i[0]] = currentTetromino
                            if tetrominoPosition[1] + i[1] < 20:
                                notLockedOut = True
                        if not notLockedOut:
                            return lang["lockOut"]

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

    if checkKeys(defaultKeys["shiftRight"]):
        autoRepeatTimer -= lastFrameTotalTime
        if autoRepeatTimer <= 0:
            if isDASCharged:
                autoRepeatTimer = autoRepeat
            else:
                autoRepeatTimer = delayedAutoShift
                isDASCharged = True
            if lineClearTimer <= 0:
                shiftTetromino(1)    
    if checkKeys(defaultKeys["shiftLeft"]):
        autoRepeatTimer -= lastFrameTotalTime
        if autoRepeatTimer <= 0:
            if isDASCharged:
                autoRepeatTimer = autoRepeat
            else:
                autoRepeatTimer = delayedAutoShift
                isDASCharged = True
            if lineClearTimer <= 0:
                shiftTetromino(-1)
    if not (checkKeys(defaultKeys["shiftLeft"]) or checkKeys(defaultKeys["shiftRight"])):
        isDASCharged = False
        autoRepeatTimer = 0.0

    # Manage rotation of tetrominoes
    if lineClearTimer <= 0:
        if checkKeys(defaultKeys["rotateRight"]):
            if not rightRotatePressedLastFrame:
                rightRotatePressedLastFrame = True
                rotateTetromino(1)
        else:
            rightRotatePressedLastFrame = False

        if checkKeys(defaultKeys["rotateLeft"]):
            if not leftRotatePressedLastFrame:
                leftRotatePressedLastFrame = True
                rotateTetromino(-1)
        else:
            leftRotatePressedLastFrame = False

    return None

# Formats number of seconds into time formatted as mm:ss.cc. For whatever reason this wasn't working as lambda function. also long-line-itis pog
def formatTime(secs):
    return str(int(secs / 600)) + str(int(secs / 60) % 10) + ":" + str(int(secs / 10) % 6) + str(int(secs) % 10) + "." + str(int(secs / .1) % 10) + str(int(secs / .01) % 10)

state = 0

startingLevel = 1
endlessGame = False
menuOptions = None
def updateMenuText():
    global menuOptions
    menuOptions = {
        1: [lang["classic"], lang["endurance"], lang["extreme"], lang["40line"], lang["3min"],],
        2: [lang["back"], lang["startingLevel"] + ": " + str(startingLevel), lang["endless"] + ": " + {False: lang["off"], True: lang["on"]}[endlessGame], lang["startGame"]],
        3: [lang["back"], lang["startGame"]],
        4: [lang["back"], lang["startingLevel"] + ": M" + str(startingLevel), lang["startGame"]],
        5: [lang["back"], lang["startGame"]],
        6: [lang["back"], lang["startGame"]]
    }

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
        keysPressedLastFrame = []
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

    if state in [0, 1]:
        render_text(lang["title"], (10, 50), size = 24)
        render_text(lang["version"] + " " + version, (20, 220), size = 14)
    if state in [1, 2, 3, 4, 5, 6]: # Menu states
        updateMenuText()
        for i in range(len(menuOptions[state])):
            render_text({False: "  ", True: "> "}[selectedOption == i] + menuOptions[state][i], (5, 90 + i * 20), size = 18)
        # Indexing into pressedKeys and keysPressedLastFrame is temporary and will be replaced
        if pressedKeys[pygame.constants.K_RETURN] and not keysPressedLastFrame[pygame.constants.K_RETURN]:
            state, selectedOption = {
                1: [(2, 3), (3, 1), (4, 2), (5, 1), (6, 1)],
                2: [(1, 0), (2, 1), (2, 2), (7, 0)],
                3: [(1, 1), (8, 0)],
                4: [(1, 2), (4, 1), (9, 0)],
                5: [(1, 3), (10, 0)],
                6: [(1, 4), (11, 0)]
            }[state][selectedOption]
            if state in [2, 4]:
                startingLevel = 1
                endlessGame = False
            elif state in [7, 8, 9, 10, 11]:
                initializeNewGame()
                gameTime = 0
                gameTimeExclLCD = 0
                pointsScoredByLineClear = 0
                if state in [7, 9]:
                    level = startingLevel
                gameOver = None
        elif pressedKeys[pygame.constants.K_DOWN] and not keysPressedLastFrame[pygame.constants.K_DOWN]:
            selectedOption = (selectedOption + 1) % len(menuOptions[state])
        elif pressedKeys[pygame.constants.K_UP] and not keysPressedLastFrame[pygame.constants.K_UP]:
            selectedOption = (selectedOption - 1) % len(menuOptions[state]) 
        elif pressedKeys[pygame.constants.K_RIGHT] and not keysPressedLastFrame[pygame.constants.K_RIGHT]:
            if state == 2:
                if selectedOption == 1:
                    startingLevel = min(startingLevel + 1, 15)
                elif selectedOption == 2:
                    endlessGame = not endlessGame
            if state == 4:
                if selectedOption == 1:
                    startingLevel = min(startingLevel + 1, 30)
        elif pressedKeys[pygame.constants.K_LEFT] and not keysPressedLastFrame[pygame.constants.K_LEFT]:
            if state == 2:
                if selectedOption == 1:
                    startingLevel = max(startingLevel - 1, 1)
                elif selectedOption == 2:
                    endlessGame = not endlessGame
            if state == 4:
                if selectedOption == 1:
                    startingLevel = max(startingLevel - 1, 1)
    if state == 0:
        render_text(lang["pressAnyKey"], (5, 100), size = 18)
        if True in pressedKeys:
            state = 1
            selectedOption = 0
    if state in [7, 8, 9, 10, 11]: # Game states
    
        gameEnd = (
            (state == 7 and lineClears >= 150 and not endlessGame and lineClearTimer <= 0) or
            (state == 8 and lineClears >= 500 and lineClearTimer <= 0) or
            (state == 9 and lineClears >= 300 and lineClearTimer <= 0) or
            (state == 10 and lineClears >= 40 and lineClearTimer <= 0) or
            (state == 11 and gameTime >= 10800)
        )
        if gameOver == None and not gameEnd:
            if state == 9:
                lockDelay = (31 - level) / 30 * (.5 - autoRepeat) + autoRepeat
                gameOver = gameTick(lambda level: 0)
            else:
                if state == 8 and level > 20:
                    lockDelay = (31 - (level - 20)) / 30 * (.5 - autoRepeat) + autoRepeat
                gameOver = gameTick()
            gameTime += lastFrameTotalTime
            if lineClearTimer <= 0:
                gameTimeExclLCD += lastFrameTotalTime
            if state in [10, 11]:
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
        render_text(lang["next"], (220, 20), flashColor(), 10)
        if tetrominoAlreadyHeld:
            holdColor = 7
        else:
            holdColor = holdQueue
        if holdQueue != -1:
            for i in tetrominoes[holdQueue][0]:
                render_mino(holdColor, (-5 + i[0], 15 + i[1]))
        render_text(lang["hold"], (60, 20), flashColor(), 10)

        # Draw the playfield grid
        for i in range(30, 220, 10):
            pygame.draw.line(screen, pygame.Color(64, 64, 64, 128), (110, i), (210, i))
        for i in range(120, 210, 10):
            pygame.draw.line(screen, pygame.Color(64, 64, 64, 128), (i, 20), (i, 220))

        if len(linesToClear) > 0 and lineClearTimer > 0 and state != 10:
            render_text(str(pointsScoredByLineClear), (145, 210 - 10 * linesToClear[0]), flashColor(), 10)

        # Draw the "tetrion"
        pygame.draw.line(screen, pygame.Color(128, 128, 128), (110, 20), (210, 20))
        pygame.draw.lines(screen, pygame.Color(255, 255, 255), False, [(110, 20), (110, 220), (210, 220), (210, 20)])

        if state in [8, 9]:
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

        if state == 8:
            levelDisp = (str(level), "M" + str(level - 20))[int(level > 20)]
        elif state == 9:
            levelDisp = "M" + str(level)
        else:
            levelDisp = str(level)

        if state == 10:
            render_text(    lang["lines"]                 , (260,  24 +  12), flashColor())
            render_text(    lang["remaining"]             , (260,  36 +  12), flashColor())
            render_text(    str(max(40 - lineClears, 0))  , (260,  48 +  12), flashColor([None, pygame.Color(255, 192, 192)][int(len(linesToClear) > 0 and lineClearTimer > 0)]))
            render_text(    lang["time"]                  , (260,  72 +  12), flashColor())
            render_text(    formatTime(gameTime)        , (260,  84 +  12), flashColor())
            render_text(    lang["exclLCD1"]              , (260, 108 +  12), flashColor())
            render_text(    lang["exclLCD2"]              , (260, 120 +  12), flashColor())
            render_text(    formatTime(gameTimeExclLCD) , (260, 136 +  12), flashColor())

        else:
            render_text(    lang["score"]                 , (260,   0 +  12), flashColor())
            render_text(    str(score)                    , (260,  12 +  12), flashColor([None, pygame.Color(0, 255, 255)][int(pointsScoredByLineClear > 0 and (len(linesToClear) <= 0 or lineClearTimer > 0))]))
            render_text(    lang["lines"]                 , (260,  36 +  12), flashColor())
            render_text(    str(         lineClears    )  , (260,  48 +  12), flashColor([None, pygame.Color(0, 255, 255)][int(len(linesToClear) > 0 and lineClearTimer > 0)]))
            if state == 11:
                render_text(lang["time"]                  , (260,  72 +  12), flashColor())
                render_text(lang["remaining"]             , (260,  84 +  12), flashColor())
                render_text(formatTime(10800 - gameTime), (260,  96 +  12), flashColor())
            else:
                render_text(lang["level"]                 , (260,  72 +  12), flashColor())
                render_text(levelDisp                     , (260,  84 +  12), flashColor())

        if state != 10:

            # Display info about whether the player achieved a T-Spin, Back-to-Back, and/or All Clear

            if tSpin >= 2:
                render_text(    lang["tSpin"]                                 , (0,  80 +   0), flashColor(pygame.Color(255, 192, 255)))
            elif tSpin >= 1:
                render_text(    lang["miniTSpin"]                             , (0,  80 +   0), flashColor(pygame.Color(255, 192, 255)))
            if len(linesToClear) > 0:
                if backToBack > 1:
                    render_text(lang["backToBack"]                            , (0,  80 +  12), flashColor(pygame.Color(128, 255, 128)))
                if allClear:
                    render_text(lang["allClear"]                              , (0,  80 +  24), flashColor(pygame.Color(128, 255, 128)))
            else:
                if tSpin > 0:
                    render_text("( +" + str(pointsScoredByLineClear) + " )"   , (0,  80 +  12), flashColor())
            if combo > 0:
                render_text(    "{ " + str(combo) + " " + lang["combo"] + " }", (0,  80 +  36), flashColor(pygame.Color(192, 192, 255)))

        if gameOver != None:
            render_text(lang["gameOver"] + " (" + gameOver + ")", (5, 120), flashColor(pygame.Color(255, 160, 160)), 18)
        elif gameEnd:
            render_text(lang["excellent"], (100, 120), flashColor(pygame.Color(0, 255, 255)), 18)


    render_text(lang["fps"] + f" = {1 / lastFrameTime:.1f} --> {1 / lastFrameTotalTime:.1f}", color = flashColor())

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