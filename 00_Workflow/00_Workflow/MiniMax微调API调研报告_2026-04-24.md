# MiniMax 微调 API 调研报告

**调研时间：** 2026-04-24  
**调研人：** Hermes Agent  
**调研目的：** 确认 MiniMax 是否支持 SFT 微调训练，以及正确的 API 接口

---

## 一、调研方法

1. 访问 MiniMax 官方文档中心 (platform.minimaxi.com/docs)
2. 检查 API 接口文档中的微调相关端点
3. 测试 API Base URL: `https://api.minimaxi.com/anthropic`
4. 搜索文档中的微调相关页面

---

## 二、调研结果

### 2.1 API Base URL 测试

| URL | 测试结果 |
|-----|---------|
| `https://api.minimaxi.com` | 404 Not Found |
| `https://api.minimaxi.com/anthropic/v1/models` | 404 Not Found |

**结论：** `https://api.minimaxi.com/anthropic` 并非有效的 API 基础路径

### 2.2 MiniMax 官方文档结构

MiniMax 开放平台文档 (platform.minimaxi.com/docs) 提供以下模块：

| 模块 | 内容 |
|-----|------|
| **开发指南** | 快速开始、AI编程工具接入 |
| **文本** | 对话生成、Prompt缓存、Function Call |
| **语音** | 同步语音合成、异步长文本语音、音色复刻 |
| **视频** | 视频生成、视频Agent |
| **图像** | 图片生成 |
| **音乐** | 音乐生成 |
| **MCP** | MCP协议支持 |
| **API 参考** | Anthropic兼容、OpenAI兼容、AI SDK |
| **产品定价** | 各模块定价 |
| **Token Plan** | 代码助手订阅计划 |

### 2.3 微调相关文档查找

- 访问 `/docs/guides/fine-tuning` → **404 页面不存在**
- 在文档导航中搜索"微调"相关页面 → **未找到**
- 检查所有 API 端点 → **未发现 SFT/RLHF 训练相关接口**

### 2.4 支持的模型

MiniMax 提供的模型（来自文档）：

| 模型类型 | 模型名称 |
|---------|---------|
| 文本 | MiniMax-M2.7, MiniMax-M2.5, MiniMax-M2.1, MiniMax-M2 |
| 语音 | speech-2.8-hd, speech-2.8-turbo, speech-2.6-hd, speech-2.6-turbo |
| 视频 | MiniMax Hailuo 2.3 / 2.3 Fast |
| 音乐 | MiniMax Music 2.6 |

---

## 三、核心发现

### ❌ MiniMax **不支持** SFT 微调训练

根据文档分析，MiniMax 开放平台 **仅提供推理 API**，不提供模型训练/微调服务：

1. **所有 API 都是推理接口**（文本对话、语音合成、视频生成等）
2. **文档中无微调页面** - `/docs/guides/fine-tuning` 返回 404
3. **无训练相关 API** - 在 API Reference 中未找到任何 `/train`, `/fine_tune`, `/training` 端点
4. **API Base 不是有效的训练端点** - `https://api.minimaxi.com/anthropic` 返回 404

---

## 四、MiniMax API 接口信息

### 4.1 官方 API Base

| 协议 | Base URL |
|-----|----------|
| Anthropic 兼容 | `https://api.minimaxi.com` (推理) |
| OpenAI 兼容 | `https://api.minimaxi.com` (推理) |

### 4.2 推理 API 示例

```
# Anthropic 兼容接口
POST https://api.minimaxi.com/v1/messages

# OpenAI 兼容接口  
POST https://api.minimaxi.com/v1/chat/completions
```

---

## 五、对接结论

| 项目 | 结论 |
|-----|------|
| 是否支持 SFT | ❌ **不支持** |
| 是否支持 RLHF | ❌ **不支持** |
| 是否支持模型训练 | ❌ **不支持** |
| 支持的功能 | 仅推理 API（对话、语音、视频、图像生成） |

### 已有数据处理建议

由于 MiniMax **不提供微调训练服务**，您现有的数据需要寻找其他方案：

| 数据类型 | 文件 | 数量 | 建议方案 |
|---------|------|------|---------|
| SFT 数据 | weili_sft_v2.jsonl | 124条 | 寻找支持 SFT 的平台 |
| RLHF 数据 | weili_rlhf_v2.jsonl | 75条 | 寻找支持 RLHF 的平台 |

---

## 六、备选方案建议

如果需要进行模型微调训练，可考虑以下平台：

1. **硅基流动** - 提供多种模型的微调服务
2. **火山引擎(字节跳动)** - 提供模型训练服务
3. **阿里云百炼** - 提供模型微调服务
4. **百度智能云** - 提供模型定制服务
5. **腾讯云** - 提供模型训练服务

---

## 七、附录：MiniMax 官方资源

- 文档中心：https://platform.minimaxi.com/docs
- API 概览：https://platform.minimaxi.com/docs/api-reference/api-overview
- 产品定价：https://platform.minimaxi.com/docs/pricing/overview
- 账户管理：https://platform.minimaxi.com/user-center/basic-information

---

**报告生成时间：** 2026-04-24 20:13