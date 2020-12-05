import random as ra
from display import display2
import numpy as np


GAMMA = float(input())

S = ['A', 'B', 'C', 'D']
A = ['l', 'r']


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


def no_pol(s,a):
    return 1

def p1(s,a,A):
    tot = 0
    for As in A:
        tot = tot + hlp(s,As)
    tot = 1/tot

    return hlp(s,a)*tot

def get_blank_pol():
    return {s:'u' for s in S}

def get_blank_pol2():
    return {s:1 for s in S}

def const_pol_hlp(c,s):
    new_s = act(s,c)
    for ss in new_s:
        if ss<0 or ss >= size:
            return 0
    return 1

def const_pol(c):
    def pol(s,a,A):
        ans = 1 if a==c else 0
        return ans * const_pol_hlp(c,s)
    return pol

def determine(pi):
    X = [ rand_select(pi,s) for s in S ]
    return X

def Q_determine(pi):
    X = [ Q_select(pi,s) for s in S ]
    return X

def Qdisp(Q):
    display2([Q[(s,Q_select(Q,s))] for s in S])

def Q_select( Q, s ):
    x = ra.random()
    if x < .5:
        return A[int(ra.random()*len(A))]
    
    maxv=-999999
    maxa='error'
    for a in A:
        x = Q[(s,a)]
        if x > maxv:
            maxv = x
            maxa = a
    return maxa


def DQ(P, s0=(0,0), rate=.8):
    NSA = {(s,a):0 for s in S for a in A}
    Q = [{ (s,a):0 for s in S for a in A },{ (s,a):0 for s in S for a in A }] 
    for i in range(10000):
        s = s0
        gameover = False
        while not gameover:
            QAB = { (s,a): Q[0][(s,a)] + Q[1][(s,a)] for a in A }
            a = Q_select( QAB, s )
            
            x = int(ra.random()*2) % 2
            QA, QB = Q[x], Q[1-x]
            
            #a = Q_select(QB, s)
            s2,r = P(s,a)
            
            NSA[(s,a)] = NSA[(s,a)] + 1
            rate = 1/ np.pow(NSA[(s,a)], .8)

            gameover = (s2=='C' or s2=='D')
            


            a_star = Q_select(QA, s2)
            QA[(s,a)] = QA[(s,a)] + rate * (r + GAMMA*QB[(s2,a_star)] - QA[(s,a)])

            s = s2

        
    print('\n--------------\n\nQ0:')
    print(Q[0])
    #Qdisp(Q[0])
    print('\nQ1')
    print(Q[1])
    #Qdisp(Q[1])
    QAB = { (ss,aa): Q[0][(ss,aa)] + Q[1][(ss,aa)] for aa in A for ss in S }
    print('\n')
    print({ss:Q_select(QAB, ss) for ss in S})
    input()



P = Build_MDP()
DQ(P, 'A')
