### 创建虚拟环境，3.12版本
py -3.12 -m venv .venv

### 激活这个虚拟环境
.\.venv\Scripts\Activate.ps1

### 升级pip
python.exe -m pip install --upgrade pip

### 安装虚拟环境依赖
python -m pip install -e ".[dev]"

### 安装fastapi
python -m pip install "fastapi[standard]"

### 运行api
fastapi dev app/api.py --port 8001

### 运行api
uvicorn app.api:app --reload --port 8001