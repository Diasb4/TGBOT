@echo off
ECHO Starting Night Telegram Bot...

:: Проверка наличия Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python not found! Please install Python and ensure it's added to PATH.
    pause
    exit /b 1
)

:: Опционально: активация виртуального окружения (раскомментируй, если используешь)
CALL C:\Users\Laptop\PycharmProjects\TGBOT\venv\Scripts\activate

:: Установка зависимостей (если requirements.txt существует)
IF EXIST requirements.txt (
    ECHO Installing dependencies...
    pip install -r requirements.txt
)

:: Запуск скрипта с аргументом night
ECHO Running night script...
python C:\Users\Laptop\PycharmProjects\TGBOT\Main.py night

:: Пауза для просмотра вывода (опционально)
pause