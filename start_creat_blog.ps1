# 设置环境变量
$env = "ueeshop"
# 读取.ps1 文件所在目录
$envPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
# 输出 $envPath
Write-Host "=== Setting up environment ==="
Write-Host "Environment path: $envPath"

Write-Host "=== Starting ollama and running Python scripts ==="

# 判断ollama 是否已安装
if (-not (Get-Command "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "ollama is not installed. "
}else {
    # 判断ollama 是否已经在运行
    $ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
    if (-not $ollamaProcess) {
        Write-Host "Starting ollama..."
        # 如果 ollama 没有运行，则后台启动它
        Start-Process -FilePath "C:\Users\Administrator\AppData\Local\Programs\Ollama\ollama app.exe" -NoNewWindow
        Write-Host "ollama started."
        # 等待一段时间确保 ollama 启动完成
        Start-Sleep -Seconds 5
    }
}

Write-Host "Activating conda environment: $env"
# 判断conda环境是否存在
if (-not (conda env list | Select-String -Pattern $env)) {
    Write-Host "Conda environment $env does not exist. Creating it..."
    # 创建conda环境
    conda create -n $env python=3.10.14 -y
    Write-Host "Conda environment $env created."
    # 安装依赖
    conda activate $env
    Write-Host "Activated conda environment: $env"
    pip install -r requirements.txt
    Write-Host "install requirements"
} else {
    Write-Host "Conda environment $env already exists."
    # 激活环境
    conda activate $env
}

Write-Host "Running Python script: blog.py"

# 运行 Python 脚本
python "$envPath\blog.py" 1

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
