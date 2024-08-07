# 设置环境变量
$env = "fnm"
# 读取.ps1 文件所在目录
$envPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
# 输出 $envPath
Write-Host "=== Setting up environment ==="
Write-Host "Environment path: $envPath"

Write-Host "=== Starting ollama and running Python scripts ==="

# 判断 ollama 是否已经在运行
$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaProcess) {
    Write-Host "Starting ollama..."
    # 如果 ollama 没有运行，则后台启动它
    Start-Process -FilePath "C:\Users\Administrator\AppData\Local\Programs\Ollama\ollama app.exe" -NoNewWindow
    Write-Host "ollama started."
}

# 等待一段时间确保 ollama 启动完成
Start-Sleep -Seconds 5

Write-Host "Activating conda environment: $env"

# 激活环境
conda activate $env

Write-Host "Running Python script: blog.py"

# 运行 Python 脚本
python "$envPath\blog.py" 10

Write-Host "Running Python script: blog_uploads.py"

# 执行 blog_uploads.py
python "$envPath\blog_uploads.py"

Write-Host "Deactivating conda environment: $env"

# 关闭环境
conda deactivate

Write-Host "Script execution completed."

# 暂停脚本执行
pause
# 等待用户按下任意键后退出
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
