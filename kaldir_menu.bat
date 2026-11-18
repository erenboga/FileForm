@echo off
chcp 65001 > nul
echo ========================================================
echo       FileForm - Windows Sağ Tık Menüsü Kaldırma
echo ========================================================
echo.
if exist "FileForm.exe" (
    "FileForm.exe" --uninstall-menu
) else (
    python main.py --uninstall-menu
)
echo.
echo Menü ve kısayollar sistemden kaldırıldı.
echo.
pause
