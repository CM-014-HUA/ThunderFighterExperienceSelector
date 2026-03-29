import json
import os
from config import PREDEFINED_EXP_BLOCKS, BACKPACK_FILE


def get_item_exp(item_name):
    """辅助函数：从配置中查找某个物品名称对应的经验值"""
    for category, items in PREDEFINED_EXP_BLOCKS.items():
        for exp, name in items:
            if name == item_name:
                return exp
    return None


def update_inventory():
    # 设置控制台编码，防止中文乱码
    if os.name == 'nt':
        os.system('chcp 65001 > nul')

    print("=" * 60)
    print("          雷霆战机背包材料快速录入 (按文件顺序)")
    print("=" * 60)
    print("说明：")
    print("1. 程序将按照 experience_backpack.json 中的顺序询问")
    print("2. 直接按 [回车] 保持当前数值")
    print("3. 输入 'q' 保存并退出")
    print("-" * 60)

    # 1. 加载现有数据
    if not os.path.exists(BACKPACK_FILE):
        print(f"错误：找不到文件 {BACKPACK_FILE}。请先运行一次 main.py 生成模板。")
        input("按回车退出...")
        return

    try:
        with open(BACKPACK_FILE, 'r', encoding='utf-8') as f:
            # Python 3.7+ 的 json.load 会保持文件中的键值顺序
            backpack_data = json.load(f)
    except Exception as e:
        print(f"加载文件失败: {e}")
        return

    # 2. 遍历 JSON 中的每一项
    for item_name, current_val in backpack_data.items():
        # 尝试获取该物品的经验值，用于辅助显示
        exp_val = get_item_exp(item_name)
        exp_str = f"({exp_val}xp)" if exp_val else ""

        prompt = f"  - {item_name} {exp_str}\n    当前数量: {current_val} -> 新数量: "

        user_input = input(prompt).strip().lower()

        if user_input == 'q':
            break

        if user_input == '':
            # 直接回车，不做修改
            continue

        try:
            count = int(user_input)
            if count < 0:
                print("    [!] 数量不能为负数，已重置为 0")
                count = 0
            backpack_data[item_name] = count
        except ValueError:
            print(f"    [!] 无效输入 '{user_input}'，跳过该项")

    # 3. 保存更新后的数据
    try:
        with open(BACKPACK_FILE, 'w', encoding='utf-8') as f:
            # indent=2 保证 JSON 文件依然易读且保持顺序
            json.dump(backpack_data, f, ensure_ascii=False, indent=2)
        print("\n" + "=" * 60)
        print("保存成功！数据已更新。")
    except Exception as e:
        print(f"\n保存失败: {e}")

    input("\n操作结束，按回车键返回...")


if __name__ == "__main__":
    try:
        update_inventory()
    except KeyboardInterrupt:
        print("\n\n操作被强制中断。")