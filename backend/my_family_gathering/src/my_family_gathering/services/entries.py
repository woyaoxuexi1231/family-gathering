# TODO: 抄 ../family_gathering/src/family_gathering/services/entries.py
from my_family_gathering.models import Gathering, Entry


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

    # python 只要满足
    # False None 0 0.0 0j Decimal(0) Fraction(0) 空序列（容器）其他一般都是 True
    if not cleaned_name:

    pass
