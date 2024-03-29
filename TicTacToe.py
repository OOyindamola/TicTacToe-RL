from random import random as ra

rng = [0,1,2]


def check_move(s, a):
    i,j,k = a[0],a[1],a[2]
    parity = sum([sum(s[i]) for i in rng]) * -2 + 1
    if not k==parity:
        return False
    if i not in rng or j not in rng or not s[i][j]==0:
        return False
    return True

def sim_move(s,a):
    k = [[s[i][j] for j in rng] for i in rng]
    k[a[0]][a[1]] = a[2]
    return check_win()

def eq(s,k):
    for i in rng:
        for j in rng:
            if s[i][j] != k[i][j]:
                return False
    return True

def move(s,a):
    k = [[s[i][j] for j in rng] for i in rng]
    k[a[0]][a[1]] = a[2]
    return k

def check_win(board):
    vert = [0 for i in rng]
    hori = [0 for i in rng]
    diag = [0, 0]
    for i in rng:
        for j in rng:
            vert[i] = vert[i] + board[i][j]
            hori[j] = hori[j] + board[i][j]
            x = board[i][j] if i==j else 0
            diag[0] = diag[0] + x
            y = board[i][j] if i + j == 2 else 0
            diag[1] = diag[1] + y

    for v in vert:
        if v ==3 or v == -3:
            return v/3
    for h in hori:
        if h == 3 or h == -3:
            return h/3
    for d in diag:
        if d == 3 or d == -3:
            return d/3
    return 0


check_win([[1, 0, 0], [0, 0, 0], [0, 0, -1]])

def get_blank():
    return [[0 for i in rng] for j in rng]

def board_tuple(board):
    return tuple([tuple(b) for b in board])

def board_string(b):
    ans = ''
    for i in rng:
        for j in rng:
            ans = ans + str(b[i][j]+1)
    return ans

def string_board(s):
    return [[int(s[3*i+j])-1 for j in rng] for i in rng]

def flip(board):
    return [[board[j][i] for j in rng] for i in rng]

def rot(board):
    ans = [[0 for i in rng] for j in rng]
    ans[0][0] = board[2][0]
    ans[2][0] = board[2][2]
    ans[2][2] = board[0][2]
    ans[0][2] = board[0][0]

    ans[0][1] = board[1][0]
    ans[1][0] = board[2][1]
    ans[2][1] = board[1][2]
    ans[1][2] = board[0][1]

    ans[1][1] = board[1][1]

    return ans

def iso_list(inp):
    b = [[inp[i][j] for j in rng] for i in rng]
    K = flip(b)
    X = [b,rot(b),rot(rot(b)),rot(rot(rot(b))), K,rot(K),rot(rot(K)),rot(rot(rot(K)))]
    return [board_string(x) for x in X]

S = []
def any_iso_in_list(b):
    for board in iso_list(b):
        if board in S:
            return True
    return False


def iso_reduce(s):
    X = iso_list(s)
    for x in X:
        if x in S:
            return x
    print(s)
    print(len(S))
    return 'error'

def get_candidates(s,k):
    cands = []
    for i in rng:
        for j in rng:
            if check_move(s,(i,j,k)):
                cands.append((i,j,k))
    return cands 


def get_S():
    return gen_S(get_blank(), 1)

def gen_S(board,k):
    if any_iso_in_list(board):
        return []
    if check_win(board) != 0:
        S.append(board_string(board))
        return

    S.append(board_string(board))
    
    Cs = get_candidates(board,k)
    mvs = [move(board,a) for a in Cs]

    for m in mvs:
        gen_S(m,k*-1)
    return S#[board_string(board)] + S

def get_A():
    return [(i,j,1) for i in rng for j in rng]

def get_start():
    return board_string(get_blank())

A = [(i,j,k) for i in rng for j in rng for k in [-1,1]]
A = [(i,j) for i in rng for j in rng]

def strat_rand(s,k):
    board = [[s[i][j]*k for j in rng] for i in rng]
    return ( int(ra()*3), int(ra()*3), k )

def strat_rand_legal(s,k):
    cands = get_candidates(s,k)
    l = len(cands)
    if l==0:
        return 'error'
    return cands[int(ra()*l)]


def has_win(s,k):
    Cs = get_candidates(s,k)
    mvs = [move(s,a) for a in Cs]
    mv_rng = range(len(mvs))
    
    #check win
    for i in mv_rng:
        if check_win(mvs[i])*k > 0:
            return Cs[i]

    return ''


def strat_optimal(s,k):
    Cs = get_candidates(s,k)
    mvs = [move(s,a) for a in Cs]
    mv_rng = range(len(mvs))

    a = has_win(s,k)
    if not a=='':
        return a
    
    for i in mv_rng:
        if has_win(mvs[i],-1*k)=='':
            return Cs[i]
    return strat_rand_legal(s,k)


def full(s):
    for c in s:
        if c=='1':
            return False
    return True


def build_P(strat=strat_rand_legal):
    def P(s,a):
        sb, bs, h = string_board, board_string, iso_reduce
        
        ss = s
        s = sb(s)
        x = check_win(s)
        if not x==0:
            return h(s),x

        if full(ss):
            return h(s),0

        i,j,k = a[0], a[1], a[2]
        if not check_move(s,a):
            return h(s),-1*k
        
        s[i][j] = k
        x = check_win(s)
        if not x==0:
            return h(s),x*10
        
        r,count = 0,0
        while not check_move(s,a) and count < 100: 
            mv = strat(s,k*-1)
            if mv=='error':
                return h(s),0 
            count = count + 1
            r = r + -1*k

        if count > 99:
            return h([[1,1,1] for i in rng]), r
        s = move(s, mv)
        
        x = check_win(s)
        if not x==0:
            return h(s),x*10
       
        return h(s),r

    return P




