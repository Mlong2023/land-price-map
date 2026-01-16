@echo off
chcp 65001 >nul
echo ========================================
echo    公示地价查询平台 - 服务器启动
echo ========================================
echo.

REM 检测 Python 是否已安装
echo 正在检测 Python 环境...
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 已安装，版本信息：
    py -3 --version
    echo.
    goto START_SERVER
)

REM Python 未安装，尝试用 python 命令
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 已安装，版本信息：
    python --version
    echo.
    goto START_SERVER_PYTHON
)

REM Python 未安装，提示下载
echo.
echo ========================================
echo    未检测到 Python，需要安装
echo ========================================
echo.
echo 是否自动下载并安装 Python 3.12？
echo.
set /p choice="输入 Y 确认下载，输入 N 取消 [Y/N]: "
if /i "%choice%" neq "Y" (
    echo.
    echo 已取消。请手动安装 Python 3 后重新运行此程序。
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b
)

REM 开始下载 Python
echo.
echo 正在下载 Python 3.12.4 安装包，请稍候...
echo 下载地址：https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe
echo.

REM 设置下载路径
set "PYTHON_INSTALLER=%TEMP%\python-3.12.4-amd64.exe"

REM 使用 PowerShell 下载
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo.
    echo 下载失败！请检查网络连接或手动下载安装。
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b
)

echo.
echo ========================================
echo    下载完成，正在启动安装程序
echo ========================================
echo.
echo 重要提示：
echo 1. 请务必勾选 "Add Python to PATH" 选项！
echo 2. 安装完成后，请关闭此窗口
echo 3. 然后重新双击运行 启动服务器.bat
echo.
pause

REM 启动安装程序
start "" "%PYTHON_INSTALLER%"

echo.
echo Python 安装程序已启动。
echo 安装完成后请重新运行此脚本。
echo.
pause
exit /b

:START_SERVER
echo 正在启动HTTP服务器...
echo.
start /min cmd /c "py -3 -m http.server 8000"
goto OPEN_BROWSER

:START_SERVER_PYTHON
echo 正在启动HTTP服务器...
echo.
start /min cmd /c "python -m http.server 8000"
goto OPEN_BROWSER

:OPEN_BROWSER
REM 等待服务器启动
echo 服务器启动中...
timeout /t 3 /nobreak >nul

REM 自动打开浏览器
echo 打开浏览器...
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
