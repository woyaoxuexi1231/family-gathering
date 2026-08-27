"""
JSON 与领域对象互转。

================================================================================
疑问解答（学习用，不影响运行）
================================================================================

Q1: typing.Any 是什么？为什么需要它？

   Any = "任意类型"。它告诉 Python 类型检查器："这个位置可以是任何类型"。
   例如 dict[str, Any] 表示"键是 str，值可以是 int / str / list / dict / ... 随便什么"。

   不加的话会怎样？
   - Python 运行时完全没问题 —— Python 本身不强制类型注解，不加也能跑
   - 但 IDE 的提示和 static type checker (mypy) 就会失去帮助：你不知道 values 列表里到底有什么
   - 加上 Any 就像给字典"留了口子"，既让类型系统开心，又不用为每种可能写一个 Union[int, str, list, dict]"

   更严谨的做法其实是不加（直接写 dict），因为加了 Any 等于放弃所有检查。
   这个项目用了 Any，属于务实折中。


Q2: 为什么需要 codec 层？json.dumps(gathering) 不就直接存了吗？

   关键原因：Python 对象不能直接变成 JSON。

   json.dumps() 只能处理这些"原生类型"：
       dict、list、str、int、float、bool、None

   但我们的 Entry、Gathering 是 dataclass 对象：
       >>> import json
       >>> json.dumps(Entry(id="abc", name="张三"))
       TypeError: Object of type Entry is not JSON serializable

   所以需要一个"翻译官"（codec = codecoding/decoding）：
       gathering_to_dict()  → 把 Gathering(dataclass) 转成 {entries: [...]}（纯 dict）
       gathering_from_dict() → 把 {entries: [...]}（纯 dict）转回 Gathering(dataclass)

   中间人就是 dict/list/str/int——这些 json.dumps() 认识的原生类型。

   整个数据流是这样的：

       [内存中的对象]                        [磁盘上的 JSON 文件]            [内存中的对象]
       ┌──────────────┐                    ┌───────────────────┐             ┌──────────────┐
       │ Gathering    │  gathering_to_dict│  {"entries":[      │ gathering_  │ Gathering    │
       │  (dataclass) │ ────────────────→  │   {"id":"a","name":│ from_dict → │  (dataclass) │
       │              │                    │    "张三",...}     │             │              │
       │              │                    │   ]}               │             │              │
       └──────────────┘                    └───────────────────┘             └──────────────┘
            ↓                                      ↑                            ↑
         写入时调用                          json.dump()                 读取后调用
                                       （只处理原生类型）                  读出的是 dict，需要转回对象

   总结：不是 JSON 不认识你的对象，而是 Python 的 json 模块设计上就不认识任何自定义类。
        codec 层就是桥梁，一边连着 dataclass，一边连着 JSON 格式。
================================================================================
"""

from typing import Any

from my_family_gathering.models import Entry, Gathering


def gathering_to_dict(gathering: Gathering) -> dict[str, Any]:
    """把 Gathering 对象转为 dict（json 能理解的格式）。"""
    return {
        "entries": [
            {
                "id": entry.id,
                "name": entry.name,
                "dish": entry.dish,
                "headcount": entry.headcount,
                "note": entry.note,
            }
            for entry in gathering.entries
        ],
    }


def gathering_from_dict(data: dict[str, Any]) -> Gathering:
    """把 dict 转回 Gathering 对象。"""
    return Gathering(
        entries=[
            Entry(
                id=str(item["id"]),
                name=str(item["name"]),
                dish=str(item["dish"]),
                headcount=int(item.get("headcount", 1)),
                note=str(item.get("note", "")),
            )
            for item in data.get("entries", [])
        ],
    )
