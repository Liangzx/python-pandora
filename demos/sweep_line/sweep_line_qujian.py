import heapq
from typing import List, Tuple


def build_recovery_mapping(
    intervals: List[Tuple[int, int, int]], total_size: int  # (start, end, backup_id)
) -> List[Tuple[int, int, str]]:
    """
    扫描线算法构建恢复映射（结束事件优先处理）
    :param intervals: 区间列表，backup_id=0 表示全量备份
    :param total_size: 文件总大小
    :return: [(start, end, source_file), ...] 按偏移升序排列
    """
    # === 1. 生成事件流（关键修改：结束事件标记为0=高优先级，开始事件标记为1=低优先级）===
    events = []
    for start, end, bid in intervals:
        events.append((start, 1, bid, end))  # 1 = start 事件（低优先级）
        events.append((end, 0, bid, end))  # 0 = end   事件（高优先级 - 优先处理）

    # 排序规则：位置升序 → 事件类型升序（0先于1，确保同位置先处理结束事件）
    events.sort(key=lambda x: (x[0], x[1]))
    print("	events (pos, type, bid, end):", events)  # 调试输出

    # === 2. 扫描构建映射 ===
    heap = []  # Min-heap 存 (-backup_id, end_pos) 模拟最大堆（backup_id越大优先级越高）
    last_pos = 0
    current_source = None
    segment_start = 0
    result = []

    for pos, etype, bid, end_val in events:
        # 【懒删除】清理所有在 last_pos 前已结束的区间（end_pos <= last_pos）
        while heap and heap[0][1] <= last_pos:
            heapq.heappop(heap)

        # 处理 [last_pos, pos) 有效区间（仅当有活跃区间且区间非空）
        if pos > last_pos and heap:
            top_bid = -heap[0][0]  # 获取最高优先级 backup_id
            source = f"{top_bid}.bin" if top_bid > 0 else "base.bin"

            # 同源区间自动合并：仅当来源变化时记录上一段
            if source != current_source:
                if current_source is not None:
                    result.append((segment_start, last_pos, current_source))
                segment_start, current_source = last_pos, source

        # 处理当前事件（关键修改：开始事件条件改为 etype == 1）
        if etype == 1:  # 新增区间：仅当是开始事件时加入堆
            heapq.heappush(heap, (-bid, end_val))
        # 结束事件（etype == 0）：无需显式操作（由后续懒删除清理）

        last_pos = pos  # 更新扫描位置

    # === 3. 补全最后一段 [last_pos, total_size) ===
    if current_source is not None and segment_start < total_size:
        # 最终清理：移除所有在 last_pos 前结束的区间
        while heap and heap[0][1] <= last_pos:
            heapq.heappop(heap)
        if heap:  # 确保存在有效区间
            final_bid = -heap[0][0]
            final_source = f"{final_bid}.bin" if final_bid > 0 else "base.bin"
            result.append((segment_start, total_size, final_source))
        elif segment_start < total_size:  # 安全兜底（理论上不应触发）
            result.append((segment_start, total_size, "base.bin"))

    return result


# === 示例调用与验证 ===
if __name__ == "__main__":
    TOTAL_SIZE = 5000
    intervals = [
        (0, 5000, 0),  # 全量备份 base.bin
        (1000, 2000, 1),  # 增量1
        (1500, 2500, 2),  # 增量2
        (500, 1000, 3),  # 增量3-1
        (3000, 4000, 3),  # 增量3-2
    ]

    mapping = build_recovery_mapping(intervals, TOTAL_SIZE)

    print("\n✅ 扫描线算法构建的恢复映射（结束事件优先）：")
    for start, end, source in mapping:
        print(f"[{start:4d}, {end:4d}) → {source}")

    # 预期结果（与理论完全一致）
    expected = [
        (0, 500, "base.bin"),
        (500, 1000, "3.bin"),
        (1000, 1500, "1.bin"),
        (1500, 2500, "2.bin"),
        (2500, 3000, "base.bin"),
        (3000, 4000, "3.bin"),
        (4000, 5000, "base.bin"),
    ]

    # 严格验证
    assert mapping == expected, f"❌ 验证失败！\n实际: {mapping}\n期望: {expected}"
    print("\n✅✅✅ 验证通过：与理论结果完全一致（结束事件优先逻辑正确）")
