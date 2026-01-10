#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码安全的启动器
"""

import os
import sys
import subprocess
import locale
import threading
import time

def setup_encoding():
    """设置安全的编码环境"""
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LANG'] = 'zh_CN.UTF-8'
    
    # 设置标准输出编码
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
            sys.stderr.reconfigure(encoding='utf-8', errors='ignore')
        except:
            pass

def safe_subprocess_run(cmd, **kwargs):
    """安全的subprocess运行"""
    try:
        # 设置编码相关参数
        kwargs.setdefault('encoding', 'utf-8')
        kwargs.setdefault('errors', 'ignore')
        kwargs.setdefault('text', True)
        
        return subprocess.run(cmd, **kwargs)
    except UnicodeDecodeError as e:
        print(f"编码错误，尝试使用gbk编码: {e}")
        try:
            kwargs['encoding'] = 'gbk'
            return subprocess.run(cmd, **kwargs)
        except:
            kwargs['encoding'] = 'latin1'
            return subprocess.run(cmd, **kwargs)
    except Exception as e:
        print(f"subprocess运行错误: {e}")
        return None

def safe_check_chrome_process():
    """安全检查Chrome进程"""
    try:
        # 使用tasklist命令检查Chrome进程
        result = safe_subprocess_run(['tasklist', '/FI', 'IMAGENAME eq chrome.exe'], 
                                   capture_output=True)
        
        if result and result.stdout:
            chrome_processes = result.stdout
            if chrome_processes and 'chrome.exe' in chrome_processes:
                return True
        return False
    except Exception as e:
        print(f"检查Chrome进程时出错: {e}")
        return False

def main():
    """主函数"""
    print("🚀 启动编码安全的数字机器人系统...")
    
    # 设置编码
    setup_encoding()
    
    try:
        # 导入主模块
        print("导入主应用...")
        import combined_launcher
        
        print("✅ 系统启动成功!")
        
    except UnicodeDecodeError as e:
        print(f"❌ 编码错误: {e}")
        print("建议检查文件编码格式")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
