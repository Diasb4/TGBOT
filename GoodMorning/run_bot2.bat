@echo off
ECHO Starting Morning Telegram Bot...

:: Установка кодировки UTF-8 для корректного отображения русских символов
chcp 65001 >nul

:: Проверка наличия Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python not found! Please install Python and ensure it's added to PATH.
    pause
    exit /b 1
)

:: Активация виртуального окружения
CALL C:\Users\Laptop\PycharmProjects\TGBOT\.venv\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to activate virtual environment! Check if .venv exists.
    pause
    exit /b 1
)

:: Установка зависимостей
IF EXIST requirements.txt (
    ECHO Installing dependencies...
    pip install -r requirements.txt
) ELSE (
    ECHO requirements.txt not found! Creating one...
    ECHO requests==2.32.3>requirements.txt
    ECHO Telethon==1.36.0>>requirements.txt
    pip install -r requirements.txt
)

:: Запуск скрипта
ECHO Running morning script...
python C:\Users\Laptop\PycharmProjects\TGBOT\Main.py morning

:: Пауза для просмотра вывода
pause