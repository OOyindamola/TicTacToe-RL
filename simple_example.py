import random as ra
from display import display2
import numpy as np


GAMMA = float(input())

S = ['A', 'B', 'C', 'D']
SS = ['A', 'C', 'D']
A = ['l', 'r']
BAs = range(10)

def Build_MDP():

    def P(s,a):
        if s=='A':
            if a=='l':
                return 'B', 0
            if a=='r':
                return 'C', 0
        if s=='B':
            return 'D', np.random.normal(loc=-.5, scale=1)
        if s=='C':
            return 'OVER',0
        if s=='D':
            return 'OVER',0
    
    return P


def Q_determine(pi):
    X = [ Q_select(pi,s) for s in S]
    return X

def Qdisp(Q):
    display2([Q[(s,Q_select(Q,s))] for s in S])

def Q_select( Q, s ):
    AA = A
    if s=='B':
        AA = BAs

    x = ra.random()
    if x < .5:
        return AA[int(ra.random()*len(AA))]
    
    maxv=-999999
    maxa='error'
    for a in AA:
        x = Q[(s,a)]
        if x > maxv:
            maxv = x
            maxa = a
    return maxa

def DQ(P, s0='A', rate=.1, DoubleQ=True):
    NSA = {(s,a):0 for s in SS for a in A}
    Q = [{ (s,a):0 for s in SS for a in A },{ (s,a):0 for s in SS for a in A }] 
    for b in BAs:
        NSA[('B',b)] = 0
        Q[0][('B',b)] = 0
        Q[1][('B',b)] = 0
    for i in range(100):
        s = s0
        gameover = False
        while not gameover:
            
            x = int(ra.random()*2) % 2
            x = x * (1 if DoubleQ else 0)
            QA, QB = Q[x], Q[1-x]
            
            AA = A
            if s=='B':
                AA = BAs
            QAB = { (s,a): Q[0][(s,a)] + Q[1][(s,a)] for a in AA }
        
            a = Q_select( QAB if DoubleQ else QA, s )
            
            #a = Q_select(QB, s)
            s2,r = P(s,a)
            
            NSA[(s,a)] = NSA[(s,a)] + 1
            rate = 1/ pow(NSA[(s,a)], .8)

            gameover = (s2=='C' or s2=='D')
            


            a_star = Q_select(QA, s2)
            if DoubleQ:
                QB = QA

            QA[(s,a)] = QA[(s,a)] + rate * (r + GAMMA*QB[(s2,a_star)] - QA[(s,a)])

            s = s2

        
    print('\n--------------\n\nQ0:')
    print(Q[0])
    #Qdisp(Q[0])
    print('\nQ1')
    print(Q[1])
    #Qdisp(Q[1])
    QAB = { (ss,aa): Q[0][(ss,aa)] + Q[1][(ss,aa)] for aa in A for ss in SS }
    for b in BAs:
        QAB[('B',b)] = Q[0][('B',b)] + Q[1][('B',b)]
    print('\n')
    print({ss:Q_select(QAB, ss) for ss in S})
    input()



#P = Build_MDP()
#DQ(P, 'A', DoubleQ=True)
#DQ(P, 'A', DoubleQ=False)


