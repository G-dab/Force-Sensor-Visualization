# 十进制转为二进制补码
def to_twos_complement(num):
    if num >= 0:
        return bin(num)[2:].zfill(8)  # 正数的原码即为补码
    else:
        inverted = bin(-num - 1)[2:].zfill(8)  # 取反
        return ''.join('1' if b == '0' else '0' for b in inverted)  # 加1得到补码

if __name__ == "__main__":
    print(to_twos_complement(1)) # 00000001
    print(to_twos_complement(2)) # 00000010
    print(to_twos_complement(-1)) # 11111111
    print(to_twos_complement(-2)) # 11111110
    s = "fffe"  # 十六进制补码表示的负数-2
    n = int(s, 16)  # 将字符串转换为整数
    n = n-65535
    print(n)