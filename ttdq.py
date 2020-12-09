import random as ra
from display import display2
import numpy as np
import TicTacToe as ttt
from display import ttt_disp

GAMMA = float(input())

S = ttt.get_S()
SS = S
A = ttt.get_A()
AA = A

def check_gameover(s):
    x = (not ttt.check_win(ttt.string_board(s)) == 0)
    if x:
        return x
    for c in s:
        if c=='1':
            return False
    return True


def Q_determine(pi):
    X = [ Q_select(pi,s) for s in S]
    return X

def Qdisp(Q):
    display2([Q[(s,Q_select(Q,s))] for s in S])

def Q_select( Q, s ):
    x = ra.random()
    if x < .5:
        return A[int(ra.random()*len(A))]
    
    maxv=-999999
    maxa='error'
    for a in AA:
        x = Q[(s,a)]
        if x > maxv:
            maxv = x
            maxa = a
    return maxa

def mat_print(Q,k):
    if k == -1:
        return
    ans = ''
    rng = range(3)
    for i in rng:
        for j in rng:
            x = Q[(i,j,k)]
            x = int( x * 100 ) / 100
            ans = ans + str(x) + "&"
        ans = ans[:-1] + '\\\\'
    print(ans[:-2])


def DQ(P, s0, rate=1, DoubleQ=True):
    NSA = {(s,a):0 for s in SS for a in A}
    Q = [{ (s,a):0 for s in SS for a in A },{ (s,a):0 for s in SS for a in A }] 
    for i in range(2000):
        if i % 1000 == 0:
            print(i)
        s = s0
        gameover  = False
        gameover2 = False
        while not gameover:            
            x = int(ra.random()*2) % 2
            x = x * (1 if DoubleQ else 0)
            QA, QB = Q[x], Q[1-x]
            QAB = { (s,a): Q[0][(s,a)] + Q[1][(s,a)] for a in AA }
        
            a = Q_select( QAB if DoubleQ else QA, s )
            
            s2,r = P(s,a)

            #NSA[(s,a)] = NSA[(s,a)] + 1
            #rate = 1/ pow(NSA[(s,a)], .8)

            gameover = check_gameover(s2)
            
            a_star = Q_select(QA, s2)
            if DoubleQ:
                QB = QA

            QA[(s,a)] = QA[(s,a)] + rate * (r + GAMMA*QB[(s2,a_star)] - QA[(s,a)])

            s = s2
    
    return Q


def query(Q):
    QA = Q[0]
    while True:
        s = input()
        s = ttt.iso_reduce(ttt.string_board(s))
        print(s)
        print('\n' + ttt_disp(s) + '\n')
        Q_disp = {a: QA[(s,a)] for a in A}
        Q_disp2= [QA[(s,a)] for a in A]
        mat_print(Q_disp,1)
        b = ttt.string_board(s)


def play(Q):    
    QA = Q[0]
    gg = False
    s = '111111111'
    k = 1
    while not gg:
        s = ttt.iso_reduce(ttt.string_board(s))
        print(s)
        print('\n' + ttt_disp(s) + '\n')
        Q_disp = {a: QA[(s,a)] for a in A}
        Q_disp2= [QA[(s,a)] for a in A]
        mat_print(Q_disp,k)
        b = ttt.string_board(s)

        if k==1:
            i,j = int(input()), int(input()) 
        else:
            a = ttt.strat_optimal(ttt.string_board(s),k)
            i,j = a[0],a[1]
            print(a)

        new_s = ttt.string_board(s)
        new_s[i][j] = k
        s = ttt.iso_reduce(new_s)
        k = k*-1

        gg = (i==-1)




P = ttt.build_P(ttt.strat_rand)
Q_double = DQ(P, ttt.get_start(), DoubleQ=True, rate=.5)
#Q = DQ(P, ttt.get_start(), DoubleQ=False, rate = .5)

#play(Q_double)
query(Q_double)

# x|_|_
# _|x|o
#  | |o

[ [0,0,0],[-1,1,0],[0,0,0] ]
'111 021 111'
'100 121 211'
'211 120 110'



