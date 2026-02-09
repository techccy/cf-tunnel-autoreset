import subprocess
import time
import os
import signal

# --- 配置区域 ---
# 如果 cloudflared 不在路径中，请修改为完整路径，如 "/usr/local/bin/cloudflared"
CLOUDFLARED_CMD = ["cloudflared", "tunnel", "run", "MyTunnel"]
TARGET_ERROR = "Connection terminated"
RESTART_DELAY = 3
# ----------------

def run_monitor():
    while True:
        print(f"[{time.strftime('%H:%M:%S')}] 🚀 启动 Tunnel...")
        
        # 启动进程
        # stderr=subprocess.STDOUT 将错误流合并到标准输出，方便统一读取
        process = subprocess.Popen(
            CLOUDFLARED_CMD,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='ignore'
        )

        try:
            # 实时读取日志行
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                clean_line = line.strip()
                print(f"  {clean_line}")

                # 精确匹配关键词
                if TARGET_ERROR in clean_line:
                    print(f"\n[!] 检测到关键错误: '{TARGET_ERROR}'")
                    print(f"[!] 正在强制终止并准备重启...")
                    break
            
        except Exception as e:
            print(f"监控发生异常: {e}")

        # --- 强制清理进程 ---
        terminate_mac_process(process)
        
        print(f"[*] 冷却 {RESTART_DELAY} 秒后重新连接...\n")
        time.sleep(RESTART_DELAY)

def terminate_mac_process(p):
    """在 macOS/Linux 上安全且强制地关闭进程"""
    if p.poll() is None: # 如果进程还在运行
        try:
            # 发送 SIGTERM 尝试优雅退出
            os.kill(p.pid, signal.SIGTERM)
            # 等待 2 秒，如果还没关掉就强制 SIGKILL
            count = 0
            while p.poll() is None and count < 20:
                time.sleep(0.1)
                count += 1
            
            if p.poll() is None:
                os.kill(p.pid, signal.SIGKILL)
                print(f"[+] 进程 {p.pid} 已强制强杀 (SIGKILL)")
            else:
                print(f"[+] 进程 {p.pid} 已正常终止")
        except ProcessLookupError:
            pass
        except Exception as e:
            print(f"终止进程时出错: {e}")

if __name__ == "__main__":
    try:
        run_monitor()
    except KeyboardInterrupt:
        print("\n[+] 监控脚本已由用户停止。")
