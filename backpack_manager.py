import json
import os
from config import PREDEFINED_EXP_BLOCKS, BACKPACK_FILE


class BackpackManager:
    def __init__(self):
        self.backpack_data = None
        self.filename = BACKPACK_FILE

    def create_backpack_template(self):
        """创建背包数据模板文件"""
        template = {}
        for category, blocks in PREDEFINED_EXP_BLOCKS.items():
            for exp, description in blocks:
                template[description] = 0  # 默认数量为0

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(template, f, ensure_ascii=False, indent=2)

        print("已创建背包数据模板文件: experience_backpack.json")
        print("请在该文件中填写您的实际物品数量，然后重新运行程序。")
        input("按回车键退出程序...")
        exit()

    def load_backpack_data(self):
        """从文件导入背包数据"""
        if not os.path.exists(self.filename):
            print("首次使用系统，正在创建背包模板文件...")
            self.create_backpack_template()

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.backpack_data = json.load(f)
            print(f"成功加载背包数据: {self.filename}")
            return True
        except Exception as e:
            print(f"加载背包文件时出错: {e}")
            return False

    def get_available_blocks(self):
        """获取可用的经验块数据"""
        if not self.backpack_data:
            if not self.load_backpack_data():
                return None, None

        blocks = []
        descriptions = []

        total_items = 0
        for description, count in self.backpack_data.items():
            if count > 0:
                total_items += 1
                # 查找对应的经验值
                exp_value = self._find_exp_value(description)
                if exp_value:
                    blocks.append((exp_value, count))
                    descriptions.append(description)

        if not blocks:
            print("背包中没有有效的经验块!")
            return None, None

        # 按经验值从大到小排序
        combined = list(zip(blocks, descriptions))
        combined.sort(key=lambda x: x[0][0], reverse=True)
        blocks, descriptions = zip(*combined)
        blocks = list(blocks)
        descriptions = list(descriptions)

        # 显示背包总览
        total_exp = sum(exp * cnt for exp, cnt in blocks)
        print(f"背包总览: 共 {total_items} 种经验块，总经验值: {total_exp}")

        # 可选：显示背包中所有物品的详细信息（按经验值排序）
        print("背包中的经验块（按经验值从大到小）:\n")
        for (exp, count), desc in zip(blocks, descriptions):
            print(f"  {count} 个 {desc}(单个经验: {exp})")

        return blocks, descriptions

    def _find_exp_value(self, description):
        """根据描述查找对应的经验值"""
        for category, block_list in PREDEFINED_EXP_BLOCKS.items():
            for exp, desc in block_list:
                if desc == description:
                    return exp
        return None

    def update_backpack(self, used_items):
        """更新背包文件，扣除使用的物品"""
        if not self.backpack_data:
            return False

        for item_name, used_count in used_items.items():
            if item_name in self.backpack_data:
                self.backpack_data[item_name] -= used_count

        # 保存更新后的背包数据
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.backpack_data, f, ensure_ascii=False, indent=2)
            print(f"\n已更新背包文件 {self.filename}，扣除了使用的物品")
            return True
        except Exception as e:
            print(f"更新背包文件时出错: {e}")
            return False