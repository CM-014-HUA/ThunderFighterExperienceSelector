class ExpSolver:
    def __init__(self):
        pass

    def solve_optimization(self, required_exp, blocks):
        """动态规划求解最优经验块组合"""
        if not blocks:
            return None, None, None

        n = len(blocks)
        total_exp_available = sum(exp * cnt for exp, cnt in blocks)

        # 检查是否有足够的经验值
        if total_exp_available < required_exp:
            return "INSUFFICIENT", total_exp_available, None

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

        return min_waste, best_exp, best_usage