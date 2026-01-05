@echo off
echo ========================================
echo    公示地价查询平台 - 服务器启动
echo ========================================
echo.
echo 正在启动HTTP服务器...
echo.

REM 启动HTTP服务器（后台运行）
start /min cmd /c "python -m http.server 8000"

REM 等待服务器启动
echo 等待服务器启动...
timeout /t 3 /nobreak >nul

REM 自动打开浏览器
echo 正在打开浏览器...
start http://localhost:8000/final_map_system.html

echo.
echo ========================================
echo 地图系统已启动！
echo 浏览器应该已自动打开地图页面
echo.
echo 如果浏览器没有自动打开，请手动访问：
echo http://localhost:8000/final_map_system.html
echo.
echo 要停止服务器，请关闭后台的命令行窗口
echo 或者按 Ctrl+C 然后关闭窗口
echo ========================================
echo.
pause