# Bemfa-miot

米家 IOT 巴法云接入

## 背景

米家关闭了个人开发者的通道，导致个人开发者，极客无法自己开发将自己的设备接入米家，[巴法云](https://cloud.bemfa.com/) 提供了平台，可以通过接入巴法云来间接接入米家。

## 说明

本项目设计上是运行在树莓派等家庭服务器上，作为一个 IOT 网关，米家的控制指令下发到巴法云，然后通过 MQTT 协议下发到树莓派，树莓派再将指令转发到实际的设备上。

## 配置

在根目录增加 `config.py` 文件，内容如下：

```python
# -*- coding: utf-8 -*-

HOST = "bemfa.com"
PORT = 9501
CLIENT_ID = "your client id"   # Replace with your MQTT client ID
PROJECTOR_BT_ADDRESS = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # Replace with your projector's Bluetooth address
```

这里需要修改的有:

- `CLIENT_ID`: 可以在 [巴法云](https://cloud.bemfa.com/) 上注册账号，创建一个应用，获取 `CLIENT_ID`。
- `PROJECTOR_BT_ADDRESS`: 需要替换为你的投影仪的蓝牙 mac 地址，可以通过手机蓝牙设置查看。

## 巴法云配置

在 [巴法云](https://cloud.bemfa.com/) 添加主题，目前支持的主题如下：

| 主题                  | 说明                                            |
| --------------------- | ----------------------------------------------- |
| ProjectorBoot006      | 投影仪开关机                                |
| ProjectorMac          | 投影仪蓝牙 mac 地址(用于开机，需要配套 apk) |
| ProjectorMoonlight006 | 投影仪 moonlight 开关(需要配套 apk)         |

## 运行

安装依赖：

```bash
pip install -r requirements.txt
```

运行程序：

```bash
python main.py
```

## 米家接入

打开米家 APP, 添加设备，选择其他平台设备，找到巴法云，绑定账号即可

## 实现的功能

| 功能                     | 状态   | 说明                       |
| ------------------------ | ------ | -------------------------- |
| 投影仪开机           | 完成   | 通过米家控制投影仪开机 |
| 投影仪关机           | 开发中 | 需要配合配套 apk           |
| 投影仪打开 moonlight | 开发中 | 需要配合配套 apk           |
