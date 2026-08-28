# TODO: 抄 ../family_gathering/src/family_gathering/services/entries.py
from my_family_gathering.errors import ValidationError, ConflictError
from my_family_gathering.models import Gathering, Entry, new_id


# 两个方法。新增 和 删除，目前没有涉及更新操作

def add_entry(
        # 这里为什么要靠传入进来呢，为什么这里不自己去拿？？
        gathering: Gathering,
        # 这个是个特殊的表示，在这里占个位置，表示这个符号左边的所有参数全部都是位置参数，不用写参数名的
        # 右边的必须写
        *,
        name: str,
        dish: str,
        headcount: int = 1,
        note: str = ""
) -> Entry:
    # 把名字和菜的名字都去掉一下空格
    cleaned_name = name.strip()
    cleaned_dish = dish.strip()

    # 校验参数是否满足要求
    # python 只要满足
    # False None 0 0.0 0j Decimal(0) Fraction(0) 空序列（容器）其他一般都是 True
    if not cleaned_name:
        raise ValidationError("名字不能为空！")
    if not cleaned_dish:
        raise ValidationError("菜名不能为空！")
    if headcount < 1:
        raise ValidationError("人数至少为1！")

    # 校验是否存在重名用户
    for entry in gathering.entries:
        if entry.name == cleaned_name:
            raise ConflictError(f"客人已存在了哦 {cleaned_name}")

    # 创建一个新的客人
    entry = Entry(
        id=new_id(),
        name=cleaned_name,
        dish=cleaned_dish,
        headcount=headcount,
        note=note.strip(),
    )

    gathering.entries.append(entry)
    return entry

    pass
