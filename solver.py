class ExpSolver:
    def __init__(self):
        pass

    def solve_optimization(self, required_exp, blocks):
        """
        优化后的动态规划：
        1. 使用一维 DP 数组减少空间复杂度从 O(N*E) 到 O(E)
        2. 使用路径索引记录代替完整的列表复制，极大地提升运行速度
        """
        if not blocks:
            return None, None, None

        n = len(blocks)
        total_exp_available = sum(exp * cnt for exp, cnt in blocks)

        # 检查是否有足够的经验值
        if total_exp_available < required_exp:
            return "INSUFFICIENT", total_exp_available, None

        # 确定搜索上限：required_exp + 最大经验块的值
        # 因为如果超过这个上限，去掉一个最大块肯定能得到一个更接近目标且 >= 目标的值
        max_item_val = max(b[0] for b in blocks)
        upper_bound = min(required_exp + max_item_val, total_exp_available)

        # dp[j] 存储达到经验值 j 时，最后添加的物品在 blocks 中的索引
        # 初始化为 -1 表示该经验值目前不可达
        dp = [-1] * (upper_bound + 1)
        dp[0] = 0  # 初始状态：0经验是可达的

        # parent_count[j] 存储达到经验值 j 时，最后添加的那种物品使用了多少个
        parent_count = [0] * (upper_bound + 1)

        # 遍历每一种经验块
        for i in range(n):
            exp_val, max_cnt = blocks[i]
            # 为了使用一维数组优化空间，必须从高到低遍历经验值
            for j in range(upper_bound, -1, -1):
                if dp[j] != -1:  # 如果当前经验值 j 是可达的
                    # 尝试加入 k 个当前的经验块
                    for k in range(1, max_cnt + 1):
                        new_exp = j + (exp_val * k)
                        if new_exp <= upper_bound:
                            # 如果这个新经验值还没被达到过，记录来源
                            if dp[new_exp] == -1:
                                dp[new_exp] = i
                                parent_count[new_exp] = k
                        else:
                            # 超出上限，不再尝试增加 k
                            break

        # 寻找最优解：从 required_exp 开始向上找第一个可达的经验值
        best_exp = -1
        for e in range(required_exp, upper_bound + 1):
            if dp[e] != -1:
                best_exp = e
                break

        if best_exp == -1:
            return None, None, None

        # --- 回溯重建最优解的物品组合 ---
        best_usage = [0] * n
        temp_exp = best_exp

        # 只要还没回溯到0经验，就继续根据记录找上一个状态
        while temp_exp > 0:
            item_idx = dp[temp_exp]
            count_used = parent_count[temp_exp]
            best_usage[item_idx] = count_used
            # 减去当前物品消耗的经验，回到上一个状态
            temp_exp -= blocks[item_idx][0] * count_used

        min_waste = best_exp - required_exp
        return min_waste, best_exp, best_usage
