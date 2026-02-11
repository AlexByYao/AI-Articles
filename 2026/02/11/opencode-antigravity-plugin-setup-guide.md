# Use Antigravity Models in OpenCode with Gemini Pro Family Plan

# 加入 Gemini Pro 家庭组后，如何在 OpenCode 中使用反重力(Antigravity)模型

`#Tutorial` `#LLM` `#Agent`

**Date / 日期**: 2026-02-11

**Reference / 参考**: [CSDN - Dvesiz](https://blog.csdn.net/Dvesiz/article/details/157515734) | [opencode-antigravity-auth](https://github.com/NoeFabris/opencode-antigravity-auth)

---

## Overview / 概述

If you've joined a **Gemini Pro family plan** (Google One AI Premium), you can use the **opencode-antigravity-auth** plugin to access powerful models like **Claude Opus 4.5/4.6**, **Claude Sonnet 4.5**, and **Gemini 3 Pro/Flash** directly in OpenCode — all through your Google account's Antigravity quota.

如果你已经加入了 **Gemini Pro 家庭组**（Google One AI Premium），你可以通过 **opencode-antigravity-auth** 插件，在 OpenCode 中直接使用 **Claude Opus 4.5/4.6**、**Claude Sonnet 4.5** 和 **Gemini 3 Pro/Flash** 等顶级模型——全部走你的 Google 账号的 Antigravity 配额。

### What You Get / 你能获得什么

| Feature | Description |
|---------|-------------|
| Claude + Gemini Models | Claude Opus 4.5/4.6, Sonnet 4.5, Gemini 3 Pro/Flash |
| Multi-Account Rotation | Add multiple Google accounts, auto-switch when rate-limited / 多账号轮换，限流自动切换 |
| Dual Quota System | Access both Antigravity and Gemini CLI quotas / 双配额系统 |
| Thinking Models | Extended thinking for Claude and Gemini with configurable budgets / 深度思考模式 |
| Pro User Benefits | 5-hour quota refresh (vs. 1-week for free users) / Pro 用户 5 小时刷新配额 |

---

## Prerequisites / 前提条件

Before you begin, make sure you have:

开始之前，确保你已具备以下条件：

- [x] **Gemini Pro subscription** — Already joined a Gemini Pro family plan or subscribed individually. Without Pro, quota is very limited (refreshes weekly instead of every 5 hours).
  
  **已订阅 Gemini Pro** — 已加入家庭组或独立订阅。未订阅也可使用，但额度很少（一周刷新一次）。

- [x] **OpenCode installed** — Have OpenCode CLI working on your system.

  **已安装 OpenCode** — 系统上已安装并能正常运行 OpenCode。

- [x] **Node.js v18+** — Required for the plugin.

  **Node.js v18+** — 插件运行需要。

- [x] **VPN with TUN mode** — Required to access Google services. Must use **TUN (virtual NIC) mode**, not just a proxy.
  
  **VPN（TUN 模式）** — 访问 Google 服务需要。必须使用**虚拟网卡（TUN）模式**，普通代理模式不行。

> **About Quota / 关于配额**:
> - **Pro users / Pro 用户**: Higher quota, refreshes every **5 hours** / 额度更多，每 5 小时刷新
> - **Free users / 免费用户**: Limited quota, refreshes **weekly** / 额度有限，每周刷新一次

---

## Step 1: Install the Plugin / 安装插件

There are two methods. We recommend Option A for simplicity.

有两种安装方式，推荐使用方式 A（最简单）。

### Option A: Let AI Do It (Recommended) / 方式 A：让 AI 自动安装（推荐）

Open OpenCode and paste this prompt directly:

打开 OpenCode，直接粘贴以下提示词：

```
Install the opencode-antigravity-auth plugin and add the Antigravity model definitions to ~/.config/opencode/opencode.json by following: https://raw.githubusercontent.com/NoeFabris/opencode-antigravity-auth/dev/README.md
```

The AI will automatically:
1. Add the plugin to your `opencode.json` plugin list
2. Add all Antigravity model definitions to the configuration

AI 会自动完成两件事：
1. 将插件加入 `opencode.json` 的 plugin 列表
2. 将所有 Antigravity 模型定义写入配置

> **Tip / 提示**: If auto-install fails due to environment differences, use Option B below.
> 
> 如果自动安装因环境差异失败，请使用下面的方式 B 手动安装。

### Option B: Manual Setup / 方式 B：手动安装

Edit your OpenCode configuration file:

编辑 OpenCode 配置文件：

- **Path / 路径**: `~/.config/opencode/opencode.json`
- **Windows**: `C:\Users\<YourName>\.config\opencode\opencode.json`

Add the following configuration:

添加以下配置：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-antigravity-auth@latest"],
  "provider": {
    "google": {
      "models": {
        "antigravity-gemini-3-pro": {
          "name": "Gemini 3 Pro (Antigravity)",
          "limit": { "context": 1048576, "output": 65535 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] },
          "variants": {
            "low": { "thinkingLevel": "low" },
            "high": { "thinkingLevel": "high" }
          }
        },
        "antigravity-gemini-3-flash": {
          "name": "Gemini 3 Flash (Antigravity)",
          "limit": { "context": 1048576, "output": 65536 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] },
          "variants": {
            "minimal": { "thinkingLevel": "minimal" },
            "low": { "thinkingLevel": "low" },
            "medium": { "thinkingLevel": "medium" },
            "high": { "thinkingLevel": "high" }
          }
        },
        "antigravity-claude-sonnet-4-5": {
          "name": "Claude Sonnet 4.5 (Antigravity)",
          "limit": { "context": 200000, "output": 64000 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] }
        },
        "antigravity-claude-sonnet-4-5-thinking": {
          "name": "Claude Sonnet 4.5 Thinking (Antigravity)",
          "limit": { "context": 200000, "output": 64000 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] },
          "variants": {
            "low": { "thinkingConfig": { "thinkingBudget": 8192 } },
            "max": { "thinkingConfig": { "thinkingBudget": 32768 } }
          }
        },
        "antigravity-claude-opus-4-5-thinking": {
          "name": "Claude Opus 4.5 Thinking (Antigravity)",
          "limit": { "context": 200000, "output": 64000 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] },
          "variants": {
            "low": { "thinkingConfig": { "thinkingBudget": 8192 } },
            "max": { "thinkingConfig": { "thinkingBudget": 32768 } }
          }
        },
        "antigravity-claude-opus-4-6-thinking": {
          "name": "Claude Opus 4.6 Thinking (Antigravity)",
          "limit": { "context": 200000, "output": 64000 },
          "modalities": { "input": ["text", "image", "pdf"], "output": ["text"] },
          "variants": {
            "low": { "thinkingConfig": { "thinkingBudget": 8192 } },
            "max": { "thinkingConfig": { "thinkingBudget": 32768 } }
          }
        }
      }
    }
  }
}
```

> **Note / 注意**: The key is `"plugin"` (singular), NOT `"plugins"`. Using the wrong key will cause an error.
>
> 配置项是 `"plugin"`（单数），不是 `"plugins"`，写错会报错。

---

## Step 2: Authenticate with Google / 使用 Google 账号登录

### 2.1 Run Auth Command / 执行认证命令

Open a **new terminal** and run:

打开一个**新终端**，执行：

```bash
opencode auth login
```

### 2.2 Select OAuth Method / 选择认证方式

When prompted, select: **OAuth with Google (Antigravity)**

出现选项时，选择：**OAuth with Google (Antigravity)**

### 2.3 Complete Google Login / 完成 Google 登录

Press Enter and your browser will open the Google login page. Log in with your Google account.

按回车后浏览器会自动打开 Google 登录页面，使用你的 Google 账号登录。

> **If you see an error page after login / 登录后如果看到报错页面**:
>
> Don't worry! Just copy the **entire URL** from the browser address bar and paste it into the terminal.
>
> 不要慌！直接复制浏览器地址栏中的**完整 URL**，粘贴到终端即可。

### 2.4 Add More Accounts (Optional) / 添加更多账号（可选）

After login, you'll be asked if you want to add more accounts. This enables **multi-account rotation** — when one account hits the rate limit, it automatically switches to the next.

登录后会提示是否继续添加其他账号。这可以实现**多账号轮换**——当一个账号达到限流时，自动切换到下一个。

---

## Step 3: Select and Use Models / 选择和使用模型

### 3.1 Switch Models / 切换模型

Restart OpenCode, then type:

重新打开 OpenCode，输入：

```
/models
```

Select a model with the **(Antigravity)** suffix.

选择后缀带有 **(Antigravity)** 的模型。

### Available Models / 可用模型列表

| Model | Type | Thinking Variants |
|-------|------|-------------------|
| `antigravity-gemini-3-pro` | Gemini 3 Pro | low, high |
| `antigravity-gemini-3-flash` | Gemini 3 Flash | minimal, low, medium, high |
| `antigravity-claude-sonnet-4-5` | Claude Sonnet 4.5 | — |
| `antigravity-claude-sonnet-4-5-thinking` | Claude Sonnet 4.5 | low, max |
| `antigravity-claude-opus-4-5-thinking` | Claude Opus 4.5 | low, max |
| `antigravity-claude-opus-4-6-thinking` | Claude Opus 4.6 | low, max |

### 3.2 Use Variants via CLI / 通过命令行指定变体

```bash
opencode run "Hello" --model=google/antigravity-claude-opus-4-5-thinking --variant=max
```

---

## Step 4: Check Your Quota / 查看使用额度

To monitor your remaining quota, you can use the **Antigravity Manager** tool:

要实时查看剩余额度，可以使用 **Antigravity Manager** 工具：

- **Download / 下载**: [https://github.com/lbjlaq/Antigravity-Manager/releases](https://github.com/lbjlaq/Antigravity-Manager/releases)
- Install and log in with your Google account to see real-time quota status.
- 安装后登录 Google 账号即可查看实时额度。

Alternatively, use the plugin's built-in quota check:

或者使用插件自带的额度检查：

```bash
opencode auth login
# Select "Check quotas" option
```

---

## Important Notes / 注意事项

> **Terms of Service Warning / 服务条款风险提醒**
>
> This plugin is an **unofficial tool** and is not endorsed by Google. A small number of users have reported account bans.
>
> 该插件是**非官方工具**，未获 Google 认可。少数用户反馈账号被封。
>
> **High-risk scenarios / 高风险情况**:
> - Fresh/new Google accounts / 新注册的 Google 账号
> - New accounts with Pro subscriptions / 新号购买 Pro 订阅
>
> **Recommendation / 建议**:
> Use an established Google account that you don't rely on for critical services.
>
> 使用一个不太重要的老号，不要用主力账号。

---

## Troubleshooting / 常见问题

### Plugin Not Loading / 插件未加载

Make sure your config key is `"plugin"` (singular):

确保配置项是 `"plugin"`（单数）：

```json
// Correct / 正确
{ "plugin": ["opencode-antigravity-auth@latest"] }

// Wrong / 错误
{ "plugins": ["opencode-antigravity-auth@latest"] }
```

### Auth Failed / 认证失败

Delete the accounts file and re-authenticate:

删除账号文件后重新认证：

```bash
rm ~/.config/opencode/antigravity-accounts.json
opencode auth login
```

### VPN Requirements / VPN 要求

You must use **TUN (virtual NIC) mode** in your VPN client. Regular HTTP/SOCKS proxy mode will not work for Google OAuth.

必须在 VPN 客户端中使用 **TUN（虚拟网卡）模式**。普通 HTTP/SOCKS 代理模式无法完成 Google OAuth 认证。

### Port Conflict / 端口冲突

If the OAuth callback fails due to port 51121 being in use:

如果 OAuth 回调因端口 51121 被占用失败：

```powershell
# Windows
netstat -ano | findstr :51121
taskkill /PID <PID> /F
opencode auth login
```

---

## References / 参考资料

- [opencode-antigravity-auth (GitHub)](https://github.com/NoeFabris/opencode-antigravity-auth)
- [OpenCode Official Docs](https://opencode.ai/docs)
- [CSDN Tutorial by Dvesiz](https://blog.csdn.net/Dvesiz/article/details/157515734)

---

*Author: AlexByYao*
