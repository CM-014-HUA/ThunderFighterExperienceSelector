# 预定义的经验块规格库
PREDEFINED_EXP_BLOCKS = {
    "小敌机残骸": [
        (1216, "小敌机残骸lv1"),
        (1524, "小敌机残骸lv2"),
        (1832, "小敌机残骸lv3"),
        (2140, "小敌机残骸lv4"),
        (2448, "小敌机残骸lv5"),
        (2756, "小敌机残骸lv6"),
        (3064, "小敌机残骸lv7"),
        (3372, "小敌机残骸lv8"),
        (3680, "小敌机残骸lv9")
    ],
    "大敌机残骸": [
        (2656, "大敌机残骸lv1"),
        (3324, "大敌机残骸lv2"),
        (3992, "大敌机残骸lv3"),
        (4660, "大敌机残骸lv4"),
        (5328, "大敌机残骸lv5"),
        (5996, "大敌机残骸lv6"),
        (6664, "大敌机残骸lv7"),
        (7332, "大敌机残骸lv8"),
        (8000, "大敌机残骸lv9")
    ],
    "BOSS的残骸": [
        (4816, "BOSS的残骸lv1"),
        (6024, "BOSS的残骸lv2"),
        (7232, "BOSS的残骸lv3"),
        (8440, "BOSS的残骸lv4"),
        (9648, "BOSS的残骸lv5"),
        (11936, "BOSS的残骸lv6"),
        (13264, "BOSS的残骸lv7"),
        (14592, "BOSS的残骸lv8"),
        (15920, "BOSS的残骸lv9")
    ],
    "强化魔方": [
        (1200, "初级强化魔方"),
        (4800, "次级强化魔方"),
        (9600, "强化魔方"),
        (28800, "高级强化魔方"),
        (115200, "超级强化魔方")
    ],
    "经验核心": [
        (2880, "次级经验核心"),
        (9600, "经验核心")
    ]
}


