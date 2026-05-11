import os
import sys
import time
import threading
from config import BACKPACK_FILE
from backpack_manager import BackpackManager
from solver import ExpSolver
from ui import UserInterface


def loading_timer(stop_event):
    """后台计时器线程函数，用于实时刷新控制台"""
    start_time = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start_time
        elapsed_ms = int(elapsed * 1000)
        if elapsed >= 1.0:
            seconds = int(elapsed)
            ms = elapsed_ms % 1000
            time_str = f"{seconds} s {ms} ms"
        else:
            time_str = f"{elapsed_ms} ms"
        # 使用 \r (回车符) 让光标回到行首覆盖输出，实现同一行刷新
        # sys.stdout.write(f"\r正在优化解决方案... 已耗时: {elapsed:.1f} 秒")
        sys.stdout.write(f"\r正在思考... 已耗时: {time_str}")
        sys.stdout.flush()
        time.sleep(1)
    # 计算完成后，清除当前行，为 UI 类的输出腾出干净空间
    # sys.stdout.write("\r" + " " * 50 + "\r")
    # sys.stdout.flush()


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

        # --- 启动计时器线程 ---
        stop_event = threading.Event()
        timer_thread = threading.Thread(target=loading_timer, args=(stop_event,))
        timer_thread.start()

        # 计算最优解
        solution_result = solver.solve_optimization(required_exp, blocks)

        # --- 停止计时器线程 ---
        stop_event.set()
        timer_thread.join()

        # 显示解决方案
        used_items = ui.display_solution(required_exp, blocks, descriptions, solution_result)

        # 确认并执行升级
        if used_items and ui.confirm_upgrade(used_items):
            if backpack_manager.update_backpack(used_items):
                print("升级完成!\n")
            else:
                print("升级失败!\n")
        else:
            print("已取消升级，背包数据未更改。")
            # 询问是否继续
            if not ui.ask_continue():
                print("\n感谢使用雷霆战机经验值优化系统!")
                break


if __name__ == "__main__":
    main()