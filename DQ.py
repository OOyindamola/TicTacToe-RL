import random as ra
from display import display2


Act = {'u': (0,1), 'd': (0,-1), 'l': (-1,0), 'r': (1,0)}
A = 'udlr'
size = 8
rng = range(size)
GAMMA = float(input())

S = [ (j,i) for i in rng for j in rng ]


def act(s,a):
    return tuple( [s[i] + Act[a][i] for i in range(len(s))] )


def build_P(R):
    def P(s,a):
        if s == (0,7):
            return (0,7),0
        if s == (2,7):
            return (6,4),-3
        if s == (3,4):
            return (0,7),15
        if s == (5,0):
            return (2,3),R
        
        new_s = act(s,a)
        for ss in new_s:
            if ss<0 or ss >= size:
                return s,-1

        if new_s == (0,7):
            return new_s,10
        
        return new_s,-.5
    
    return P


def hlp(s,a):
    new_s = act(s,a) 
    for ss in new_s:
        if ss<0 or ss >= size:
            return 0
    return 1

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

    maxv=-999999
    maxa='error'
    for a in A:
        x = Q[(s,a)]
        if x > maxv:
            maxv = x
            maxa = a
    return maxa


def DQ(P, s0=(0,0), rate=.5):
    Q = [{ (s,a):0 for s in S for a in A },{ (s,a):0 for s in S for a in A }]
    s = s0

    count = 0
    while True:
        if s==(0,7):
            s = (0,0)
        count = count+1

        QAB = { (s,a): Q[0][(s,a)] + Q[1][(s,a)] for a in A }
        a = Q_select( QAB, s )
        
        print(s)
        print(a)

        s2,r = P(s,a)

        x = int(ra.random()*2) % 2
        QA, QB = Q[x], Q[1-x]

        a_star = Q_select(QA, s2)
        QA[(s,a)] = QA[(s,a)] + rate * (r + GAMMA*QB[(s2,a_star)] - QA[(s,a)])

        s = s2

        if count % 1 == 0:
            Qdisp(Q[0])
            print('\n')
            Qdisp(Q[1])
            input() 

P = build_P(0)
DQ(P)
