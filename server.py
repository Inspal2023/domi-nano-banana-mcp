"""多米nano-banana文生图和图片编辑MCP服务器

使用FastMCP框架实现的完整MCP服务器，提供文本生成图像和图片编辑功能
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from src.domi_nano_banana_mcp.tools import DomiNanoBananaAPI

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建MCP服务器实例
mcp = FastMCP("多米nano-banana图像生成服务器")

# 全局API客户端实例
_api_client: Optional[DomiNanoBananaAPI] = None


def get_api_client() -> DomiNanoBananaAPI:
    """获取API客户端实例"""
    global _api_client
    if _api_client is None:
        _api_client = DomiNanoBananaAPI()
    return _api_client


@mcp.tool
def text_to_image(
    prompt: str,
    size: str = "1x1",
    seed: int = -1,
    api_token: Optional[str] = None
) -> str:
    """
    文生图功能 - 根据文本描述生成图片
    
    使用多米API的nano-banana模型（基于Gemini 2.5 Flash）根据文本描述生成高质量图像。
    支持多种图片尺寸和随机种子控制。
    
    Args:
        prompt: 图像描述文本，详细描述希望生成的图像内容
                建议包含风格、色彩、构图等详细信息以获得最佳效果
        size: 图片尺寸，默认为"1x1"
              可选值：
              - "1x1": 正方形 (1024x1024)
              - "3x4": 垂直矩形 (768x1024)
              - "4x3": 水平矩形 (1024x768)
              - "9x16": 竖屏比例 (576x1024)
              - "16x9": 宽屏比例 (1024x576)
        seed: 随机种子，默认为-1（随机生成）
              设置固定值可以获得可重现的结果
        api_token: 多米API的Bearer Token，可选
                  如果不提供，将从环境变量DOMI_API_TOKEN获取
    
    Returns:
        JSON格式的结果字符串，包含：
        - success: 操作是否成功
        - image_url: 生成的图片URL地址
        - metadata: 图片元数据（提示词、尺寸、种子值、生成时间等）
        - error: 错误信息（如果失败）
        - error_code: 错误代码（如果失败）
    """
    try:
        # 验证必需参数
        if not prompt or not prompt.strip():
            return json.dumps({
                "success": False,
                "error": "Prompt is required and cannot be empty",
                "error_code": "INVALID_PROMPT"
            }, ensure_ascii=False)
        
        # 验证尺寸参数
        valid_sizes = ["1x1", "3x4", "4x3", "9x16", "16x9"]
        if size not in valid_sizes:
            return json.dumps({
                "success": False,
                "error": f"Invalid size '{size}'. Must be one of: {', '.join(valid_sizes)}",
                "error_code": "INVALID_SIZE"
            }, ensure_ascii=False)
        
        # 创建API客户端
        if api_token:
            client = DomiNanoBananaAPI(api_token=api_token)
        else:
            client = get_api_client()
        
        # 调用API
        result = client.text_to_image(
            prompt=prompt.strip(),
            size=size,
            seed=seed
        )
        
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Text to image error: {str(e)}")
        return json.dumps({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "error_code": "INTERNAL_ERROR"
        }, ensure_ascii=False)


@mcp.tool
def image_edit(
    image: str,
    prompt: str,
    api_token: Optional[str] = None
) -> str:
    """
    图片编辑功能 - 对现有图片进行智能编辑
    
    使用多米API的nano-banana编辑功能对现有图片进行智能修改和优化。
    支持基于文本指令的图像编辑，包括风格转换、内容修改、元素添加等。
    
    Args:
        image: 原图片，可以是以下格式之一：
               - 图片URL地址（推荐）
               - Base64编码的图片数据
        prompt: 编辑指令，详细描述希望对图片进行的修改
                例如："将背景改为蓝色，添加一些云朵"
        api_token: 多米API的Bearer Token，可选
                  如果不提供，将从环境变量DOMI_API_TOKEN获取
    
    Returns:
        JSON格式的结果字符串，包含：
        - success: 操作是否成功
        - image_url: 编辑后的图片URL地址
        - metadata: 编辑元数据（处理时间、模型信息等）
        - error: 错误信息（如果失败）
        - error_code: 错误代码（如果失败）
    """
    try:
        # 验证必需参数
        if not image or not image.strip():
            return json.dumps({
                "success": False,
                "error": "Image is required and cannot be empty",
                "error_code": "INVALID_IMAGE"
            }, ensure_ascii=False)
        
        if not prompt or not prompt.strip():
            return json.dumps({
                "success": False,
                "error": "Prompt is required and cannot be empty",
                "error_code": "INVALID_PROMPT"
            }, ensure_ascii=False)
        
        # 创建API客户端
        if api_token:
            client = DomiNanoBananaAPI(api_token=api_token)
        else:
            client = get_api_client()
        
        # 调用API
        result = client.image_edit(
            image=image.strip(),
            prompt=prompt.strip()
        )
        
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Image edit error: {str(e)}")
        return json.dumps({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "error_code": "INTERNAL_ERROR"
        }, ensure_ascii=False)


@mcp.tool
def get_supported_sizes() -> str:
    """
    获取支持的图片尺寸列表
    
    返回当前API支持的所有图片尺寸选项及其说明。
    
    Returns:
        JSON格式的尺寸列表信息
    """
    sizes_info = {
        "supported_sizes": [
            {
                "size": "1x1",
                "description": "正方形图片 (1024x1024)",
                "use_case": "适合头像、图标、社交媒体帖子"
            },
            {
                "size": "3x4",
                "description": "垂直矩形 (768x1024)",
                "use_case": "适合手机壁纸、海报、书籍封面"
            },
            {
                "size": "4x3",
                "description": "水平矩形 (1024x768)",
                "use_case": "适合电脑壁纸、演示文稿、网页横幅"
            },
            {
                "size": "9x16",
                "description": "竖屏比例 (576x1024)",
                "use_case": "适合抖音、快手等短视频平台"
            },
            {
                "size": "16x9",
                "description": "宽屏比例 (1024x576)",
                "use_case": "适合YouTube缩略图、宽屏视频"
            }
        ],
        "default_size": "1x1",
        "recommendation": "选择尺寸时考虑最终使用场景，以获得最佳显示效果"
    }
    
    return json.dumps(sizes_info, ensure_ascii=False)


@mcp.tool
def validate_api_token(api_token: str) -> str:
    """
    验证API令牌的有效性
    
    检查提供的API令牌是否有效，并返回验证结果。
    
    Args:
        api_token: 要验证的API令牌
    
    Returns:
        JSON格式的验证结果
    """
    try:
        # 创建临时客户端进行验证
        client = DomiNanoBananaAPI(api_token=api_token)
        
        # 尝试一个简单的API调用来验证令牌
        test_result = client.text_to_image(
            prompt="test",
            size="1x1",
            seed=1
        )
        
        # 如果API调用成功（即使生成失败），说明令牌有效
        if "error_code" not in test_result or test_result["error_code"] not in ["INVALID_PROMPT", "INVALID_SIZE"]:
            return json.dumps({
                "valid": True,
                "message": "API token is valid",
                "test_result": test_result
            }, ensure_ascii=False)
        else:
            return json.dumps({
                "valid": False,
                "message": "API token appears to be invalid",
                "error": test_result.get("error", "Unknown validation error")
            }, ensure_ascii=False)
            
    except Exception as e:
        return json.dumps({
            "valid": False,
            "message": f"Token validation failed: {str(e)}",
            "error": str(e)
        }, ensure_ascii=False)


@mcp.prompt
def image_generation_prompt(subject: str, style: str = "realistic", size: str = "1x1") -> str:
    """
    生成图像提示词模板
    
    为图像生成创建优化的提示词模板，包含主题、风格和构图建议。
    
    Args:
        subject: 图像主题描述
        style: 艺术风格，默认为"realistic"
               可选值：realistic, artistic, cartoon, anime, abstract等
        size: 图片尺寸，默认为"1x1"
    
    Returns:
        优化的提示词文本
    """
    style_descriptions = {
        "realistic": "照片级真实感，高清细节，专业摄影",
        "artistic": "艺术风格，创意构图，色彩丰富",
        "cartoon": "卡通风格，可爱生动，色彩鲜明",
        "anime": "动漫风格，精致画风，角色设计",
        "abstract": "抽象艺术，现代设计，概念表达",
        "vintage": "复古风格，怀旧色调，经典构图",
        "minimalist": "极简主义，简洁设计，留白艺术"
    }
    
    style_desc = style_descriptions.get(style, style_descriptions["realistic"])
    
    prompt_template = f"""
