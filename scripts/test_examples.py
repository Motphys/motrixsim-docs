# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""测试脚本：验证 examples 目录中的所有示例能正常运行"""

import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# 配置
EXAMPLES_DIR = Path("examples")
EXCLUDE_PATTERNS = ["assets", "mujoco", "randomize", "render", "sensors", "utils", "parallel_bench.py"]
TIMEOUT_SECONDS = 10  # 每个示例运行10秒后自动终止
MAX_RETRIES = 1


def should_test_file(filepath: Path) -> bool:
    """判断文件是否需要测试"""
    # 排除目录
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(filepath):
            return False

    # 只测试 .py 文件
    if not filepath.suffix == ".py":
        return False

    # 排除测试脚本本身
    if filepath.name.startswith("test_"):
        return False

    return True


def get_test_files() -> List[Path]:
    """获取所有需要测试的示例文件"""
    test_files = []

    # 测试根目录下的 .py 文件
    for py_file in EXAMPLES_DIR.glob("*.py"):
        if should_test_file(py_file):
            test_files.append(py_file)

    # 测试子目录中的 .py 文件
    for subdir in EXAMPLES_DIR.iterdir():
        if subdir.is_dir() and subdir.name not in EXCLUDE_PATTERNS:
            for py_file in subdir.glob("*.py"):
                if should_test_file(py_file):
                    test_files.append(py_file)

    return sorted(test_files)


def run_example_with_timeout(filepath: Path, timeout: int) -> Tuple[bool, str, str]:
    """运行示例文件，在指定时间后终止"""
    cmd = [sys.executable, str(filepath)]

    try:
        # 使用 subprocess.Popen 启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid if hasattr(os, "setsid") else None,
        )

        # 等待指定时间
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode

            # 如果进程在超时前正常退出
            if return_code == 0:
                return True, stdout, stderr
            else:
                return False, stdout, f"退出码: {return_code}\n{stderr}"

        except subprocess.TimeoutExpired:
            # 超时后终止进程
            try:
                if hasattr(os, "killpg"):
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                else:
                    process.terminate()

                # 等待进程结束
                process.wait(timeout=2)
            except OSError:
                try:
                    if hasattr(os, "killpg"):
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    else:
                        process.kill()
                except OSError:
                    pass

            # 超时视为成功（因为示例程序会持续运行直到手动关闭）
            return True, "程序正常运行（超时自动终止）", ""

    except Exception as e:
        return False, "", f"启动失败: {str(e)}"


def test_single_example(filepath: Path) -> bool:
    """测试单个示例文件"""
    print(f"测试: {filepath.relative_to(EXAMPLES_DIR)}", end=" ... ")

    success, stdout, stderr = run_example_with_timeout(filepath, TIMEOUT_SECONDS)

    if success:
        print("\033[32m✓ 通过\033[0m")
        if stdout and "超时自动终止" not in stdout:
            print(f"\033[32m  输出: {stdout[:100]}\033[0m")
        return True
    else:
        print("\033[31m✗ 失败\033[0m")
        print(f"\033[31m  错误: {stderr[:1000]}\033[0m")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("开始测试 examples 目录中的示例")
    print(f"超时设置: {TIMEOUT_SECONDS}秒/示例")
    print("=" * 60)

    # 获取所有测试文件
    test_files = get_test_files()

    if not test_files:
        print("错误: 没有找到需要测试的示例文件")
        return 1

    print(f"找到 {len(test_files)} 个示例文件需要测试\n")

    # 运行测试
    results = {"passed": [], "failed": [], "total": len(test_files)}

    for i, filepath in enumerate(test_files, 1):
        print(f"[{i}/{len(test_files)}] ", end="")

        if test_single_example(filepath):
            results["passed"].append(filepath)
        else:
            results["failed"].append(filepath)

        print()  # 空行分隔

    # 打印测试结果摘要
    print("=" * 60)
    print("测试结果摘要")
    print("=" * 60)
    print(f"总计: {results['total']} 个示例")
    print(f"通过: {len(results['passed'])} 个 ✓")
    print(f"失败: {len(results['failed'])} 个 ✗")

    if results["failed"]:
        print("\n失败的示例:")
        for filepath in results["failed"]:
            print(f"  - {filepath.relative_to(EXAMPLES_DIR)}")

    # 返回退出码
    return 0 if not results["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
