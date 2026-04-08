# 🐺 DG-MCP — 让 AI 控制郊狼 3.0

> 🔌 基于 MCP (Model Context Protocol) 的 DG-Lab 郊狼 3.0 脉冲主机控制器，让 Claude 等 AI 通过蓝牙直连控制设备。

## ✨ 特性

- 🦷 **BLE 直连** — 无需 APP，电脑蓝牙直接连接郊狼 3.0
- 🤖 **MCP 协议** — Claude Desktop / Claude Code 等 AI 客户端即插即用
- 🎛️ **10 个 Tools** — 扫描、连接、强度控制、波形播放、自定义波形设计、状态查询
- 🌊 **6 种预设波形** — 呼吸、潮汐、低/中/高脉冲、敲击
- 🔒 **安全保护** — 强度软上限，防止 AI 误操作

## 📦 安装

### 前置要求

- 📡 电脑蓝牙（支持 BLE）
- 🔋 DG-Lab 郊狼 3.0 脉冲主机
- 📦 [uv](https://docs.astral.sh/uv/getting-started/installation/) 包管理器

## 🚀 使用方法

### 1️⃣ 配置 MCP 客户端

#### 🖥️ Claude Desktop

编辑 `claude_desktop_config.json`，文件位置因操作系统而异：

| 操作系统 | 路径 |
|----------|------|
| 🍎 macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| 🪟 Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| 🐧 Linux | `~/.config/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "dg-lab": {
      "command": "uvx",
      "args": ["dg-mcp"]
    }
  }
}
```

#### 💻 Claude Code

```bash
claude mcp add dg-lab -- uvx dg-mcp
```

> 🗑️ 移除：`claude mcp remove dg-lab`

### 2️⃣ 开机连接

1. 🔋 长按郊狼 3.0 电源键开机
2. 📡 确保电脑蓝牙已开启（**无需手动配对**，BLE 直连）
3. 🤖 在 AI 对话中说："扫描并连接郊狼设备"

### 3️⃣ AI 自动完成

AI 会按以下流程操作：

```
🔍 scan()          → 扫描附近的郊狼设备
🔗 connect(地址)    → 连接设备
⚡ set_strength()   → 设置通道强度
🌊 send_wave()      → 发送预设/自定义波形
🎨 design_wave()    → 设计多步变化波形
```

## 🎛️ MCP Tools 一览

| Tool | 说明 | 示例 |
|------|------|------|
| 🔍 `scan` | 扫描附近郊狼设备 | `scan(timeout=5)` |
| 🔗 `connect` | 连接设备 | `connect("AA:BB:CC:DD:EE:FF")` |
| ❌ `disconnect` | 断开连接 | `disconnect()` |
| ⚡ `set_strength` | 设置通道强度 (0~200) | `set_strength("A", 10)` |
| ➕ `add_strength` | 增减强度 | `add_strength("A", 5)` |
| 🔒 `set_strength_limit` | 设置强度软上限（断电保存） | `set_strength_limit(50, 50)` |
| 🌊 `send_wave` | 发送预设/自定义波形 | `send_wave("A", preset="breath")` |
| 🎨 `design_wave` | 设计多步变化波形 | `design_wave("A", steps=[...])` |
| ⏹️ `stop_wave` | 停止波形（省略通道停止全部） | `stop_wave("A")` / `stop_wave()` |
| 📊 `get_status` | 查询设备状态 | `get_status()` |

## 🌊 预设波形

| 名称 | 说明 | 体感 |
|------|------|------|
| 🫁 `breath` | 呼吸 | 缓慢起伏，从无到强再回落 |
| 🌊 `tide` | 潮汐 | 频率渐变，波浪感 |
| 💤 `pulse_low` | 低脉冲 | 轻柔持续 |
| ⚡ `pulse_mid` | 中脉冲 | 中等持续 |
| 🔥 `pulse_high` | 高脉冲 | 强烈持续 |
| 👆 `tap` | 敲击 | 有节奏的间歇脉冲 |

### 🎨 自定义波形

除了预设，还可以用 `send_wave` 自定义固定频率和强度：

```
send_wave("A", frequency=100, intensity=50, duration_frames=10, loop=True)
```

- `frequency`: 波形频率 10~1000ms（值越小频率越高）
- `intensity`: 波形强度 0~100
- `duration_frames`: 持续帧数，每帧 100ms（默认 10 = 1 秒）
- `loop`: 是否循环播放（默认 `True`）

### 🎼 设计多步波形

使用 `design_wave` 可以创建频率和强度随时间变化的复杂波形，每个 step 持续 100ms：

```
design_wave("A", steps=[
    {"freq": 10, "intensity": 0},
    {"freq": 10, "intensity": 25},
    {"freq": 10, "intensity": 50},
    {"freq": 10, "intensity": 75},
    {"freq": 10, "intensity": 100, "repeat": 3},
    {"freq": 10, "intensity": 0,   "repeat": 2}
], loop=True)
```

- `freq`: 脉冲频率 10~1000ms（值越小频率越高）
- `intensity`: 强度 0~100（0=无输出，100=最强）
- `repeat`: 该步骤重复次数（默认 1）
- `loop`: 是否循环播放（默认 `True`，设为 `False` 播放一次后停止）

> 💡 AB 双通道可同时独立播放不同波形

## ⚠️ 安全须知

> 🚨 **重要！请务必阅读！**

1. ⚡ **从低强度开始** — 首次使用建议强度设为 `5~10`，逐步增加
2. 🔒 **设置软上限** — 使用 `set_strength_limit` 限制最大强度，防止意外
3. 🚫 **紧急停止** — 直接关闭郊狼电源即可立即停止所有输出
4. 💓 **禁止区域** — 请勿将电极放置在心脏区域或头颈部
5. 🤖 **AI 不是人** — AI 无法感知你的实际体验，请随时手动调整或停止

## 🏗️ 项目结构

```
DG-MCP/
├── 📄 pyproject.toml          # 项目配置 + 依赖
├── 📦 dg_mcp/
│   ├── 📡 protocol.py         # V3 BLE 协议 (B0/BF 指令)
│   ├── 🌊 waves.py            # 预设波形 + 自定义波形
│   ├── 🦷 device.py           # BLE 设备管理 (扫描/连接/控制)
│   └── 🤖 server.py           # MCP Server (10 个 Tools)
```

## 🔧 技术细节

- **通信协议**: DG-Lab Coyote V3 BLE 协议
- **BLE 库**: [bleak](https://github.com/hbldh/bleak) — 跨平台 BLE
- **MCP SDK**: [mcp](https://modelcontextprotocol.io/) — Model Context Protocol
- **B0 指令**: 20 字节，每 100ms 写入，同时控制 AB 双通道强度 + 波形
- **BF 指令**: 7 字节，设置强度软上限（断电保存）

## 🖥️ 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| 🪟 Windows | ✅ 支持 | 直接使用 |
| 🍎 macOS | ✅ 支持 | 直接使用 |
| 🐧 Linux | ✅ 支持 | 需要 BlueZ |
| 🐧 WSL2 | ⚠️ 需配置 | 需要 USB 蓝牙透传 ([usbipd](https://github.com/dorssel/usbipd-win)) |

## 📜 致谢

- [DG-LAB-OPENSOURCE](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE) — 官方开源 BLE 协议
- [Model Context Protocol](https://modelcontextprotocol.io/) — MCP 协议规范

## 🚨 免责声明

> **本项目仅供学习交流使用，不得用于任何违法或不当用途。使用者应自行承担使用本项目所产生的一切风险和责任，项目作者不对因使用本项目而导致的任何直接或间接损害承担责任。**

## 📄 License

MIT
