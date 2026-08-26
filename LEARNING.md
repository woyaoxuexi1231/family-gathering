# 抄写顺序

对照 `backend/family_gathering/` → 填到 `backend/my_family_gathering/`。  
前端只用一份 `frontend/`。

## 后端

路径相对于各自项目里的 `src/<包名>/`：

| 步骤 | 文件 | 验证 |
|------|------|------|
| 1 | `models/enums.py` | — |
| 2 | `models/gathering.py` | — |
| 3 | `models/__init__.py` | — |
| 4 | `errors.py` | — |
| 5 | `config.py` | 端口保持 8800 |
| 6 | `persistence/` | — |
| 7 | `services/participants.py` | — |
| 8 | `services/dishes.py` | — |
| 9 | `services/signup.py` | — |
| 10 | `services/overview.py` | — |
| 11 | `schemas/` | — |
| 12 | `api/` | — |
| 13 | `main.py` | `/docs` 能开 |

参考版完整路径示例：

`backend/family_gathering/src/family_gathering/services/signup.py`

练习版对应：

`backend/my_family_gathering/src/my_family_gathering/services/signup.py`

## 验收

```powershell
# 停掉参考版，启动练习版
cd backend/my_family_gathering
uv run uvicorn my_family_gathering.main:app --reload --port 8800
```

前端继续 http://127.0.0.1:5173/，能报名、取消就算过关。

## 提示

- import：`family_gathering` → `my_family_gathering`
- 数据文件分开：参考版 `data/gathering.json`，练习版 `data/my_gathering.json`
- 卡住就并排 diff 两个目录同名文件
