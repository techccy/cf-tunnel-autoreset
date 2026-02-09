# cf-tunnel-autoreset (macOS)

[「中文」](README.md)

A lightweight Python-based watchdog script designed to maintain the high availability of Cloudflared Tunnels on macOS.

### 💡 Why this exists?

In unstable network environments, `cloudflared` sometimes enters a "zombie" state—the process remains running, but the connection is dead, often flooding logs with `Connection terminated`. This script monitors the logs in real-time and performs a **force-restart** the moment a connection failure is detected.

### ✨ Key Features

* **Real-time Log Interception**: Uses line-buffered monitoring to capture errors instantly.
* **Aggressive Recovery**: Specifically optimized for macOS to ensure stalled processes are fully purged using `SIGKILL` before restarting.
* **Minimalist Design**: Zero external dependencies; runs on standard Python 3.

### 🚀 Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/your-username/cf-tunnel-autoreset.git
cd cf-tunnel-autoreset

```


2. **Configure**
Open `cloudflared_tunnel_protect.py` and update the `TUNNEL_NAME` with your actual tunnel configuration.
3. **Run in Background**
Since the script needs to manage processes, use `sudo` with `sh -c` for a reliable background session:
```bash
sudo sh -c 'nohup python3 cloudflared_tunnel_protect.py > tunnel_watchdog.log 2>&1 &'

```


4. **Stop the Watchdog**
```bash
ps aux | grep cloudflared_tunnel_protect.py | awk '{print $2}' | xargs sudo kill -9

```



### 🛠 Configuration

```python
CLOUDFLARED_CMD = ["cloudflared", "tunnel", "run", "YourTunnelName"]
TARGET_ERROR = "Connection terminated" # Keyword that triggers a restart
RESTART_DELAY = 3 # Cooldown period (seconds) before reconnecting

```
