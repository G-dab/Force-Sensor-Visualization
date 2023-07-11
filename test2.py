'''
根据力传感器传来的数据进行绘图
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
# 中文支持
plt.rcParams['font.family'] = "SimHei"
plt.rcParams['axes.unicode_minus'] = False
# ==================== 力传感器 ====================
ser = serial.Serial("COM10", 9600)   # 选择串口，并设置波特率
# 指令帧
cmd_force = '01 03 00 50 00 02 C4 1A'
cmd_zero = '01 10 00 5E 00 01 02 00 01 6A EE'

def read_force():
    if ser.is_open:
        print("Serial Port open success")
        # hex(16进制)转换为bytes(2进制)
        send_data = cmd_force
        send_data_byte = bytes.fromhex(send_data)
        print("发送的数据:",send_data)
        ser.write(send_data_byte)   # 发送命令
        time.sleep(0.1)        # 延时，否则len_return_data将返回0，此处易忽视！！！
        len_return_data = ser.inWaiting()  # 获取缓冲数据（接收数据）长度

        if len_return_data:
            return_data = ser.read(len_return_data)  # 读取缓冲数据
            # bytes(2进制)转换为hex(16进制)
            return_data_hex = str(return_data.hex())
            return_data_hex_format = ' '.join([return_data_hex[i:i+2] for i in range(0, len(return_data_hex), 2)]) # 格式化字符串, 每两个字符加一个空格
            print("返回的数据:",return_data_hex_format)
            # 判断是拉力还是压力 (第4,5位是FF FF则是拉力，00 00则是压力)
            if return_data_hex[6:10] == 'ffff':
                force = int(return_data_hex[10:14], 16)
                print("拉力：", force)
                return force
            elif return_data_hex[6:10] == '0000':
                force = int(return_data_hex[10:14], 16)
                print("压力：", force)
                return force
            else:
                print("数据错误")
        else:
            print("No data received")
    else:
        print("Serial Port open failed")
# ==================== 动态图绘制 ====================
# 设置画布
def set_canvas():
    fig, ax = plt.subplots()
    ax.set_title('力传感器动态曲线',fontsize=17)
    ax.set_xlabel(r'$x/s$', fontsize=15)
    ax.set_ylabel(r'$y/a.u.$', fontsize=15)
    x_max = 10
    y_max = 10000
    ax.set_xlim(0, x_max) # 设置x轴的范围
    ax.set_ylim(-100, y_max) # 设置y轴的范围
    line, = ax.plot([], [])
    return fig, ax, line, x_max, y_max


def update(t, ax, line, x_max):
    # 读取力传感器数据
    force = read_force()
    # 将数据放入数组
    global data_force
    data_force = np.insert(data_force, 0, force)
    data_force = data_force[:-1]
    print(data_force)
    # 画图
    line.set_data(np.arange(0, size, 1), data_force)
    # # 更新x轴范围
    # ax.set_xlim(t, t + x_max)
    # # 更新y轴范围
    # # ax.set_ylim(-100, y_max)
    # # 更新x轴刻度
    # ax.set_xticks(np.arange(t, t + x_max, 1))
    # 更新x轴刻度标签
    ax.set_xticklabels(np.arange(t, t + x_max, interval))
    # # 更新y轴刻度
    # ax.set_yticks(np.arange(0, y_max, 10))
    # # 更新y轴刻度标签
    # ax.set_yticklabels(np.arange(0, y_max, 10))




if __name__ == '__main__':
    now = 0 # 当前时间
    interval = 0.1 # 每隔0.1s获取一次数据

    fig, ax, line, x_max, y_max = set_canvas()

    size = x_max # 数据个数
    global data_force
    data_force = np.zeros(int(size)) # 存放力传感器数据

    # 创建动画
    # - frames 总共帧数
    # - interval 每帧间隔时间(ms)
    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 100), interval=interval * 1000, fargs=(ax, line, x_max))
    plt.show()


