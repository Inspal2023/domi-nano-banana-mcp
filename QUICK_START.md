# Domi Nano-Banana MCP 快速入门指南

## 🚀 5分钟快速集成

### 步骤 1: 准备环境
```bash
# 确保你有MCP兼容的客户端（如Claude Desktop）
# 获取多米API令牌
export DOMI_API_TOKEN="your_api_token_here"
```

### 步骤 2: 启动MCP服务
```bash
cd domi-nano-banana-mcp
./run.sh
```

### 步骤 3: 开始使用

#### 基础文生图示例
```javascript
// 生成一张图片
const result = await mcpClient.call_tool("text_to_image", {
  "prompt": "一只可爱的小猫坐在花园里",
  "size": "3x4",
  "seed": 12345
});

console.log("生成的图片:", JSON.parse(result.content[0].text).image_url);
```

#### 基础图片编辑示例
```javascript
// 编辑现有图片
const editResult = await mcpClient.call_tool("image_edit", {
  "image": "https://example.com/image.jpg",
  "prompt": "将背景改为蓝色，添加云朵"
});

console.log("编辑后的图片:", JSON.parse(editResult.content[0].text).image_url);
```

## 📋 核心工具一览

| 工具名称 | 功能 | 复杂度 | 响应时间 |
|---------|------|--------|---------|
| `text_to_image` | 文生图 | ⭐⭐ | 15-30秒 |
| `image_edit` | 图片编辑 | ⭐⭐⭐ | 10-25秒 |
| `validate_api_token` | 验证令牌 | ⭐ | 即时 |
| `get_supported_sizes` | 查询尺寸 | ⭐ | 即时 |

## 🎯 常见使用场景

### 1. 社交媒体内容生成
```javascript
// 生成Instagram帖子图片
const socialImage = await mcpClient.call_tool("text_to_image", {
  "prompt": "现代简约风格的咖啡店内部，温暖灯光，木质装修",
  "size": "1x1", // 正方形适合Instagram
  "seed": 42
});
```

### 2. 网站横幅制作
```javascript
// 生成网站横幅
const banner = await mcpClient.call_tool("text_to_image", {
  "prompt": "科技公司官网横幅，蓝色主调，现代设计",
  "size": "16x9", // 宽屏比例
  "seed": 100
});
```

### 3. 产品图片编辑
```javascript
// 编辑产品图片
const productEdit = await mcpClient.call_tool("image_edit", {
  "image": "product_image_url",
  "prompt": "添加白色背景，使产品更加突出"
});
```

### 4. 头像生成
```javascript
// 生成个人头像
const avatar = await mcpClient.call_tool("text_to_image", {
  "prompt": "专业商务头像，正装，微笑，自然光线",
  "size": "1x1",
  "seed": 999
});
```

## ⚡ 性能优化技巧

### 1. 批量处理
```javascript
async function batchGenerate(prompts) {
  const results = [];
  for (const prompt of prompts) {
    try {
      const result = await mcpClient.call_tool("text_to_image", {
        "prompt": prompt,
        "size": "1x1"
      });
      results.push(JSON.parse(result.content[0].text));
      
      // 避免API限制
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      console.error(`生成失败: ${prompt}`, error);
    }
  }
  return results;
}
```

### 2. 缓存策略
```javascript
// 简单的结果缓存
const cache = new Map();

async function cachedGenerate(prompt, size = "1x1") {
  const cacheKey = `${prompt}_${size}`;
  
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }
  
  const result = await mcpClient.call_tool("text_to_image", {
    "prompt": prompt,
    "size": size
  });
  
  const parsed = JSON.parse(result.content[0].text);
  cache.set(cacheKey, parsed);
  
  return parsed;
}
```

### 3. 错误重试
```javascript
async function retryGenerate(prompt, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const result = await mcpClient.call_tool("text_to_image", {
        "prompt": prompt,
        "size": "1x1"
      });
      return JSON.parse(result.content[0].text);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      console.log(`重试 ${i + 1}/${maxRetries}: ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, 2000 * (i + 1)));
    }
  }
}
```

## 🔧 故障排除

### 快速诊断
```javascript
// 1. 检查API令牌
const tokenCheck = await mcpClient.call_tool("validate_api_token", {
  "api_token": process.env.DOMI_API_TOKEN
});
console.log("令牌状态:", JSON.parse(tokenCheck.content[0].text));

// 2. 检查支持的尺寸
const sizes = await mcpClient.call_tool("get_supported_sizes", {});
console.log("支持尺寸:", JSON.parse(sizes.content[0].text));

// 3. 测试简单生成
const testResult = await mcpClient.call_tool("text_to_image", {
  "prompt": "测试图片",
  "size": "1x1",
  "seed": 1
});
console.log("测试结果:", JSON.parse(testResult.content[0].text));
```

### 常见错误快速解决
- **"API token is required"** → 设置 `DOMI_API_TOKEN` 环境变量
- **"Invalid size"** → 使用支持的尺寸: 1x1, 3x4, 4x3, 9x16, 16x9
- **"Request timeout"** → 增加超时时间，复杂任务需要更多时间
- **"Image generation failed"** → 检查提示词是否合适，尝试简化描述

## 📱 集成到不同平台

### Claude Desktop
在 `claude_desktop_config.json` 中添加：
```json
{
  "mcpServers": {
    "domi-nano-banana": {
      "command": "/path/to/domi-nano-banana-mcp/run.sh",
      "env": {
        "DOMI_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### 自定义应用
```javascript
// 简单的HTTP包装器
class DomiMCPClient {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  async callTool(toolName, args) {
    const response = await fetch(`${this.baseUrl}/tools/${toolName}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify(args)
    });
    
    return await response.json();
  }
}
```

## 💡 创意提示词模板

### 艺术风格
- "印象派风格的花园风景"
- "现代抽象艺术作品"
- "复古海报设计"
- "像素艺术风格"

### 商业用途
- "专业产品展示图"
- "现代办公室环境"
- "科技感界面设计"
- "温暖的品牌形象"

### 个人用途
- "个人头像照片风格"
- "家庭合影背景"
- "宠物可爱瞬间"
- "旅行风景照片"

## 🎨 尺寸选择指南

| 尺寸 | 比例 | 最佳用途 |
|------|------|----------|
| 1x1 | 1:1 | 头像、图标、Instagram帖子 |
| 3x4 | 3:4 | 手机壁纸、海报、书籍封面 |
| 4x3 | 4:3 | 电脑壁纸、演示文稿 |
| 9x16 | 9:16 | 抖音、快手短视频 |
| 16x9 | 16:9 | YouTube缩略图、宽屏视频 |

## 🚀 下一步

1. **查看完整文档**: 阅读 `INTEGRATION_GUIDE.md`
2. **运行示例代码**: 查看 `examples/` 目录
3. **测试所有功能**: 使用 `tests/test_mcp_server.py`
4. **加入社区**: 在GitHub上提交Issue和PR

---

**需要帮助？** 查看完整集成指南或提交GitHub Issue！