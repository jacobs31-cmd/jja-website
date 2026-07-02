@echo off
REM Copies the five archive images into the wp-content/uploads tree so the
REM legacy WordPress URLs continue to resolve after the DNS cutover to the
REM new Cloudflare-hosted site.
REM
REM Source: C:\Website\assets\img\
REM Destinations:
REM   wp-content\uploads\sites\38\2026\03\  (4 files)
REM   wp-content\uploads\sites\38\2026\04\  (1 file)

setlocal
cd /d "%~dp0"

echo Creating folder structure...
if not exist "wp-content\uploads\sites\38\2026\03" mkdir "wp-content\uploads\sites\38\2026\03"
if not exist "wp-content\uploads\sites\38\2026\04" mkdir "wp-content\uploads\sites\38\2026\04"

echo Copying images...
copy /Y "assets\img\Bryan-sig-file-2.jpg"        "wp-content\uploads\sites\38\2026\03\Bryan-sig-file-2.jpg"
copy /Y "assets\img\Rons-email-sig.jpg"          "wp-content\uploads\sites\38\2026\03\Rons-email-sig.jpg"
copy /Y "assets\img\image-4.jpg"                 "wp-content\uploads\sites\38\2026\03\image-4.jpg"
copy /Y "assets\img\JJA-Google-Review-QR-Code.png" "wp-content\uploads\sites\38\2026\03\JJA-Google-Review-QR-Code.png"
copy /Y "assets\img\Best-of-the-Best-all-7.png"  "wp-content\uploads\sites\38\2026\04\Best-of-the-Best-all-7.png"

echo.
echo Done. Verifying:
dir /b "wp-content\uploads\sites\38\2026\03"
dir /b "wp-content\uploads\sites\38\2026\04"
echo.
pause
