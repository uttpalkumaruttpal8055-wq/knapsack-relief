@echo off
setlocal
cd /d "%~dp0"
set "KNAPSACK_NODE=C:\Users\uttpa\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
echo Knapsack Disaster Intelligence
echo Open http://127.0.0.1:3000/auth in your browser.
echo Create your account, then sign in with your own email and password.
echo Keep this window open while presenting the website.
echo If the website is already running, use the browser link instead.
if exist "%KNAPSACK_NODE%" (
  "%KNAPSACK_NODE%" server.mjs
) else (
  node server.mjs
)
if errorlevel 1 pause
