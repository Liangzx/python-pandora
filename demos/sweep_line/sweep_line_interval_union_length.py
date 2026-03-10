# 应用场景：区间覆盖总长度
# 问题描述：给定一组可能重叠的区间，例如 [[1,3], [2,6], [8,10], [15,18]]，计算这些区间在数轴上一共覆盖了多长。
# 期望输出
# 对于上述示例，合并后的区间为 [[1,6], [8,10], [15,18]]，总长度为 (6-1) + (10-8) + (18-15) = 10。
# 算法思路
# 核心是将“区间”转化为“事件点”，然后扫描这些点，动态维护当前被覆盖的区间总长度。
# 事件化：将每个区间 [l, r]拆分为两个事件 (l, +1)和 (r, -1)。
# 排序：将所有事件按坐标 x升序排列。若坐标相同，结束事件 (-1)优先于开始事件 (+1)，以避免重复计算边界。
# 扫描与计数：遍历排序后的事件，维护一个计数器 cnt表示当前被覆盖的区间层数，以及一个变量 length表示当前总覆盖长度。
#  遇到 +1事件：cnt加 1。若 cnt从 0 变为 1，说明开启了一段新的覆盖，length增加 x - last_x（last_x是上一个事件点）。
#  遇到 -1事件：cnt减 1。若 cnt从 1 变为 0，说明结束了一段覆盖，length增加 x - last_x。

from typing import List


def interval_union_length(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0

    # 1. 构建事件列表：(坐标, 变化量)
    events = []
    for left, r in intervals:
        events.append((left, 1))   # 区间开始
        events.append((r, -1))  # 区间结束

    # 2. 排序事件
    # 按坐标升序；坐标相同时，结束事件(-1)优先
    events.sort(key=lambda x: (x[0], x[1]))
    print(events)

    total_length = 0  # 总覆盖长度
    cnt = 0           # 当前被覆盖的区间层数
    last_x = events[0][0]  # 上一个事件点

    # 3. 扫描所有事件
    for x, delta in events:
        # 在 [last_x, x) 这段区间上，覆盖层数是 cnt
        if cnt > 0:
            total_length += x - last_x

        # 更新覆盖层数和上一个事件点
        cnt += delta
        last_x = x

    return total_length


if __name__ == "__main__":
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(interval_union_length(intervals))  # 输出: 10
