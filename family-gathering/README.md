# family-gathering

单次家庭聚餐邀约：参与人报名、认领菜品、总览统计。

## 技术栈

- FastAPI + Pydantic
- 数据：`data/gathering.json`（单文件，不进 Git）
- 包管理：[uv](UV.md)

## 快速开始

```powershell
cd family-gathering
uv sync --group dev
uv run uvicorn family_gathering.main:app --reload --port 8800
```

浏览器打开 **<http://127.0.0.1:8800/>** 即可使用页面（报名、加菜、认领）。

- API 文档：<http://127.0.0.1:8800/docs>
- JSON 总览：<http://127.0.0.1:8800/api/overview>

## 测试

```powershell
uv run pytest -v
```

## 目录

```text
src/family_gathering/
  main.py           # FastAPI 入口
  config.py         # 聚会固定信息、数据路径
  models/           # dataclass 领域模型
  schemas/          # API 入参/出参
  services/         # 业务规则（pytest 重点测这里）
  persistence/      # JSON 读写
  api/              # JSON 路由（薄层）
  web/              # Jinja2 页面 + static/
    templates/
    static/
    routes.py
data/gathering.json # 运行时生成
tests/
```

## API 一览

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/meta` | 聚会固定信息 |
| GET | `/api/overview` | 总览 |
| GET/POST | `/api/participants` | 参与人列表 / 报名 |
| PATCH/DELETE | `/api/participants/{id}` | 修改 / 删除 |
| GET/POST | `/api/dishes` | 菜品列表 / 新增 |
| POST | `/api/dishes/{id}/claim` | 认领 |
| POST | `/api/dishes/{id}/unclaim` | 取消认领 |

聚会时间地点可在 `.env` 或环境变量里改（见 `config.py`），不必写「创建聚会」接口。
