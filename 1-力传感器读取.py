'''
力传感器数据读取测试
单位: g

'''
import serial
import time

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
                # print("拉力：", return_data_hex[10:14])
                print("拉力：", int(return_data_hex[10:14], 16)-65535) #!补码转换
            elif return_data_hex[6:10] == '0000':
                # print("压力：", return_data_hex[10:14])
                print("压力：", int(return_data_hex[10:14], 16))
            else:
                print("数据错误")

        else:
            print("No data received")
    else:
        print("Serial Port open failed")

def set_zero():
    if ser.is_open:
        print("Serial Port open success")
        # hex(16进制)转换为bytes(2进制)
        send_data = cmd_zero
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
            if return_data_hex_format == '01 10 00 5e 00 01 60 1b':
                print("手动置零成功")
            else:
                print("手动置零失败")
        else:
            print("No data received")
    else:
        print("Serial Port open failed")
if __name__ == "__main__":
    
    print("==================== 手动置零 ====================")
    set_zero()
    print("==================== 读取数据 ====================")
    read_force()
    time.sleep(0.5)
    while True:
        read_force()
        time.sleep(0.5)