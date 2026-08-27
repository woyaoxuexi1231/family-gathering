"""
聚会数据读写 — 单文件 JSON 存储。

负责"怎么从磁盘读/写 Gathering 对象"。
"""

import json          # Python 内置的 JSON 模块：dump/load
import logging       # Python 内置的日志模块：记录运行信息
from collections.abc import Callable  # 可调用类型（函数/method）
from pathlib import Path   # 操作路径的类，比字符串操作安全方便
from typing import TypeVar  # 泛型：让函数可以接受任意返回类型


# ── 导入本项目的模块 ──────────────────────────────────────────────

from my_family_gathering.config import Settings, get_settings    # 应用配置
from my_family_gathering.models import Gathering                 # 领域模型
from my_family_gathering.persistence.codec import (              # 编解码器：dataclass ↔ dict
    gathering_from_dict,
    gathering_to_dict,
)

# ── 日志 ───────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)  # __name__ = "my_family_gathering.persistence.store"

# ── 泛型变量 T ─────────────────────────────────────────────────────
# T 是一个"占位符类型"，代表"某种具体类型，但我们现在不知道也不关心是什么"。
# update() 方法的返回值可以是任何类型（str、int、bool），用 T 来告诉类型检查器："放心，有返回值的"。
T = TypeVar("T")


# ────────────────────────────────────────────────────────────────────
# GatheringStore — 聚会的持久化存储
#
# Q: 为什么需要这个类？直接写成方法不行吗？
# A: 因为这个类的实例持有"状态"——self._data_path 和 self._settings。
#    所有方法都需要用到同一个路径和配置，把它们包装在一个对象里，
#    就不需要每个方法都传一遍这些参数了。
#
# Q: 为什么不用 @dataclass，自己写 __init__？
# A: dataclass 是"数据的容器"（自动生成 __init__/__repr__/__eq__）。
#    GatheringStore 不是纯数据，它有行为（load/save/update），
#    而且有些字段不需要自动生成（比如 _settings 不需要出现在 __repr__ 里）。
#    手动写 __init__ 更灵活，也表达了"这是一个有行为的类，不是干数据"。
#
# Q: 这看起来像 Java 吗？
# A: 很像！但 Python 里其实不流行手动写 class —— 因为很多时候直接用函数+局部变量就够了。
#    这个项目之所以用类，是因为它确实需要存"状态"。如果只是无状态的工具函数，
#    也可以全部拆成独立的函数写。两种写法都可以，只是风格不同。
# ────────────────────────────────────────────────────────────────────

class GatheringStore:

    def __init__(self, data_path: Path, settings: Settings | None = None) -> None:
        """
        初始化时保存两个东西：
        - data_path: 数据文件的路径（哪里存）
        - settings: 应用配置（有哪些默认值可用）

        settings 为什么可以省略？因为如果没传就用全局配置 get_settings() 作为默认值，
        这样测试时可以传自定义配置，平时用全局配置就行。
        """
        self._data_path = data_path      # 前缀 _ 表示"内部使用，外部不应该直接访问"
        self._settings = settings or get_settings()

    @property
    def data_path(self) -> Path:
        """
        @property 装饰器：把方法当成属性来用。
        self.data_path → 不加括号就能访问，但内部是个 getter 方法。
        这里纯粹是为了封装，暴露只读路径，不让外部直接修改 self._data_path。
        """
        return self._data_path

    def load(self) -> Gathering:
        """从磁盘加载数据。"""

        # 情况1：文件不存在 —— 新建一个空的 Gathering 并保存
        if not self._data_path.exists():
            gathering = Gathering()        # 空列表
            self.save(gathering)           # 在磁盘上写入一个初始化的 JSON 文件
            logger.info("初始化数据文件: %s", self._data_path)  # 记日志：刚创建了文件
            return gathering

        # 文件存在，读取内容
        raw = self._data_path.read_text(encoding="utf-8")  # 读出文件的字符串内容

        # 情况2：文件存在但是空的（比如之前创建后还没写入内容）—— 同情况1，给个空列表
        if not raw.strip():         # .strip() 去掉首尾空白字符（换行、空格等）
            gathering = Gathering() # 创建一个空的 Gathering
            self.save(gathering)    # 写入一个格式正确的 JSON 文件
            return gathering

        # 情况3：正常情况 —— 文件里有数据
        # json.loads(raw): 把 JSON 字符串解析成 dict（{"entries": [...]}）
        # gathering_from_dict(...): 再把 dict 转成 Gathering dataclass 对象
        return gathering_from_dict(json.loads(raw))

    def save(self, gathering: Gathering) -> None:
        """把 Gathering 保存到磁盘。"""

        # mkdir: 确保父目录存在。比如 data 文件夹可能不存在，先创建它。
        # parents=True: 递归创建（即使上层目录也不存在就一层层建）
        # exist_ok=True: 已存在也不报错
        self._data_path.parent.mkdir(parents=True, exist_ok=True)

        # 先把 gathering 对象转换成 dict（codec 做的事），然后序列化为 JSON 字符串
        payload = json.dumps(
            gathering_to_dict(gathering),  # 把 dataclass 变成 {entries: [...]}
            ensure_ascii=False,             # 中文字符不要转成 \\uXXXX，保持可读性
            indent=2,                       # 缩进 2 空格，方便人看
        )

        # 原子写入：先写到临时文件 .json.tmp，再 replace 到正式文件名。
        # 为什么要多这一步？防止写入过程中程序崩溃，导致产生半截垃圾文件。
        # 比如写到一半断电，直接写的话文件就是损坏的；先写 tmp 再 rename 的话，
        # rename 要么是完整的，要么原文件完好无损（replace 是系统级原子操作）。
        tmp_path = self._data_path.with_suffix(".json.tmp")  # 把 .json 替换成 .json.tmp
        tmp_path.write_text(payload + "\n", encoding="utf-8")  # 写入末尾加换行
        tmp_path.replace(self._data_path)                       # 原子替换正式文件

        logger.debug("已写入 %s", self._data_path)  # debug 级别日志：只在调试时输出

    def update(self, mutator: Callable[[Gathering], T]) -> T:
        """
        原子更新：加载 → 执行修改 → 保存。一步完成三件事。

        mutator 参数是一个"回调函数"，由调用者传入，决定如何修改数据。
        Callable[[Gathering], T] 意思是：
          - 接收一个 Gathering 参数
          - 返回类型是 T（任意类型）

        用法举例：
            store.update(lambda g: g.entries.append(entry))  # 添加一条
            store.update(lambda g: g.entries.pop())           # 删除最后一条
            result = store.update(lambda g: len(g.entries))   # 返回条目数量
        """
        gathering = self.load()           # 第一步：从磁盘加载最新数据
        result = mutator(gathering)       # 第二步：按调用者的意图修改 gathering（原地 mutation）
        self.save(gathering)              # 第三步：把修改后的数据存回磁盘
        return result                     # 第四步：返回修改函数的结果值


def get_store() -> GatheringStore:
    """
    工厂函数：创建一个默认的 GatheringStore 实例。
    内部会从配置中自动读取 data_path 和 settings，不用每次都手动传参。
    这也对应 main.py 里的 FastAPI Depends(get_store) 注入。
    """
    settings = get_settings()                   # 获取全局配置
    return GatheringStore(settings.data_path, settings)  # 带着配置创建 Store 实例
