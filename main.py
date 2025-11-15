import os
from config import BACKPACK_FILE
from backpack_manager import BackpackManager
from solver import ExpSolver
from ui import UserInterface


def main():
    # 初始化组件
    backpack_manager = BackpackManager()
    solver = ExpSolver()
    ui = UserInterface(backpack_manager, solver)

    # 检查是否是首次运行
    if not os.path.exists(BACKPACK_FILE):
        print("\n首次使用系统，正在创建背包模板文件...")
        backpack_manager.create_backpack_template()

    # 显示欢迎信息
    ui.display_welcome()

    # 主循环
    while True:
        # 获取背包数据
        blocks, descriptions = backpack_manager.get_available_blocks()
        if blocks is None:
            print("无法获取背包数据，程序结束。")
            break

        # 获取所需经验值
        required_exp = ui.get_required_exp()
        if required_exp is None:
            continue

        print("正在优化解决方案...")

        # 计算最优解
        solution_result = solver.solve_optimization(required_exp, blocks)

        # 显示解决方案
        used_items = ui.display_solution(required_exp, blocks, descriptions, solution_result)

        # 确认并执行升级
        if used_items and ui.confirm_upgrade(used_items):
            if backpack_manager.update_backpack(used_items):
                print("升级完成!")
            else:
                print("升级失败!")
        else:
            print("已取消升级，背包数据未更改。")
            # 询问是否继续
            if not ui.ask_continue():
                print("\n感谢使用雷霆战机经验值优化系统!")
                break


if __name__ == "__main__":
    main()