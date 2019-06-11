import sys
sys.path.append('./LightModule')
# print(sys.path)

from lightingFunction import *

# from fileManager import *

def main():
    # lx,Kをintの整数値で整理する(judegする時に楽)
    lx = 0
    K = 7
    # lxはstr型，tempはintで使用する
    print("-----")
    sig,ill,temp = getSignal(lx,K)
    lighting(sig)

if __name__ == '__main__':
    main()