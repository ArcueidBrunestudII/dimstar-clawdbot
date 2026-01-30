#!/usr/bin/env python3
"""
圆周率计算器 - 包含多种经典算法
"""

import math
import random
from decimal import Decimal, getcontext


def monte_carlo(n=1000000):
    """
    蒙特卡洛方法 - 随机投点法
    通过在单位正方形内随机投点，计算落在单位圆内的比例
    π ≈ 4 * (圆内点数 / 总点数)
    """
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            inside += 1
    return 4 * inside / n


def leibniz(n=1000000):
    """
    莱布尼茨级数
    π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
    收敛较慢，但原理简单
    """
    pi = 0
    sign = 1
    for i in range(n):
        term = 1 / (2 * i + 1)
        pi += sign * term
        sign *= -1
    return 4 * pi


def ramanujan(n=10):
    """
    拉马努金公式 - 极快收敛
    1/π = (√8 / 9801) * Σ(4n)! * (1103 + 26390n) / ((n!)^4 * 396^(4n))
    仅需几项就能得到极高精度
    """
    getcontext().prec = 100  # 设置高精度

    s = Decimal(0)
    for k in range(n):
        numerator = Decimal(math.factorial(4 * k)) * Decimal(1103 + 26390 * k)
        denominator = Decimal(math.factorial(k) ** 4) * Decimal(396 ** (4 * k))
        s += numerator / denominator

    pi = Decimal(9801) / Decimal(2).sqrt() / s
    return float(pi)


def wallis(n=1000000):
    """
    沃利斯乘积
    π/2 = (2/1) * (2/3) * (4/3) * (4/5) * (6/5) * (6/7) * ...
    """
    pi = 2.0
    for i in range(1, n + 1):
        left = (2 * i) / (2 * i - 1)
        right = (2 * i) / (2 * i + 1)
        pi *= left * right
    return pi


def archimedes(n=1000000):
    """
    阿基米德多边形法
    从圆内接和外切多边形开始，不断加倍边数逼近圆周
    """
    sides = 6  # 从六边形开始
    a = 1  # 内接多边形边长
    b = 1 / math.sqrt(3)  # 外切多边形边长

    for _ in range(int(math.log2(n / 3))):  # 加倍边数直到接近n
        sides *= 2
        # 计算新的内接和外切边长
        a_new = math.sqrt(2 - math.sqrt(4 - a * a))
        b_new = (math.sqrt(a * a + b * b) - b) / (math.sqrt(a * a + b * b) + b) * 2 * b

        a = a_new
        b = b_new

    # 圆周率在两者之间
    pi_lower = sides * a / 2
    pi_upper = sides * b / 2
    return (pi_lower + pi_upper) / 2


def calculate_all():
    """运行所有算法并比较结果"""
    print("=" * 60)
    print("圆周率计算器 - 多种算法对比")
    print("=" * 60)
    print(f"数学库标准值: {math.pi:.15f}\n")

    # 蒙特卡洛方法
    print("1. 蒙特卡洛方法 (100万次采样)")
    result = monte_carlo(1000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.pi):.10f}\n")

    # 莱布尼茨级数
    print("2. 莱布尼茨级数 (100万项)")
    result = leibniz(1000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.pi):.10f}\n")

    # 沃利斯乘积
    print("3. 沃利斯乘积 (100万项)")
    result = wallis(1000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.pi):.10f}\n")

    # 拉马努金公式（只需要几项）
    print("4. 拉马努金公式 (仅需5项)")
    result = ramanujan(5)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.pi):.10f}\n")

    # 阿基米德方法
    print("5. 阿基米德多边形法")
    result = archimedes(1000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.pi):.10f}\n")

    print("=" * 60)
    print("结论: 拉马努金公式收敛最快，仅需几项就能达到极高精度")
    print("      莱布尼茨和沃利斯方法收敛较慢，需要百万级项")
    print("      蒙特卡洛方法适合理解概率思想，精度有限")
    print("=" * 60)


if __name__ == '__main__':
    calculate_all()
