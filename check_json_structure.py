#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

# 检查JSON文件的基本结构

def check_json_structure(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            # 使用迭代器方式加载文件，避免一次性加载整个大文件
            data = json.load(f)
            
            if not isinstance(data, list):
                print(f"错误: {os.path.basename(json_file)} 不是一个JSON数组")
                return False
                
            if len(data) == 0:
                print(f"警告: {os.path.basename(json_file)} 是空的")
                return False
                
            # 检查第一个条目是否包含必要的字段
            first_item = data[0]
            print(f"文件 {os.path.basename(json_file)} 包含 {len(data)} 个词汇条目")
            print(f"第一个条目的键: {list(first_item.keys())}")
            
            # 检查是否包含vocabulary_tester.py中需要的字段
            required_fields = ['word', 'translations', 'phrases']
            missing_fields = [field for field in required_fields if field not in first_item]
            
            if missing_fields:
                print(f"警告: 缺少必要字段: {missing_fields}")
                # 即使缺少字段也继续检查内容
            
            # 检查translations字段的结构
            if 'translations' in first_item:
                translations = first_item['translations']
                print(f"translations字段类型: {type(translations).__name__}")
                if isinstance(translations, list) and translations:
                    print(f"第一个翻译条目的结构: {translations[0]}")
                    if 'translation' not in translations[0]:
                        print("警告: translations中的条目缺少translation字段")
            
            # 检查phrases字段的结构
            if 'phrases' in first_item:
                phrases = first_item['phrases']
                print(f"phrases字段类型: {type(phrases).__name__}")
                if isinstance(phrases, list) and phrases:
                    print(f"第一个短语条目的结构: {phrases[0]}")
                    if 'phrase' not in phrases[0] or 'translation' not in phrases[0]:
                        print("警告: phrases中的条目缺少phrase或translation字段")
            
            return True
            
    except json.JSONDecodeError as e:
        print(f"JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return False

if __name__ == "__main__":
    # 检查当前目录下json文件夹中的所有JSON文件
    json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json")
    
    if not os.path.exists(json_dir):
        print(f"错误: 找不到json文件夹: {json_dir}")
        exit(1)
    
    # 获取所有JSON文件
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"错误: json文件夹中没有找到JSON文件")
        exit(1)
    
    print(f"找到 {len(json_files)} 个JSON文件，开始检查...\n")
    
    # 检查每个文件
    for json_file in json_files:
        print(f"\n===== 检查文件: {json_file} =====")
        full_path = os.path.join(json_dir, json_file)
        check_json_structure(full_path)
    
    print("\n检查完成!")