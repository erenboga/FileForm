@echo off
chcp 65001 > nul
echo ========================================================
echo       FileForm - Windows Sağ Tık Menüsü Kurulumu
echo ========================================================
echo.
if exist "FileForm.exe" (
    "FileForm.exe" --install-menu
) else (
    python main.py --install-menu
)
echo.
echo Kurulum tamamlandı! Artık herhangi bir dosyaya sağ tıklayarak
echo dönüştürme yapabilirsiniz.
echo.
pause
