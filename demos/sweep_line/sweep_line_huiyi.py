# 问题描述
# 给定若干会议的开始和结束时间，计算同一时刻最多有多少场会议在同时进行。
# 示例输入：
# intervals = [[0, 30], [5, 10], [15, 20]]
# 期望输出：2
# 解释：在 [5, 10]和 [15, 20]这两个时间段，最多有 2 场会议重叠。

#  解题思路
# 1. 事件化 (Event Creation)
#  将每个会议的开始和结束时间抽象为事件。
#  开始事件：(时间, +1)，表示会议开始，需要增加一个“正在进行的会议”计数。
#  结束事件：(时间, -1)，表示会议结束，需要减少一个计数。
# 2. 排序 (Sorting)
#  将所有事件按时间排序。如果时间相同，结束事件 (-1) 优先于开始事件 (+1)。这可以避免在会议结束的同一时刻错误地增加计数。
# 3. 扫描与计数 (Sweeping & Counting)
#  从左到右扫描排序后的事件，维护一个计数器 cnt来记录当前正在进行的会议数量，并同步更新最大并发数 max_cnt。


from typing import List


def minMeetingRooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0
    # 1. 构建事件列表：(时间, 变化量)
    events = []
    for start, end in intervals:
        events.append((start, 1))   # 会议开始，+1
        events.append((end, -1))    # 会议结束，-1

    # 2. 排序事件
    # 时间不同时，按时间升序
    # 时间相同时，结束事件(-1)排在开始事件(+1)前面
    events.sort(key=lambda x: (x[0], x[1]))
    print(events)

    cnt = 0          # 当前同时进行的会议数
    max_cnt = 0      # 最大同时进行的会议数

    # 3. 扫描所有事件
    for time, delta in events:
        cnt += delta
        max_cnt = max(max_cnt, cnt)

    return max_cnt


if __name__ == "__main__":
    intervals = [[0, 9], [9, 10], [15, 20]]
    print(minMeetingRooms(intervals))  # 输出: 2
