@echo off
chcp 65001 > nul
:menu
cls
echo ==========================================
echo       雷霆战机经验优化系统工具包
echo ==========================================
echo  1. 运行优化计算器 (main.py)
echo  2. 录入/更新背包材料 (update_inventory.py)
echo  3. 退出
echo ==========================================
set /p opt=请选择操作 (1-3):

if "%opt%"=="1" python main.py
if "%opt%"=="2" python update_inventory.py
if "%opt%"=="3" exit

pause
goto menu