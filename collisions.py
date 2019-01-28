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
            print("{}/{}".format(i,2**d))
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


def mail_address(N, d):
    s = "pierre.tholoniat@polytechnique.edu"
    mail = "0000111010010110101001100100111001001110101001100111010000101110000101101111011000110110111101100111011010010110100001100010111000000010000011101111011000110110100111100010111010100110110001100001011001110110100101101000111010101110101001100111010010100110001001101010111001010000"
    hash_t = {}
    hash_t[shake128(mail, 8*N)] = ""
    c = 0
    for i in range(2**(8*d)):
        if i%32 == 0:
            print(f"{i}/{2**(8*d)}")
            # print(hash_t)
        suffix = bin(i)[2:].zfill(8*d)
        h = shake128(mail + suffix,8*N)
        if h not in hash_t:
            hash_t[h] = suffix
        else:
            write_bitstring_to_file(mail + suffix, f"./collisions-mail-{N}/ex-{c}.A")
            write_bitstring_to_file(mail + hash_t[h], f"./collisions-mail-{N}/ex-{c}.B")
            c = c + 1
    return


def main():
    N = int(sys.argv[1])
    if N == 4:
        brute_force(4)
    if N == 5:
        brute_force(5)
    if N == -3:
        mail_address(3,5)
    if N == -4:
        mail_address(4,5)
    return

main()
