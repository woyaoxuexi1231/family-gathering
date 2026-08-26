# family-gathering

家庭聚餐邀约相关项目集合。

## 项目

| 目录 | 说明 |
|------|------|
| [`family-gathering/`](family-gathering/) | 完整版：参与人报名、认领菜品、Web 页面 + API |
| [`my-family-gathering/`](my-family-gathering/) | 个人练习版（FastAPI 脚手架） |

## 快速开始（完整版）

```powershell
cd family-gathering
uv sync --group dev
uv run uvicorn family_gathering.main:app --reload --port 8800
```

浏览器打开 <http://127.0.0.1:8800/> 即可使用。

详细说明见各子目录下的 `README.md`。
