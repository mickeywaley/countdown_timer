#!/usr/bin/env python3
# 作者: mickeywaley
# 日期: 2025-06-17
# 描述: 简单的倒计时应用程序

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

class CountdownTimer:
    def __init__(self, root):
        """初始化倒计时器"""
        self.root = root
        self.root.title("倒计时器")
        self.root.geometry("300x80")  # 增加初始宽度，确保按钮不被截断
        self.root.attributes("-topmost", True)  # 设置窗口置顶
        
        # 设置中文字体
        self.font = ("WenQuanYi Micro Hei", 36)
        
        # 创建主容器 - 用于显示时间，背景为黑色
        self.time_frame = tk.Frame(root, bg="black")
        self.time_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建倒计时显示标签，文字为红色
        self.time_label = tk.Label(self.time_frame, text="00:00:00", font=self.font, fg="red", bg="black")
        self.time_label.pack(expand=True, fill=tk.BOTH)
        
        # 创建设置菜单
        self.create_menu()
        
        # 倒计时状态变量
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.countdown_thread = None
        
        # 绑定事件 - 鼠标进入/离开时间区域显示/隐藏设置菜单
        self.time_frame.bind("<Enter>", self.show_menu)
        self.menu_frame.bind("<Leave>", self.hide_menu)
        
        # 显示初始时间
        self.update_time_display()
    
    def create_menu(self):
        """创建设置菜单"""
        self.menu_frame = tk.Frame(self.root, bg="darkgray", bd=2, relief=tk.RAISED)
        
        # 时间设置行
        time_frame = tk.Frame(self.menu_frame, bg="darkgray")
        time_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(time_frame, text="时:", font=("WenQuanYi Micro Hei", 10), background="darkgray").pack(side=tk.LEFT, padx=2)
        self.hour_var = tk.StringVar(value="0")
        ttk.Spinbox(time_frame, from_=0, to=23, width=2, textvariable=self.hour_var).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(time_frame, text="分:", font=("WenQuanYi Micro Hei", 10), background="darkgray").pack(side=tk.LEFT, padx=2)
        self.minute_var = tk.StringVar(value="15")
        ttk.Spinbox(time_frame, from_=0, to=59, width=2, textvariable=self.minute_var).pack(side=tk.LEFT, padx=2)
        
        ttk.Label(time_frame, text="秒:", font=("WenQuanYi Micro Hei", 10), background="darkgray").pack(side=tk.LEFT, padx=2)
        self.second_var = tk.StringVar(value="0")
        ttk.Spinbox(time_frame, from_=0, to=59, width=2, textvariable=self.second_var).pack(side=tk.LEFT, padx=2)
        
        # 快捷设置按钮 - 分三排显示
        quick_frame = tk.Frame(self.menu_frame, bg="darkgray")
        quick_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # 第一排快捷按钮
        row1_frame = tk.Frame(quick_frame, bg="darkgray")
        row1_frame.pack(pady=1, fill=tk.X)
        
        ttk.Button(row1_frame, text="1分钟", command=lambda: self.set_quick_time(1)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row1_frame, text="2分钟", command=lambda: self.set_quick_time(2)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row1_frame, text="3分钟", command=lambda: self.set_quick_time(3)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # 第二排快捷按钮
        row2_frame = tk.Frame(quick_frame, bg="darkgray")
        row2_frame.pack(pady=1, fill=tk.X)
        
        ttk.Button(row2_frame, text="5分钟", command=lambda: self.set_quick_time(5)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row2_frame, text="10分钟", command=lambda: self.set_quick_time(10)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row2_frame, text="15分钟", command=lambda: self.set_quick_time(15)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # 第三排快捷按钮
        row3_frame = tk.Frame(quick_frame, bg="darkgray")
        row3_frame.pack(pady=1, fill=tk.X)
        
        ttk.Button(row3_frame, text="20分钟", command=lambda: self.set_quick_time(20)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row3_frame, text="25分钟", command=lambda: self.set_quick_time(25)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        ttk.Button(row3_frame, text="30分钟", command=lambda: self.set_quick_time(30)).pack(side=tk.LEFT, padx=1, expand=True, fill=tk.X)
        
        # 控制按钮行
        button_frame = tk.Frame(self.menu_frame, bg="darkgray")
        button_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_countdown, width=8)
        self.start_button.pack(side=tk.LEFT, padx=2)
        
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_countdown, state=tk.DISABLED, width=8)
        self.pause_button.pack(side=tk.LEFT, padx=2)
        
        self.reset_button = ttk.Button(button_frame, text="重置", command=self.reset_countdown, width=8)
        self.reset_button.pack(side=tk.LEFT, padx=2)
        
        # 关于按钮
        self.about_button = ttk.Button(button_frame, text="关于", command=self.show_about)
        self.about_button.pack(side=tk.LEFT, padx=2)
        
        # 退出按钮
        self.exit_button = ttk.Button(self.menu_frame, text="关闭", command=root.destroy)
        self.exit_button.pack(pady=2, fill=tk.X, padx=5)  # 增加左右边距
        
        # 初始隐藏菜单
        self.menu_frame.pack_forget()
    
    def show_about(self, event=None):
        """显示关于对话框"""
        messagebox.showinfo(
            "关于", 
            "倒计时器 v1.0\n\n"
            "作者: mickeywaley\n"
            "日期: 2025-06-17\n\n"
            "一个简单的倒计时应用程序"
        )
    
    def show_menu(self, event=None):
        """显示设置菜单"""
        self.menu_frame.pack(fill=tk.X)
        # 调整窗口大小以适应菜单 - 增加高度到240
        self.root.geometry(f"300x{240}")
    
    def hide_menu(self, event=None):
        """隐藏设置菜单"""
        # 延迟隐藏，避免鼠标移动到菜单上时闪烁
        self.root.after(200, self._actually_hide_menu)
    
    def _actually_hide_menu(self):
        """实际隐藏菜单的方法"""
        # 获取鼠标位置
        x, y = self.root.winfo_pointerxy()
        x_root, y_root = self.root.winfo_rootx(), self.root.winfo_rooty()
        x_rel, y_rel = x - x_root, y - y_root
        
        # 检查鼠标是否在菜单区域内
        if self.menu_frame.winfo_ismapped():
            menu_y = self.time_frame.winfo_height()
            menu_height = self.menu_frame.winfo_height()
            
            if 0 <= x_rel < self.root.winfo_width() and menu_y <= y_rel < menu_y + menu_height:
                # 鼠标在菜单区域内，不隐藏
                return
        
        # 鼠标不在菜单区域内，隐藏菜单
        self.menu_frame.pack_forget()
        self.root.geometry("300x80")  # 保持宽度一致
    
    def set_quick_time(self, minutes):
        """设置快捷时间"""
        self.hour_var.set("0")
        self.minute_var.set(str(minutes))
        self.second_var.set("0")
        self.remaining_seconds = minutes * 60
        self.update_time_display()
    
    def update_time_display(self):
        """更新时间显示"""
        hours, remainder = divmod(self.remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.time_label.config(text=time_str)
    
    def start_countdown(self):
        """开始倒计时"""
        if not self.running:
            try:
                hours = int(self.hour_var.get())
                minutes = int(self.minute_var.get())
                seconds = int(self.second_var.get())
                self.remaining_seconds = hours * 3600 + minutes * 60 + seconds
                
                if self.remaining_seconds <= 0:
                    messagebox.showerror("错误", "请设置有效的倒计时时间！")
                    return
                
                self.running = True
                self.paused = False
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                
                # 在新线程中运行倒计时
                self.countdown_thread = threading.Thread(target=self._run_countdown)
                self.countdown_thread.daemon = True
                self.countdown_thread.start()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字！")
        elif self.paused:
            # 恢复倒计时
            self.paused = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, text="暂停")
    
    def pause_countdown(self):
        """暂停倒计时"""
        if self.running and not self.paused:
            self.paused = True
            self.start_button.config(state=tk.NORMAL, text="继续")
            self.pause_button.config(state=tk.DISABLED)
    
    def reset_countdown(self):
        """重置倒计时"""
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        
        # 更新显示
        self.update_time_display()
        
        # 更新按钮状态
        self.start_button.config(state=tk.NORMAL, text="开始")
        self.pause_button.config(state=tk.DISABLED, text="暂停")
    
    def _run_countdown(self):
        """在后台线程中运行倒计时"""
        start_time = time.time()
        target_time = start_time + self.remaining_seconds
        
        while self.running and time.time() < target_time:
            if not self.paused:
                # 计算剩余秒数
                self.remaining_seconds = max(0, int(round(target_time - time.time())))
                
                # 直接在主线程中更新UI，避免重复调用after
                self.root.after(0, self.update_time_display)
            
            # 短暂休眠，减少CPU使用率
            time.sleep(0.01)
        
        # 倒计时结束
        if self.running:
            self.root.after(0, self._countdown_complete)
    
    def _countdown_complete(self):
        """倒计时完成时执行"""
        self.running = False
        self.remaining_seconds = 0
        self.update_time_display()
        
        # 更新按钮状态
        self.start_button.config(state=tk.NORMAL, text="开始")
        self.pause_button.config(state=tk.DISABLED, text="暂停")
        
        # 显示提示消息
        messagebox.showinfo("提示", "倒计时结束！")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
