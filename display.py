

def round(x, d):
    p = pow(10,d)
    return int( x*p + .5 ) / p


def display2(V, fun=round):
    count = 0
    S = [V[(7-i) * 8 : (8-i)*8 ]  for i in range(8)]

    ans = ''

    for s in S:
        out = ''
        for v in s:
            out = out + '{} {} '.format(fun(v,1), '&')
        ans = ans + out[:-2] + '\\\\ \n'

    print(ans[:-4])

base_string ='''
    |    | 
  {} | {}  | {} 
----------------
    |    | 
  {} | {}  | {}
-----------------
    |    | 
  {} | {}  | {} 

'''
char_map = {'0':'O', '2':'X', '1':' '}
def ttt_disp(board_string):
    a = [char_map[c] for c in board_string]
    return base_string.format(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8])


