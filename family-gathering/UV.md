# family-gathering — 用 uv 搭项目

本文只讲 **uv 怎么把 Python 环境弄好**，让你专心写 `app/` 里的代码。  
不展开 `.env`、业务配置——那些等你写 `config.py` 时再管。

---

## uv 是什么

[uv](https://docs.astral.sh/uv/) 管三件事：

1. **Python 版本**（需要时自动下载）
2. **虚拟环境**（项目下的 `.venv/`，别用系统全局 Python）
3. **依赖**（写在 `pyproject.toml`，锁在 `uv.lock`）

日常记住两条：

- `uv sync` — 按锁文件装好环境  
- `uv run …` — 在项目环境里跑命令（一般不用手动 `activate`）

---

## 1. 安装 uv（Windows PowerShell，只需一次）

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

装完新开一个终端，确认：

```powershell
uv --version
```

---

## 2. 进入本目录

```powershell
cd backend/python/family-gathering
```

后面所有命令都在这个目录里执行。

---

## 3. 创建项目（两种情形）

### 情形 A：空文件夹，从零开始

```powershell
# 生成 pyproject.toml（选 app 布局、Python 3.11+）
uv init --app --python 3.11

# 加运行时依赖
uv add fastapi "uvicorn[standard]" pydantic pydantic-settings

# 加开发依赖（测试、调 API）
uv add --dev pytest httpx
```

`uv add` 会同时：改 `pyproject.toml`、更新 `uv.lock`、装进 `.venv`。

### 情形 B：已有 pyproject.toml（本仓库当前就是这样）

不用 `uv init`，直接同步：

```powershell
uv sync
```

开发依赖一起装：

```powershell
uv sync --extra dev
```

---

## 4. 同步环境（clone 仓库或别人改了依赖之后）

```powershell
cd backend/python/family-gathering
uv sync --extra dev
```

- 没有 `.venv` → 自动创建  
- 没有合适 Python → uv 会按 `requires-python` 拉取  
- `uv.lock` 存在 → 装**锁定的版本**，团队一致  

**`uv.lock` 要提交 Git**（和 `package-mgmt-lab/uv-demo` 一样）。

---

## 5. 写代码时你怎么跑

### 启动 FastAPI（等你写好 `app/main.py` 之后）

```powershell
uv run uvicorn family_gathering.main:app --reload --host 127.0.0.1 --port 8800
```

浏览器：

- 接口文档：<http://127.0.0.1:8800/docs>  
- 健康检查：看你 `main.py` 里有没有根路径  

`--reload`：改 `.py` 自动重启，开发期开着即可。

### 跑测试（等你写好 `tests/` 之后）

```powershell
uv run pytest
uv run pytest -v
uv run pytest tests/test_participants.py -v
```

### 临时执行一行 Python

```powershell
uv run python -c "import fastapi; print(fastapi.__version__)"
```

---

## 6. 以后加 / 删依赖

```powershell
# 加库
uv add httpx

# 加仅开发用的库
uv add --dev ruff

# 删库
uv remove python-dotenv

# 只刷新锁文件（不常用手动跑）
uv lock
```

改完依赖记得再 `uv sync`（有时 `uv add` 已经帮你装好了）。

---

## 7. 常用命令速查

| 你想干什么 | 命令 |
|------------|------|
| 装好环境 | `uv sync --extra dev` |
| 启动服务 | `uv run uvicorn app.main:app --reload --port 8800` |
| 跑测试 | `uv run pytest -v` |
| 加依赖 | `uv add 包名` |
| 看已装包 | `uv pip list` |
| 用项目 Python | `uv run python` |

---

## 8. 本目录里 uv 相关文件分工

| 文件 | 谁维护 | 作用 |
|------|--------|------|
| `pyproject.toml` | 你 + `uv add` | 项目名、Python 版本、依赖声明 |
| `uv.lock` | `uv` 自动生成 | 精确版本，提交 Git |
| `.venv/` | `uv sync` 生成 | 本地虚拟环境，**不提交** Git |
| `UV.md` | 文档 | 就是本文件 |

业务代码全在 `app/`、`tests/`；**别往 `.venv` 里手改东西**。

---

## 9. 推荐工作流（写代码阶段）

```text
1. uv sync --extra dev          # 开工前 / pull 之后
2. 写 app/、tests/
3. uv run pytest -v             # 规则测绿
4. uv run uvicorn app.main:app --reload --port 8800
5. 浏览器打开 /docs 点接口
6. 要新库 → uv add xxx → 继续写
```

---

## 10. 踩坑

**`ModuleNotFoundError: fastapi`**  
没在项目目录跑，或没 `uv sync`。用 `uv run`，不要裸 `python`。

**端口被占用**  
换 `--port 8801`，或关掉占 8800 的进程。

**改 pyproject 忘了 sync**  
执行 `uv sync --extra dev`。

**和 from-zero 课的区别**  
from-zero 很多课是 `pip install` + 系统/课内目录；**本项目统一用 uv + 本目录 `.venv`**，和 `rag-cs-lab`、`package-mgmt-lab/uv-demo` 同一套习惯。

---

## 11. 下一步（才是写代码）

环境 OK 之后，按你自己的架构写：

- `app/models/` → `services/` → `persistence/` → `schemas/` → `api/` → `main.py`  
- 测试先写 `services`，再挂路由  

uv 部分到此为止；后面不用再管包管理，专心填业务即可。
