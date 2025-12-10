#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试脚本：验证错题本保存功能
"""
import os
import subprocess
import time
import glob

def test_mistake_book():
    """测试错题本保存功能"""
    print("=== 开始测试错题本保存功能 ===")
    
    # 清理之前的测试错题本文件
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    old_mistake_files = glob.glob(os.path.join(data_dir, "错题本_*.txt"))
    for f in old_mistake_files:
        try:
            os.remove(f)
            print(f"已清理旧错题本文件: {f}")
        except Exception as e:
            print(f"清理旧文件失败: {e}")
    
    # 启动测试进程
    cmd = ["python", "main.py"]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    try:
        # 等待程序启动
        time.sleep(1)
        
        # 1. 选择模块 (1 - 初中)
        process.stdin.write("1\n")
        process.stdin.flush()
        time.sleep(0.5)
        print("已选择初中词汇模块")
        
        # 2. 选择测试模式 (2 - 英文模式)
        process.stdin.write("2\n")
        process.stdin.flush()
        time.sleep(0.5)
        print("已选择英文测试模式")
        
        # 3. 故意答错几道题
        for i in range(3):
            # 故意选择错误答案 (假设正确答案不是1)
            process.stdin.write("1\n")
            process.stdin.flush()
            time.sleep(0.5)
            print(f"已回答第{i+1}题 (故意答错)")
        
        # 4. 退出测试
        process.stdin.write("quit\n")
        process.stdin.flush()
        time.sleep(1)
        print("已退出测试")
        
        # 5. 选择保存错题本
        process.stdin.write("y\n")
        process.stdin.flush()
        time.sleep(1)
        print("已选择保存错题本")
        
        # 获取输出
        stdout, stderr = process.communicate(timeout=10)
        
        # 检查输出
        print("\n=== 测试输出 ===")
        print(stdout)
        
        if stderr:
            print("\n=== 错误信息 ===")
            print(stderr)
        
        # 检查错题本是否保存成功
        new_mistake_files = glob.glob(os.path.join(data_dir, "错题本_*.txt"))
        if new_mistake_files:
            print(f"\n✅ 测试成功！错题本已保存到data目录:")
            for f in new_mistake_files:
                print(f"   - {os.path.basename(f)}")
                print(f"     完整路径: {f}")
            return True
        else:
            print("\n❌ 测试失败！未在data目录找到错题本文件")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        print("\n❌ 测试超时")
        return False
    except Exception as e:
        process.kill()
        print(f"\n❌ 测试过程中发生错误: {e}")
        return False
    finally:
        if process.poll() is None:
            process.kill()

if __name__ == "__main__":
    test_mistake_book()