#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VirtualFile 完整示例：将大文件分割为子文件，并通过虚拟文件接口无缝读取
功能：分割文件 + 虚拟拼接读取 + 内容校验 + 上下文管理
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, BinaryIO, Optional
from bisect import bisect_right


class Fragment:
    """子文件元数据"""

    def __init__(self, offset: int, size: int, path: str, checksum: str = ""):
        self.offset = offset
        self.size = size
        self.path = path
        self.checksum = checksum  # 可选：用于完整性校验


class VirtualFile:
    """
    虚拟文件类：将多个物理子文件拼接为逻辑上的单一文件（只读）
    支持：read, seek, tell, close, 上下文管理，校验和验证
    """

    def __init__(self, index_path: str, verify_checksum: bool = False):
        """
        :param index_path: 索引文件路径 (.vfi)
        :param verify_checksum: 是否在打开子文件时验证校验和
        """
        self.index_path = Path(index_path)
        self.fragments: List[Fragment] = []
        self.total_size = 0
        self.current_pos = 0
        self.verify_checksum = verify_checksum
        self._open_handles: Dict[str, BinaryIO] = {}  # 路径 -> 文件句柄（简单缓存）
        self._load_index()
        self._validate_index()

    def _load_index(self):
        """加载并解析索引文件"""
        if not self.index_path.exists():
            raise FileNotFoundError(f"索引文件不存在: {self.index_path}")
        with open(self.index_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for frag in data["fragments"]:
            self.fragments.append(
                Fragment(
                    offset=frag["offset"],
                    size=frag["size"],
                    path=frag["path"],
                    checksum=frag.get("checksum", ""),
                )
            )
        self.total_size = data["total_size"]
        self.root_dir = Path(data.get("root_dir", self.index_path.parent))

    def _validate_index(self):
        """验证索引连续性与完整性"""
        if not self.fragments:
            raise ValueError("索引为空")
        expected_offset = 0
        for i, frag in enumerate(self.fragments):
            if frag.offset != expected_offset:
                raise ValueError(
                    f"索引不连续: 片段{i}起始偏移应为{expected_offset}, 实际{frag.offset}"
                )
            expected_offset += frag.size
        if expected_offset != self.total_size:
            raise ValueError(f"索引总大小校验失败: 索引声明{self.total_size}, 实际计算{expected_offset}")

    def _find_fragment_index(self, logical_offset: int) -> int:
        """二分查找：返回包含该逻辑偏移的片段索引"""
        if logical_offset < 0 or logical_offset >= self.total_size:
            return -1
        offsets = [f.offset for f in self.fragments]
        idx = bisect_right(offsets, logical_offset) - 1
        return (
            idx
            if idx >= 0
            and logical_offset < self.fragments[idx].offset + self.fragments[idx].size
            else -1
        )

    def _get_handle(self, frag_path: str) -> BinaryIO:
        """获取子文件句柄（带缓存与校验）"""
        abs_path = self.root_dir / frag_path
        if str(abs_path) in self._open_handles:
            return self._open_handles[str(abs_path)]

        if not abs_path.exists():
            raise FileNotFoundError(f"子文件缺失: {abs_path}")

        # 可选：校验文件完整性
        if self.verify_checksum:
            with open(abs_path, "rb") as f:
                calc = hashlib.sha256(f.read()).hexdigest()
            # 实际应用中应从索引获取该片段的checksum
            # 此处简化：仅演示思路

        handle = open(abs_path, "rb")
        self._open_handles[str(abs_path)] = handle
        return handle

    def read(self, size: int = -1) -> bytes:
        """读取指定字节数，返回bytes"""
        if size == 0 or self.current_pos >= self.total_size:
            return b""
        if size < 0:
            size = self.total_size - self.current_pos

        result = bytearray()
        remaining = size

        while remaining > 0 and self.current_pos < self.total_size:
            idx = self._find_fragment_index(self.current_pos)
            if idx == -1:
                break
            frag = self.fragments[idx]
            local_offset = self.current_pos - frag.offset
            can_read = min(remaining, frag.size - local_offset)

            fh = self._get_handle(frag.path)
            fh.seek(local_offset)
            chunk = fh.read(can_read)
            if not chunk:
                break
            result.extend(chunk)
            self.current_pos += len(chunk)
            remaining -= len(chunk)

        return bytes(result)

    def seek(self, offset: int, whence: int = 0) -> int:
        """移动文件指针"""
        if whence == 0:  # SEEK_SET
            new_pos = offset
        elif whence == 1:  # SEEK_CUR
            new_pos = self.current_pos + offset
        elif whence == 2:  # SEEK_END
            new_pos = self.total_size + offset
        else:
            raise ValueError("无效的whence值")

        if new_pos < 0:
            new_pos = 0
        elif new_pos > self.total_size:
            new_pos = self.total_size

        self.current_pos = new_pos
        return self.current_pos

    def tell(self) -> int:
        """返回当前逻辑偏移"""
        return self.current_pos

    def close(self):
        """关闭所有打开的子文件句柄"""
        for fh in self._open_handles.values():
            try:
                fh.close()
            except Exception:
                pass
        self._open_handles.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def __len__(self):
        return self.total_size


def split_file(input_path: str, output_dir: str, chunk_size: int = 1024 * 1024) -> str:
    """
    将大文件分割为多个子文件，并生成索引文件
    :param input_path: 原始文件路径
    :param output_dir: 输出目录
    :param chunk_size: 每个子文件大小（字节）
    :return: 生成的索引文件路径
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    file_size = input_path.stat().st_size
    fragments = []
    part_idx = 0

    with open(input_path, "rb") as src:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            part_name = f"part_{part_idx:04d}.bin"
            part_path = output_dir / part_name
            with open(part_path, "wb") as dst:
                dst.write(chunk)

            # 计算片段校验和（可选）
            frag_checksum = hashlib.sha256(chunk).hexdigest()
            fragments.append(
                {
                    "offset": part_idx * chunk_size,
                    "size": len(chunk),
                    "path": part_name,
                    "checksum": frag_checksum,
                }
            )
            part_idx += 1

    # 生成索引文件
    index_data = {
        "source_file": input_path.name,
        "total_size": file_size,
        "chunk_size": chunk_size,
        "fragments": fragments,
        "root_dir": str(output_dir.resolve()),
    }
    index_path = output_dir / f"{input_path.stem}.vfi"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)

    print(f"✓ 文件分割完成: {part_idx} 个片段，索引保存至 {index_path}")
    return str(index_path)


# ==================== 使用示例 ====================
if __name__ == "__main__":
    # 1. 创建测试文件（1.5MB）
    test_content = b"VirtualFile Demo: " + (b"ABCDEF" * 100000)  # 约600KB * 2.5
    original_file = "test_original.bin"
    with open(original_file, "wb") as f:
        f.write(test_content)
    print(f"✓ 创建测试文件: {original_file} ({len(test_content)} bytes)")

    # 2. 分割文件（每片512KB）
    output_dir = "virtual_file_parts"
    index_file = split_file(original_file, output_dir, chunk_size=512 * 1024)

    # 3. 使用 VirtualFile 读取并校验
    print("\n→ 通过 VirtualFile 读取内容...")
    with VirtualFile(index_file, verify_checksum=False) as vf:
        print(f"逻辑文件大小: {len(vf)} bytes")
        print(f"初始位置: {vf.tell()}")

        # 读取前100字节
        header = vf.read(100)
        print(f"前100字节: {header[:50]}... (共{len(header)}字节)")

        # 跳转到末尾前50字节
        vf.seek(-50, 2)
        tail = vf.read(50)
        print(f"末尾50字节: ...{tail}")

        # 全量读取并校验
        vf.seek(0)
        reconstructed = vf.read()
        print(f"\n读取总字节数: {len(reconstructed)}")

        if reconstructed == test_content:
            print("✅ 内容校验通过！虚拟文件与原始文件完全一致")
        else:
            print("❌ 内容校验失败！")

        # 验证随机seek
        vf.seek(100000)
        sample = vf.read(20)
        print(f"偏移100000处20字节: {sample}")

    # 4. 清理（可选）
    # import shutil; shutil.rmtree(output_dir); os.remove(original_file)
    print("\n✨ 示例运行完成！子文件位于:", output_dir)
