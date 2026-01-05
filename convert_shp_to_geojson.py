#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SHP文件转换为GeoJSON格式脚本
根据不同图层保留指定的属性字段
"""

import os
import json
import sys
from pathlib import Path

try:
    import geopandas as gpd
    import pandas as pd
    print("✅ 成功导入 geopandas 和 pandas")
except ImportError as e:
    print("❌ 缺少必要的库，请安装：")
    print("pip install geopandas pandas")
    print(f"错误详情: {e}")
    sys.exit(1)

def convert_shp_to_geojson(shp_path, output_path, keep_fields=None, layer_name=""):
    """
    将SHP文件转换为GeoJSON格式
    
    Args:
        shp_path: SHP文件路径
        output_path: 输出GeoJSON文件路径
        keep_fields: 要保留的字段列表
        layer_name: 图层名称（用于日志）
    """
    try:
        print(f"\n🔄 开始处理 {layer_name} 图层...")
        print(f"   输入文件: {shp_path}")
        print(f"   输出文件: {output_path}")
        
        # 尝试不同的编码方式读取SHP文件
        encodings_to_try = ['gbk', 'gb2312', 'utf-8', 'cp936', 'latin1']
        gdf = None
        
        for encoding in encodings_to_try:
            try:
                print(f"   🔄 尝试编码: {encoding}")
                gdf = gpd.read_file(shp_path, encoding=encoding)
                print(f"   ✅ 成功使用编码 {encoding} 读取SHP文件，包含 {len(gdf)} 个要素")
                break
            except UnicodeDecodeError:
                print(f"   ❌ 编码 {encoding} 失败")
                continue
            except Exception as e:
                print(f"   ❌ 编码 {encoding} 失败: {str(e)}")
                continue
        
        if gdf is None:
            print("   ❌ 所有编码方式都失败了")
            return False
        
        # 显示原始字段
        print(f"   📋 原始字段: {list(gdf.columns)}")
        
        # 如果指定了要保留的字段，则过滤字段
        if keep_fields:
            # 确保geometry字段始终保留
            fields_to_keep = ['geometry'] + [field for field in keep_fields if field in gdf.columns]
            
            # 检查哪些字段不存在
            missing_fields = [field for field in keep_fields if field not in gdf.columns]
            if missing_fields:
                print(f"   ⚠️  以下字段在数据中不存在: {missing_fields}")
                # 尝试模糊匹配字段名
                available_fields = list(gdf.columns)
                for missing_field in missing_fields:
                    for available_field in available_fields:
                        if missing_field in available_field or available_field in missing_field:
                            print(f"   💡 可能的匹配字段: '{missing_field}' -> '{available_field}'")
                            if available_field not in fields_to_keep:
                                fields_to_keep.append(available_field)
            
            # 过滤字段
            gdf = gdf[fields_to_keep]
            print(f"   ✂️  保留字段: {[col for col in fields_to_keep if col != 'geometry']}")
        
        # 确保使用WGS84坐标系统 (EPSG:4326)
        if gdf.crs is None:
            print("   ⚠️  未检测到坐标系统，假设为WGS84")
            gdf.crs = 'EPSG:4326'
        elif gdf.crs.to_string() != 'EPSG:4326':
            print(f"   🔄 转换坐标系统从 {gdf.crs} 到 WGS84")
            gdf = gdf.to_crs('EPSG:4326')
        
        # 显示数据预览
        print(f"   📊 数据预览:")
        for i, row in gdf.head(2).iterrows():
            print(f"      要素 {i+1}: {dict(row.drop('geometry'))}")
        
        # 转换为GeoJSON格式
        geojson_data = json.loads(gdf.to_json())
        
        # 添加名称属性
        geojson_data['name'] = layer_name
        
        # 保存为GeoJSON文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ 成功转换并保存到: {output_path}")
        print(f"   📈 输出统计: {len(geojson_data['features'])} 个要素")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 转换失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 开始SHP到GeoJSON转换任务")
    print("=" * 50)
    
    # 定义输入和输出目录
    input_dir = Path("data/GeoJSON")
    output_dir = input_dir  # 输出到同一目录
    
    # 检查输入目录是否存在
    if not input_dir.exists():
        print(f"❌ 输入目录不存在: {input_dir}")
        return
    
    # 定义转换配置
    conversion_configs = [
        {
            'layer_name': '定级范围',
            'shp_file': '定级范围.shp',
            'output_file': '定级范围.geojson',
            'keep_fields': ['面积']  # 只保留面积字段
        },
        {
            'layer_name': '住宅用地',
            'shp_file': '住宅用地.shp',
            'output_file': '住宅用地.geojson',
            'keep_fields': ['一级用途', '土地级别', '面积', '地面地价']
        },
        {
            'layer_name': '商服用地',
            'shp_file': '商服用地.shp',
            'output_file': '商服用地.geojson',
            'keep_fields': ['一级用途', '土地级别', '面积', '地面地价']
        },
        {
            'layer_name': '工业用地',
            'shp_file': '工业用地.shp',
            'output_file': '工业用地.geojson',
            'keep_fields': ['一级用途', '土地级别', '面积', '地面地价']
        },
        {
            'layer_name': '公共用地',
            'shp_file': '公共用地.shp',
            'output_file': '公共用地.geojson',
            'keep_fields': ['一级用途', '土地级别', '面积', '地面地价']
        }
    ]
    
    # 执行转换
    success_count = 0
    total_count = len(conversion_configs)
    
    for config in conversion_configs:
        shp_path = input_dir / config['shp_file']
        output_path = output_dir / config['output_file']
        
        # 检查SHP文件是否存在
        if not shp_path.exists():
            print(f"\n❌ SHP文件不存在: {shp_path}")
            continue
        
        # 执行转换
        if convert_shp_to_geojson(
            shp_path=shp_path,
            output_path=output_path,
            keep_fields=config['keep_fields'],
            layer_name=config['layer_name']
        ):
            success_count += 1
    
    # 输出总结
    print("\n" + "=" * 50)
    print("📊 转换任务完成")
    print(f"✅ 成功转换: {success_count}/{total_count} 个图层")
    
    if success_count == total_count:
        print("🎉 所有图层转换成功！")
    else:
        print(f"⚠️  有 {total_count - success_count} 个图层转换失败")
    
    # 列出输出文件
    print("\n📁 输出文件列表:")
    for config in conversion_configs:
        output_path = output_dir / config['output_file']
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"   ✅ {config['output_file']} ({file_size:,} 字节)")
        else:
            print(f"   ❌ {config['output_file']} (未生成)")

if __name__ == "__main__":
    main()