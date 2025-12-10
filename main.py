#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语词汇测试系统 - 主程序入口

这是英语词汇测试系统的主入口文件，负责初始化系统并启动测试流程。
系统支持命令行界面和图形界面两种交互方式，本文件是命令行界面的入口点。

作者: Python班级
版本: 1.1
日期: 2025
"""

from vocabulary_tester import VocabularyTester


def main():
    """
    主函数，初始化并运行词汇测试器。
    
    包含错误处理，确保程序在遇到异常时能够优雅地退出。
    """
    # 显示欢迎信息
    print("========== 欢迎使用英语词汇测试系统 ==========")
    print("本系统支持多种词汇测试，帮助您提升英语水平")
    print("支持初中、高中、CET4、CET6、考研、托福、SAT共7个词汇模块")
    print("=====================================")
    
    try:
        # 初始化词汇测试器
        tester = VocabularyTester()
        # 开始测试
        tester.start_test()
    except KeyboardInterrupt:
        print("\n程序已被用户中断。")
    except Exception as e:
        print(f"\n程序运行时发生错误: {e}")
        print("请检查Python环境或联系开发者获取帮助。")
    finally:
        print("\n感谢使用英语词汇测试系统！")


if __name__ == "__main__":
    # 当作为主程序运行时，调用主函数
    main()