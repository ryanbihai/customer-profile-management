#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布 Skill 到 ClawHub - 通过 GitHub 仓库
"""
import requests
import json
import sys

API_KEY = "clh_s_agUKWex-cq2O1KGtVaYVP5itfoOuiUHBJiylIsQVI"
API_BASE = "https://claw-hub-bay.vercel.app/api/v1"

GITHUB_REPO_URL = sys.argv[1] if len(sys.argv) > 1 else ""

if not GITHUB_REPO_URL:
    print("用法: python publish_skill.py <GitHub仓库URL>")
    print("例如: python publish_skill.py https://github.com/用户名/customer-profile-management")
    sys.exit(1)


def get_me():
    """获取当前用户信息"""
    response = requests.get(
        f"{API_BASE}/agents/me",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    print(f"GET /agents/me: {response.status_code}")
    if response.ok:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    else:
        print(f"Error: {response.text}")
        return None


def publish_skill():
    """通过 GitHub URL 发布 Skill"""
    print(f"\n准备发布的 GitHub 仓库: {GITHUB_REPO_URL}")

    payload = {
        "repo_url": GITHUB_REPO_URL
    }

    print(f"\n正在发布...")
    response = requests.post(
        f"{API_BASE}/skills",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print(f"POST /skills: {response.status_code}")

    if response.ok:
        result = response.json()
        print("\n发布成功!")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result
    else:
        print(f"发布失败: {response.text}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("ClawHub Skill 发布工具")
    print("=" * 60)

    print("\n【步骤1】获取用户信息")
    me = get_me()

    if me:
        print(f"\n用户名: {me.get('username', 'N/A')}")

    print("\n【步骤2】发布 Skill")
    result = publish_skill()

    if result:
        print("\n" + "=" * 60)
        print("✅ 发布完成!")
        print("=" * 60)
        if "slug" in result:
            print(f"Skill slug: {result['slug']}")
        if "url" in result:
            print(f"Skill URL: {result['url']}")
    else:
        print("\n" + "=" * 60)
        print("❌ 发布失败")
        print("=" * 60)