def create_backpack_template():
    """创建背包数据模板文件"""
    template = {}
    for category, blocks in PREDEFINED_EXP_BLOCKS.items():
        for exp, description in blocks:
            template[description] = 0  # 默认数量为0

    import json
    with open("experience_backpack.json", "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print("已创建背包数据模板文件: experience_backpack.json")
    print("请在该文件中填写您的实际物品数量，然后重新运行程序。")
    input("按回车键退出程序...")
    exit()


def import_backpack_from_file():
    """从文件导入背包数据"""
    import os
    import json

    # 检查默认背包文件是否存在
    default_filename = "experience_backpack.json"
    if not os.path.exists(default_filename):
        print("首次使用系统，正在创建背包模板文件...")
        create_backpack_template()

    try:
        # 直接使用默认文件
        with open(default_filename, "r", encoding="utf-8") as f:
            backpack_data = json.load(f)

        print(f"成功加载背包数据: {default_filename}")
        return backpack_data, default_filename
    except Exception as e:
        print(f"加载背包文件时出错: {e}")
        return None, None


def update_backpack_file(backpack_data, filename, used_items):
    """更新背包文件，扣除使用的物品"""
    for item_name, used_count in used_items.items():
        if item_name in backpack_data:
            backpack_data[item_name] -= used_count
            if backpack_data[item_name] <= 0:
                del backpack_data[item_name]  # 如果数量为0或负数，删除该物品

    # 保存更新后的背包数据
    import json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(backpack_data, f, ensure_ascii=False, indent=2)

    print(f"\n已更新背包文件 {filename}，扣除了使用的物品")


def get_exp_blocks_from_backpack():
    """从背包文件获取经验块数据"""
    print("\n正在加载背包数据...")

    backpack_data, filename = import_backpack_from_file()
    if not backpack_data:
        return None, None, None, None

    blocks = []
    descriptions = []

    # 从背包数据创建经验块列表
    total_items = 0
    for description, count in backpack_data.items():
        if count > 0:
            total_items += 1
            # 查找对应的经验值
            exp_value = None
            category_name = "未知"
            for category, block_list in PREDEFINED_EXP_BLOCKS.items():
                for exp, desc in block_list:
                    if desc == description:
                        exp_value = exp
                        category_name = category
                        break
                if exp_value:
                    break

            if exp_value:
                blocks.append((exp_value, count))
                descriptions.append(description)

    if not blocks:
        print("背包中没有有效的经验块!")
        return None, None, None, None

    # 显示背包总览
    total_exp = sum(exp * cnt for exp, cnt in blocks)
    print(f"背包总览: 共 {total_items} 种经验块，总经验值: {total_exp}")

    return blocks, descriptions, backpack_data, filename


def exp_optimization_solution():
    # 输入升级所需经验值
    try:
        required_exp = int(input("\n请输入升级所需经验值: "))
        if required_exp <= 0:
            print("经验值必须是正整数!")
            return
    except ValueError:
        print("请输入有效的整数经验值!")
        return

    # 从背包获取经验块数据
    result = get_exp_blocks_from_backpack()
    if not result:
        print("无法获取背包数据，程序结束。")
        return

    blocks, descriptions, backpack_data, filename = result
    total_exp_available = sum(exp * cnt for exp, cnt in blocks)

    # 检查是否有足够的经验值
    if total_exp_available < required_exp:
        print("\n警告: 所有可用经验值小于升级所需经验值，无法升级!")
        print(f"可用经验值: {total_exp_available}, 所需经验值: {required_exp}")
        return

    # 动态规划求解
    # 使用二维DP数组，dp[i][j]表示使用前i种物品达到经验值j的最小浪费
    n = len(blocks)
    max_exp_needed = min(required_exp + max(exp for exp, cnt in blocks), total_exp_available)

    # 初始化DP表
    dp = [[float('inf')] * (max_exp_needed + 1) for _ in range(n + 1)]
    usage = [[None] * (max_exp_needed + 1) for _ in range(n + 1)]

    # 初始化第一行
    dp[0][0] = 0
    usage[0][0] = [0] * n

    # 填充DP表
    for i in range(1, n + 1):
        exp_val, max_cnt = blocks[i - 1]
        for j in range(max_exp_needed + 1):
            # 不选当前物品
            if dp[i - 1][j] < dp[i][j]:
                dp[i][j] = dp[i - 1][j]
                if usage[i - 1][j]:
                    usage[i][j] = usage[i - 1][j][:]

            # 选k个当前物品
            for k in range(1, max_cnt + 1):
                exp_added = exp_val * k
                if j >= exp_added:
                    prev_exp = j - exp_added
                    if dp[i - 1][prev_exp] != float('inf'):
                        waste = max(0, j - required_exp)
                        if waste < dp[i][j]:
                            dp[i][j] = waste
                            if usage[i - 1][prev_exp]:
                                new_usage = usage[i - 1][prev_exp][:]
                                new_usage[i - 1] = k
                                usage[i][j] = new_usage

    # 寻找最优解
    min_waste = float('inf')
    best_exp = -1
    best_usage = None

    for exp in range(required_exp, max_exp_needed + 1):
        if dp[n][exp] < min_waste:
            min_waste = dp[n][exp]
            best_exp = exp
            best_usage = usage[n][exp]

    # 输出结果
    if best_usage is None:
        print("\n无法找到合适的经验块组合来满足升级需求")
    else:
        print("\n" + "=" * 50)
        print("最优升级方案")
        print("=" * 50)
        print(f"升级所需经验值: {required_exp}")
        print(f"使用经验块总经验值: {best_exp}")
        print(f"经验浪费: {min_waste}")
        print("\n经验块使用方案:")

        total_used = 0
        used_items = {}  # 记录使用的物品和数量

        for i in range(n):
            exp_val, available_cnt = blocks[i]
            used_cnt = best_usage[i] if best_usage else 0
            desc = descriptions[i]
            if used_cnt > 0:
                # 验证使用数量不超过背包数量
                if used_cnt <= available_cnt:
                    # print(f"  {desc}: 使用 {used_cnt}/{available_cnt} 个")
                    print(f"  {desc}: 使用 {used_cnt}个")
                    total_used += exp_val * used_cnt
                    used_items[desc] = used_cnt
                else:
                    print(f"  错误: {desc} 使用数量 {used_cnt} 超过背包数量 {available_cnt}!")
                    return

        print(f"\n验证: 使用经验块总经验值 = {total_used}")

        # 显示效率
        efficiency = (required_exp / total_used) * 100 if total_used > 0 else 0
        print(f"经验利用效率: {efficiency:.2f}%")

        # 提供建议
        if min_waste == 0:
            print("\n完美! 没有经验浪费!")
        elif min_waste < 100:
            print(f"\n建议: 浪费的经验很少，只有 {min_waste}，可以直接升级")
        else:
            print(f"\n注意: 有 {min_waste} 经验被浪费，考虑寻找更合适的经验块组合")

        # 询问用户是否按照此方案升级
        upgrade_choice = input("\n是否按照此方案升级? (y/n): ").lower()
        if upgrade_choice == 'y':
            # 更新背包文件，扣除使用的物品
            update_backpack_file(backpack_data, filename, used_items)
            print("升级完成!")
        else:
            print("已取消升级，背包数据未更改。")


def main():
    print("=" * 60)
    print("          雷霆战机经验值优化系统")
    print("=" * 60)
    print("系统将自动加载经验背包数据 (experience_backpack.json)")
    print("并直接给出最优升级方案")

    # 检查是否是首次运行
    import os
    if not os.path.exists("experience_backpack.json"):
        print("\n首次使用系统，正在创建背包模板文件...")
        create_backpack_template()

    while True:
        exp_optimization_solution()

        continue_choice = input("\n是否继续计算? (y/n): ").lower()
        if continue_choice != 'y':
            print("\n感谢使用雷霆战机经验值优化系统!")
            break


if __name__ == "__main__":
    main()