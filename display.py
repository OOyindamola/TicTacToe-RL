

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

