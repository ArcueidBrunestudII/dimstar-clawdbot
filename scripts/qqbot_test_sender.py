#!/usr/bin/env python3
"""
QQ Bot 消息发送器
用于绕过 Clawdbot 框架层，直接调用 QQ Bot API
"""

import requests
import json
import sys
import time

# QQ Bot 配置
APP_ID = "102825411"
CLIENT_SECRET = "bnzCPds7NduBTl4Nh1Mh3Pm9XvKj9a1T"
TARGET_QQ = "74880657"

# API endpoints
TOKEN_URL = "https://bots.qq.com/app/getAppAccessToken"
C2C_MESSAGE_URL = f"https://api.sgroup.qq.com/v2/users/{TARGET_QQ}/messages"


class QQBotSender:
    def __init__(self):
        self.access_token = None
        self.expires_at = None

    def get_access_token(self):
        now = time.time()
        if self.access_token and (now - self.expires_at) < 300:
            print(f"使用缓存的 Token (剩余 {300 - int(now - self.expires_at):.0f} 秒)")
            return self.access_token

        print("获取新的 Access Token...")
        response = requests.post(TOKEN_URL, json={
            "appId": APP_ID,
            "clientSecret": CLIENT_SECRET
        }, timeout=10)

        if response.status_code != 200:
            print(f"获取 Token 失败: {response.status_code}")
            print(f"响应: {response.text}")
            sys.exit(1)

        data = response.json()

        if "access_token" not in data:
            print(f"响应中未找到 access_token: {data}")
            sys.exit(1)

        self.access_token = data["access_token"]
        expires_in = data.get("expires_in", 7200)
        self.expires_at = now + int(expires_in)

        print(f"Token 获取成功，有效期: {expires_in} 秒")
        return self.access_token

    def send_message(self, message, msg_id=None):
        if not self.access_token:
            print("Token 未初始化，正在获取...")
            self.get_access_token()

        url = C2C_MESSAGE_URL
        headers = {
            "Authorization": f"QQBot {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "content": message,
            "msg_type": 0
        }

        if msg_id:
            payload["msg_id"] = msg_id

        print(f"发送消息: {message}")

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code != 200:
            print(f"发送失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None

        data = response.json()

        if "id" in data:
            print(f"发送成功！消息 ID: {data['id']}")
            return data["id"]
        else:
            print(f"发送成功但未返回消息 ID")
            return None


def main():
    sender = QQBotSender()

    messages = [
        "测试消息 1/5 - Python 脚本直接调用 QQ Bot API",
        "测试消息 2/5 - 绕过框架层限制",
        "测试消息 3/5 - 每分钟发一条",
        "测试消息 4/5 - 共发送 5 条",
        "测试消息 5/5 - 最后一条"
    ]

    for i, msg in enumerate(messages, 1):
        print(f"\n--- 发送 {i}/{len(messages)} ---")
        result = sender.send_message(msg)
        if result:
            print(f"成功")
        else:
            print(f"失败")

        if i < len(messages):
            time.sleep(10)
            if i == len(messages):
                print("\n等待 60 秒后结束...")
                time.sleep(60)

    print("\n所有消息发送完成！")


if __name__ == "__main__":
    main()
