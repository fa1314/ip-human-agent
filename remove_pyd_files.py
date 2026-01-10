#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除.pyd文件，使系统使用恢复的.py源文件
"""

import os
import glob
from pathlib import Path

def find_pyd_files():
    """查找所有.pyd文件"""
    pyd_files = []
    
    # 查找所有.pyd文件
    for root, dirs, files in os.walk('.'):
        # 跳过备份目录
        if 'python_source_backup' in root:
            continue
            
        for file in files:
            if file.endswith('.pyd'):
                pyd_path = os.path.join(root, file)
                pyd_files.append(pyd_path)
    
    return pyd_files

def categorize_pyd_files(pyd_files):
    """分类.pyd文件"""
    # 有对应.py文件的.pyd文件
    with_py_source = []
    # 没有对应.py文件的.pyd文件（保留）
    without_py_source = []
    
    for pyd_file in pyd_files:
        # 计算对应的.py文件路径
        py_file = pyd_file.replace('.cp312-win_amd64.pyd', '.py').replace('.pyd', '.py')
        
        if os.path.exists(py_file):
            with_py_source.append((pyd_file, py_file))
        else:
            without_py_source.append(pyd_file)
    
    return with_py_source, without_py_source

def remove_pyd_files(pyd_files_to_remove):
    """删除指定的.pyd文件"""
    print(f"🗑️  开始删除 {len(pyd_files_to_remove)} 个.pyd文件...")
    
    removed_count = 0
    error_count = 0
    
    for pyd_file, py_file in pyd_files_to_remove:
        try:
            if os.path.exists(pyd_file):
                os.remove(pyd_file)
                print(f"   ✅ 删除: {pyd_file} (对应 {py_file})")
                removed_count += 1
            else:
                print(f"   ⚠️  文件不存在: {pyd_file}")
        except Exception as e:
            print(f"   ❌ 删除失败: {pyd_file} - {e}")
            error_count += 1
    
    print(f"\n📊 删除结果:")
    print(f"   ✅ 成功删除: {removed_count} 个文件")
    print(f"   ❌ 删除失败: {error_count} 个文件")
    
    return removed_count

def main():
    """主函数"""
    print("🔄 .pyd文件删除工具")
    print("=" * 50)
    
    # 查找所有.pyd文件
    print("🔍 查找.pyd文件...")
    pyd_files = find_pyd_files()
    print(f"找到 {len(pyd_files)} 个.pyd文件")
    
    # 分类.pyd文件
    with_py_source, without_py_source = categorize_pyd_files(pyd_files)
    
    print(f"\n📊 文件分析:")
    print(f"   有对应.py源文件: {len(with_py_source)} 个")
    print(f"   无对应.py源文件: {len(without_py_source)} 个")
    
    if with_py_source:
        print(f"\n📋 将删除的.pyd文件 (有对应.py源文件):")
        for i, (pyd_file, py_file) in enumerate(with_py_source[:10]):
            print(f"   {i+1}. {pyd_file}")
        if len(with_py_source) > 10:
            print(f"   ... 还有 {len(with_py_source) - 10} 个文件")
        
        # 删除有对应.py源文件的.pyd文件
        removed_count = remove_pyd_files(with_py_source)
        
        if removed_count > 0:
            print(f"\n🎉 成功删除 {removed_count} 个.pyd文件")
            print("✅ 系统现在将使用.py源文件运行")
        else:
            print("\n⚠️  没有删除任何.pyd文件")
    else:
        print("\n✅ 没有找到需要删除的.pyd文件")
    
    if without_py_source:
        print(f"\n📋 保留的.pyd文件 (无对应.py源文件):")
        for i, pyd_file in enumerate(without_py_source[:5]):
            print(f"   - {pyd_file}")
        if len(without_py_source) > 5:
            print(f"   ... 还有 {len(without_py_source) - 5} 个文件")
    
    print(f"\n📝 操作完成!")
    print("   1. 已删除有对应.py源文件的.pyd文件")
    print("   2. 保留了没有.py源文件的.pyd文件")
    print("   3. 系统现在将优先使用.py源文件")
    print("   4. 可以正常编辑和调试源代码")

if __name__ == "__main__":
    main()
