#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语词汇测试系统图形界面

作者: 英语词汇测试系统开发团队
版本: 1.1
日期: 2024-01-20

此模块提供了英语词汇测试系统的图形用户界面，通过Tkinter实现。
它通过子进程调用main.py来运行词汇测试的核心功能，并在GUI中展示输出和接收输入。
"""
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, simpledialog, colorchooser
from vocabulary_tester import VocabularyTester
import json
from datetime import datetime
import subprocess
import os
import sys
import threading
import queue
import re

class VocabularyTestGUI:
    """
    英语词汇测试图形用户界面类
    
    提供了一个基于Tkinter的图形界面，用于运行英语词汇测试系统。
    通过子进程调用main.py来执行测试功能，并在GUI中显示输出和接收用户输入。
    """
    def __init__(self, root):
        """
        初始化图形界面
        
        Args:
            root: Tkinter的根窗口对象
        """
        # 确保tkinter模块在类中可用
        global tk
        
        self.root = root
        self.root.title("英语词汇测试")
        self.root.geometry("950x750")  # 增大窗口尺寸，提供更舒适的使用空间
        self.root.resizable(True, True)
        
        # 创建背景画布 - 确保主题系统正常工作
        self.bg_canvas = tk.Canvas(self.root)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 设置字体，增加字体兼容性检测，提升界面可读性
        self.font_family = "Segoe UI"
        try:
            import tkinter.font as tk_font
            test_font = tk_font.Font(family=self.font_family, size=12)
        except:
            try:
                self.font_family = "Microsoft YaHei"
                import tkinter.font as tk_font
                test_font = tk_font.Font(family=self.font_family, size=12)
            except:
                self.font_family = "Times New Roman"
        
        # 设置字体
        self.normal_font = (self.font_family, 16)
        self.title_font_cn = (self.font_family, 24, "bold")
        self.title_font_en = (self.font_family, 18, "bold")
        self.button_font = (self.font_family, 16, "bold")
        self.large_font = (self.font_family, 18)
        self.small_font = (self.font_family, 12)
        
        self.colors = {
            "primary": "#4A7BFF",
            "primary_light": "#F0F4FF",
            "primary_dark": "#3A6BEE",
            "accent": "#4ECDC4",
            "accent_secondary": "#FF6B8B",
            "accent_tertiary": "#FFA36C",
            "warn": "#FFBE3D",
            "error": "#FF6B6B",
            "success": "#5CD85A",
            "background": "#FAFCFE",
            "surface": "#F5F7FA",
            "surface_variant": "#EBEFF5",
            "text": "#2D3748",
            "text_secondary": "#718096",
            "text_tertiary": "#A0AEC0",
            "text_inverse": "#FFFFFF",
            "border": "#E2E8F0",
            "border_light": "#EDF2F7",
            "shadow": "#2D3748",
            "overlay": "#2D3748",
            "divider": "#E2E8F0",
            "hover": "#E6EDFF",
            "active": "#DCE6FF",
            "focus": "#A7C0FF",
            "disabled": "#A0AEC0"
        }
        self.animations = {
            "fast": "0.2s cubic-bezier(0.4, 0.0, 0.2, 1)",
            "medium": "0.3s cubic-bezier(0.4, 0.0, 0.2, 1)",
            "slow": "0.5s cubic-bezier(0.4, 0.0, 0.2, 1)",
            "hover_scale": "transform 0.2s ease",
            "hover_color": "background-color 0.2s ease",
        }
        
        # 创建主框架 - 优化布局比例
        self.main_frame = tk.Frame(root, bg=self.colors["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=0)
        
        # 创建标题区域 - 紧凑设计
        self.title_frame = tk.Frame(self.main_frame, bg=self.colors["primary"], padx=12, pady=6)
        self.title_frame.pack(fill=tk.X, pady=(0, 2))
        self.title_frame.pack_propagate(False)
        self.title_frame.configure(height=44)
        
        # 中文标题
        self.title_label_cn = tk.Label(
            self.title_frame, 
            text="英语词汇测试", 
            font=self.title_font_cn,
            bg=self.colors["primary"], 
            fg=self.colors["text_inverse"]
        )
        self.title_label_cn.pack(pady=(3, 0), anchor="w")
        
        # 英文标题
        self.title_label_en = tk.Label(
            self.title_frame, 
            text="English Vocabulary Test", 
            font=self.title_font_en,
            bg=self.colors["primary"], 
            fg=self.colors["text_inverse"]
        )
        self.title_label_en.pack(pady=(0, 1), anchor="w")
        
        # 帮助文本 - 移除以节省空间
        # 帮助信息已在操作流程中体现，不再需要在标题栏显示
        # self.help_label = tk.Label(self.title_frame, ...)
        
        # 创建控制区域 - 模块选择和模式设置
        self.control_frame = tk.Frame(self.main_frame, pady=0)  # 进一步减小内边距
        self.control_frame.pack(fill=tk.X)
        
        # 创建显示区域框架 - 紧凑布局
        self.display_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        # 终端显示框 - 进一步压缩
        self.terminal = scrolledtext.ScrolledText(
            self.display_frame,
            font=("Courier New", 10),  # 减小字体
            bg=self.colors["surface"],
            fg=self.colors["text"],
            wrap=tk.WORD,
            height=6,
            bd=1, 
            relief=tk.FLAT,
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        self.terminal.pack(fill=tk.X, expand=False, padx=3, pady=2)
        
        # 选项框架 - 紧凑设计
        self.options_frame = tk.Frame(self.main_frame, 
                                     bg=self.colors["background"],
                                     padx=16, 
                                     pady=4)
        self.options_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        # 左右分栏：左侧题干，右侧选项
        self.question_panel = tk.Frame(self.options_frame, bg=self.colors["background"]) 
        self.answers_panel = tk.Frame(self.options_frame, bg=self.colors["background"]) 
        self.question_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 8))
        self.answers_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(8, 0))
        
        # 问题标签
        self.question_label = tk.Label(self.question_panel, 
                                     text="", 
                                     font=(self.font_family, 18, "bold"),
                                     bg=self.colors["background"],
                                     fg=self.colors["text"],
                                     wraplength=850,
                                     justify=tk.LEFT
        )
        self.question_label.pack(anchor="w", pady=(0, 8))
        # 直接使用answers_panel作为选项容器，移除无用的滚动区域
        self.options_inner_frame = self.answers_panel
        self.option_buttons = []
        
        # 初始化解析状态变量
        self.expect_question_text = False
        self.collecting_options = False
        
        # 显示欢迎信息和使用说明
        self.terminal.insert(tk.END, "欢迎！这是一个轻松好用的英语词汇练习工具。\n\n")
        self.terminal.insert(tk.END, "如何开始：\n")
        self.terminal.insert(tk.END, "- 在底部选择模块与模式后点击【开始测试】，直接用鼠标作答\n")
        self.terminal.insert(tk.END, "- 提示：随时点击【停止并保存】即可退出并查看统计\n\n")
        self.terminal.config(state=tk.DISABLED)
        
        # 创建输入区域 - 紧凑设计
        self.input_frame = tk.Frame(self.main_frame, bg=self.colors["background"])
        self.input_frame.pack(fill=tk.X, pady=8, padx=16)
        
        self.input_label = tk.Label(
            self.input_frame, 
            text="输入答案: ", 
            font=self.small_font,
            bg=self.colors["background"],
            fg=self.colors["text"]
        )
        self.input_label.pack(side=tk.LEFT, padx=(0, 8), pady=3)
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            self.input_frame,
            textvariable=self.input_var,
            font=self.normal_font,
            width=30,
            bd=0,
            relief=tk.FLAT,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["focus"],
            highlightthickness=1,
            bg=self.colors["surface"]
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=6)
        self.input_entry.bind("<Return>", self.send_input)
        
        # 发送按钮直接放在输入框旁边，Google风格按钮
        self.send_button = tk.Button(
            self.input_frame, 
            text="发送", 
            font=self.button_font,
            command=self.send_input, 
            width=8,
            bg=self.colors["primary"],
            fg=self.colors["text_inverse"],
            bd=0,
            relief=tk.FLAT,
            padx=15,
            pady=8
        )
        self.send_button.pack(side=tk.LEFT, padx=8)
        
        # 按钮区域已整合到control_frame中，不再需要单独的button_frame
        
        # 这些按钮将通过render_controls方法在需要时创建
        
        self.internal_mode = True
        self.tester = None
        # 先定义所有必要的变量
        self.module_var = tk.StringVar(value="1")
        self.mode_var = tk.StringVar(value="chinese")
        self.time_limit_var = tk.IntVar(value=0)
        self.favorites = set()
        self.preferences_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "preferences.json")
        
        # 控制框架，Google风格设计
        self.control_frame = tk.Frame(self.main_frame, bg=self.colors["surface_variant"], padx=8, pady=8)
        self.control_frame.pack(fill=tk.X, padx=8, pady=4)
        
        # 在所有变量定义后再调用render_controls
        self.render_controls()
        self.stats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "stats.json")
        self.favorites_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "favorites.json")
        self.wrongbook_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "wrong_book.json")
        self.ensure_data_dir()
        self.load_preferences()
        self.render_controls()
        
        # 初始化变量
        self.process = None
        self.running = False
        self.queue = queue.Queue()
        self.collecting_options = False
        self.parsed_options = {}
        self.last_line = ""
        self.current_theme = "Fluent"
        self.themes = {
            "Fluent": {
                "bg": self.colors["background"],
                "title_bg": self.colors["primary"],
                "title_fg": self.colors["text_inverse"],
                "terminal_bg": self.colors["surface"],
                "terminal_fg": self.colors["text"],
                "accent": self.colors["accent"]
            },
            "Light": {
                "bg": "#F7F9FC",
                "title_bg": "#2F6FED",
                "title_fg": "#ffffff",
                "terminal_bg": "#0B1222",
                "terminal_fg": "#E6EDF7",
                "accent": "#4CAF50"
            },
            "Dark": {
                "bg": "#0F172A",
                "title_bg": "#1E293B",
                "title_fg": "#E2E8F0",
                "terminal_bg": "#000000",
                "terminal_fg": "#E6E6E6",
                "accent": "#00D1FF"
            }
        }
        self.apply_theme()
        self.main_frame.bind("<Configure>", self.on_resize)
        self.root.bind("<Key>", self.on_key)
        self.current_question = None
        self.timer_id = None
        
        # 启动消息处理线程
        self.message_thread = threading.Thread(target=self.process_messages, daemon=True)
        self.message_thread.start()
        try:
            self.ensure_controls_visible()
        except Exception:
            pass
    
    def append_text(self, text):
        """
        向终端显示区域添加文本
        
        Args:
            text: 要添加的文本内容
        """
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)
        self.try_parse_line(text)
    
    def clear_terminal(self):
        """
        清空终端显示区域的所有内容
        """
        self.terminal.config(state=tk.NORMAL)
        self.terminal.delete(1.0, tk.END)
        self.terminal.config(state=tk.DISABLED)
    
    def start_test(self):
        """
        启动词汇测试程序
        
        创建一个子进程运行main.py，并启动输出读取线程
        同时更新UI按钮状态
        """
        if self.running:
            self.append_text("测试已经在运行中...\n")
            return
        
        try:
            # 清空终端
            self.clear_terminal()
            self.append_text("正在启动词汇测试系统...\n\n")
            
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(script_dir, "main.py")
            
            # 启动词汇测试程序
            self.process = subprocess.Popen(
                [sys.executable, main_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=script_dir
            )
            
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # 启动输出读取线程
            self.output_thread = threading.Thread(target=self.read_output, daemon=True)
            self.output_thread.start()
            self.help_label.config(text="已启动：请按提示选择模块与模式；题目出现后点击下方选项按钮作答。按 Q 或点击停止退出。")
            
        except Exception as e:
            self.append_text(f"启动错误: {str(e)}\n")
    
    def stop_test(self):
        """
        停止词汇测试程序
        
        终止子进程，并更新UI按钮状态
        """
        if not self.running or not self.process:
            return
        
        try:
            # 发送终止信号
            self.process.terminate()
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.kill()
        
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.append_text("\n词汇测试系统已停止\n")
    
    def send_input(self, event=None):
        """
        发送用户输入到测试程序
        
        Args:
            event: 键盘事件对象（可选，用于回车键绑定）
        """
        if not self.running or not self.process:
            self.append_text("请先点击【启动测试】按钮开始测试\n")
            return
        
        user_input = self.input_var.get().strip()
        if user_input:
            try:
                # 发送输入到程序
                self.process.stdin.write(user_input + "\n")
                self.process.stdin.flush()
                
                # 在终端中显示用户输入
                self.append_text(f"> {user_input}\n")
                
                # 清空输入框
                self.input_var.set("")
            except Exception as e:
                self.append_text(f"发送输入错误: {str(e)}\n")
    
    def read_output(self):
        """
        读取测试程序的输出
        
        在单独的线程中运行，将程序输出放入消息队列
        """
        try:
            while self.running and self.process:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.queue.put(line)
        except Exception as e:
            self.queue.put(f"读取输出错误: {str(e)}\n")
        finally:
            if self.running:
                self.running = False
                self.root.after(0, lambda: self.stop_test())
    
    def process_messages(self):
        """
        处理消息队列中的输出信息
        
        从队列中获取输出并在UI中显示
        """
        while True:
            try:
                message = self.queue.get(timeout=0.1)
                self.root.after(0, lambda msg=message: self.append_text(msg))
                self.queue.task_done()
            except queue.Empty:
                pass

    def on_key(self, event):
        ch = event.char
        if ch in ("q", "Q"):
            self.stop_internal_test()
        # 处理Ctrl+P快捷键实现重复发音
        elif event.state == 4 and event.keysym.lower() == "p":
            self.pronounce_current()
    
    def update_ui_state(self):
        # 确保所有按钮都存在，避免引用不存在的属性
        if not hasattr(self, 'start_button') or not hasattr(self, 'exit_button'):
            return
        
        # 根据测试状态更新按钮状态
        is_testing = hasattr(self, 'tester') and self.tester is not None and self.tester.total_questions > 0
        
        # 开始测试按钮 - 测试未运行时可用
        self.start_button.config(state=tk.DISABLED if is_testing else tk.NORMAL)
        
        # 退出程序按钮 - 始终可用
        self.exit_button.config(state=tk.NORMAL)  # 退出按钮应始终可用
        
        # 辅助按钮始终可见，但根据需要调整状态
        if hasattr(self, 'clear_button'):
            pass  # 使用grid布局，无需额外配置
        if hasattr(self, 'settings_button'):
            # 测试运行时禁用设置按钮，避免中断测试
            self.settings_button.config(state=tk.DISABLED if is_testing else tk.NORMAL)
        
        # 确保控制框架始终可见且在底部
        if hasattr(self, 'control_frame'):
            try:
                self.control_frame.pack_forget()
            except Exception:
                pass
            self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False, padx=16, pady=8)
            self.control_frame.lift()

        # 顶部区域在测试时收缩
        try:
            if is_testing:
                self.title_frame.configure(height=32, padx=6, pady=2)
                self.title_label_cn.config(font=(self.font_family, 18, 'bold'))
                self.title_label_en.config(font=(self.font_family, 12, 'bold'))
                if hasattr(self, 'config_frame'):
                    self.config_frame.pack_configure(pady=(0, 2), padx=4)
                if hasattr(self, 'buttons_container'):
                    self.buttons_container.pack_configure(pady=(2, 2))
                if hasattr(self, 'terminal'):
                    self.terminal.pack_configure(fill=tk.X, expand=False, padx=3, pady=2)
                    try:
                        self.terminal.configure(height=6)
                    except Exception:
                        pass
                if hasattr(self, 'options_frame'):
                    self.options_frame.pack_configure(pady=2)
                if hasattr(self, 'options_scroll_canvas'):
                    try:
                        self.options_scroll_canvas.configure(height=80)
                    except Exception:
                        pass
            else:
                self.title_frame.configure(height=44, padx=12, pady=6)
                self.title_label_cn.config(font=self.title_font_cn)
                self.title_label_en.config(font=self.title_font_en)
                if hasattr(self, 'config_frame'):
                    self.config_frame.pack_configure(pady=(0, 4), padx=4)
                if hasattr(self, 'buttons_container'):
                    self.buttons_container.pack_configure(pady=(4, 4))
                if hasattr(self, 'terminal'):
                    self.terminal.pack_configure(fill=tk.X, expand=False, padx=3, pady=2)
                    try:
                        self.terminal.configure(height=6)
                    except Exception:
                        pass
                if hasattr(self, 'options_frame'):
                    self.options_frame.pack_configure(pady=4)
                if hasattr(self, 'options_scroll_canvas'):
                    try:
                        self.options_scroll_canvas.configure(height=100)
                    except Exception:
                        pass
                if hasattr(self, 'question_label'):
                    self.question_label.config(font=(self.font_family, 16, 'bold'))
                if hasattr(self, 'input_frame'):
                    try:
                        self.input_frame.pack(fill=tk.X, pady=4, padx=8)
                    except Exception:
                        pass
        except Exception:
            pass
    
    def exit_program(self):
        """
        退出整个应用程序
        
        先停止测试进程（如果正在运行），然后销毁主窗口
        """
        if self.running:
            self.stop_test()
        self.root.destroy()

    def lower_widget(self, widget):
        try:
            widget.tk.call('lower', widget._w)
        except Exception:
            pass

    def ensure_data_dir(self):
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)

    def load_preferences(self):
        try:
            if os.path.isfile(self.preferences_path):
                with open(self.preferences_path, "r", encoding="utf-8") as f:
                    p = json.load(f)
                    self.module_var.set(p.get("default_module", "1"))
                    self.mode_var.set(p.get("default_mode", "chinese"))
                    size = p.get("font_size", 16)
                    self.normal_font = (self.font_family, size)
                    self.time_limit_var.set(p.get("time_limit", 0))
                    if p.get("night_mode", False):
                        self.current_theme = "Dark"
        except Exception:
            pass

    def save_preferences(self):
        try:
            data = {
                "default_module": self.module_var.get(),
                "default_mode": self.mode_var.get(),
                "font_size": self.normal_font[1],
                "time_limit": self.time_limit_var.get(),
                "night_mode": self.current_theme == "Dark"
            }
            with open(self.preferences_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def save_stats(self):
        try:
            s = []
            if os.path.isfile(self.stats_path):
                with open(self.stats_path, "r", encoding="utf-8") as f:
                    s = json.load(f)
            if self.tester:
                s.append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "module": self.tester.modules.get(self.tester.current_module, {}).get("name", ""),
                    "total": self.tester.total_questions,
                    "correct": self.tester.correct_answers
                })
            with open(self.stats_path, "w", encoding="utf-8") as f:
                json.dump(s, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def render_controls(self):
        # 清空现有控件
        for w in self.control_frame.winfo_children():
            w.destroy()
        
        # 第一部分：配置区域 - 紧凑设计
        self.config_frame = tk.Frame(self.control_frame, bg=self.colors["surface_variant"]) 
        self.config_frame.pack(fill=tk.X, pady=(0, 4), padx=4)
        
        # 左侧：模块选择 - 紧凑设计
        module_frame = tk.Frame(self.config_frame, bg=self.colors["surface_variant"]) 
        module_frame.pack(side=tk.LEFT, padx=(0, 4))
        tk.Label(module_frame, text="词汇模块", font=self.small_font, pady=0, bg=self.colors["surface_variant"]).grid(row=0, column=0, sticky="w")
        modules_container = tk.Frame(module_frame, bg=self.colors["surface_variant"]) 
        modules_container.grid(row=1, column=0)
        
        # 紧凑的模块选择布局
        for i, k in enumerate(["1","2","3","4","5","6","7"]):
            row = i // 3
            col = i % 3
            b = tk.Radiobutton(modules_container, text=self.get_module_name(k), 
                             variable=self.module_var, value=k, 
                             font=(self.font_family, 10),
                             bg=self.colors["surface_variant"])
            b.grid(row=row, column=col, sticky="w", padx=2, pady=0)
        
        # 右侧：测试模式和限时设置 - 紧凑设计
        self.settings_frame = tk.Frame(self.config_frame, bg=self.colors["surface_variant"]) 
        self.settings_frame.pack(side=tk.LEFT, padx=4)
        
        # 模式选择 - 紧凑设计
        mode_frame = tk.Frame(self.settings_frame, bg=self.colors["surface_variant"]) 
        mode_frame.pack(pady=(0, 2))
        tk.Label(mode_frame, text="测试模式", font=self.small_font, bg=self.colors["surface_variant"]).pack(anchor="w")
        mode_radio_frame = tk.Frame(mode_frame, bg=self.colors["surface_variant"]) 
        mode_radio_frame.pack(fill=tk.X)
        tk.Radiobutton(mode_radio_frame, text="中文", variable=self.mode_var, 
                     value="chinese", font=(self.font_family, 10), bg=self.colors["surface_variant"]).pack(side=tk.LEFT, padx=4)
        tk.Radiobutton(mode_radio_frame, text="英文", variable=self.mode_var, 
                     value="english", font=(self.font_family, 10), bg=self.colors["surface_variant"]).pack(side=tk.LEFT, padx=4)
        
        # 限时设置 - 紧凑设计
        time_frame = tk.Frame(self.settings_frame, bg=self.colors["surface_variant"]) 
        time_frame.pack(fill=tk.X)
        tk.Label(time_frame, text="限时:", font=(self.font_family, 10), bg=self.colors["surface_variant"]).pack(side=tk.LEFT, padx=(0, 4))
        spinbox = tk.Spinbox(time_frame, from_=0, to=120, textvariable=self.time_limit_var, 
                           width=5, font=self.small_font, 
                           bd=1,
                           bg=self.colors["surface"],
                           relief=tk.FLAT)
        spinbox.pack(side=tk.LEFT, padx=4)
        tk.Label(time_frame, text="(0不限时)", font=(self.font_family, 10), bg=self.colors["surface_variant"]).pack(side=tk.LEFT, padx=4)
        
        # 第二部分：所有操作按钮 - 紧凑设计
        self.buttons_container = tk.Frame(self.control_frame, bg=self.colors["surface_variant"]) 
        self.buttons_container.pack(fill=tk.X, pady=(4, 4))
        
        # 按钮平铺展开布局，充分利用水平空间 - 紧凑设计
        all_buttons_frame = tk.Frame(self.buttons_container, bg=self.colors["surface_variant"]) 
        all_buttons_frame.pack(fill=tk.X, pady=4)
        
        # 设置列权重，使按钮均匀分布
        all_buttons_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="buttons")
        
        # 开始测试按钮 - 紧凑设计
        self.start_button = tk.Button(all_buttons_frame, text="开始测试", 
                            font=self.button_font, bg=self.colors["accent"], fg=self.colors["text_inverse"], 
                            command=self.start_internal_test, 
                            padx=8, pady=6, relief=tk.FLAT, bd=0, cursor="hand2")
        self.start_button.grid(row=0, column=0, sticky="ew", padx=3, pady=2)
        self.apply_button_hover(self.start_button)
        
        # 停止并保存按钮 - 紧凑设计
        self.stop_button = tk.Button(all_buttons_frame, text="退出测试", 
                           font=self.button_font, bg=self.colors["error"], fg=self.colors["text_inverse"], 
                           command=self.stop_internal_test, 
                           padx=8, pady=6, relief=tk.FLAT, bd=0, cursor="hand2")
        self.stop_button.grid(row=0, column=1, sticky="ew", padx=3, pady=2)
        self.apply_button_hover(self.stop_button)
        
        # 清空显示按钮 - 紧凑设计
        self.clear_button = tk.Button(all_buttons_frame, text="清空显示", 
                            font=self.button_font, 
                            command=self.clear_terminal, 
                           padx=8, pady=6, relief=tk.FLAT, bd=0, cursor="hand2",
                           bg=self.colors["surface"]) 
        self.clear_button.grid(row=0, column=2, sticky="ew", padx=3, pady=2)
        self.apply_button_hover(self.clear_button)
        
        # 设置按钮 - 紧凑设计
        self.settings_button = tk.Button(all_buttons_frame, text="设置", 
                            font=self.button_font, 
                            command=self.open_settings, 
                            padx=8, pady=6, relief=tk.FLAT, bd=0, cursor="hand2",
                            bg=self.colors["surface"]) 
        self.settings_button.grid(row=0, column=3, sticky="ew", padx=3, pady=2)
        self.apply_button_hover(self.settings_button)
        
        # 退出按钮 - 紧凑设计
        self.exit_button = tk.Button(all_buttons_frame, text="退出程序", 
                            font=self.button_font, 
                           bg=self.colors["warn"], fg=self.colors["text_inverse"],
                            command=self.exit_program, 
                           padx=8, pady=6, relief=tk.FLAT, bd=0, cursor="hand2")
        self.exit_button.grid(row=0, column=4, sticky="ew", padx=3, pady=2)
        self.apply_button_hover(self.exit_button)
        
        # 显示提示信息确保所有按钮都能在测试模式下正常显示
        self.update_ui_state()
        
        # 显示提示信息
        self.append_text("\n提示：错题本将自动保存至data/wrong_book.json，也可手动点击导出错题按钮导出\n")

    def get_module_name(self, k):
        m = VocabularyTester().modules
        return m.get(k, {}).get("name", k)

    def start_internal_test(self):
        # 确保测试器已初始化
        if not self.tester:
            self.tester = VocabularyTester()
        
        # 重置测试器的统计信息，但保留复习模式下的错题列表
        self.tester.total_questions = 0
        self.tester.correct_answers = 0
        
        # 检查是否在复习模式
        is_review_mode = hasattr(self.tester, 'review_mode') and self.tester.review_mode
        
        # 只有在非复习模式下才清空错题列表
        if not is_review_mode:
            self.tester.wrong_answers = []
        
        # 加载选定的模块
        if not self.tester.load_vocabulary(self.module_var.get()):
            # 出错时也更新UI状态
            self.update_ui_state()
            return
        
        # 设置测试模式
        self.tester.test_mode = self.mode_var.get()
        
        # 开始测试
        self.next_question()
        
        # 更新UI状态，确保按钮正确显示
        self.update_ui_state()

    def stop_internal_test(self):
        if not self.tester:
            return
        
        # 退出复习模式
        if hasattr(self.tester, 'set_review_mode'):
            self.tester.set_review_mode(False)
        
        self.save_stats()
        self.clear_options()
        self.question_label.config(text="")
        self.display_internal_statistics()
        if self.tester.wrong_answers:
            try:
                from tkinter import messagebox as _mb
                if _mb.askyesno("保存错题本", "是否保存错题本为文本文件？"):
                    self.tester.save_wrong_answers()
            except Exception:
                pass
            self.export_wrongbook()
            # 添加明确的提示信息
            self.append_text("\n=== 错题本保存信息 ===\n")
            self.append_text(f"1. 错题已以JSON格式保存至: {self.wrongbook_path}\n")
            self.append_text("2. 如选择文本格式，已保存至当前目录\n")
            self.append_text("=" * 50 + "\n")
        if hasattr(self, 'timer_id') and self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None
        self.tester = None
        
        # 更新UI状态，确保按钮正确显示
        self.update_ui_state()

    def next_question(self):
        if not self.tester:
            return
        q = self.tester.generate_question()
        if not q:
            return
        self.current_question = q
        
        # 优化问题标签的显示配置
        if self.tester.test_mode == "chinese":
            self.question_label.config(text=f"' {q['question_text']}' 的英文单词是什么？")
        else:
            self.question_label.config(text=f"' {q['question_text']}' 的中文释义是什么？")
        
        # 确保问题标签有足够的可见空间
        self.question_label.pack_configure(pady=(8, 12))
        
        self.parsed_options = q['options']
        self.render_options_internal()
        # 自动发音当前词汇 - 仅在英文模式下自动发音，中文模式下不自动发音
        if self.tester.test_mode != "chinese":
            self.pronounce_current()
        self.start_timer()

    def render_options_internal(self):
        self.clear_options()
        # 压缩选项框架空间
        self.options_frame.pack_configure(pady=(5, 5))
        
        # 紧凑的选项按钮布局
        for i in ["1","2","3","4"]:
            if i in self.parsed_options:
                b = tk.Button(
                    self.options_frame, 
                    text=f"{i}. {self.parsed_options[i]}", 
                    font=self.small_font,  # 使用小字体
                    command=lambda num=i: self.on_option_click(num), 
                    wraplength=700,
                    justify="left",
                    relief=tk.FLAT,
                    bd=0,
                    highlightthickness=1,
                    highlightbackground=self.colors["primary"],
                    bg=self.colors["surface"],
                    fg=self.colors["text"],
                    padx=10,
                    pady=6,  # 减小内边距
                    cursor="hand2"
                )
                # 自定义悬停效果
                b.bind("<Enter>", lambda e, b=b: b.config(bg=self.colors["active"]))
                b.bind("<Leave>", lambda e, b=b: b.config(bg=self.colors["surface"]))
                # 紧凑的外边距
                b.pack(fill=tk.X, padx=5, pady=4)
                self.option_buttons.append(b)


    def apply_button_hover(self, btn):
        def enter(e):
            try:
                btn.config(bg=self.colors["active"]) 
            except Exception:
                pass
        def leave(e):
            try:
                # reset using stored default bg if available
                if hasattr(btn, '_default_bg'):
                    btn.config(bg=btn._default_bg)
            except Exception:
                pass
        def press(e):
            try:
                btn.config(bg=self.colors["hover"]) 
            except Exception:
                pass
        def release(e):
            try:
                if hasattr(btn, '_default_bg'):
                    btn.config(bg=btn._default_bg)
            except Exception:
                pass
        try:
            btn._default_bg = btn.cget('bg')
        except Exception:
            pass
        btn.bind("<Enter>", enter)
        btn.bind("<Leave>", leave)
        btn.bind("<ButtonPress-1>", press)
        btn.bind("<ButtonRelease-1>", release)

    def start_timer(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        t = self.time_limit_var.get()
        if t and t > 0:
            self.timer_id = self.root.after(t*1000, self.on_timeout)

    def on_timeout(self):
        if not self.current_question:
            return
        self.evaluate_answer(None)

    def on_option_click(self, num):
        self.evaluate_answer(num)

    def evaluate_answer(self, num):
        if not self.tester or not self.current_question:
            return
        try:
            self.tester.total_questions += 1
            target_word = self.current_question['correct_item']['word']
            target_def = self.current_question['correct_item']['definition']
            correct_option = None
            for option, content in self.current_question['options'].items():
                if self.tester.test_mode == "chinese":
                    if content == target_word:
                        correct_option = option
                        break
                else:
                    if content == target_def:
                        correct_option = option
                        break
            if correct_option is None:
                # 兜底：根据题干匹配
                for option, content in self.current_question['options'].items():
                    if content == self.current_question['question_text']:
                        correct_option = option
                        break
            if num == correct_option:
                self.tester.correct_answers += 1
                self.append_text("\n✅ 恭喜你回答正确！\n")
            else:
                corr_text = self.current_question['options'].get(correct_option, '未知')
                self.append_text(f"\n❌ 回答错误！正确答案是: {correct_option}. {corr_text}\n")
                self.tester.wrong_answers.append({
                    'question': self.current_question['question_text'],
                    'user_answer': self.current_question['options'].get(str(num), '超时' if num is None else '未知'),
                    'correct_answer': corr_text,
                    'word': target_word,
                    'definition': target_def
                })
                
            # 立即显示当前统计信息，确保每次回答后都显示
            self._display_current_statistics()
            
        except Exception as e:
            # 防止异常导致界面卡住，记录并继续下一题
            try:
                self.append_text(f"\n处理答案时出现问题: {str(e)}\n")
            except Exception:
                pass
    
    def _display_current_statistics(self):
        """显示当前的测试统计信息"""
        if not self.tester or self.tester.total_questions == 0:
            return
            
        # 计算基本统计数据
        total_count = self.tester.total_questions
        correct_count = self.tester.correct_answers
        module_info = self.tester.modules.get(self.tester.current_module, {})
        total_vocab = module_info.get('total', 0)
        
        # 计算认识率和估计掌握个数
        if total_count > 0:
            accuracy_rate = (correct_count / total_count) * 100
            # 估计掌握个数
            estimated_knowledge = int(total_vocab * (correct_count / total_count)) if total_vocab > 0 else 0
            estimated_recognition_rate = accuracy_rate  # 基于已答题的正确率估计整体认识率
        else:
            accuracy_rate = 0
            estimated_knowledge = 0
            estimated_recognition_rate = 0
        
        # 显示统计信息
        self.append_text("\n" + "="*60 + "\n")
        self.append_text("📊 测试统计信息\n")
        self.append_text("="*60 + "\n")
        self.append_text(f"🔤 已测试词汇量总数: {total_count}\n")
        self.append_text(f"✅ 回答正确次数: {correct_count}\n")
        self.append_text(f"❌ 回答错误次数: {total_count - correct_count}\n")
        self.append_text(f"📈 当前正确率: {accuracy_rate:.1f}%\n")
        self.append_text(f"🧠 估计认识率: {estimated_recognition_rate:.1f}%\n")
        if total_vocab > 0:
            self.append_text(f"📚 当前模块总词汇量: {total_vocab}\n")
            self.append_text(f"🎯 估计掌握词汇个数: {estimated_knowledge} / {total_vocab}\n")
        self.append_text("="*60 + "\n")
        
        self.current_question = None
        self.next_question()

    def display_internal_statistics(self):
        if not self.tester:
            return
        total = self.tester.total_questions
        correct = self.tester.correct_answers
        wrong = total - correct
        if total == 0:
            self.append_text("还没有答题记录\n")
            return
        accuracy = (correct / total) * 100
        module_total = self.tester.module_total_words
        estimated_rate = min(100.0, accuracy)
        estimated_known = int(module_total * (estimated_rate / 100)) if module_total > 0 else 0
        self.append_text("\n=== 统计信息 ===\n")
        self.append_text(f"已答题: {total} 题\n")
        self.append_text(f"正确数: {correct} 题\n")
        self.append_text(f"错误数: {wrong} 题\n")
        self.append_text(f"正确率: {accuracy:.1f}%\n")
        if module_total > 0:
            self.append_text("\n=== 词汇认识率估计 ===\n")
            self.append_text(f"当前模块总词汇量: {module_total} 个\n")
            self.append_text(f"估计认识率: {estimated_rate:.1f}%\n")
            self.append_text(f"估计已掌握词汇: {estimated_known} 个\n")

    def pronounce_current(self):
        if not self.current_question:
            return
        w = self.current_question['correct_item']['word']
        self.speak_text(w)

    def speak_definition(self):
        if not self.current_question:
            return
        d = self.current_question['correct_item']['definition']
        self.speak_text(d)

    def speak_text(self, text):
        try:
            cmd = f"$s=New-Object -ComObject SAPI.SpVoice; $s.Speak(\"{text}\")"
            subprocess.Popen(["powershell", "-Command", cmd])
        except Exception:
            pass

    def toggle_favorite(self):
        if not self.current_question:
            return
        w = self.current_question['correct_item']['word']
        if w in self.favorites:
            self.favorites.remove(w)
        else:
            self.favorites.add(w)
        try:
            with open(self.favorites_path, "w", encoding="utf-8") as f:
                json.dump(sorted(list(self.favorites)), f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def export_wrongbook(self):
        if not self.tester:
            return
        try:
            # 创建带时间戳的错题记录，并去重（根据单词去重）
            unique_wrong_answers = []
            seen_words = set()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for item in self.tester.wrong_answers:
                # 使用单词作为去重的唯一标识符
                if item.get('word') not in seen_words:
                    seen_words.add(item.get('word'))
                    # 添加时间戳和更详细的结构
                    enhanced_item = {
                        "time": timestamp,
                        "word_info": {
                            "word": item.get('word', '未知单词'),
                            "definition": item.get('definition', '无定义')
                        },
                        "question_info": {
                            "question": item.get('question', '未知问题'),
                            "your_answer": item.get('user_answer', '未作答'),
                            "correct_answer": item.get('correct_answer', '未知正确答案')
                        }
                    }
                    unique_wrong_answers.append(enhanced_item)
            
            # 创建包含元数据的错题本结构
            wrongbook_content = {
                "metadata": {
                    "export_time": timestamp,
                    "total_wrong_items": len(unique_wrong_answers),
                    "module": getattr(self.tester, 'current_module', '未知模块'),
                    "test_mode": getattr(self.tester, 'test_mode', '未知模式')
                },
                "wrong_answers": unique_wrong_answers
            }
            
            with open(self.wrongbook_path, "w", encoding="utf-8") as f:
                json.dump(wrongbook_content, f, ensure_ascii=False, indent=4)
            
            self.append_text(f"\n错题已导出: {self.wrongbook_path}\n")
            self.append_text(f"共导出 {len(unique_wrong_answers)} 个不重复的错题\n")
            
        except Exception as e:
            try:
                self.append_text(f"\n导出错题时出错: {str(e)}\n")
            except Exception:
                pass

    def import_wrongbook(self):
        try:
            if os.path.isfile(self.wrongbook_path):
                with open(self.wrongbook_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if self.tester:
                    self.tester.wrong_answers = data
                self.append_text("\n已导入错题本\n")
        except Exception:
            pass
    
    def import_previous_session_wrongbook(self):
        """
        手动导入上次测试会话的错题
        """
        if not self.tester:
            self.append_text("\n请先开始测试会话\n")
            return
        
        # 获取当前会话的错题
        previous_wrong_answers = self.tester.get_current_session_wrong_answers() if hasattr(self.tester, 'get_current_session_wrong_answers') else []
        
        if not previous_wrong_answers:
            self.append_text("\n当前没有可导入的上次测试错题\n")
            # 提示用户可以先进行测试
            self.append_text("\n请先进行一次测试，答错的题目将自动记录\n")
            return
        
        # 显示上次错题数量
        self.append_text(f"\n找到 {len(previous_wrong_answers)} 道上次测试的错题\n")
        
        # 询问用户是否确认导入
        try:
            from tkinter import messagebox
            response = messagebox.askyesno("导入错题", f"是否导入 {len(previous_wrong_answers)} 道上次测试的错题进行复习？")
            
            if response:
                # 导入错题并进入复习模式
                if hasattr(self.tester, 'set_review_mode'):
                    self.tester.set_review_mode(True)
                    self.append_text("\n已进入错题复习模式\n")
                    
                    # 如果当前不在测试中，则提示用户开始测试
                    if not hasattr(self, 'is_testing') or not self.is_testing:
                        self.append_text("\n请点击'开始测试'按钮开始错题复习\n")
                else:
                    self.append_text("\n错题复习模式功能不可用\n")
            else:
                self.append_text("\n已取消导入错题\n")
        except ImportError:
            # 如果无法导入messagebox，直接导入错题
            if hasattr(self.tester, 'set_review_mode'):
                self.tester.set_review_mode(True)
                self.append_text("\n已进入错题复习模式\n")
            else:
                self.append_text("\n错题复习模式功能不可用\n")



    def try_parse_line(self, text):
        t = text.strip()
        if t == "选项:":
            self.collecting_options = True
            self.parsed_options = {}
            return
        if self.collecting_options:
            m = re.match(r"^(\d+)\.\s+(.*)$", t)
            if m:
                self.parsed_options[m.group(1)] = m.group(2)
                if len(self.parsed_options) >= 4:
                    self.collecting_options = False
                    self.render_options()
                    return
        if t.startswith("问题:"):
            self.clear_options()
            self.question_label.config(text="")
            self.expect_question_text = True
            return
        if self.expect_question_text and t:
            self.question_label.config(text=t)
            self.expect_question_text = False
            return
        if t.startswith("请输入答案"):
            return
        self.last_line = t

    def render_options(self):
        self.clear_options()
        for i in ["1", "2", "3", "4"]:
            if i in self.parsed_options:
                b = tk.Button(
                    self.options_frame,
                    text=f"{i}. {self.parsed_options[i]}",
                    font=self.normal_font,
                    command=lambda num=i: self.send_option(num),
                    wraplength=600,
                    justify="left",
                )
                b.pack(fill=tk.X, padx=4, pady=4)
                self.option_buttons.append(b)

    def clear_options(self):
        for b in self.option_buttons:
            b.destroy()
        self.option_buttons = []

    def send_option(self, num):
        if not self.running or not self.process:
            return
        try:
            self.process.stdin.write(str(num) + "\n")
            self.process.stdin.flush()
            self.append_text(f"> {num}\n")
        except Exception as e:
            self.append_text(f"发送输入错误: {str(e)}\n")

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("设置")
        tk.Label(win, text="主题").pack(anchor="w", padx=10, pady=(10, 0))
        theme_var = tk.StringVar(value=self.current_theme)
        theme_menu = tk.OptionMenu(win, theme_var, *list(self.themes.keys()))
        theme_menu.pack(fill=tk.X, padx=10)
        def apply_and_close():
            self.current_theme = theme_var.get()
            self.apply_theme()
            self.save_preferences()
            win.destroy()
        tk.Button(win, text="应用", command=apply_and_close).pack(fill=tk.X, padx=10, pady=10)

    def apply_theme(self):
        th = self.themes.get(self.current_theme, {})
        bg = th.get("bg", self.colors["background"]) 
        title_bg = th.get("title_bg", self.colors["primary"]) 
        title_fg = th.get("title_fg", self.colors["text_inverse"]) 
        terminal_bg = th.get("terminal_bg", self.colors["surface"]) 
        terminal_fg = th.get("terminal_fg", self.colors["text"]) 
        accent = th.get("accent", self.colors["accent"]) 
        self.main_frame.config(bg=bg)
        self.title_frame.config(bg=title_bg)
        self.title_label_cn.config(bg=title_bg, fg=title_fg)
        self.title_label_en.config(bg=title_bg, fg=title_fg)
        self.display_frame.config(bg=bg)
        self.terminal.config(bg=terminal_bg, fg=terminal_fg)
        self.control_frame.config(bg=self.colors.get("surface_variant", bg)) 
        if hasattr(self, 'clear_button'):
            self.clear_button.config(bg=self.colors["surface"], fg=self.colors["text"]) 
        if hasattr(self, 'settings_button'):
            self.settings_button.config(bg=self.colors["surface"], fg=self.colors["text"]) 
        if hasattr(self, 'exit_button'):
            self.exit_button.config(bg=self.colors["warn"], fg=self.colors["text_inverse"]) 
        self.options_frame.config(bg=bg)
        self.draw_background()

    def on_resize(self, event):
        self.draw_background()
        try:
            self.ensure_controls_visible()
        except Exception:
            pass

    def draw_background(self):
        th = self.themes.get(self.current_theme, {})
        self.bg_canvas.delete("all")
        self.bg_canvas.configure(bg=th.get("bg", "#ffffff"))
        if self.current_theme == "Morandi Cute":
            try:
                w = max(self.bg_canvas.winfo_width(), 1)
                h = self.title_frame.winfo_height() or 60
                steps = max(h, 1)
                def _hex_to_rgb(hx):
                    hx = hx.lstrip('#')
                    return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
                def _rgb_to_hex(r, g, b):
                    return f"#{r:02x}{g:02x}{b:02x}"
                c1 = _hex_to_rgb(self.colors.get("primary", "#EADDCD"))
                c2 = _hex_to_rgb("#F4A261")
                for i in range(steps):
                    t = i / steps
                    r = int(c1[0] + (c2[0] - c1[0]) * t)
                    g = int(c1[1] + (c2[1] - c1[1]) * t)
                    b = int(c1[2] + (c2[2] - c1[2]) * t)
                    color = _rgb_to_hex(r, g, b)
                    self.bg_canvas.create_rectangle(0, i, w, i + 1, outline="", fill=color)
            except Exception:
                pass

    def ensure_controls_visible(self):
        if hasattr(self, 'control_frame'):
            try:
                self.control_frame.pack_forget()
            except Exception:
                pass
            self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False, padx=16, pady=8)
            try:
                self.control_frame.lift()
            except Exception:
                pass
        
    def hide_cli_controls(self):
        # 只处理input_frame，保留control_frame中的核心控制按钮
        try:
            self.input_frame.destroy()
        except Exception:
            pass
        
        # 不要清空control_frame，以保持核心按钮（开始测试、停止测试、退出等）可见

if __name__ == "__main__":
    root = tk.Tk()
    app = VocabularyTestGUI(root)
    root.mainloop()
