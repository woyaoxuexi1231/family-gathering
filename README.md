# family-gathering

## 简介 / Introduction

**中文** — 家庭聚餐邀约 —— Python 学习项目。同时提供完整参考版后端与"空壳 + TODO"练习版后端，共享一份前端：对照参考版往练习版抄写实现，抄完切换启动命令，用同一套接口验收，为 Python 后端学习提供清晰的起手路径（详见 LEARNING.md）。

**English** — A family-dinner invitation app built as a hands-on Python tutorial. It ships a full reference backend plus a "shell + TODO" practice backend sharing one frontend — copy the implementation into the practice version, flip the start command, and validate against the same API for a clear on-ramp to Python backend development (see LEARNING.md).

## 结构

```text
backend/
  family_gathering/      # 参考版后端（完整）
  my_family_gathering/   # 练习版后端（空壳 + TODO）
frontend/                # 一份前端，共用
LEARNING.md
```

端口统一：后端 **8800**，前端 **5173**。一次只跑一个后端。

## 快速开始

**终端 1 — 后端（先跑参考版）**

```powershell
cd backend/family_gathering
uv sync --group dev
uv run uvicorn family_gathering.main:app --reload --port 8800
```

练习时改成：

```powershell
cd backend/my_family_gathering
uv sync --group dev
uv run uvicorn my_family_gathering.main:app --reload --port 8800
```

**终端 2 — 前端**

```powershell
cd frontend
npm install
npm run dev
```

打开 http://127.0.0.1:5173/

## 怎么学

见 [`LEARNING.md`](LEARNING.md)：对照 `backend/family_gathering` 往 `backend/my_family_gathering` 里抄，抄完切换启动命令，用同一份前端验收。
