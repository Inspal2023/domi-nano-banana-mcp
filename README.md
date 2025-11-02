# Domi Nano-Banana MCP 服务

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Inspal2023/domi-nano-banana-mcp)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-2024.11.05-orange.svg)](https://modelcontextprotocol.io)

一个基于 Model Context Protocol (MCP) 的强大图像生成和编辑服务，集成多米API的nano-banana模型（基于Gemini 2.5 Flash），为AI应用提供专业级的图像处理能力。

## ✨ 核心功能

- 🎨 **文生图功能**: 根据文本描述生成高质量图像
- 🖼️ **图片编辑功能**: 基于文本指令的智能图像编辑
- 🔐 **API令牌验证**: 验证API令牌的有效性
- 📏 **尺寸查询**: 获取所有支持的图片尺寸列表
- ⚡ **异步处理**: 支持长时间生成和编辑任务
- 🔄 **智能重试**: 内置错误处理和重试机制

### 工具列表
1. **text_to_image**: 文生图功能
2. **image_edit**: 图片编辑功能  
3. **get_supported_sizes**: 获取支持的图片尺寸
4. **validate_api_token**: 验证API令牌有效性

### 提示词模板
1. **image_generation_prompt**: 图像生成提示词模板
2. **image_editing_prompt**: 图像编辑提示词模板

## 🚀 快速开始

### 1分钟体验

```bash
# 克隆项目
git clone https://github.com/Inspal2023/domi-nano-banana-mcp.git
cd domi-nano-banana-mcp

# 设置API令牌
export DOMI_API_TOKEN="your_api_token_here"

# 启动服务
./run.sh
```

### 基础使用

```javascript
// 生成图片
const result = await mcpClient.call_tool("text_to_image", {
  "prompt": "一只可爱的小猫坐在花园里",
  "size": "3x4",
  "seed": 12345
});

console.log("生成的图片:", result.image_url);
```

## 📚 文档导航

| 文档 | 描述 | 目标读者 |
|------|------|----------|
| [快速入门](QUICK_START.md) | 5分钟快速集成指南 | 新用户 |
| [集成指南](INTEGRATION_GUIDE.md) | 完整的API参考和集成文档 | 开发者 |
| [配置示例](examples/config_examples.md) | 各种环境配置示例 | 运维人员 |
| [Python示例](examples/python_client.py) | Python客户端代码示例 | Python开发者 |
| [JavaScript示例](examples/javascript_client.js) | JavaScript客户端代码示例 | Web开发者 |

## 📋 系统要求

- Python 3.7+
- 多米API访问权限和有效的API Token
- MCP兼容的客户端（如Claude Desktop）

## 🛠️ 安装和配置

### 1. 环境准备
```bash
# 确保已安装Python 3.7+
python --version
```

### 2. 获取API Token
1. 访问多米API平台：https://duomiapi.com/
2. 注册账号并获取API Token
3. 设置环境变量：
```bash
export DOMI_API_TOKEN="your_api_token_here"
```

### 3. 项目部署
```bash
# 克隆或下载项目到本地
cd domi-nano-banana-mcp

# 安装依赖
pip install -r requirements.txt

# 启动MCP服务器
chmod +x run.sh
./run.sh
```

## 📖 使用指南

### 基本使用

#### 1. 文生图示例
```python
# 生成一张正方形图片
result = text_to_image(
    prompt="一只可爱的小猫坐在花园里，阳光明媚，色彩鲜艳",
    size="1x1",
    seed=42
)

# 生成竖屏图片
result = text_to_image(
    prompt="现代城市夜景，霓虹灯闪烁，科技感十足",
    size="9x16"
)
```

#### 2. 图片编辑示例
```python
# 编辑现有图片
result = image_edit(
    image="https://example.com/original-image.jpg",
    prompt="将背景改为蓝色，添加一些云朵，保持主体不变"
)
```

#### 3. 验证API Token
```python
# 验证API令牌是否有效
result = validate_api_token("your_api_token_here")
```

### 高级功能

#### 提示词优化
使用内置的提示词模板来优化生成效果：

```python
# 生成优化的图像提示词
prompt = image_generation_prompt(
    subject="一只在雪地里玩耍的哈士奇",
    style="realistic",
    size="4x3"
)
```

#### 尺寸选择指南
- **1x1**: 适合头像、图标、社交媒体
- **3x4**: 适合手机壁纸、海报、书籍封面  
- **4x3**: 适合电脑壁纸、演示文稿、网页横幅
- **9x16**: 适合短视频平台内容
- **16x9**: 适合YouTube缩略图、宽屏视频

## 🔧 配置说明

### 环境变量
- `DOMI_API_TOKEN`: 多米API的Bearer Token（必需）

### MCP服务器配置
服务器配置文件 `mcp-server.json` 包含以下关键设置：
- 服务器类型：MCP Server (type: 3)
- 启动命令：sh run.sh
- 认证方式：Bearer Token
- 支持的功能：文生图、图片编辑、尺寸查询、Token验证

## 📊 API参考

### 工具列表

| 工具名称 | 功能 | 参数 | 返回时间 |
|---------|------|------|---------|
| `text_to_image` | 文生图 | prompt, size, seed, api_token | 15-30秒 |
| `image_edit` | 图片编辑 | image, prompt, api_token | 10-25秒 |
| `validate_api_token` | 验证令牌 | api_token | 即时 |
| `get_supported_sizes` | 查询尺寸 | 无参数 | 即时 |

### 支持的图片尺寸

| 尺寸 | 比例 | 最佳用途 |
|------|------|----------|
| 1x1 | 1:1 | 头像、图标、Instagram帖子 |
| 3x4 | 3:4 | 手机壁纸、海报、书籍封面 |
| 4x3 | 4:3 | 电脑壁纸、演示文稿 |
| 9x16 | 9:16 | 抖音、快手短视频 |
| 16x9 | 16:9 | YouTube缩略图、宽屏视频 |

### 响应格式

#### 成功响应
```json
{
  "success": true,
  "image_url": "https://cdn3.dmiapi.com/attachments/gemini/...",
  "metadata": {
    "task_id": "task-uuid",
    "status": "succeeded",
    "status_code": "3",
    "model": "nano-banana"
  }
}
```

#### 错误响应
```json
{
  "success": false,
  "error": "详细错误信息",
  "error_code": "ERROR_CODE"
}
```

## 🚨 错误处理

### 常见错误代码
- `INVALID_PROMPT`: 提示词为空或无效
- `INVALID_SIZE`: 图片尺寸不支持
- `INVALID_IMAGE`: 图片格式无效
- `API_ERROR`: API调用失败
- `TIMEOUT`: 请求超时
- `UNKNOWN_ERROR`: 未知错误

### 错误响应格式
```json
{
  "success": false,
  "error": "详细错误信息",
  "error_code": "ERROR_CODE"
}
```

## 🔒 安全注意事项

1. **API Token安全**: 
   - 不要在代码中硬编码API Token
   - 使用环境变量存储敏感信息
   - 定期轮换API Token

2. **图片处理**:
   - 验证输入图片的来源和格式
   - 避免处理敏感或受版权保护的内容
   - 遵守相关法律法规

3. **网络请求**:
   - 使用HTTPS进行API调用
   - 设置合理的超时时间
   - 处理网络异常情况

## 💻 使用示例

### Python 集成

```python
from domi_mcp_client import DomiNanoBananaMCPClient

# 初始化客户端
mcp = DomiNanoBananaMCPClient(mcp_client)

# 生成图片
result = await mcp.generate_image(
    prompt="现代简约风格的办公室",
    size="16x9",
    seed=42
)

if result["success"]:
    print(f"生成的图片: {result['image_url']}")
```

### JavaScript 集成

```javascript
const { DomiNanoBananaMCPClient } = require('./domi-mcp-client');

// 初始化客户端
const mcp = new DomiNanoBananaMCPClient(mcpClient);

// 编辑图片
const editResult = await mcp.editImage({
  image: "https://example.com/image.jpg",
  prompt: "将背景改为蓝色，添加云朵"
});

if (editResult.success) {
  console.log(`编辑后的图片: ${editResult.image_url}`);
}
```

### 批量处理

```python
# 批量生成社交媒体内容
prompts = [
    "温暖的品牌形象，柔和色调",
    "科技感设计，现代简约",
    "自然风景，清新空气"
]

results = await mcp.batch_generate(prompts, size="1x1")
successful = sum(1 for r in results if r["result"]["success"])
print(f"成功生成 {successful}/{len(prompts)} 张图片")
```

## 🏗️ 项目结构

```
domi-nano-banana-mcp/
├── README.md                    # 项目说明
├── QUICK_START.md              # 快速入门指南
├── INTEGRATION_GUIDE.md        # 完整集成指南
├── server.py                   # 主服务文件
├── run.sh                      # 启动脚本
├── requirements.txt            # Python依赖
├── mcp-server.json            # MCP服务器配置
├── src/
│   └── domi_nano_banana_mcp/
│       ├── __init__.py
│       └── tools.py           # 核心工具实现
├── examples/                   # 示例代码
│   ├── python_client.py       # Python客户端示例
│   ├── javascript_client.js   # JavaScript客户端示例
│   └── config_examples.md     # 配置示例
├── tests/                      # 测试文件
│   └── test_mcp_server.py
└── docs/                       # 文档目录
    ├── API_REFERENCE.md       # API参考文档
    ├── DEPLOYMENT.md          # 部署指南
    └── TROUBLESHOOTING.md     # 故障排除
```

### 扩展开发
1. **添加新工具**: 在 `server.py` 中使用 `@mcp.tool` 装饰器
2. **添加提示词**: 使用 `@mcp.prompt` 装饰器
3. **API扩展**: 在 `tools.py` 中添加新的API客户端方法

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目：

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 👨‍💻 作者

**MiniMax Agent** - AI开发助手

## 🆘 支持

如果遇到问题或需要帮助：

1. 查看本文档的常见问题部分
2. 检查API文档和错误日志
3. 提交Issue描述问题

## 🧪 测试

### 运行测试套件

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_mcp_server.py::test_text_to_image -v

# 运行集成测试
python examples/python_client.py
```

### 性能测试

```bash
# 压力测试
python tests/load_test.py --concurrent 10 --requests 100

# 内存使用测试
python tests/memory_test.py
```

## 🛡️ 安全

### 最佳实践

- 🔐 使用环境变量存储API令牌
- 🚫 避免在代码中硬编码敏感信息
- 🔒 启用HTTPS和防火墙
- 📊 实施访问控制和监控

### 安全检查

```bash
# 检查安全配置
python scripts/security_check.py

# 扫描依赖漏洞
pip-audit
```

## 🤝 贡献

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/Inspal2023/domi-nano-banana-mcp.git
cd domi-nano-banana-mcp

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest

# 代码格式化
black src/ tests/
flake8 src/ tests/
```

## 📄 许可证

本项目采用 MIT 许可证。详情请查看 [LICENSE](LICENSE) 文件。

## 🆘 支持

- 📧 邮件支持: support@example.com
- 🐛 问题报告: [GitHub Issues](https://github.com/Inspal2023/domi-nano-banana-mcp/issues)
- 💬 社区讨论: [GitHub Discussions](https://github.com/Inspal2023/domi-nano-banana-mcp/discussions)
- 📖 文档: [在线文档](https://domi-mcp-docs.example.com)

## 🙏 致谢

- [多米API](https://duomiapi.com) - 提供强大的图像生成能力
- [MCP](https://modelcontextprotocol.io) - 标准化协议支持
- [FastMCP](https://github.com/microsoft/fastmcp) - 快速MCP开发框架

## 📈 路线图

- [ ] 支持更多图像格式
- [ ] 批量处理优化
- [ ] 实时进度跟踪
- [ ] Web界面管理
- [ ] API限流和配额管理
- [ ] 多语言客户端库

## 📈 更新日志

### v1.0.0 (2025-11-02)
- 初始版本发布
- 实现文生图和图片编辑功能
- 支持多种图片尺寸
- 完整的集成文档和示例代码
- 添加Python和JavaScript客户端库
- 实现异步任务处理机制
- 完整的错误处理和日志记录

---

**由 MiniMax Agent 开发** | **版本 1.0.0** | **最后更新: 2025-11-02**