# Claude-to-IM-skill 安装失败记录

> 记录时间：2026-04-09
> 操作人：Jarvis
> 结果：❌ 安装失败，已清理

---

## 背景

用户（陈总）从 GitHub 了解到 `op7418/Claude-to-IM-skill`，要求安装。

**skill 简介：**
- 桥接 IM（飞书/微信/Telegram/Discord/QQ）→ Claude Code/Codex
- 支持审批流、token 安全、流式预览、会话持久化
- 零配置向导：`/claude-to-im setup`

---

## 安装过程

### Step 1：ClawHub 搜索（失败）

```bash
clawhub search claude-to-im
```
**结果：** ClawHub 上无此 skill（未上架）

### Step 2：直接从 GitHub 克隆 skill 包

```bash
git clone https://github.com/op7418/Claude-to-IM-skill.git C:\Users\pc\.claude\skills\claude-to-im
```
**结果：** ✅ 克隆成功

### Step 3：安装依赖并构建

```bash
cd C:\Users\pc\.claude\skills\claude-to-im
pnpm install
node scripts/build.js
```
**结果：** ❌ 构建失败，esbuild 报错：
```
Could not resolve "claude-to-im/src/lib/bridge/context.js"
Could not resolve "claude-to-im/src/lib/bridge/bridge-manager.js"
Could not resolve "claude-to-im/src/lib/bridge/adapters/index.js"
...
```

---

## 根因分析

### 发现一：skill 是 monorepo 结构

`claude-to-im-skill` 本身不是完整项目，它依赖主包 `Claude-to-IM`（在 sibling 目录）：

```
~/.claude/
├── Claude-to-IM/           ← 主包（完整项目）
│   ├── src/lib/bridge/     ← 核心库所在
│   ├── package.json
│   └── ...
└── skills/
    └── claude-to-im/       ← skill 包
        ├── SKILL.md
        ├── scripts/build.js
        └── src/main.ts      ← 引用 'claude-to-im/src/lib/bridge/...'
```

skill 的 `src/main.ts` 里用了绝对路径引用：
```typescript
import { initBridgeContext } from 'claude-to-im/src/lib/bridge/context.js';
```

这在 monorepo 内部包引用时需要 pnpm workspace 的 symlink 才能解析。

### 发现二：pnpm workspace symlink 不被 esbuild 识别

即使建立了 pnpm workspace（`pnpm-workspace.yaml`），让 skill 的 `node_modules` 链接到主包，esbuild 仍然无法解析这个路径。

**原因：** esbuild 的 alias 解析基于 CWD，不认 pnpm 的 symlink。

### 发现三：主包安装在了错误位置

最初主包被克隆到了 `C:\Users\pc\Claude-to-IM`（非 workspace 路径），导致 symlink 路径对不上。

### 发现四：尝试修复 build.js 的 alias 也失败

修改 `scripts/build.js`，添加 esbuild alias 指向主包路径：
```javascript
alias: {
  'claude-to-im': 'C:\\Users\\pc\\.claude\\Claude-to-IM\\src',
}
```

**结果：** esbuild 把路径解析成了 `C:\Users\pc\.claude\skills\Claude-to-IM\src`（多了一层 skills 路径），仍然对不上。

---

## 尝试过的方案

| 方案 | 操作 | 结果 |
|------|------|------|
| 直接 git clone skill | ✅ 成功 | skill 代码到位 |
| pnpm install | ✅ 成功 | 依赖安装完成 |
| node scripts/build.js | ❌ 失败 | esbuild 找不到主包 |
| 建立 pnpm workspace | ✅ 成功 | workspace 结构建立 |
| 修改 build.js 加 alias | ❌ 失败 | 路径拼接错误 |
| 把主包含进 workspace | ✅ 成功 | 主包安装到位 |
| 再次 build | ❌ 失败 | esbuild 仍然找不到 |

---

## 最终结论

**安装失败。** 用户于 09:12 要求放弃，文件已全部清理。

**根本原因：**
1. skill 设计为 monorepo，但安装文档没有说明需要同时克隆主包
2. 主包和 skill 必须是相邻目录（sibling），且需要正确建立 workspace
3. 即使建立 workspace，esbuild 的路径解析机制也不认 pnpm 的虚拟 symlink
4. 需要修改 skill 的 `build.js`，让 esbuild 的 alias 指向正确路径

**正确的安装方式（理论上）：**
```bash
# 克隆主包到正确位置
git clone https://github.com/op7418/Claude-to-IM.git C:\Users\pc\.claude\Claude-to-IM
cd C:\Users\pc\.claude\Claude-to-IM
pnpm install && pnpm build

# 克隆 skill
git clone https://github.com/op7418/Claude-to-IM-skill.git C:\Users\pc\.claude\skills\claude-to-im
cd C:\Users\pc\.claude\skills\claude-to-im
pnpm install

# 修改 build.js 的 alias 指向正确路径
# 然后 node scripts/build.js
```

**如果需要这个 skill：**
- 需要有人修复 `scripts/build.js` 的路径问题
- 或者改用 Codex 模式（通过 `install-codex.sh` 安装，脚本会自动处理路径）

---

<!-- JARVIS_DONE: Claude-to-IM-skill 安装失败全流程已归档。根因：monorepo 结构 + esbuild 路径解析问题 + 主包位置错误。已清理所有文件。用户已知晓。记录位置：99_Tools/claude-to-im-skill安装失败记录.md -->
