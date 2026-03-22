@echo off
REM MOKSHA AI - Mock Test Pipeline (CPU Only, No GPU Required)
REM Tests all code flows WITHOUT requiring GPU hardware

echo ========================================================================
echo MOKSHA AI - MOCK TEST PIPELINE (CPU Mode)
echo ========================================================================
echo.
echo This will test all engines WITHOUT GPU:
echo   - Voice Engine (Mock Audio Generation)
echo   - Avatar Engine (Code Validation + FFmpeg Fallback)
echo   - Video Engine (Code Validation + FFmpeg Fallback)
echo   - Layer Engine (Video Concatenation)
echo   - Script Engine (API Call if key available)
echo   - Scene Planner (NLP Logic)
echo.
echo GPU-based inference will be tested during cloud deployment
echo.
echo Press any key to start...
pause >nul
echo.

REM Check Python installation
echo [Step 0/6] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Install Python 3.10+ first
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo SUCCESS: Python found
echo.

REM Check FFmpeg installation
echo [Pre-Check] Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg not found in PATH
    echo Some tests may be skipped
    echo Install from: https://ffmpeg.org/download.html
    echo.
) else (
    ffmpeg -version | findstr /C:"ffmpeg version"
    echo SUCCESS: FFmpeg found
    echo.
)

REM Run mock test pipeline
echo [Step 1/6] Running Mock Test Pipeline...
echo.
python test_mock_pipeline.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================================================
    echo ERROR: Mock tests failed!
    echo DO NOT deploy to GPU until these errors are fixed
    echo Check COMPLETE_SYSTEM_FLOW.md for troubleshooting
    echo ========================================================================
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo MOCK TESTS COMPLETE!
echo ========================================================================
echo.
echo Next Steps:
echo   1. Review test results above
echo   2. If ALL tests PASSED: Ready for GPU deployment
echo   3. Follow GPU_DEPLOYMENT_GUIDE.md for cloud deployment
echo.
echo Files Created:
echo   - outputs/mock_tests/test_voice.wav
echo   - outputs/mock_tests/test_avatar.mp4
echo   - outputs/mock_tests/test_video.mp4
echo   - outputs/mock_tests/test_final.mp4
echo   - outputs/mock_tests/test_results.json
echo.
echo ========================================================================
pause
