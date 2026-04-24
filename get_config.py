import requests
import base64
import os

# --- 从环境变量读取配置 ---
# 订阅链接
SUB_URL = os.environ.get('SUB_URL', '')
# 容器内保存路径
SAVE_PATH = "/config/config.yaml"


def main():
    if not SUB_URL:
        print("❌ 错误: 未设置 SUB_URL 环境变量")
        return

    # 模拟 Clash 客户端请求，防止机场拦截
    headers = {
        'User-Agent': 'ClashMeta/1.18.0 (Mihomo)'
    }

    print(f"开始拉取原始订阅...")

    try:
        # 1. 拉取数据
        response = requests.get(SUB_URL, headers=headers, timeout=15)
        response.raise_for_status()
        raw_text = response.text.strip()

        # 2. 处理 Base64 解码（机场链接通常是加密的）
        try:
            # 自动补齐 Base64 填充符并解码
            decoded_bytes = base64.b64decode(raw_text + '=' * (-len(raw_text) % 4))
            yaml_content = decoded_bytes.decode('utf-8')
            print("检测到 Base64 编码，已成功解码为明文。")
        except Exception:
            # 解码失败则说明原本就是明文
            yaml_content = raw_text
            print("内容已是明文 YAML，直接保存。")

        # 3. 写入文件（直接写入流，不经过任何解析，保证原汁原味）
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        print(f"✅ 成功！原始配置已保存至: {SAVE_PATH}")

    except Exception as e:
        print(f"❌ 拉取过程中出现错误: {e}")


if __name__ == "__main__":
    main()