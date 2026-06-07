@echo off
chcp 65001 >nul
title 考试平台 - 一键重启

echo.
echo ========================================
echo   考试平台 一键重启脚本
echo ========================================
echo.

:: ===== Config =====
set PROJECT_DIR=%~dp0
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend
set MVN=%USERPROFILE%\.m2\wrapper\dists\apache-maven-3.9.6-bin\3311e1d4\apache-maven-3.9.6\bin\mvn.cmd
set JAVA_HOME=E:\develop\jdk-21

:: ===== 1. Stop Backend =====
echo [1/3] 停止旧后端进程...
for /f "tokens=2" %%i in ('tasklist ^| findstr "java.exe"') do (
    taskkill /PID %%i /F >nul 2>&1
)
echo       旧进程已清理

:: ===== 2. Start Backend =====
echo [2/3] 启动后端 (编译+运行)...
start "Exam-Backend" cmd /c "cd /d %BACKEND_DIR% && set JAVA_HOME=%JAVA_HOME% && %MVN% spring-boot:run -DskipTests 2>&1 | tee backend.log"
echo       后端正在启动，请等待 30 秒...

:: Wait for backend
timeout /t 5 /nobreak >nul

:: ===== 3. Start Frontend =====
echo [3/3] 启动前端...
start "Exam-Frontend" cmd /c "cd /d %FRONTEND_DIR% && npm run dev"

echo.
echo ========================================
echo   启动完成！
echo   后端:  http://localhost:8080
echo   前端:  http://localhost:5173
echo   健康:  http://localhost:8080/api/health
echo ========================================
echo.
echo 按任意键退出...
pause >nul
