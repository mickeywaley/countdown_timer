#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

class CountdownTimer:
    def __init__(self, root):
        """初始化倒计时器"""
        self.root = root
        self.root.title("演示倒计时器")
        self.root.geometry("300x200")
        self.root.attributes("-topmost", True)  # 设置窗口置顶
        
        # 设置中文字体
        self.font = ("WenQuanYi Micro Hei", 24)
        
        # 创建倒计时显示标签
        self.time_label = tk.Label(root, text="00:00:00", font=self.font, fg="red")
        self.time_label.pack(pady=20)
        
        # 创建时间设置控件
        frame = ttk.Frame(root)
        frame.pack(pady=10)
        
        ttk.Label(frame, text="小时:", font=("WenQuanYi Micro Hei", 10)).grid(row=0, column=0)
        self.hour_var = tk.StringVar(value="0")
        ttk.Spinbox(frame, from_=0, to=23, width=5, textvariable=self.hour_var).grid(row=0, column=1)
        
        ttk.Label(frame, text="分钟:", font=("WenQuanYi Micro Hei", 10)).grid(row=0, column=2)
        self.minute_var = tk.StringVar(value="15")
        ttk.Spinbox(frame, from_=0, to=59, width=5, textvariable=self.minute_var).grid(row=0, column=3)
        
        ttk.Label(frame, text="秒:", font=("WenQuanYi Micro Hei", 10)).grid(row=0, column=4)
        self.second_var = tk.StringVar(value="0")
        ttk.Spinbox(frame, from_=0, to=59, width=5, textvariable=self.second_var).grid(row=0, column=5)
        
        # 创建控制按钮
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="开始", command=self.start_countdown)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="暂停", command=self.pause_countdown, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="重置", command=self.reset_countdown)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # 倒计时状态变量
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.countdown_thread = None
    
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
        self.time_label.config(text="00:00:00")
        
        # 更新按钮状态
        self.start_button.config(state=tk.NORMAL, text="开始")
        self.pause_button.config(state=tk.DISABLED, text="暂停")
    
    def _run_countdown(self):
        """在后台线程中运行倒计时"""
        while self.running and self.remaining_seconds > 0:
            if not self.paused:
                # 更新显示
                hours, remainder = divmod(self.remaining_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                
                # 使用after方法在主线程中更新UI
                self.root.after(0, lambda s=time_str: self.time_label.config(text=s))
                
                # 减少剩余时间
                self.remaining_seconds -= 1
                
                # 检查是否倒计时结束
                if self.remaining_seconds == 0:
                    self.root.after(0, self._countdown_complete)
            
            # 等待1秒
            time.sleep(1)
    
    def _countdown_complete(self):
        """倒计时完成时执行"""
        self.running = False
        self.time_label.config(text="00:00:00")
        self.start_button.config(state=tk.NORMAL, text="开始")
        self.pause_button.config(state=tk.DISABLED, text="暂停")
        
        # 显示提示消息
        messagebox.showinfo("提示", "倒计时结束！")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()
