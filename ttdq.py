import random as ra
from display import display2
import numpy as np
import TicTacToe as ttt

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
    
    QA = Q[0]
    while True:
        s = input()
        s = ttt.iso_reduce(ttt.string_board(s))
        print(s)
        Q_disp = {a: QA[(s,a)] for a in A}
        print(Q_disp)

    print('\n--------------\n\nQ0:')
    print(Q[0])
    #Qdisp(Q[0])
    print('\nQ1')
    print(Q[1])
    #Qdisp(Q[1])
    QAB = { (ss,aa): Q[0][(ss,aa)] + Q[1][(ss,aa)] for aa in A for ss in SS }
    print('\n')
    print({ss:Q_select(QAB, ss) for ss in S})
    input()



P = ttt.build_P()
DQ(P, ttt.get_start(), DoubleQ=True)
DQ(P, ttt.get_start(), DoubleQ=False)


