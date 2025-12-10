#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

# 查看词汇JSON文件的格式
def check_json_format(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            # 只加载前10个元素来查看格式
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                print(f"文件 {os.path.basename(json_file)} 包含 {len(data)} 个词汇条目")
                print("前3个条目的格式:")
                for i, item in enumerate(data[:3], 1):
                    print(f"条目 {i}: {item}")
                    print("键值对:")
                    for key, value in item.items():
                        print(f"  {key}: {value}")
                    print()
    except Exception as e:
        print(f"读取文件时出错: {e}")

if __name__ == "__main__":
    # 获取当前脚本所在目录，然后构建json文件夹的路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(script_dir, "json")
    
    # 检查初中词汇文件格式
    json_file = os.path.join(json_dir, "1-初中-顺序.json")
    
    if os.path.exists(json_file):
        check_json_format(json_file)
    else:
        print(f"错误: 找不到文件 {json_file}")
        print("请确保json文件夹存在于当前项目目录中")