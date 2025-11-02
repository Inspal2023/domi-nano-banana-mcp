"""多米nano-banana API工具实现

提供文生图和图片编辑功能的具体实现
"""

import os
import json
import time
import base64
import requests
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urlparse


class DomiNanoBananaAPI:
    """多米nano-banana API客户端"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        初始化API客户端
        
        Args:
            api_token: API认证令牌，如果为None则从环境变量获取
        """
        self.api_token = api_token or os.getenv('DOMI_API_TOKEN')
        
        # 多米API端点
        self.base_url = "https://duomiapi.com"
        self.text_to_image_url = f"{self.base_url}/api/gemini/nano-banana"
        self.image_edit_url = f"{self.base_url}/api/gemini/nano-banana-edit"
        
        # 请求头
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _validate_image_url(self, url: str) -> bool:
        """验证图片URL是否有效"""
        try:
            parsed = urlparse(url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    def _is_base64(self, data: str) -> bool:
        """检查字符串是否为base64编码"""
        if not data or not data.strip():
            return False
        try:
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False
    
    def text_to_image(
        self, 
        prompt: str, 
        size: str = "1x1", 
        seed: int = -1,
        **kwargs
    ) -> Dict[str, Any]:
        """
        文生图功能
        
        Args:
            prompt: 图像描述文本
            size: 图片尺寸，支持: 1x1, 3x4, 4x3, 9x16, 16x9
            seed: 随机种子，-1表示随机
            **kwargs: 其他参数
            
        Returns:
            包含生成结果的字典
        """
        # 验证API token
        if not self.api_token:
            return {
                "success": False,
                "error": "API token is required. Set DOMI_API_TOKEN environment variable or pass api_token parameter.",
                "error_code": "MISSING_API_TOKEN"
            }
        
        try:
            # 验证参数
            if not prompt or not prompt.strip():
                return {
                    "success": False,
                    "error": "Prompt cannot be empty",
                    "error_code": "INVALID_PROMPT"
                }
            
            valid_sizes = ["1x1", "3x4", "4x3", "9x16", "16x9"]
            if size not in valid_sizes:
                return {
                    "success": False,
                    "error": f"Invalid size '{size}'. Must be one of: {', '.join(valid_sizes)}",
                    "error_code": "INVALID_SIZE"
                }
            
            # 构建请求数据 - 符合多米API格式
            payload = {
                "prompt": prompt.strip(),
                "size": size
            }
            
            if seed != -1:
                payload["seed"] = seed
            
            # 添加其他参数
            for key, value in kwargs.items():
                if value is not None:
                    payload[key] = value
            
            # 发送请求
            response = requests.post(
                self.text_to_image_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                
                # 多米API异步任务模式
                if result.get("code") == 200 and "data" in result and "task_id" in result["data"]:
                    # 获取任务ID并轮询状态
                    task_id = result["data"]["task_id"]
                    return self._poll_generation_status(task_id)
                else:
                    return {
                        "success": False,
                        "error": f"Unexpected API response format: {result}",
                        "error_code": "UNEXPECTED_RESPONSE"
                    }
            else:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text}"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "error_code": "API_ERROR"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout",
                "error_code": "TIMEOUT"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "error_code": "REQUEST_ERROR"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_code": "UNKNOWN_ERROR"
            }
    
    def image_edit(
        self,
        image: str,
        prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        图片编辑功能
        
        Args:
            image: 原图片URL或base64编码
            prompt: 编辑指令
            **kwargs: 其他参数
            
        Returns:
            包含编辑结果的字典
        """
        # 验证API token
        if not self.api_token:
            return {
                "success": False,
                "error": "API token is required. Set DOMI_API_TOKEN environment variable or pass api_token parameter.",
                "error_code": "MISSING_API_TOKEN"
            }
        
        try:
            # 验证参数
            if not image or not image.strip():
                return {
                    "success": False,
                    "error": "Image cannot be empty",
                    "error_code": "INVALID_IMAGE"
                }
            
            if not prompt or not prompt.strip():
                return {
                    "success": False,
                    "error": "Prompt cannot be empty",
                    "error_code": "INVALID_PROMPT"
                }
            
            # 确定图片输入格式
            if self._validate_image_url(image):
                image_input = {"url": image.strip()}
            elif self._is_base64(image):
                image_input = {"data": image.strip()}
            else:
                return {
                    "success": False,
                    "error": "Invalid image format. Must be a valid URL or base64 encoded string",
                    "error_code": "INVALID_IMAGE_FORMAT"
                }
            
            # 构建请求数据 - 多米API图片编辑格式
            payload = {
                "prompt": prompt.strip(),
                "image_urls": [image.strip()] if isinstance(image, str) else [image]
            }
            
            # 添加其他参数
            for key, value in kwargs.items():
                if value is not None:
                    payload[key] = value
            
            # 发送请求
            response = requests.post(
                self.image_edit_url,
                headers=self.headers,
                json=payload,
                timeout=120  # 编辑可能需要更长时间
            )
            
            # 处理响应 - 多米API图片编辑格式
            if response.status_code == 200:
                result = response.json()
                
                # 多米API图片编辑返回异步任务格式
                if result.get("code") == 200 and "data" in result and "task_id" in result["data"]:
                    task_id = result["data"]["task_id"]
                    return self._poll_edit_status(task_id)
                else:
                    return {
                        "success": False,
                        "error": f"Unexpected edit API response: {result}",
                        "error_code": "UNEXPECTED_EDIT_RESPONSE"
                    }
            else:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f": {response.text}"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "error_code": "API_ERROR"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout",
                "error_code": "TIMEOUT"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "error_code": "REQUEST_ERROR"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_code": "UNKNOWN_ERROR"
            }
    
    def _poll_edit_status(self, task_id: str, max_attempts: int = 30) -> Dict[str, Any]:
        """
        轮询异步编辑任务状态
        
        Args:
            task_id: 编辑任务ID
            max_attempts: 最大轮询次数
            
        Returns:
            最终结果
        """
        status_url = f"{self.base_url}/api/gemini/nano-banana/status"
        
        for attempt in range(max_attempts):
            try:
                # 构建状态查询请求
                payload = {"id": task_id}
                
                response = requests.post(
                    status_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 检查状态
                    if result.get("code") == 200 and "data" in result:
                        status_data = result["data"]
                        status = status_data.get("state", "unknown")
                        status_code = status_data.get("status", "0")
                        
                        if status == "succeeded" or status_code == "3":
                            # 任务完成，提取图片URL
                            image_url = ""
                            if "data" in status_data and "images" in status_data["data"]:
                                images = status_data["data"]["images"]
                                if len(images) > 0:
                                    image_url = images[0].get("url", "")
                            
                            if image_url:
                                return {
                                    "success": True,
                                    "image_url": image_url,
                                    "metadata": {
                                        "task_id": task_id,
                                        "status": status,
                                        "status_code": status_code,
                                        "action": status_data.get("action", "edit"),
                                        "model": "nano-banana-edit"
                                    }
                                }
                            else:
                                return {
                                    "success": False,
                                    "error": f"No edited image URL in completed task: {status_data}",
                                    "error_code": "NO_EDITED_IMAGE"
                                }
                        elif status == "failed" or status_code == "4":
                            error_msg = status_data.get("msg", "Image editing failed")
                            return {
                                "success": False,
                                "error": error_msg,
                                "error_code": "EDIT_FAILED"
                            }
                        elif status_code in ["0", "1", "2"] or status in ["pending", "processing", "queued", "running"]:
                            # 继续轮询
                            time.sleep(3)
                            continue
                        else:
                            return {
                                "success": False,
                                "error": f"Unknown edit task status: {status} (code: {status_code})",
                                "error_code": "UNKNOWN_STATUS"
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"Invalid edit status response: {result}",
                            "error_code": "INVALID_STATUS_RESPONSE"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Edit status check failed with status {response.status_code}: {response.text}",
                        "error_code": "STATUS_CHECK_ERROR"
                    }
                    
            except Exception as e:
                if attempt == max_attempts - 1:
                    return {
                        "success": False,
                        "error": f"Edit status polling failed: {str(e)}",
                        "error_code": "POLLING_ERROR"
                    }
                time.sleep(3)
        
        return {
            "success": False,
            "error": "Image editing timeout",
            "error_code": "TIMEOUT"
        }
    
    def _poll_generation_status(self, task_id: str, max_attempts: int = 30) -> Dict[str, Any]:
        """
        轮询文生图任务状态
        
        Args:
            task_id: 任务ID
            max_attempts: 最大轮询次数
            
        Returns:
            最终结果
        """
        status_url = f"{self.base_url}/api/gemini/nano-banana/status"
        
        for attempt in range(max_attempts):
            try:
                # 构建状态查询请求 - 多米API使用"id"参数
                payload = {"id": task_id}
                
                response = requests.post(
                    status_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 检查状态 - 多米API响应格式
                    if result.get("code") == 200 and "data" in result:
                        status_data = result["data"]
                        status = status_data.get("state", "unknown")  # 使用state字段
                        
                        # 多米API状态码：0=pending, 1=running, 2=processing, 3=succeeded, 4=failed
                        status_code = status_data.get("status", "0")
                        
                        if status == "succeeded" or status_code == "3":
                            # 任务完成，提取图片URL
                            image_url = ""
                            if "data" in status_data and "images" in status_data["data"]:
                                images = status_data["data"]["images"]
                                if len(images) > 0:
                                    image_url = images[0].get("url", "")
                            
                            if image_url:
                                return {
                                    "success": True,
                                    "image_url": image_url,
                                    "metadata": {
                                        "task_id": task_id,
                                        "status": status,
                                        "status_code": status_code,
                                        "create_time": status_data.get("create_time"),
                                        "update_time": status_data.get("update_time"),
                                        "model": "nano-banana"
                                    }
                                }
                            else:
                                return {
                                    "success": False,
                                    "error": f"No image URL in completed task: {status_data}",
                                    "error_code": "NO_IMAGE_IN_COMPLETED_TASK"
                                }
                        elif status == "failed" or status_code == "4":
                            error_msg = status_data.get("msg", "Image generation failed")
                            return {
                                "success": False,
                                "error": error_msg,
                                "error_code": "GENERATION_FAILED"
                            }
                        elif status_code in ["0", "1", "2"] or status in ["pending", "processing", "queued", "running"]:
                            # 继续轮询
                            time.sleep(3)
                            continue
                        else:
                            return {
                                "success": False,
                                "error": f"Unknown task status: {status} (raw: {status_data.get('status')})",
                                "error_code": "UNKNOWN_STATUS"
                            }
                    else:
                        return {
                            "success": False,
                            "error": f"Invalid status response: {result}",
                            "error_code": "INVALID_STATUS_RESPONSE"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Status check failed with status {response.status_code}: {response.text}",
                        "error_code": "STATUS_CHECK_ERROR"
                    }
                    
            except Exception as e:
                if attempt == max_attempts - 1:
                    return {
                        "success": False,
                        "error": f"Status polling failed: {str(e)}",
                        "error_code": "POLLING_ERROR"
                    }
                time.sleep(3)
        
        return {
            "success": False,
            "error": "Image generation timeout",
            "error_code": "TIMEOUT"
        }