from shake128lib import *
import random

def floyd(f, x_0):
    """ f : X -> X """
    s, T, H = 1, f(x_0), f(f(x_0))
    while H != T:
        s, T, H = s+1, f(T), f(f(H))
    T_1, T_2 = T, x_0
    T_1_, T_2_ = f(T_1), f(T_2)
    while T_1_ != T_2_:
        T_1, T_2 = T_1_, T_2_
        T_1_, T_2_ = f(T_1), f(T_2)
    return T_1,T_2

def multi_floyd(N):
    def f(x):
        return shake128(x, len(x))

    d = N*8
    print("rbits")
    for i in range(2**d):
        if i%16 == 0:
            print(i)
        seed = bin(i)[2:].zfill(d)
        T_1, T_2 = floyd(f, seed)
        write_bitstring_to_file(T_1, "./collisions-{}/ex-{}.A".format(d//8, i))
        write_bitstring_to_file(T_2, "./collisions-{}/ex-{}.B".format(d//8, i))
    return


def brute_force(N):
    d = 8*N
    int_of_hash = {}
    c = 0
    for i in range(2**d):
        if i%32 == 0:
            print(f"{i}/{2**d}")
            # print(int_of_hash)
        h = shake128(bin(i)[2:].zfill(d),d)
        if h not in int_of_hash:
            int_of_hash[h] = i
        else:
            j = int_of_hash[h]
            write_bitstring_to_file(bin(i)[2:].zfill(d), "./collisions-{}/ex-{}.A".format(N,c))
            write_bitstring_to_file(bin(j)[2:].zfill(d), "./collisions-{}/ex-{}.B".format(N,c))
            c = c +1
    return


def main():
    brute_force(3)
    return

main()
