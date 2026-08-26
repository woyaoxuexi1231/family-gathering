# my_family_gathering（练习版）

空壳 + TODO。对照 `../family_gathering/` 同名文件抄写。

```powershell
cd backend/my_family_gathering
uv sync --group dev
uv run uvicorn my_family_gathering.main:app --reload --port 8800
uv run pytest -v
```

端口与参考版相同（8800）。一次只跑一个后端，前端始终用 `frontend/`。
