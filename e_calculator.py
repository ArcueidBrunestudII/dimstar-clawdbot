#!/usr/bin/env python3
"""
自然常数 e 计算器 - 包含多种经典算法
e ≈ 2.71828182845904523536...
"""

import math


def limit_definition(n=100000000):
    """
    极限定义法
    e = lim(n→∞) (1 + 1/n)^n
    这是 e 的原始定义，但收敛较慢
    """
    return (1 + 1/n) ** n


def taylor_series(n=20):
    """
    泰勒级数展开（最常用）
    e = 1 + 1/1! + 1/2! + 1/3! + 1/4! + ...
    收敛很快，这是最实用的方法
    """
    e = 0
    factorial = 1
    for i in range(n):
        if i > 0:
            factorial *= i  # 递归计算阶乘
        e += 1 / factorial
    return e


def continued_fraction(n=20):
    """
    连分数展开
    e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, ..., 1, 2n, 1, ...]
    规律：2, 1, 2, 1, 1, 4, 1, 1, 6, 1, 1, 8, 1, ...
    """
    # 从下往上计算连分数
    def get_element(k):
        if k == 0:
            return 2
        if k % 3 == 2:  # 第3、6、9...位置是 2, 4, 6, 8, ...
            return 2 * ((k + 1) // 3)
        return 1

    # 从最底层的分数开始往上计算
    result = get_element(n)
    for k in range(n - 1, -1, -1):
        result = get_element(k) + 1 / result

    return result


def bernoulli_compound_interest(years=10000):
    """
    伯努利复利问题（e的发现来源）
    假设年利率100%，复利次数趋近于无穷
    e = lim(n→∞) (1 + 1/n)^n
    这里模拟连续复利
    """
    # 将1年分成 n 个计息周期
    n = years
    rate = 1.0  # 100% 年利率
    return (1 + rate / n) ** n


def newtons_method(n=20):
    """
    牛顿法
    e = lim(n→∞) (n+1)^(n+1) / n^n / n
    这是另一种极限形式
    """
    return ((n + 1) ** (n + 1)) / (n ** n * n)


def integral_definition(n=1000000):
    """
    积分定义（数值计算）
    e = ∫(从-∞到+∞) e^(-x^2) dx = √π
    但这里用更简单的：e = ∫(从1到e) (1/x) dx = 1

    使用数值积分求使得 ∫(从1到x) (1/t) dt = 1 的 x
    """
    def integrate(x):
        """计算 ∫(从1到x) (1/t) dt"""
        if x == 1:
            return 0

        # 梯形法则数值积分
        a, b = (1, x) if x > 1 else (x, 1)
        n_steps = 10000
        h = (b - a) / n_steps
        result = 0

        for i in range(n_steps):
            t1 = a + i * h
            t2 = a + (i + 1) * h
            result += (h / 2) * (1/t1 + 1/t2)

        return result if x > 1 else -result

    # 二分查找满足 ∫(1到x) 1/t dt = 1 的 x
    low, high = 1.0, 10.0
    for _ in range(100):
        mid = (low + high) / 2
        integral = integrate(mid)
        if abs(integral - 1) < 1e-15:
            return mid
        if integral < 1:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def calculate_all():
    """运行所有算法并比较结果"""
    print("=" * 70)
    print("自然常数 e 计算器 - 多种算法对比")
    print("=" * 70)
    print(f"数学库标准值: {math.e:.15f}\n")

    # 极限定义
    print("1. 极限定义法 (n = 1亿)")
    result = limit_definition(100000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.e):.10f}\n")

    # 泰勒级数（最快）
    print("2. 泰勒级数展开 (20项)")
    result = taylor_series(20)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.e):.10f}\n")

    # 连分数
    print("3. 连分数展开 (20层)")
    result = continued_fraction(20)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.e):.10f}\n")

    # 牛顿法
    print("4. 牛顿极限法 (n = 1亿)")
    result = newtons_method(100000000)
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.e):.10f}\n")

    # 积分定义
    print("5. 积分定义法 (数值积分)")
    result = integral_definition()
    print(f"   计算结果: {result:.15f}")
    print(f"   误差: {abs(result - math.e):.10f}\n")

    print("=" * 70)
    print("结论: 泰勒级数展开最快最精确，仅需20项即可达到15位精度")
    print("      连分数方法也非常高效")
    print("      极限定义法需要极大的n值才能收敛")
    print("=" * 70)


if __name__ == '__main__':
    calculate_all()
