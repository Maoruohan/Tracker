#!/usr/bin/env python3
"""
生成卫星跟踪器软件图标
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

def create_icon():
    """创建应用图标"""
    # 尺寸：1024x1024 (macOS 图标标准尺寸)
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # ===== 1. 深蓝色渐变背景 =====
    # 从深蓝到更深的蓝紫色
    for y in range(size):
        ratio = y / size
        r = int(8 + 10 * ratio)      # 8 -> 18
        g = int(20 + 60 * ratio)     # 20 -> 80
        b = int(80 + 120 * ratio)    # 80 -> 200
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # ===== 2. 圆角矩形遮罩 =====
    # 创建一个圆角矩形遮罩
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = 180
    mask_draw.rounded_rectangle([(0, 0), (size, size)], radius=radius, fill=255)
    
    # 应用遮罩
    img.putalpha(mask)
    
    # ===== 3. 星空效果 =====
    import random
    random.seed(42)  # 固定随机种子，使星星位置固定
    
    for _ in range(80):
        x = random.randint(20, size - 20)
        y = random.randint(20, size - 20)
        brightness = random.randint(80, 200)
        radius_star = random.randint(1, 3)
        draw.ellipse([(x - radius_star, y - radius_star), (x + radius_star, y + radius_star)], 
                     fill=(brightness, brightness, brightness + 50, random.randint(100, 200)))
    
    # 几颗亮星带光晕
    for _ in range(5):
        x = random.randint(100, size - 100)
        y = random.randint(100, size - 300)
        # 光晕
        for r in range(20, 5, -3):
            alpha = int(30 * (1 - r / 20))
            draw.ellipse([(x - r, y - r), (x + r, y + r)], 
                         fill=(150, 200, 255, alpha))
        # 星核
        draw.ellipse([(x - 3, y - 3), (x + 3, y + 3)], fill=(255, 255, 255, 220))
    
    # ===== 4. 绘制卫星 =====
    # 卫星主体
    sat_x, sat_y = size // 2, size // 2 - 60
    
    # 卫星主体（椭圆形）
    draw.ellipse([(sat_x - 70, sat_y - 45), (sat_x + 70, sat_y + 45)], 
                 fill=(180, 210, 240, 230), outline=(220, 240, 255, 200), width=3)
    
    # 卫星主体高光
    draw.ellipse([(sat_x - 50, sat_y - 30), (sat_x - 20, sat_y - 5)], 
                 fill=(220, 240, 255, 100))
    
    # 卫星天线（左边）
    draw.line([(sat_x - 70, sat_y - 10), (sat_x - 140, sat_y - 60)], 
              fill=(200, 220, 240, 200), width=4)
    draw.ellipse([(sat_x - 150, sat_y - 75), (sat_x - 130, sat_y - 45)], 
                 fill=(220, 235, 255, 180), outline=(200, 220, 240, 150), width=2)
    
    # 卫星天线（右边）
    draw.line([(sat_x + 70, sat_y + 10), (sat_x + 140, sat_y + 60)], 
              fill=(200, 220, 240, 200), width=4)
    draw.ellipse([(sat_x + 130, sat_y + 45), (sat_x + 150, sat_y + 75)], 
                 fill=(220, 235, 255, 180), outline=(200, 220, 240, 150), width=2)
    
    # 卫星翅膀（太阳能板）
    # 左翅膀
    draw.rectangle([(sat_x - 160, sat_y - 80), (sat_x - 80, sat_y - 60)], 
                   fill=(60, 100, 180, 200), outline=(100, 150, 220, 150), width=2)
    # 左翅膀格子
    for i in range(4):
        x1 = sat_x - 155 + i * 20
        draw.line([(x1, sat_y - 78), (x1, sat_y - 62)], fill=(100, 150, 220, 80), width=1)
    for i in range(2):
        y1 = sat_y - 75 + i * 15
        draw.line([(sat_x - 158, y1), (sat_x - 82, y1)], fill=(100, 150, 220, 80), width=1)
    
    # 右翅膀
    draw.rectangle([(sat_x + 80, sat_y - 80), (sat_x + 160, sat_y - 60)], 
                   fill=(60, 100, 180, 200), outline=(100, 150, 220, 150), width=2)
    # 右翅膀格子
    for i in range(4):
        x1 = sat_x + 85 + i * 20
        draw.line([(x1, sat_y - 78), (x1, sat_y - 62)], fill=(100, 150, 220, 80), width=1)
    for i in range(2):
        y1 = sat_y - 75 + i * 15
        draw.line([(sat_x + 82, y1), (sat_x + 158, y1)], fill=(100, 150, 220, 80), width=1)
    
    # 卫星底部设备
    draw.rectangle([(sat_x - 20, sat_y + 40), (sat_x + 20, sat_y + 65)], 
                   fill=(150, 180, 210, 200), outline=(200, 220, 240, 150), width=2)
    draw.ellipse([(sat_x - 12, sat_y + 58), (sat_x + 12, sat_y + 70)], 
                 fill=(100, 130, 180, 180))
    
    # 卫星信号波（装饰）
    for i, angle_offset in enumerate([-30, 0, 30]):
        for j, r in enumerate([60, 80, 100]):
            alpha = int(40 * (1 - j / 3))
            draw.arc([(sat_x - r - 40, sat_y - r - 40 + 20), 
                      (sat_x + r - 40, sat_y + r - 40 + 20)], 
                     start=220 + angle_offset, end=260 + angle_offset, 
                     fill=(100, 200, 255, alpha), width=2)
    
    # ===== 5. 绘制文字 "Tracker" =====
    # 尝试加载字体，如果失败则使用默认字体
    try:
        # macOS 系统字体
        font_paths = [
            "/System/Library/Fonts/SFProDisplay-Bold.otf",
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Arial.ttf",
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path):
                font = ImageFont.truetype(path, 140)
                break
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 文字阴影
    shadow_offset = 6
    draw.text((size//2 - 200 + shadow_offset, size//2 + 180 + shadow_offset), 
              "Tracker", font=font, fill=(30, 60, 100, 150))
    
    # 主文字 - 渐变效果
    text_x = size//2 - 200
    text_y = size//2 + 180
    
    # 逐像素绘制渐变文字（简化版：分层绘制）
    for i in range(5):
        offset = i * 2
        alpha = 200 - i * 20
        color = (100 + i * 20, 180 + i * 10, 255, alpha)
        draw.text((text_x - offset, text_y - offset), "Tracker", font=font, fill=color)
    
    # 最上层文字 - 亮白色
    draw.text((text_x, text_y), "Tracker", font=font, fill=(220, 240, 255, 255))
    
    # ===== 6. 底部小字 "Satellite Tracking System" =====
    try:
        font_small = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 36)
    except:
        font_small = ImageFont.load_default()
    
    small_text = "Satellite Tracking System"
    # 使用 getbbox 计算文字宽度
    bbox = draw.textbbox((0, 0), small_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x_small = (size - text_width) // 2
    draw.text((text_x_small, size//2 + 330), small_text, font=font_small, fill=(150, 190, 220, 180))
    
    # ===== 7. 装饰性轨道环 =====
    for i in range(3):
        r = 300 + i * 40
        alpha = 60 - i * 15
        draw.ellipse([(size//2 - r, size//2 - r + 20), (size//2 + r, size//2 + r + 20)], 
                     outline=(100, 180, 255, max(alpha, 10)), width=1)
    
    # ===== 8. 保存 =====
    # 保存为 PNG
    img.save('icon.png', 'PNG')
    
    # 转换为 ICNS (macOS 图标格式)
    try:
        # 生成不同尺寸
        sizes = [16, 32, 64, 128, 256, 512, 1024]
        iconset_dir = 'icon.iconset'
        os.makedirs(iconset_dir, exist_ok=True)
        
        for s in sizes:
            if s <= 1024:
                img_resized = img.resize((s, s), Image.Resampling.LANCZOS)
                img_resized.save(f'{iconset_dir}/icon_{s}x{s}.png', 'PNG')
                # 2x 版本
                if s * 2 <= 1024:
                    img_resized_2x = img.resize((s * 2, s * 2), Image.Resampling.LANCZOS)
                    img_resized_2x.save(f'{iconset_dir}/icon_{s}x{s}@2x.png', 'PNG')
        
        # 使用系统命令转换为 icns
        os.system(f'iconutil -c icns {iconset_dir} -o icon.icns 2>/dev/null')
        os.system(f'rm -rf {iconset_dir}')
        print("✅ 已生成 icon.icns")
    except Exception as e:
        print(f"⚠️ ICNS 生成失败: {e}")
    
    print("✅ 图标已生成: icon.png")
    return img

if __name__ == "__main__":
    create_icon()
