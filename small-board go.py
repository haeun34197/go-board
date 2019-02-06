## Citation: Followed tutorial from codercaste

## boardsize x boardsize go-board
boardsize = 8
gameCont = True

## Initialize game board nxn with '-' representing a blank spot on the board
def initialize():
    gs = []
    for i in range(0, boardsize):
        gs.append([])
        for j in range(0, boardsize):
            gs[i].append('-')
    return gs
 
## Prints ascii representation of board
def printboard(gs):
    global boardsize
    for row in gs:
        rowprint = ''
        for element in row:
            rowprint += element
            rowprint += ' '
        print(rowprint)
 
## Returns a list of the board positions surrounding the passed group.
def gperm(group):
    permimeter = []
    global boardsize
    hit = 0
    loss = 0

    i = 0
    j = 0
    while i < boardsize:
        j = 0
        hit = 0
        while j < boardsize:
            if [i,j] in group:
                hit = 1
            elif (hit == 1) & ([i,j] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([i,j])
                hit = 0
                loss = 0
            j += 1
        i += 1
    ## Adds permimeter spots to the right
    i = 0
    j = 0
    while i < boardsize:
        j = 0
        hit = 0
        while j < boardsize:
            if [j,i] in group:
                hit = 1
            elif (hit == 1) & ([j,i] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([j,i])
                hit = 0
                loss = 0
            j += 1
        i += 1
    ## Adds permimeter spots above
    i = 0
    j = boardsize-1
    while i < boardsize:
        j = boardsize-1
        hit = 0
        while j >= 0:
            if [i,j] in group:
                hit = 1
            elif (hit == 1) & ([i,j] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([i,j])
                hit = 0
                loss = 0
            j -= 1
        i += 1
    ## Adds permimeter spots to the left
    i = 0
    j = boardsize-1
    while i < boardsize:
        j = boardsize-1
        hit = 0
        while j >= 0:
            if [j,i] in group:
                hit = 1
            elif (hit == 1) & ([j,i] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([j,i])
                hit = 0
                loss = 0
            j -= 1l
        i += 1
    return permimeter
 
## Returns a string that describes the game state
def readable(gs):
    readthis = ''
    readthis += '<<'
    for row in gs:
        for element in row:
            readthis += element
    readthis += '>>'
    return readthis
 
## Score count
def scoreCount():
    global gsc
    global non_groups
    global p1_points
    global p2_points
    global boardsize
 
    ## Creates a list of groups (non_groups) of empty positions.
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if gsc[j][i] == '-':
                new = 1
                for group in non_groups:
                    if [i,j] in gperm(group):
                        group.append([i,j])
                        new = 0
                if new == 1:
                    non_groups.append([[i,j]])
    concat('-')
 
    p1_points = 0
    p2_points = 0
 
    ## Tally # of stones on board for score
    for group in p1_groups:
        p1_points += len(group)
    for group in p2_groups:
        p2_points += len(group)
 
    ## Handles capture and points scored from that capture
    for group in non_groups:
        no = 0
        for element in gperm(group):
            if gsc[element[1]][element[0]] != 'o':
                no = 1
        if no == 0:
            p1_points += len(group)
 
    for group in non_groups:
        no = 0
        for element in gperm(group):
            if gsc[element[1]][element[0]] != 'x':
                no = 1
        if no == 0:
            p2_points += len(group)
 
## Lists of groups that have been removed from the board via capture
restore_o = []
restore_x = []
 

## Checks for capture, and removes the captured pieces from the board
def capture(whoseturn):
    global p1_groups
    global p2_groups
    global gsf
    global restore_o
    global restore_x
    global edited
    if whoseturn == 'p1':
        groups = p2_groups
        otherplayer = 'o'
    else:
        groups = p1_groups
        otherplayer = 'x'
 
    ## Checks for capture state, and removes stones as necessary
    for group in groups:
        safe = 0
        for element in gperm(group):
            if gsf[element[1]][element[0]] != otherplayer:
                safe = 1
        if safe != 1:
            edited = 1
            if whoseturn == 'p1':
                restore_x.append(group)
            else:
                restore_o.append(group)
            groups.remove(group)
 
    # Sets gsf given the new captures
    gsf = initialize()
    for group in p1_groups:
        for point in group:
            gsf[point[1]][point[0]] = 'o'
    for group in p2_groups:
        for point in group:
            gsf[point[1]][point[0]] = 'x'
 
## Checks for validity of new move
def validMove():
    global gscache
    global gsc
    global gsp
    global gsf
    if readable(gsf) not in gscache:
        gsp = []
        gsc = []
        for element in gsf:
            gsp.append(element)
            gsc.append(element)
        gscache += readable(gsf)
        return True
    else:
        return False
 
## Joins into one group if any groups contain the same point;
def concat(whoseturn):
    global p1_groups
    global p2_groups
    global non_groups
    if whoseturn == 'p1':
        groups = p1_groups
    elif whoseturn == 'p2':
        groups = p2_groups
    else:
        groups = non_groups
    i = 0

    currentgroups = len(groups)
    previousgroups = currentgroups + 1

    while previousgroups != currentgroups:
        while i < len(groups)-1:
            reset = 0
            j = i + 1
            while j < len(groups):
                k = 0
                while k < len(groups[i]):
                    if groups[i][k] in groups[j]:
                        for element in groups[j]:
                            if element not in groups[i]:
                                groups[i].append(element)
                        groups.remove(groups[j])
                        reset = 1
                    if reset == 1:
                        break
                    k += 1
                j += 1
            if reset == 1:
                i = -1
            i += 1
        previousgroups = currentgroups
        currentgroups = len(groups)
 
## Adds point xy to a group
def addpoint(xy, whoseturn):
    global p1_groups
    global p2_groups
    if whoseturn == 'p1':
        groups = p1_groups
    else:
        groups = p2_groups
    new = 1
    for group in groups:
        if xy in gperm(group):
            group.append(xy)
            new = 0
    if new == 1:
        groups.append([xy])
 
## Lets the player select a move.
def selectmove(whoseturn):
    global boardsize
    global gsf
    hold = 1
    while hold == 1:
 
        minihold = 1
        while minihold == 1:
            pp = raw_input('Place a stone (y/n)? ')
            if pp == 'n':
                return 'pass'
            elif pp == 'y':
                minihold = 0
                error = 0
                try:
                    x = int(raw_input('x: '))
                except ValueError:
                    error = 1
                try:
                    y = int(raw_input('y: '))
                except ValueError:
                    error = 1
                if error == 1:
                    minihold = 1
                    print('invalid')
            else:
                print('invalid')
        ## Ensures that the raw_input is on the board
        if (x > boardsize) | (x < 0) | (y > boardsize) | (y < 0):
            print('invalid')
        elif gsc[y][x] != '-':
            print('invalid')
        else:
            hold = 0 
    ## The board used to test if a move is valid
    if whoseturn == 'p1':
        gsf[y][x] = 'o'
    else:
        gsf[y][x] = 'x'
 
    return [x,y]
 
## Defines functionality and validity of turn of each player
def turn():
    global whoseturn
    global notwhoseturn
    global player1_pass
    global player2_pass
    global gameover
    hold = 1
    while hold == 1:
        print('Turn ' + whoseturn)

        xy = selectmove(whoseturn)
        if xy == 'pass':
            if whoseturn == 'p1':
                player1_pass = 1
            else:
                player2_pass = 1
            hold = 0
        ## If the player doesn't pass...
        else:
            player1_pass = 0
            player2_pass = 0

            addpoint(xy,whoseturn)
            concat(whoseturn)
            minihold = 1
            ## Edited is a value used to check whether any capture is made. 
            edited = 0
            while minihold == 1:
                restore_o = []
                restore_x = []
                capture(whoseturn)
                capture(notwhoseturn)
                if edited == 0:
                    minihold = 0
                    edited = 0
                else:
                    edited = 0
        
            if validMove():
                hold = 0
            ## If the move is invalid, the captured groups need to be returned to the board
            else:
                print('invalid move - board will be restored to a previous state')
                for group in restore_o:
                    p1_groups.append(group)
                for group in restore_x:
                    p2_groups.append(group)
    if (player1_pass == 1) & (player2_pass == 1):
        gameover = 1
 
## Start game
def main():
    global whoseturn
    global notwhoseturn
    ## Game State Current, the current layout of the board
    global gsc
    global gameover
    ## Game State Future, same setup as gsc, used for testing 
    global gsf
    global p1_groups
    global p2_groups
    ## Groups of empty positions
    global non_groups
    ## String containing all the game states encountered in a particular game
    global gscache
    ## 0 or 1, for whether the player has passed their turn or not
    global player1_pass
    global player2_pass
    global p1_points
    global p2_points
 
    ## Creates blank board
    gsc = initialize()
    gsf = initialize()
    ## Initialize values
    p1_groups = []
    p2_groups = []
    player1_pass = 0
    player2_pass = 0
    p1_points = 0
    p2_points = 0
    gameover = 0
    non_groups = []
    gscache = ''
 
    while gameover != 1:
 
        ## Player 1's turn
        whoseturn = 'p1'
        notwhoseturn = 'p2'
        printboard(gsc)
        turn()

        if gameover == 1:
            break
 
        ## Player 2's turn
        whoseturn = 'p2'
        notwhoseturn = 'p1'
        printboard(gsc)
        turn()
 
    ## Counts the score of both players
    scoreCount()
    print('\nFinal board state:\n')
    printboard(gsc)
    print('\n')
    print('Player 1 points: ' + str(p1_points))
    print('Player 2 points: ' + str(p2_points))
    ## Determines the winner
    if p1_points > p2_points:
        print('\nPlayer 1 wins\n')
    elif p2_points > p1_points:
        print('\nPlayer 2 wins\n')
    else:
        print('\nGame tied\n')
 
## make new game
while gameCont:
    main()
    cont = True
    while cont:
        newGame = raw_input('New game (y/n)? ')
        if newGame == 'n':
            gameCont = False
            cont = False
        elif newGame == 'y':
            cont = False
        else:
            print('Invalid input')