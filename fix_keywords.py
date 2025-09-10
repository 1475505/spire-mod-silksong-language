#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复杀戮尖塔JSON文件中预留关键词的空格问题
确保关键词如 NL, [G], [E], [B], [R], [W] 等前后至少有一个英文空格
"""

import json
import os
import re
from typing import Dict, Any

def fix_keywords_in_text(text: str) -> str:
    """
    修复文本中的关键词空格问题
    """
    if not isinstance(text, str):
        return text
    
    # 定义需要处理的关键词模式
    patterns = [
        # 能量符号 [G], [E], [B], [R], [W] - 处理各种边界情况
        (r'([^\s])\[([GEBRW])\]([^\s。，！？])', r'\1 [\2] \3'),  # 前后都没空格
        (r'([^\s])\[([GEBRW])\]', r'\1 [\2]'),  # 前面没空格
        (r'\[([GEBRW])\]([^\s。，！？])', r'[\1] \2'),  # 后面没空格（排除标点）
        
        # NL 换行符 - 处理各种边界情况
        (r'([^\s])NL([^\s])', r'\1 NL \2'),  # 前后都没空格
        (r'([^\s])NL', r'\1 NL'),  # 前面没空格
        (r'NL([^\s])', r'NL \1'),  # 后面没空格
        (r'^NL([^\s])', r'NL \1'),  # 行首后面没空格
    ]
    
    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)
    
    return result

def process_json_value(value: Any) -> Any:
    """
    递归处理JSON值
    """
    if isinstance(value, str):
        return fix_keywords_in_text(value)
    elif isinstance(value, dict):
        return {k: process_json_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [process_json_value(item) for item in value]
    else:
        return value

def fix_json_file(file_path: str) -> bool:
    """
    修复单个JSON文件
    """
    try:
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 处理数据
        fixed_data = process_json_value(data)
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 已处理: {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        print(f"✗ 处理失败 {os.path.basename(file_path)}: {e}")
        return False

def main():
    """
    主函数
    """
    silksong_dir = "d:\\sts-mod-silksong-language\\src\\main\\resources\\localization\\silksong"
    
    if not os.path.exists(silksong_dir):
        print(f"错误: 目录不存在 {silksong_dir}")
        return
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(silksong_dir) if f.endswith('.json')]
    
    if not json_files:
        print("未找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件")
    print("开始处理...\n")
    
    success_count = 0
    for json_file in sorted(json_files):
        file_path = os.path.join(silksong_dir, json_file)
        if fix_json_file(file_path):
            success_count += 1
    
    print(f"\n处理完成: {success_count}/{len(json_files)} 个文件成功")

if __name__ == "__main__":
    main()