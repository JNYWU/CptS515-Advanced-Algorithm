from pyeda.inter import *

prime_number = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

# 32 nodes == 2^5, we need u and v to mark R(u,v)
U = bddvars('u', 5)
V = bddvars('v', 5)

# R[i][j] stores the edges from i to j
R = [[0 for i in range(32)] for j in range(32)]

# strings to store the truthtable values
R_truth = ""
even_truth = ""
prime_truth = ""

# if there is an edge from i to j, R[i][j] = 1
for i in range(32):
    for j in range(32):
        
        # if the condition is satisfied, there is an edge
        if ((i + 3) % 32 == j % 32) | ((i + 8) % 32 == j % 32):
            R[i][j] = 1
        
        # set up the truthtable value for the graph
        R_truth = R_truth + str(R[i][j])
            
    # even numbers
    if (i % 2 == 0):
        even_truth = even_truth + "1"
    else:
        even_truth = even_truth + "0"
        
    # prime numbers
    if i in prime_number:
        prime_truth = prime_truth + "1"
    else:
        prime_truth = prime_truth + "0"

# the truthtable of R(u,v)
G = [U[0], U[1], U[2], U[3], U[4], V[0], V[1], V[2], V[3], V[4]]
table_G = truthtable(G, R_truth)
expr_G = truthtable2expr(table_G)

# BDD of R
bdd_G = expr2bdd(expr_G)

# BDD of [even]
table_even = truthtable(U, even_truth)
expr_even = truthtable2expr(table_even)
bdd_even = expr2bdd(expr_even)

# BDD of [prime]
table_prime = truthtable(U, prime_truth)
expr_prime = truthtable2expr(table_prime)
bdd_prime = expr2bdd(expr_prime)

# function for EFp
def EF(G, p):
    Hk = p
    while True:
        
        H = Hk.compose({U[0]:V[0], U[1]:V[1], U[2]:V[2], U[3]:V[3], U[4]:V[4]})
        Ht = (H & G).smoothing(V) | Hk
        
        if Hk == Ht:
            break
        Hk = Ht
        
    return Hk

# function for EGp
def EG(G, p):
    Hk = p
    while True:
        H = Hk.compose({U[0]:V[0], U[1]:V[1], U[2]:V[2], U[3]:V[3], U[4]:V[4]})
        Ht = (H & G).smoothing(V) & p
        
        if Hk == Ht:
            break
        Hk = Ht
        
    return Hk

# EG(even & EF(prime))
# = a set of nodes s where there is a path from s 
# that all the nodes on the path is even, and from at least one of the even numbers
# there is a path to a prime number
ans = EG(bdd_G, (bdd_even & EF(bdd_G, bdd_prime)))

print(list(ans.satisfy_all()))
# we get [{u[0]: 0}], which is the set of all even nodes
