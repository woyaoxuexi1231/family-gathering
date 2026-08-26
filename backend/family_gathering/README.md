# family_gathering（参考版）

完整可跑的后端。对照学习时抄这里。

```powershell
cd backend/family_gathering
uv sync --group dev
uv run uvicorn family_gathering.main:app --reload --port 8800
uv run pytest -v
```

前端用仓库根目录的 `frontend/`（端口 5173）。
