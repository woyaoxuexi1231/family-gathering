# models 包的「入口文件」
#
# 你已经知道：有 __init__.py，Python 才会把 models/ 当成一个「包（package）」，
# 别的 .py 文件才能写 import my_family_gathering.models ...
#
# 但这个文件里还可以做更多事——下面两行就是常见的两种写法。

# ── 1. 从子模块「转出口」名字，方便别人 import ──────────────────────────────
#
# Entry、Gathering、new_id 其实定义在 gathering.py 里。
# 这里把它们「再 import 一遍」，挂到 models 包这一层。
#
# 效果：别的文件可以写短路径：
#   from my_family_gathering.models import Entry, Gathering, new_id   ✅ 推荐
# 而不用写长路径：
#   from my_family_gathering.models.gathering import Entry           ❌ 也能用，但啰嗦
#
# 类比：gathering.py 是仓库里的货架；__init__.py 是柜台——
# 顾客（其他模块）在柜台直接拿 Entry，不用自己进仓库找。
from my_family_gathering.models.gathering import Entry, Gathering, new_id

# ── 2. __all__：声明「这个包对外公开哪些名字」────────────────────────────────
#
# __all__ 是一个列表，列出「从包级别 import 时，允许拿出去的名字」。
#
# 主要影响两种写法：
#   from my_family_gathering.models import *   → 只会 import __all__ 里的三项
#   from my_family_gathering.models import Entry  → 不受 __all__ 限制，照样能用
#
# 日常项目里更常见的是「显式 import 名字」（上面第一种），
# 很少用 import *；但写上 __all__ 可以：
#   - 文档化：一眼看出 models 包对外提供什么
#   - 工具/IDE 知道哪些是公开 API
__all__ = [
    "Entry",
    "Gathering",
    "new_id",
]
