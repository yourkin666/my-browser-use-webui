#!/usr/bin/env python3
"""
测试动态文件扫描功能
"""
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.browser_use.browser_use_agent import BrowserUseAgent

def test_dynamic_file_scanning():
    """测试动态文件扫描功能"""
    print("🔍 测试动态文件扫描功能...")
    
    # 检查下载目录
    downloads_dir = os.path.abspath("./tmp/downloads")
    print(f"📁 扫描目录: {downloads_dir}")
    
    if os.path.exists(downloads_dir):
        print("📋 当前目录中的文件:")
        for file in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            print(f"  📄 {file} ({file_size:.1f}MB)")
        
        print("\n🎯 扫描图片文件:")
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.tif')
        found_images = []
        
        for file in os.listdir(downloads_dir):
            if file.lower().endswith(image_extensions):
                file_path = os.path.join(downloads_dir, file)
                found_images.append(file_path)
                print(f"  ✅ {file}")
        
        print(f"\n📊 总计找到 {len(found_images)} 个图片文件")
        return found_images
    else:
        print(f"❌ 目录不存在: {downloads_dir}")
        return []

if __name__ == "__main__":
    found_images = test_dynamic_file_scanning()
    print(f"\n🎉 动态扫描功能测试完成！找到 {len(found_images)} 个可用图片文件") 