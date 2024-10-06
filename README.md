# WiFi 大师 | WiFi Guru | WiFi Гуру

---

## 🌐 简介 | Introduction | Введение

**WiFi 大师** 是一个强大的工具，旨在帮助用户扫描和连接 WiFi 网络。请注意，本工具仅供学习和交流使用，禁止用于任何非法用途。

**WiFi Guru** is a powerful tool designed to help users scan and connect to WiFi networks. Please note that this tool is for educational and communication purposes only and should not be used for any illegal activities.

**WiFi Гуру** — это мощный инструмент, предназначенный для помощи пользователям в сканировании и подключении к WiFi-сетям. Обратите внимание, что этот инструмент предназначен только для образовательных и коммуникационных целей и не должен использоваться для каких-либо незаконных действий.

---

## 📜 功能 | Features | Функции

- 扫描附近的 WiFi 网络
- 自动连接到已知网络
- 支持暴力破解 WiFi 密码
- 生成密码字典文件

- Scan nearby WiFi networks
- Automatically connect to known networks
- Support brute force WiFi password cracking
- Generate password dictionary files

- Сканирование ближайших WiFi-сетей
- Автоматическое подключение к известным сетям
- Поддержка взлома паролей WiFi методом перебора
- Генерация файлов словарей паролей

---

## 🚀 快速开始 | Quick Start | Быстрый старт

1. 克隆此仓库
2. 安装所需的 Python 库
3. 运行 `WiFi大师.py`

1. Clone this repository
2. Install the required Python libraries
3. Run `WiFi大师.py`

1. Клонируйте этот репозиторий
2. Установите необходимые библиотеки Python
3. Запустите `WiFi大师.py`

---

## 🎮 互动小游戏 | Interactive Game | Интерактивная игра

在这里，我们为您准备了一个简单的“围住小猫”游戏！尝试在小猫逃跑之前围住它。

Here, we have prepared a simple "Trap the Cat" game for you! Try to trap the cat before it escapes.

Здесь мы подготовили для вас простую игру "Поймай кота"! Попробуйте поймать кота, прежде чем он убежит.

```python
import random

def trap_the_cat():
    grid_size = 5
    cat_position = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]
    traps = []

    print("欢迎来到围住小猫游戏！")
    print("Welcome to the Trap the Cat Game!")
    print("Добро пожаловать в игру Поймай кота!")

    while True:
        print(f"当前小猫位置: {cat_position}")
        trap = input("请输入你想放置陷阱的位置 (格式: x,y): ")
        try:
            x, y = map(int, trap.split(','))
            if [x, y] in traps:
                print("该位置已经有陷阱，请选择其他位置。")
                continue
            traps.append([x, y])
            if cat_position in traps:
                print("恭喜你！你成功围住了小猫！")
                break
            else:
                # 随机移动小猫
                cat_position[0] = (cat_position[0] + random.choice([-1, 0, 1])) % grid_size
                cat_position[1] = (cat_position[1] + random.choice([-1, 0, 1])) % grid_size
        except ValueError:
            print("请输入有效的位置格式。")

if __name__ == "__main__":
    trap_the_cat()
````

---

## 📧 联系方式 | Contact | Контакты

- 作者：无氪（wuke）
- 联系邮箱：wuke15279888684@gmail.com
- 项目仓库：[GitHub](https://github.com/HonkerWuKe/WiFi__GURU)

- Author: Wuke
- Contact Email: wuke15279888684@gmail.com
- Project Repository: [GitHub](https://github.com/HonkerWuKe/WiFi__GURU)

- Автор: Wuke
- Контактный Email: wuke15279888684@gmail.com
- Репозиторий проекта: [GitHub](https://github.com/HonkerWuKe/WiFi__GURU)

---

## ⚠️ 免责声明 | Disclaimer | Отказ от ответственности

### 中文

本工具仅供学习交流，请勿用于非法用途，否则后果自负。使用本工具可能违反当地法律法规，用户需自行承担使用本工具所带来的任何法律责任。开发者不对因使用本工具而导致的任何直接或间接损害负责。用户在使用本工具时，需确保其行为符合所在国家或地区的法律法规。任何因使用本工具而导致的法律问题，均与开发者无关。

### English

This tool is for educational and communication purposes only and should not be used for any illegal activities. Using this tool may violate local laws and regulations, and users are solely responsible for any legal liabilities arising from the use of this tool. The developer is not responsible for any direct or indirect damages caused by the use of this tool. Users must ensure that their actions comply with the laws and regulations of their country or region. Any legal issues arising from the use of this tool are not the responsibility of the developer.

### Русский

Этот инструмент предназначен только для образовательных и коммуникационных целей и не должен использоваться для каких-либо незаконных действий. Использование этого инструмента может нарушать местные законы и правила, и пользователи несут полную ответственность за любые юридические обязательства, возникающие в результате использования этого инструмента. Разработчик не несет ответственности за любые прямые или косвенные убытки, вызванные использованием этого инструмента. Пользователи должны убедиться, что их действия соответствуют законам и правилам их страны или региона. Любые юридические проблемы, возникающие в результате использования этого инструмента, не являются ответственностью разработчика.
