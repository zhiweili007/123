import os
import json
import random
import time

def log(msg):
    print(f"[刷步日志] {msg}")

def load_config():
    raw = os.environ.get("CONFIG")
    if not raw:
        raise ValueError("未检测到 CONFIG，请检查 GitHub Secrets 设置")

    try:
        config = json.loads(raw)
        if isinstance(config, dict):
            return [config]  # 单账号转为列表
        elif isinstance(config, list):
            return config    # 多账号列表
        else:
            raise ValueError("CONFIG 必须为 JSON 格式的对象或列表")
    except Exception as e:
        raise ValueError(f"CONFIG 解析失败：{e}")

def simulate_login(user, pwd):
    # 在这里接入 Zepp Life 登录逻辑（可根据已有项目模块替换）
    log(f"尝试登录账号：{user}")
    if "@" not in user and len(user) < 6:
        return False
    return True  # 模拟登录成功

def upload_step(user, step):
    # 模拟上传步数（此处需要替换为实际 ZeppLife 接口调用逻辑）
    log(f"账号 {user} 上传步数：{step}")
    return True

def run_for_user(cfg):
    user = cfg.get("USER")
    pwd = cfg.get("PWD")
    min_step = int(cfg.get("MIN_STEP", "8000"))
    max_step = int(cfg.get("MAX_STEP", "12000"))
    sleep_gap = int(cfg.get("SLEEP_GAP", "5"))

    if not user or not pwd:
        log(f"账号或密码为空，跳过该项")
        return

    if not simulate_login(user, pwd):
        log(f"账号登录失败：{user}")
        return

    step = random.randint(min_step, max_step)
    if upload_step(user, step):
        log(f"✅ {user} 成功上传步数：{step}")
    else:
        log(f"❌ {user} 上传失败")

    time.sleep(sleep_gap)

def main():
    all_cfg = load_config()
    for cfg in all_cfg:
        run_for_user(cfg)

if __name__ == "__main__":
    main()
