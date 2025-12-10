# 英语词汇测试系统

[![Python 3.6+](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release/yourusername/english-vocabulary-tester.svg)](https://GitHub.com/yourusername/english-vocabulary-tester/releases/)

## 系统简介

本系统是一个功能完善的英语词汇测试应用程序，支持多种词汇模块（初中、高中、CET4、CET6、考研、托福、SAT）和测试模式（中文模式和英文模式），帮助用户高效学习和记忆英语词汇。系统提供命令行界面和图形用户界面(GUI)两种使用方式，满足不同用户的需求。

## 功能特点

### 1. 多模块词汇支持
- 初中词汇
- 高中词汇
- 大学英语四级(CET4)
- 大学英语六级(CET6)
- 考研词汇
- 托福词汇
- SAT词汇

### 2. 灵活的测试模式
- **中文模式**：显示中文释义，选择对应的英文单词
- **英文模式**：显示英文单词，选择对应的中文释义

### 3. 智能题目生成
- 随机抽取词汇
- 自动生成4个选项（1个正确答案，3个干扰项）
- 选项随机排序，增加挑战性

### 4. 实时统计功能
- 显示已答题数、正确数、错误数
- 计算并显示正确率
- 估算词汇认识率和已掌握词汇数量

### 5. 错题管理
- 自动记录所有答错的题目
- 退出测试时显示错题详情
- 支持导出错题本为文本文件，方便复习

### 6. 多界面支持
- **命令行界面**：轻量级，适合快速使用
- **图形用户界面(GUI)**：直观友好，操作便捷

### 7. 便捷操作
- 输入数字1-4选择答案
- 输入'quit'或'q'随时退出测试
- 无需按回车键确认继续，答题后自动进入下一题

## 安装要求

- Python 3.6 或更高版本
- 无需额外第三方库依赖（使用Python标准库）

## 使用方法

### 方法一：使用图形界面（推荐）
1. 双击运行 `gui.py` 文件
2. 在图形界面中点击【启动测试】按钮
3. 使用界面中的输入框和按钮进行操作

### 方法二：使用命令行
1. 打开命令提示符
2. 切换到程序所在目录
3. 执行命令：`python main.py`
4. 按照命令行提示进行操作

### 详细终端操作指南

有关如何在不同操作系统上通过终端命令打开和使用软件的详细说明，请参阅：
[OPERATION_GUIDE.md](OPERATION_GUIDE.md)

### 答题流程
1. **选择词汇模块**：输入1-7之间的数字选择您需要的词汇模块
2. **选择测试模式**：输入1选择中文模式，输入2选择英文模式
3. **开始测试**：
   - 查看题目和4个选项（1-4）
   - 输入对应数字选择您认为正确的答案
   - 系统立即显示答题结果
4. **退出测试**：输入'quit'或'q'退出测试
5. **查看统计**：退出时查看测试统计信息，可选择保存错题本

## 文件结构

```
english-vocabulary-tester/
├── main.py                    # 命令行程序入口文件
├── vocabulary_tester.py       # 核心功能类，包含所有测试功能实现
├── gui.py                     # 图形界面实现文件
├── check_json_format.py       # 辅助脚本，用于检查词汇JSON文件格式
├── check_json_structure.py    # JSON文件结构验证脚本
├── .gitignore                 # Git忽略文件配置
├── README.md                  # 程序说明文档
├── LICENSE                    # 许可证文件
├── requirements.txt           # 项目依赖文件
├── data/                      # 用户数据存储目录
└── json/                      # 词汇数据文件夹
    ├── 1-初中-顺序.json       # 初中词汇数据
    ├── 2-高中-顺序.json       # 高中词汇数据
    ├── 3-CET4-顺序.json       # 大学英语四级词汇数据
    ├── 4-CET6-顺序.json       # 大学英语六级词汇数据
    ├── 5-考研-顺序.json       # 考研词汇数据
    ├── 6-托福-顺序.json       # 托福词汇数据
    └── 7-SAT-顺序.json        # SAT词汇数据
```

## 各文件功能说明

- `main.py` - 命令行程序入口，负责初始化和启动测试系统
- `vocabulary_tester.py` - 核心功能类，实现词汇加载、测试、统计和错题管理等所有核心功能
- `gui.py` - 基于Tkinter实现的图形用户界面，提供可视化操作体验
- `check_json_format.py` - 辅助工具，用于检查和显示词汇JSON文件的格式和内容
- `check_json_structure.py` - 验证JSON文件结构完整性，确保与核心功能兼容
- `data/` - 存储用户数据、偏好设置和统计信息
- `json/` - 存放所有词汇数据文件的文件夹

## 注意事项

1. 请确保Python已正确安装在您的系统上
2. 本程序需要访问词汇JSON文件，请不要移动或删除json文件夹中的相关词汇文件
3. 错题本将保存在程序运行目录下，文件名格式为"错题本_模块名_时间戳.txt"
4. 如果遇到词汇文件加载错误，请检查文件路径是否正确
5. 图形界面使用Tkinter库，这是Python标准库的一部分，无需额外安装

## 常见问题

**Q: 如何选择不同的词汇模块？**
A: 启动程序后，输入1-7之间的数字选择对应的词汇模块。

**Q: 测试过程中可以随时退出吗？**
A: 是的，输入'quit'或'q'可以随时退出测试。在GUI界面中也可以点击【停止测试】按钮。

**Q: 错题本保存在哪里？**
A: 错题本保存在程序运行目录下，文件名格式为"错题本_模块名_时间戳.txt"。

**Q: 可以自定义词汇吗？**
A: 当前版本暂不支持自定义词汇，系统使用内置的词汇JSON文件。

**Q: 图形界面无法启动怎么办？**
A: 请检查Python是否正确安装，以及是否支持Tkinter（大多数Python发行版默认包含Tkinter）。如果仍有问题，可以尝试使用命令行界面。

## 更新日志

### 1.1 版本
- 添加图形用户界面(GUI)支持
- 优化代码结构，提高程序稳定性
- 更新使用文档，增加GUI使用说明

### 1.0 版本
- 实现基本词汇测试功能
- 支持7个词汇模块
- 提供两种测试模式
- 实现实时统计和错题记录
- 添加批处理启动脚本
- 创建详细使用说明文档

## 贡献指南

欢迎对本项目提出改进建议或贡献代码！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [提交问题](https://github.com/yourusername/english-vocabulary-tester/issues)

---

**作者**: AI Assistant  
**创建日期**: 2025年  
**版本**: 1.1