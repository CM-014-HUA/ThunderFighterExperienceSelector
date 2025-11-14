class UserInterface:
    def __init__(self, backpack_manager, solver):
        self.backpack_manager = backpack_manager
        self.solver = solver

    def display_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("          雷霆战机经验值优化系统")
        print("=" * 60)
        print("系统将自动加载经验背包数据 (experience_backpack.json)")
        print("并直接给出最优升级方案")

    def get_required_exp(self):
        """获取用户输入的所需经验值"""
        try:
            required_exp = int(input("\n请输入升级所需经验值: "))
            if required_exp <= 0:
                print("经验值必须是正整数!")
                return None
            return required_exp
        except ValueError:
            print("请输入有效的整数经验值!")
            return None

    def display_solution(self, required_exp, blocks, descriptions, solution_result):
        """显示解决方案"""
        min_waste, best_exp, best_usage = solution_result

        if min_waste == "INSUFFICIENT":
            print("\n警告: 所有可用经验值小于升级所需经验值，无法升级!")
            print(f"可用经验值: {best_exp}, 所需经验值: {required_exp}")
            return None

        if best_usage is None:
            print("\n无法找到合适的经验块组合来满足升级需求")
            return None

        print("\n经验块使用方案:")

        # 收集使用的物品信息并按经验值排序
        used_blocks_info = []
        for i in range(len(blocks)):
            exp_val, available_cnt = blocks[i]
            used_cnt = best_usage[i]
            desc = descriptions[i]
            if used_cnt > 0:
                used_blocks_info.append((exp_val, desc, used_cnt, available_cnt))

        # 按照单个经验块的经验值从大到小排序
        used_blocks_info.sort(key=lambda x: x[0], reverse=True)

        total_used = 0
        used_items = {}

        # 显示排序后的使用方案
        for exp_val, desc, used_cnt, available_cnt in used_blocks_info:
            if used_cnt <= available_cnt:
                print(f"  使用 {used_cnt} 个 {desc}(单个经验: {exp_val})")
                total_used += exp_val * used_cnt
                used_items[desc] = used_cnt
            else:
                print(f"  错误: {desc} 使用数量 {used_cnt} 超过背包数量 {available_cnt}!")
                return None

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

        return used_items

    def confirm_upgrade(self, used_items):
        """确认升级操作，支持直接回车默认确认"""
        if not used_items:
            return False

        upgrade_choice = input("\n是否按照此方案升级? (Y/n): ").strip().lower()
        # 直接回车、输入y、yes都视为确认升级
        return upgrade_choice in ['', 'y', 'yes']

    def ask_continue(self):
        """询问是否继续，支持直接回车默认继续"""
        continue_choice = input("\n是否继续计算? (Y/n): ").strip().lower()
        # 直接回车、输入y、yes都视为继续
        return continue_choice in ['', 'y', 'yes']
