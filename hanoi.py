import models
from models import Tower, Move

move = Move()

def Hanoi(A, B, C, n):
    STACK = []
    STACK.insert(0, [A, B, C, n])

    while STACK and not models.RESET:
        data = STACK.pop(0)
        A, B, C, n = data
 
        if n == 1:
            move.run(A, C)
        else:
            STACK.insert(0, [B, A, C, n-1])
            STACK.insert(0, [A, B, C, 1])
            STACK.insert(0, [A, C, B, n-1])


def ExHanoi(A: Tower, B: Tower, C: Tower, n):
    if n == 1 and not models.RESET:
        move.run(C, B)
        move.run(A, C)
        move.run(B, A)
        move.run(B, C)
        move.run(A, C)
    elif not models.RESET:
        ExHanoi(A, B, C, n-1)
        Hanoi(C, A, B, 3*n - 2)
        move.run(A, C)
        Hanoi(B, A, C, 3*n - 1)
