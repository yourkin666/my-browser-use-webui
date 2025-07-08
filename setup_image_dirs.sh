#!/bin/bash

# 小红书发帖目录设置脚本
# 用于快速创建图片和文案存放目录

echo "🎯 小红书发帖目录设置工具"
echo "=================================="

# 创建主要目录
echo "📁 创建主要目录..."
mkdir -p tmp/xiaohongshu_posts
mkdir -p tmp/downloads
mkdir -p tmp/deep_research

echo "✅ 主要目录创建完成"

# 询问用户是否要创建示例帖子
echo ""
echo "📝 是否创建示例帖子目录? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🎨 创建示例帖子目录..."
    
    # 创建示例帖子目录
    mkdir -p "tmp/xiaohongshu_posts/我的美食分享"
    mkdir -p "tmp/xiaohongshu_posts/旅游日记"
    mkdir -p "tmp/xiaohongshu_posts/生活随拍"
    
    # 创建示例文案
    cat > "tmp/xiaohongshu_posts/我的美食分享/文案.txt" << 'EOF'
🍜 今日美食推荐

分享一家超好吃的餐厅！
环境很棒，服务贴心，最重要的是食物真的很棒！

📍 地址：请在此处填写具体地址
💰 人均：请在此处填写价格
⭐ 推荐指数：5星

#美食 #餐厅推荐 #生活分享 #今日美食
EOF

    cat > "tmp/xiaohongshu_posts/旅游日记/游记.md" << 'EOF'
# 🌟 周末小旅行

## 📍 目的地
请在此处填写旅行目的地

## 🎯 行程安排
- 上午：景点参观
- 中午：当地美食
- 下午：拍照打卡
- 晚上：夜景欣赏

## 💡 旅行小贴士
1. 记得带充电宝
2. 提前查看天气预报
3. 准备舒适的鞋子

#旅行 #周末游 #打卡 #生活记录
EOF

    cat > "tmp/xiaohongshu_posts/生活随拍/文案.txt" << 'EOF'
📸 生活中的小美好

记录平凡日子里的不平凡瞬间
每一个moment都值得被记录

✨ 今日心情：很棒
🌈 今日天气：晴朗
💭 今日感悟：生活很美好

#生活记录 #随拍 #日常 #美好时光
EOF

    echo "✅ 示例帖子创建完成！"
    echo ""
    echo "📋 已创建以下示例目录："
    echo "  • tmp/xiaohongshu_posts/我的美食分享/"
    echo "  • tmp/xiaohongshu_posts/旅游日记/"
    echo "  • tmp/xiaohongshu_posts/生活随拍/"
    echo ""
    echo "💡 在每个目录中放入对应的图片文件即可！"
fi

echo ""
echo "🎉 目录设置完成！"
echo ""
echo "📝 下一步："
echo "1. 在 tmp/xiaohongshu_posts/ 下创建子目录"
echo "2. 在子目录中放入图片文件（.jpg, .png等）"
echo "3. 在子目录中放入文案文件（.txt, .md）"
echo "4. 运行小红书Agent开始发帖"
echo ""
echo "📖 详细说明请查看：tmp/xiaohongshu_posts/README.md" 