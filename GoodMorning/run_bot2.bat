@echo off
REM Запуск Python-скрипта Main.py для генерации сообщений

REM Проверяем, установлен ли Python
where python >nul 2>&1
if errorlevel 1 (
    echo Python не найден в PATH. Пожалуйста, установите Python и добавьте его в системный PATH.
    pause
    exit /b 1
)

REM Запускаем Main.py
python Main.py morning

pause