创建一个关于{subject}的{style_desc}图像。

建议的构图和细节：
- 主体：{subject}
- 风格：{style_desc}
- 尺寸：{size}
- 质量：高清，细节丰富，色彩饱满
- 光线：自然光线，层次分明
- 构图：居中对称，视觉平衡

请确保图像具有专业水准，适合商业或艺术用途。
"""
    
    return prompt_template.strip()


@mcp.prompt
def image_editing_prompt(original_description: str, editing_request: str) -> str:
    """
    生成图像编辑提示词模板
    
    为图像编辑创建详细的指令模板，确保编辑效果符合预期。
    
    Args:
        original_description: 原图描述
        editing_request: 编辑需求描述
    
    Returns:
        详细的编辑指令文本
    """
    prompt_template = f"""
基于以下原图进行智能编辑：

原图描述：{original_description}

编辑需求：{editing_request}

编辑指导原则：
1. 保持原图的主要构图和风格
2. 自然融合编辑内容，避免违和感
3. 保持色彩协调和视觉平衡
4. 确保编辑后的图像质量清晰
5. 符合实际的物理规律和美学原则

请生成高质量的编辑结果，确保编辑内容与原图完美融合。
"""
    
    return prompt_template.strip()


if __name__ == "__main__":
    # 启动MCP服务器
    mcp.run()