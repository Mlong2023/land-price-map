# 公示地价查询平台

基于高德地图API的WEB GIS网站，支持地价查询、地块信息展示和空间分析功能。

## 🚀 快速开始

### 1. 启动项目

**重要**: 必须使用HTTP服务器运行项目，不能直接双击HTML文件打开。

```bash
# 方法1: 使用Python (推荐)
python -m http.server 8000

# 方法2: 使用Node.js
npx http-server

# 方法3: 使用PHP
php -S localhost:8000
```

然后在浏览器中访问: `http://localhost:8000`

### 2. 功能测试

1. **地图显示测试**:
   - 打开页面后应该看到登封市的卫星地图
   - 如果地图不显示，请查看[故障排除指南](TROUBLESHOOTING.md)

2. **图层面板测试**:
   - 点击右上角的三条横线图标
   - 应该显示图层控制面板
   - 包含"城镇基准地价"和"交易案例"两个组

3. **图层功能测试**:
   - 勾选/取消勾选各个图层选项
   - 点击"城镇基准地价"展开子选项
   - 测试各个子图层的显示/隐藏

### 3. 调试工具

如果遇到问题，可以使用内置的调试工具：

```javascript
// 在浏览器控制台中运行
window.debugGIS.checkStatus()  // 检查系统状态
window.debugGIS.forceInitMap() // 强制初始化地图
window.testLayerPanel()        // 测试图层面板
```

### 4. 简化测试页面

如果主页面有问题，可以使用简化的测试页面：
- 访问: `http://localhost:8000/test.html`
- 点击"初始化地图"按钮测试基本功能

## 📋 系统要求

- **浏览器**: Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- **网络**: 需要访问高德地图API
- **服务器**: 必须使用HTTP服务器（不支持file://协议）

## 🗺️ 地图信息

- **中心点**: 河南省郑州市登封市 `[113.050651, 34.459389]`
- **坐标系**: GCJ02（火星坐标系）
- **默认缩放**: 12级
- **地图类型**: 支持影像图和电子地图切换

## 📊 数据说明

### 图层结构
- **城镇基准地价**
  - 定级范围 ✓
  - 商服用地 ✓
  - 住宅用地 ✓
  - 工业用地 ✓
  - 公共用地 ☐
- **交易案例**
  - 交易案例_商服用地 ☐
  - 交易案例_住宅用地 ☐
  - 交易案例_工业用地 ☐

### 数据文件
- `data/GeoJSON/定级范围.geojson`
- `data/GeoJSON/商服用地.geojson`
- `data/GeoJSON/住宅用地.geojson`
- `data/GeoJSON/工业用地.geojson`
- `data/GeoJSON/公共用地.geojson`

## 🔧 故障排除

如果遇到问题，请按以下步骤排查：

1. **检查控制台错误**: 打开F12开发者工具查看错误信息
2. **运行状态检查**: 在控制台运行 `window.debugGIS.checkStatus()`
3. **查看详细指南**: 参考 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. **使用测试页面**: 访问 `test.html` 进行基础功能测试

## 🎯 主要功能

- ✅ 高德地图集成（影像图/电子地图切换）
- ✅ 图层管理（显示/隐藏、分组管理）
- ✅ 地块信息查询（点击查看详情）
- ✅ 搜索功能（地址搜索、高级筛选）
- ✅ 响应式设计（支持移动端）
- ✅ 数据可视化（不同用地类型不同颜色）

## 📝 开发说明

### 文件结构
```
project/
├── index.html              # 主页面
├── test.html              # 测试页面
├── css/
│   ├── style.css          # 主样式
│   └── responsive.css     # 响应式样式
├── js/
│   ├── map.js            # 地图管理
│   ├── layers.js         # 图层管理
│   ├── search.js         # 搜索功能
│   ├── dataLoader.js     # 数据加载
│   ├── utils.js          # 工具函数
│   └── debug.js          # 调试工具
├── data/GeoJSON/         # GeoJSON数据文件
└── assets/               # 静态资源
```

### API配置
高德地图API密钥在 `index.html` 中配置：
```html
<script src="https://webapi.amap.com/maps?v=2.0&key=YOUR_API_KEY"></script>
```

## 📞 技术支持

如果遇到无法解决的问题，请提供：
1. 浏览器控制台的完整错误信息
2. `window.debugGIS.checkStatus()` 的输出
3. 浏览器版本和操作系统信息