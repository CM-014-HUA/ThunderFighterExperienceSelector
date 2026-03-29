import streamlit as st
import json
import os
from solver import ExpSolver
from config import PREDEFINED_EXP_BLOCKS, BACKPACK_FILE

# 页面配置：设置标题和图标
st.set_page_config(page_title="雷霆战机经验优化", page_icon="🚀", layout="wide")

# 自定义 CSS 让界面更紧凑（适合手机）
st.markdown("""
    <style>
    .stNumberInput { margin-bottom: -15px; }
    .stButton button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)


def load_data():
    """从本地读取 JSON，如果不存在则初始化"""
    if os.path.exists(BACKPACK_FILE):
        with open(BACKPACK_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # 初始化全为 0
    return {name: 0 for cat in PREDEFINED_EXP_BLOCKS.values() for _, name in cat}


def save_data(data):
    """保存数据到本地 JSON"""
    with open(BACKPACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    st.title("🚀 雷霆战机经验优化系统")

    # 初始化 Session State
    if 'inventory' not in st.session_state:
        st.session_state.inventory = load_data()

    solver = ExpSolver()

    # --- 侧边栏：库存录入 ---
    st.sidebar.header("📦 背包库存管理")

    # 侧边栏按钮：一键保存和重置
    col_s1, col_s2 = st.sidebar.columns(2)
    if col_s1.button("💾 保存库存"):
        save_data(st.session_state.inventory)
        st.sidebar.success("已同步到 JSON！")
    if col_s2.button("🧹 全部清零"):
        for k in st.session_state.inventory: st.session_state.inventory[k] = 0
        st.rerun()

    # 按配置文件顺序和分类显示录入框
    for category, items in PREDEFINED_EXP_BLOCKS.items():
        with st.sidebar.expander(f"📁 {category}", expanded=False):
            for exp, name in items:
                # 使用 number_input，实时同步到 session_state
                st.session_state.inventory[name] = st.number_input(
                    f"{name} ({exp}xp)",
                    min_value=0,
                    value=st.session_state.inventory.get(name, 0),
                    key=f"input_{name}"
                )

    # --- 主界面：计算与结果 ---
    st.subheader("🎯 优化计算")

    # 布局：左侧输入，右侧结果
    main_col1, main_col2 = st.columns([1, 1.5])

    with main_col1:
        req_exp = st.number_input("请输入目标升级经验值:", min_value=0, step=1000, value=10000)

        # 准备数据给 solver
        active_blocks = []
        descriptions = []
        for name, count in st.session_state.inventory.items():
            if count > 0:
                # 从配置找经验值
                exp_val = next(e for cat in PREDEFINED_EXP_BLOCKS.values() for e, n in cat if n == name)
                active_blocks.append((exp_val, count))
                descriptions.append(name)

        if st.button("✨ 开始计算方案", type="primary"):
            if not active_blocks:
                st.warning("背包是空的，请先在左侧输入库存数量。")
            else:
                with st.spinner('正在寻找最优解...'):
                    # 调用你优化过的 solver.py
                    min_waste, best_exp, best_usage = solver.solve_optimization(req_exp, active_blocks)

                if min_waste == "INSUFFICIENT":
                    st.error(f"库存不足！当前总计只有 {best_exp} 经验。")
                elif best_usage:
                    # 将结果存入 session 以便在右侧持久显示
                    st.session_state.last_result = {
                        "min_waste": min_waste,
                        "best_exp": best_exp,
                        "best_usage": best_usage,
                        "descriptions": descriptions,
                        "req_exp": req_exp
                    }
                else:
                    st.error("计算出错，未找到方案。")

    # 右侧结果展示区
    with main_col2:
        if 'last_result' in st.session_state:
            res = st.session_state.last_result
            st.info(f"✅ 最佳匹配经验：**{res['best_exp']}**")

            # 指标卡片
            m1, m2 = st.columns(2)
            m1.metric("目标经验", res['req_exp'])
            m2.metric("浪费经验", res['min_waste'], delta=f"-{res['min_waste']}", delta_color="inverse")

            # 表格展示
            solution_data = []
            final_used_dict = {}  # 用于扣减库存
            for i, count in enumerate(res['best_usage']):
                if count > 0:
                    name = res['descriptions'][i]
                    solution_data.append({"材料名称": name, "使用数量": f"x {count}"})
                    final_used_dict[name] = count

            st.table(solution_data)

            # 执行扣减操作
            if st.button("确认升级 (自动扣除库存)"):
                for name, used_count in final_used_dict.items():
                    st.session_state.inventory[name] -= used_count
                save_data(st.session_state.inventory)
                del st.session_state.last_result  # 清除结果
                st.balloons()
                st.success("库存已更新！")
                st.rerun()


if __name__ == "__main__":
    main()
