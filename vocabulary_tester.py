#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import os
from datetime import datetime

class VocabularyTester:
    """
    英语词汇测试器类
    
    提供词汇测试的核心功能，包括词汇数据加载、测试题目生成、测试执行和结果统计等。
    """
    def __init__(self):
        """
        初始化词汇测试器
        
        设置初始状态，包括词汇数据存储、统计信息和模块配置等。
        """
        # 存储词汇数据
        self.vocab_data = {}
        
        # 当前选择的模块
        self.current_module = None
        
        # 测试模式：'chinese'（中文模式）或 'english'（英文模式）
        self.test_mode = None
        
        # 是否处于错题复习模式
        self.review_mode = False
        
        # 统计变量
        self.total_questions = 0
        self.correct_answers = 0
        self.wrong_answers = []
        # 本次测试新产生的错题
        self.current_session_wrong_answers = []
        
        # 模块配置
        self.modules = {
            "1": {"name": "初中", "file": "1-初中-顺序.json"},
            "2": {"name": "高中", "file": "2-高中-顺序.json"},
            "3": {"name": "CET4", "file": "3-CET4-顺序.json"},
            "4": {"name": "CET6", "file": "4-CET6-顺序.json"},
            "5": {"name": "考研", "file": "5-考研-顺序.json"},
            "6": {"name": "托福", "file": "6-托福-顺序.json"},
            "7": {"name": "SAT", "file": "7-SAT-顺序.json"}
        }
        
        # 词汇文件目录（相对路径，指向项目中的json文件夹）
        self.json_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json")
        
        # 模块词汇总数（用于估算认识率）
        self.module_total_words = 0
    
    def load_vocabulary(self, module_id):
        """
        加载指定模块的词汇数据
        
        Args:
            module_id: 模块ID（字符串或整数）
            
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            # 确保module_id是字符串格式
            module_id_str = str(module_id)
            module_info = self.modules.get(module_id_str)
            if not module_info:
                print("无效的模块ID")
                return False
            
            file_path = os.path.join(self.json_dir, module_info['file'])
            
            print(f"正在加载 {module_info['name']} 词汇数据...")
            with open(file_path, 'r', encoding='utf-8') as f:
                # 加载词汇数据
                all_vocab = json.load(f)
                
                # 处理词汇数据，转换为我们需要的格式
                processed_vocab = []
                for item in all_vocab:
                    word = item.get('word', '')
                    definition = ""
                    
                    # 尝试从translations获取释义（增强兼容性）
                    translations = item.get('translations', [])
                    if isinstance(translations, list) and translations:
                        # 确保第一个translation条目有translation字段
                        if 'translation' in translations[0]:
                            definition = translations[0].get('translation', '')
                    
                    # 如果没有找到释义，尝试从phrases获取（增强兼容性）
                    if not definition:
                        # 安全地检查phrases字段是否存在
                        if 'phrases' in item:
                            phrases = item.get('phrases', [])
                            if isinstance(phrases, list) and phrases:
                                if 'translation' in phrases[0]:
                                    definition = phrases[0].get('translation', '')
                    
                    # 初始化examples列表
                    examples = []
                    
                    # 安全地处理phrases字段（增强兼容性）
                    if 'phrases' in item:
                        phrases_list = item.get('phrases', [])
                        if isinstance(phrases_list, list):
                            for ph in phrases_list[:3]:  # 只取前3个短语
                                # 确保ph是字典类型并有需要的字段
                                if isinstance(ph, dict):
                                    p_text = ph.get('phrase', '')
                                    p_tr = ph.get('translation', '')
                                    if p_text or p_tr:
                                        examples.append({'phrase': p_text, 'translation': p_tr})
                    
                    # 只有当word和definition都有值时才添加到处理列表
                    if word and definition:
                        processed_vocab.append({'word': word, 'definition': definition, 'examples': examples})
                
                # 保存处理后的词汇数据
                self.vocab_data[module_id_str] = processed_vocab
                self.current_module = module_id_str
                self.module_total_words = len(processed_vocab)
                
                print(f"成功加载 {module_info['name']} 词汇，共 {len(processed_vocab)} 个词汇条目")
                return True
                
        except Exception as e:
            print(f"加载词汇文件失败: {e}")
            return False
    
    def select_module(self):
        """让用户选择词汇模块"""
        print("\n请选择词汇模块：")
        print("=" * 50)
        for key, module in self.modules.items():
            print(f"{key}. {module['name']}")
        print("=" * 50)
        
        while True:
            choice = input("请输入模块编号 (1-7): ").strip()
            if choice in self.modules:
                # 加载选择的模块
                if self.load_vocabulary(choice):
                    return choice
                else:
                    print("请重新选择模块")
            else:
                print("无效的选择，请输入1-7之间的数字")
    
    def select_test_mode(self):
        """让用户选择测试模式"""
        print("\n请选择测试模式：")
        print("=" * 50)
        print("1. 中文模式（显示中文释义，选择英文单词）")
        print("2. 英文模式（显示英文单词，选择中文释义）")
        print("=" * 50)
        
        while True:
            choice = input("请输入模式编号 (1-2): ").strip()
            if choice == "1":
                self.test_mode = "chinese"
                print("\n已选择：中文模式")
                return "chinese"
            elif choice == "2":
                self.test_mode = "english"
                print("\n已选择：英文模式")
                return "english"
            else:
                print("无效的选择，请输入1或2")
    
    def generate_question(self):
        """生成测试题目"""
        if not self.current_module or self.current_module not in self.vocab_data:
            return None
        
        vocab_list = self.vocab_data[self.current_module]
        if not vocab_list:
            return None
        
        # 复习模式：优先从错题中生成题目
        if hasattr(self, 'review_mode') and self.review_mode and self.wrong_answers:
            # 从错题中随机选择一个作为正确答案
            wrong_item = random.choice(self.wrong_answers)
            
            # 构建正确答案项
            correct_item = {
                'word': wrong_item['word'],
                'definition': wrong_item['definition']
            }
            
            # 生成干扰项 - 确保干扰项来自词汇列表
            distractors = []
            
            # 从词汇列表中排除正确答案对应的单词
            other_items = [item for item in vocab_list if item['word'] != correct_item['word']]
            
            # 确保有足够的干扰项
            if len(other_items) >= 3:
                distractors = random.sample(other_items, 3)
            elif other_items:
                distractors = other_items.copy()
                while len(distractors) < 3:
                    distractors.append(random.choice(other_items))
            else:
                # 如果词汇列表中只有一个词，创建一些不同的干扰项
                for _ in range(3):
                    dummy_item = {'word': f"干扰词_{random.randint(1000, 9999)}",
                                  'definition': f"干扰释义_{random.randint(1000, 9999)}"}
                    distractors.append(dummy_item)
        else:
            # 正常模式：从词汇列表生成题目
            # 随机选择一个正确答案
            correct_item = random.choice(vocab_list)
            
            # 生成干扰项
            distractors = []
            
            # 从词汇列表中排除正确答案，然后随机选择
            other_items = [item for item in vocab_list if item != correct_item]
            
            # 确保有足够的干扰项
            if len(other_items) >= 3:
                # 当有足够多其他词汇时，随机选择3个作为干扰项
                distractors = random.sample(other_items, 3)
            elif other_items:
                # 如果其他词汇数量不足但大于0，使用所有可用词汇作为干扰项
                # 然后复制一些来凑够3个（如果需要）
                distractors = other_items.copy()
                while len(distractors) < 3:
                    # 从其他词汇中随机选择一个添加到干扰项中（允许重复）
                    distractors.append(random.choice(other_items))
            else:
                # 如果词汇列表中只有一个词，使用这个词作为所有选项
                for _ in range(3):
                    # 创建一个新的字典副本，以避免引用同一对象
                    distractors.append(correct_item.copy())
        
        # 组合正确答案和干扰项
        all_items = [correct_item] + distractors
        # 随机排列
        random.shuffle(all_items)
        
        # 准备选项
        options = {}
        for i, item in enumerate(all_items):
            option_number = str(i + 1)  # 1, 2, 3, 4
            if self.test_mode == "chinese":
                # 中文模式：选项是英文单词
                options[option_number] = item['word']
            else:
                # 英文模式：选项是中文释义
                options[option_number] = item['definition']
        
        return {
            'correct_item': correct_item,
            'options': options,
            'question_text': correct_item['definition'] if self.test_mode == "chinese" else correct_item['word']
        }
    
    def display_statistics(self):
        """显示统计信息，包括正确率和估计的词汇认识率"""
        if self.total_questions == 0:
            print("还没有答题记录")
            return
        
        accuracy = (self.correct_answers / self.total_questions) * 100
        wrong_count = self.total_questions - self.correct_answers
        
        # 估算词汇认识率（基于正确率和模块总词汇数）
        if self.module_total_words > 0:
            estimated_knowledge_rate = min(100, accuracy)
            estimated_known_words = int(self.module_total_words * (estimated_knowledge_rate / 100))
        else:
            estimated_knowledge_rate = 0
            estimated_known_words = 0
        
        print("\n=== 统计信息 ===")
        print(f"已答题: {self.total_questions} 题")
        print(f"正确数: {self.correct_answers} 题")
        print(f"错误数: {wrong_count} 题")
        print(f"正确率: {accuracy:.1f}%")
        
        if self.module_total_words > 0:
            print(f"\n=== 词汇认识率估计 ===")
            print(f"当前模块总词汇量: {self.module_total_words} 个")
            print(f"估计认识率: {estimated_knowledge_rate:.1f}%")
            print(f"估计已掌握词汇: {estimated_known_words} 个")
        print("=" * 30)
    
    def save_wrong_answers(self):
        """将错题本保存为文本文件"""
        if not self.wrong_answers:
            print("没有错题记录")
            return False
        
        try:
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            module_name = self.modules.get(self.current_module, {}).get("name", "未知")
            
            # 获取当前文件所在目录，构建data目录路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, "data")
            
            # 确保data目录存在
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # 构建完整的文件路径
            filename = f"错题本_{module_name}_{timestamp}.txt"
            filepath = os.path.join(data_dir, filename)
            
            # 写入错题信息
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"=== 英语词汇错题本 ===\n")
                f.write(f"模块: {module_name}\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"总错题数: {len(self.wrong_answers)}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, wrong in enumerate(self.wrong_answers, 1):
                    f.write(f"第{i}题:\n")
                    f.write(f"  问题: {wrong['question']}\n")
                    f.write(f"  你的答案: {wrong['user_answer']}\n")
                    f.write(f"  正确答案: {wrong['correct_answer']}\n")
                    f.write(f"  单词: {wrong['word']}\n")
                    f.write(f"  释义: {wrong['definition']}\n")
                    if 'timestamp' in wrong:
                        f.write(f"  时间: {wrong['timestamp']}\n")
                    f.write("-" * 50 + "\n")
            
            print(f"错题本已保存为: {filename}")
            print(f"保存路径: {filepath}")
            return True
        except Exception as e:
            print(f"保存错题本时出错: {str(e)}")
            return False
    
    def import_wrong_answers_from_file(self, file_path=None):
        """
        从文件手动导入之前的错题
        
        Args:
            file_path: 错题文件路径，如果为None则让用户输入
            
        Returns:
            bool: 是否成功导入
        """
        try:
            if file_path is None:
                file_path = input("请输入错题本文件路径: ").strip()
            
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                return False
            
            imported_wrong_answers = []
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 简单解析文本格式的错题本
                # 按错题块分割
                wrong_blocks = content.split('-' * 50)
                
                for block in wrong_blocks:
                    if '单词:' in block and '释义:' in block and '正确答案:' in block:
                        # 提取错题信息
                        word_line = [line for line in block.split('\n') if '单词:' in line]
                        definition_line = [line for line in block.split('\n') if '释义:' in line]
                        correct_line = [line for line in block.split('\n') if '正确答案:' in line]
                        
                        if word_line and definition_line and correct_line:
                            word = word_line[0].split('单词:')[1].strip()
                            definition = definition_line[0].split('释义:')[1].strip()
                            correct_answer = correct_line[0].split('正确答案:')[1].strip()
                            
                            # 创建错题记录
                            wrong_info = {
                                'word': word,
                                'definition': definition,
                                'question': word if self.test_mode == 'chinese' else definition,
                                'correct_answer': correct_answer,
                                'user_answer': '未知',  # 从文件导入时无法确定用户答案
                                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
                            }
                            imported_wrong_answers.append(wrong_info)
            
            if imported_wrong_answers:
                # 导入错题
                success = self.import_previous_session_wrong_answers(imported_wrong_answers)
                if success:
                    print(f"成功导入 {len(imported_wrong_answers)} 道错题")
                    return True
            else:
                print("文件中没有找到有效错题")
                return False
                
        except Exception as e:
            print(f"导入错题时出错: {str(e)}")
            return False
        
        return False
            
    def evaluate_answer(self, user_answer, correct_answer, word, definition):
        """
        评估用户答案的正确性
        
        Args:
            user_answer: 用户输入的答案
            correct_answer: 正确的答案
            word: 单词
            definition: 释义
            
        Returns:
            bool: 用户答案是否正确
        """
        if user_answer.lower() == correct_answer.lower():
            self.correct_answers += 1
            return True
        else:
            # 构建错题信息
            wrong_info = {
                'word': word,
                'definition': definition,
                'question': word if self.test_mode == 'chinese' else definition,
                'correct_answer': correct_answer,
                'user_answer': user_answer,
                'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
            }
            # 记录错题到总错题列表
            self.wrong_answers.append(wrong_info)
            # 记录到本次测试错题列表
            if not self.review_mode:
                self.current_session_wrong_answers.append(wrong_info)
            return False
        
    def get_current_session_wrong_answers(self):
        """
        获取本次测试会话中产生的错题
        
        Returns:
            list: 本次测试的错题列表
        """
        return self.current_session_wrong_answers
    
    def clear_current_session_wrong_answers(self):
        """
        清空本次测试会话的错题记录
        """
        self.current_session_wrong_answers = []
    
    def set_review_mode(self, mode):
        """
        设置是否处于错题复习模式
        
        Args:
            mode: bool，True表示进入复习模式，False表示退出复习模式
        """
        self.review_mode = mode
    
    def import_previous_session_wrong_answers(self, wrong_answers):
        """
        导入之前会话的错题用于复习
        
        Args:
            wrong_answers: list，要导入的错题列表
        """
        if wrong_answers:
            self.wrong_answers.extend(wrong_answers)
            return True
        return False
        
    def start_test(self):
        """开始测试"""
        # 选择模块
        self.select_module()
        
        # 选择测试模式
        self.select_test_mode()
        
        print("\n测试开始！输入 'quit' 或 'q' 随时退出测试。")
        print("=" * 50)
        
        while True:
            # 显示当前统计信息
            self.display_statistics()
            
            # 生成题目
            question = self.generate_question()
            if not question:
                print("无法生成题目，请检查词汇数据")
                break
            
            # 显示题目
            print("\n问题:")
            if self.test_mode == "chinese":
                print(f"  '{question['question_text']}' 的英文单词是什么？")
            else:
                print(f"  '{question['question_text']}' 的中文释义是什么？")
            
            # 显示选项
            print("\n选项:")
            for option, content in question['options'].items():
                print(f"  {option}. {content}")
            
            # 获取用户输入
            user_input = input("\n请输入答案 (1/2/3/4) 或输入 'quit'/'q' 退出: ").strip()
            
            # 检查是否退出
            if user_input.lower() in ['quit', 'q']:
                print("\n测试已停止")
                
                # 显示最终统计
                print("\n=== 最终测试结果 ===")
                self.display_statistics()
                
                # 显示错题本
                if self.wrong_answers:
                    print(f"\n你在本次测试中有 {len(self.wrong_answers)} 道错题")
                    print("\n错题详情:")
                    for i, wrong in enumerate(self.wrong_answers, 1):
                        print(f"{i}. 单词: {wrong['word']} - 释义: {wrong['definition']}")
                        print(f"   你的答案: {wrong['user_answer']} - 正确答案: {wrong['correct_answer']}")
                        print()
                    
                    # 询问是否保存错题本
                    save_choice = input("\n是否保存错题本？(y/n): ").strip().lower()
                    if save_choice == 'y':
                        self.save_wrong_answers()
                else:
                    print("\n恭喜！你没有答错任何题目！")
                
                break
            
            # 检查答案是否有效
            if user_input not in question['options']:
                print("无效的输入，请输入 1、2、3 或 4")
                continue
            
            # 更新统计信息
            self.total_questions += 1
            
            # 判断答案是否正确
            correct_option = None
            for option, content in question['options'].items():
                if self.test_mode == "chinese":
                    if content == question['correct_item']['word']:
                        correct_option = option
                else:
                    if content == question['correct_item']['definition']:
                        correct_option = option
            
            user_answer = question['options'].get(user_input, '未知')
            correct_answer = question['options'].get(correct_option, '未知')
            
            if self.evaluate_answer(user_answer, correct_answer, question['correct_item']['word'], question['correct_item']['definition']):
                print("\n恭喜你回答正确！")
            else:
                print(f"\n回答错误！正确答案是: {correct_option}. {correct_answer}")
            
            print("=" * 50)