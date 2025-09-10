#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《杀戮尖塔》「丝之歌语言」简化翻译工具

功能：
1. 调用OpenAI API进行翻译
2. 适配杀戮尖塔JSON格式
3. 支持批量翻译
"""

import os
import json
import asyncio
import logging
from typing import Dict, List
from pathlib import Path
from openai import AsyncOpenAI


class SilksongTranslator:
    def __init__(self, api_key: str = None, api_url: str = None):
        """
        初始化翻译器
        
        Args:
            api_key: OpenAI API密钥，如果为None则从环境变量读取
            api_url: API接口URL
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.api_url = api_url or os.getenv('OPENAI_API_URL')

        print(self.api_url)
        
        if not self.api_key:
            raise ValueError("需要提供API密钥，请设置环境变量OPENAI_API_KEY或传入api_key参数")
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.api_url
        )
        
        self.batch_size = 100  # 简化批次大小
        
        # 配置日志系统
        self.setup_logging()
        
        # 加载翻译风格模板
        self.load_prompt_template()
    
    def setup_logging(self, input_file: str = None):
        """配置日志系统"""
        # 创建logger
        self.logger = logging.getLogger('SilksongTranslator')
        self.logger.setLevel(logging.INFO)
        
        # 清除已有的处理器
        self.logger.handlers.clear()
        
        # 创建silksong_test目录（如果不存在）
        os.makedirs('silksong_test', exist_ok=True)
        
        # 根据输入文件名生成日志文件名
        if input_file:
            log_filename = os.path.splitext(os.path.basename(input_file))[0] + '.log'
            log_path = f'silksong_test/{log_filename}'
        else:
            log_path = 'silksong_test/translation.log'
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 创建格式器
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 添加处理器到logger
        self.logger.addHandler(file_handler)
    
    def load_prompt_template(self):
        """加载翻译风格模板"""
        try:
            with open('prompt.md', 'r', encoding='utf-8') as f:
                content = f.read()
                self.base_prompt = content.split('-----')[0].strip()
        except FileNotFoundError:
            # 默认prompt
            self.base_prompt = """
你现在是「文盲古文小生」翻译师。请将正常中文改写为半白半文的玄虚风格：

【翻译规则】
1. 核心技法：错置词性语序、乱用拟古词。无需强求改写，适时保留原文，只对有玄虚效果的部分进行修改。
2. 字数控制：与原文大体一致
3. 可读性：确保玩家只能模糊地理解基本含义，不知所云
"""
    
    def build_translation_prompt(self, items: List[tuple]) -> str:
        """构建翻译Prompt"""
        prompt = f"""{self.base_prompt}

【待翻译内容】：
"""
        
        for i, (key, text) in enumerate(items, 1):
            prompt += f"{i}. {key}: {text}\n"
        
        prompt += """

请按照以下JSON格式输出翻译结果：
{
  "translations": [
    {"key": "原始key", "original": "原文", "translation": "丝之歌译文"},
    ...
  ]
}

要求：
1. 严格按照JSON格式输出
2. 保持key不变
3. 译文字数与原文大体一致
4. 保持游戏格式标记（如NL、!D!、[G]等）
"""
        
        return prompt

    async def call_openai_api(self, prompt: str, model: str = "deepseek-chat") -> Dict:
        """调用OpenAI API进行翻译，支持重试机制"""
        max_retries = 3
        base_delay = 1  # 基础延迟时间（秒）
        
        for attempt in range(max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是《杀戮尖塔》「文盲古风小生语言」翻译师。请严格按照JSON格式输出翻译结果。"
                        },
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=1.2,
                    max_tokens=12000
                )
                
                result = json.loads(response.choices[0].message.content)
                return result
                
            except Exception as e:
                error_msg = str(e)
                is_retryable = any(code in error_msg for code in ['502', '503', '504', '429', 'timeout', 'connection'])
                
                if attempt < max_retries and is_retryable:
                    delay = base_delay * (2 ** attempt)  # 指数退避
                    print(f"API调用失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}")
                    print(f"等待 {delay} 秒后重试...")
                    await asyncio.sleep(delay)
                else:
                    print(f"API调用最终失败: {e}")
                    return {"translations": []}
    
    async def translate_file(self, file_path: str, model: str = "deepseek-chat") -> Dict:
        """翻译单个JSON文件"""
        print(f"\n处理文件: {file_path}")
        
        # 加载原始数据
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取待翻译文本
        translation_items = []
        self._extract_translation_items(data, translation_items)
        
        print(f"待翻译条目数: {len(translation_items)}")
        
        # 批量翻译
        all_translations = {}
        for i in range(0, len(translation_items), self.batch_size):
            batch = translation_items[i:i + self.batch_size]
            print(f"翻译批次 {i//self.batch_size + 1}: {len(batch)} 条目")
            
            # 构建prompt并调用API
            prompt = self.build_translation_prompt(batch)
            result = await self.call_openai_api(prompt, model)
            
            # 处理结果
            if 'translations' in result:
                for trans in result['translations']:
                    key = trans.get('key')
                    translation = trans.get('translation')
                    if key and translation:
                        all_translations[key] = translation
            
            # 简单延迟避免频率限制
            if i + self.batch_size < len(translation_items):
                await asyncio.sleep(1)
        
        # 重建JSON结构
        return self.rebuild_json_structure(data, all_translations)
    
    def _extract_translation_items(self, data, translation_items, prefix=""):
        """递归提取待翻译文本"""
        if isinstance(data, dict):
            for key, item_data in data.items():
                current_prefix = f"{prefix}_{key}" if prefix else key
                
                if isinstance(item_data, dict):
                    # 处理NAME字段
                    if 'NAME' in item_data:
                        translation_items.append((f"{current_prefix}_NAME", item_data['NAME']))
                    elif 'NAMES' in item_data and item_data['NAMES']:
                        # 如果NAMES是列表，把列表里的每一项都提取
                        for idx, name in enumerate(item_data['NAMES']):
                            if isinstance(name, str):
                                translation_items.append((f"{current_prefix}_NAME_{idx}", name))
                    
                    # 处理DESCRIPTION字段
                    if 'DESCRIPTION' in item_data:
                        translation_items.append((f"{current_prefix}_DESC", item_data['DESCRIPTION']))
                    elif 'UPGRADE_DESCRIPTION' in item_data:
                        translation_items.append((f"{current_prefix}_UPGRADE_DESC", item_data['UPGRADE_DESCRIPTION']))
                        
                    # 处理TEXT字段（UI文本）
                    if 'TEXT' in item_data:
                        if isinstance(item_data['TEXT'], list):
                            for i, text in enumerate(item_data['TEXT']):
                                translation_items.append((f"{current_prefix}_TEXT_{i}", text))
                        elif isinstance(item_data['TEXT'], str):
                            translation_items.append((f"{current_prefix}_TEXT", item_data['TEXT']))
                    
                    # 处理其他可能包含文本的字段（如UNIQUE_REWARDS, OPTIONS等）
                    for field_name, field_value in item_data.items():
                        if field_name not in ['NAME', 'NAMES', 'DESCRIPTION', 'UPGRADE_DESCRIPTION', 'TEXT']:
                            if isinstance(field_value, list):
                                for i, text in enumerate(field_value):
                                    if isinstance(text, str):
                                        translation_items.append((f"{current_prefix}_{field_name}_{i}", text))
                            elif isinstance(field_value, str):
                                translation_items.append((f"{current_prefix}_{field_name}", field_value))
                            elif isinstance(field_value, dict):
                                # 递归处理嵌套字典
                                self._extract_translation_items(field_value, translation_items, f"{current_prefix}_{field_name}")
                elif isinstance(item_data, list):
                    # 处理直接的列表字段（如keywords.json中的TEXT字段）
                    for i, text in enumerate(item_data):
                        if isinstance(text, str):
                            translation_items.append((f"{current_prefix}_{i}", text))
                        elif isinstance(text, dict):
                            # 如果列表中包含字典，递归处理
                            self._extract_translation_items(text, translation_items, f"{current_prefix}_{i}")
                elif isinstance(item_data, str):
                    # 处理直接的字符串字段
                    translation_items.append((current_prefix, item_data))
                else:
                    # 如果item_data本身不包含翻译字段，但是一个字典容器，继续递归
                    if isinstance(item_data, dict):
                        self._extract_translation_items(item_data, translation_items, current_prefix)
    
    def rebuild_json_structure(self, original_data: Dict, translations: Dict[str, str]) -> Dict:
        """重建JSON结构，将翻译结果合并回原始格式
        - 支持多层嵌套（prefix用下划线连接）
        - 正确处理以下键格式：
          * <path>_NAME
          * <path>_DESC
          * <path>_UPGRADE_DESC
          * <path>_TEXT           (TEXT为字符串)
          * <path>_TEXT_<idx>     (TEXT为列表)
          * <path>_<FIELD>        (任意单字段字符串)
          * <path>_<FIELD>_<idx>  (任意列表字段)
        - 如果字段本身是列表，则把列表里的每一项都翻译
        """
        result_data = json.loads(json.dumps(original_data))  # 深拷贝

        def get_nested_container(root: Dict, path_parts: List[str]):
            """根据路径片段进入嵌套字典，返回目标容器(dict)。若路径不存在则返回None"""
            node = root
            for part in path_parts:
                if isinstance(node, dict) and part in node:
                    node = node[part]
                else:
                    return None
            return node

        for key, translation in translations.items():
            parts = key.split('_')
            if len(parts) < 2:
                continue

            original_text = None

            # 情况一：末尾是固定字段名（无索引）
            if parts[-1] in ("NAME", "DESC", "UPGRADE_DESC", "TEXT"):
                field_tag = parts[-1]
                container_path = parts[:-1]
                container = get_nested_container(result_data, container_path)
                if not isinstance(container, dict):
                    continue

                if field_tag == 'NAME':
                    if 'NAME' in container and isinstance(container['NAME'], str):
                        original_text = container['NAME']
                        container['NAME'] = translation
                    elif 'NAMES' in container and isinstance(container['NAMES'], list):
                        # 如果NAMES是列表，把列表里的每一项都翻译
                        for idx, item in enumerate(container['NAMES']):
                            if isinstance(item, str):
                                original_text = item
                                container['NAMES'][idx] = translation
                                self.logger.info(f"翻译: [{key}_{idx}] {original_text} -> {translation}")
                        continue  # 已经记录日志，跳过下面的统一记录
                elif field_tag == 'DESC':
                    if 'DESCRIPTION' in container and isinstance(container['DESCRIPTION'], str):
                        original_text = container['DESCRIPTION']
                        container['DESCRIPTION'] = translation
                elif field_tag == 'UPGRADE_DESC':
                    if 'UPGRADE_DESCRIPTION' in container and isinstance(container['UPGRADE_DESCRIPTION'], str):
                        original_text = container['UPGRADE_DESCRIPTION']
                        container['UPGRADE_DESCRIPTION'] = translation
                elif field_tag == 'TEXT':
                    if 'TEXT' in container and isinstance(container['TEXT'], str):
                        original_text = container['TEXT']
                        container['TEXT'] = translation
                    elif 'TEXT' in container and isinstance(container['TEXT'], list):
                        # 如果TEXT是列表，把列表里的每一项都翻译
                        for idx, item in enumerate(container['TEXT']):
                            if isinstance(item, str):
                                original_text = item
                                container['TEXT'][idx] = translation
                                self.logger.info(f"翻译: [{key}_{idx}] {original_text} -> {translation}")
                        continue  # 已经记录日志，跳过下面的统一记录

            # 情况二：末尾是索引（列表项），如 _TEXT_3 或 _OPTIONS_1
            elif parts[-1].isdigit():
                idx = int(parts[-1])
                
                if len(parts) >= 3:
                    # 标准情况：container_field_idx
                    field_name = parts[-2]
                    container_path = parts[:-2]
                    container = get_nested_container(result_data, container_path)
                    if not isinstance(container, dict):
                        continue

                    # NAME列表（NAMES字段）
                    if field_name == 'NAME':
                        if 'NAMES' in container and isinstance(container['NAMES'], list) and 0 <= idx < len(container['NAMES']):
                            if isinstance(container['NAMES'][idx], str):
                                original_text = container['NAMES'][idx]
                                container['NAMES'][idx] = translation
                    # TEXT列表
                    elif field_name == 'TEXT':
                        if 'TEXT' in container and isinstance(container['TEXT'], list) and 0 <= idx < len(container['TEXT']):
                            original_text = container['TEXT'][idx]
                            container['TEXT'][idx] = translation
                    else:
                        # 其他列表字段（如 OPTIONS、UNIQUE_REWARDS 等）
                        if field_name in container and isinstance(container[field_name], list) and 0 <= idx < len(container[field_name]):
                            if isinstance(container[field_name][idx], str):
                                original_text = container[field_name][idx]
                                container[field_name][idx] = translation
                elif len(parts) == 2:
                    # 直接列表字段情况：field_idx（如 TEXT_0）
                    field_name = parts[0]
                    container = result_data
                    if field_name in container and isinstance(container[field_name], list) and 0 <= idx < len(container[field_name]):
                        if isinstance(container[field_name][idx], str):
                            original_text = container[field_name][idx]
                            container[field_name][idx] = translation

            # 情况三：任意单字段字符串，如 _FOOTER 之类
            else:
                if len(parts) == 1:
                    # 直接字符串字段情况（如单独的字符串字段）
                    field_name = parts[0]
                    container = result_data
                    if field_name in container and isinstance(container[field_name], str):
                        original_text = container[field_name]
                        container[field_name] = translation
                else:
                    # 嵌套字段情况
                    field_name = parts[-1]
                    container_path = parts[:-1]
                    container = get_nested_container(result_data, container_path)
                    if not isinstance(container, dict):
                        continue
                    if field_name in container and isinstance(container[field_name], str):
                        original_text = container[field_name]
                        container[field_name] = translation

            # 记录日志（列表翻译已在循环内记录，这里只记录单个字符串的翻译）
            if original_text is not None:
                self.logger.info(f"翻译: [{key}] {original_text} -> {translation}")

        return result_data


# 简单的使用示例
async def translate_single_file(input_file: str, output_file: str = None, model: str = "deepseek-chat"):
    """翻译单个文件的简单接口"""
    translator = SilksongTranslator()
    # 重新配置日志系统以使用基于文件名的日志文件
    translator.setup_logging(input_file)
    
    result = await translator.translate_file(input_file, model)
    
    if output_file is None:
        output_file = "silksong/" + os.path.basename(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"翻译完成，保存到: {output_file}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python trans.py <输入文件> [输出文件] [模型]")
        print("示例: python trans.py zhs/cards.json silksong/cards.json deepseek-chat")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    model = sys.argv[3] if len(sys.argv) > 3 else "deepseek-v3.1"
    
    asyncio.run(translate_single_file(input_file, output_file, model))