#!/usr/bin/env python3
"""
Progressive Probe Position Sizing - Numerical Verification

验证数学模型中的关键公式和数值例子。
本脚本仅用于数学审计，不连接真实市场或经纪商。
"""

import math

def arithmetic_progression_loss(r0, d, n):
    """
    算术递增累计亏损
    L_n = n × (r_0 + d(n-1)/2)
    """
    return n * (r0 + d * (n - 1) / 2)

def arithmetic_position_size(r0, d, n, r_max=None):
    """
    算术递增仓位大小
    r_n = min(r_0 + n × d, r_max)
    """
    r_n = r0 + n * d
    if r_max is not None:
        r_n = min(r_n, r_max)
    return r_n

def geometric_progression_loss(r0, m, n):
    """
    几何递增累计亏损
    L_n = r_0 × (m^n - 1) / (m - 1)
    """
    return r0 * (m**n - 1) / (m - 1)

def geometric_position_size(r0, m, n, r_max=None):
    """
    几何递增仓位大小
    r_n = min(r_0 × m^n, r_max)
    """
    r_n = r0 * (m ** n)
    if r_max is not None:
        r_n = min(r_n, r_max)
    return r_n

def breakeven_R_arithmetic(r0, d, n):
    """
    算术递增的 break-even R
    R >= L_n / r_n
    """
    L_n = arithmetic_progression_loss(r0, d, n)
    r_n = arithmetic_position_size(r0, d, n)
    return L_n / r_n

def breakeven_R_geometric(m, n):
    """
    几何递增的 break-even R
    R >= (1 - m^(-n)) / (m - 1)
    """
    return (1 - m**(-n)) / (m - 1)

def cycle_failure_probability(p, K):
    """
    单 cycle 连续 K+1 次失败概率
    P(cycle_failure) = (1 - p)^(K+1)
    注意：这不是账户破产概率
    """
    return (1 - p) ** (K + 1)

def max_K_under_budget(r0, d, budget):
    """
    Budget 约束下的最大 K
    K_max = [-(r_0 - d/2) + sqrt((r_0 - d/2)^2 + 2×d×B)] / d
    """
    a = d / 2
    b = r0 - d / 2
    discriminant = b**2 + 2 * d * budget
    K_max = (-b + math.sqrt(discriminant)) / d
    return K_max

def verify_arithmetic_example():
    """验证算术递增数值例子（Section 2.1）"""
    print("=== 算术递增 Break-Even R 验证 ===")
    print("参数: r_0=1%, d=0.5%, K=5\n")

    r0, d, K = 1.0, 0.5, 5

    for n in range(6):
        L_n = arithmetic_progression_loss(r0, d, n)
        r_n = arithmetic_position_size(r0, d, n)
        if n == 0:
            R_min = 0  # 首次无需回本
        else:
            R_min = breakeven_R_arithmetic(r0, d, n)

        print(f"n={n}: L_{n}={L_n:.1f}%, r_{n}={r_n:.1f}%, R_min>={R_min:.2f}")

    print()

def verify_geometric_example():
    """验证几何递增数值例子（Section 2.2）"""
    print("=== 几何递增 Break-Even R 验证 ===")
    print("参数: m=2 (doubling)\n")

    r0, m = 1.0, 2.0

    for n in range(1, 6):
        L_n = geometric_progression_loss(r0, m, n)
        r_n = geometric_position_size(r0, m, n)
        R_min = breakeven_R_geometric(m, n)

        print(f"n={n}: L_{n}={L_n:.0f}×r_0, r_{n}={r_n:.0f}×r_0, R_min>={R_min:.5f}")

    print(f"\n极限: R_min → 1/(m-1) = {1/(m-1):.5f}")
    print()

def verify_cycle_failure():
    """验证单 cycle 失败概率（Section 5.1）"""
    print("=== 单 Cycle 失败概率验证 ===")
    print("注意：这不是账户破产概率，仅是单 cycle 连续失败概率\n")

    test_cases = [
        (0.4, 5),
        (0.3, 5),
        (0.4, 10),
    ]

    for p, K in test_cases:
        P_fail = cycle_failure_probability(p, K)
        print(f"p={p}, K={K}: P(cycle_failure) = {P_fail:.4f} ({P_fail*100:.2f}%)")

    print()

def verify_budget_constraint():
    """验证 Budget 约束下的最大 K（Section 5.3）"""
    print("=== Budget 约束最大 K 验证 ===\n")

    test_cases = [
        (1.0, 0.5, 10.0),
        (1.0, 0.5, 15.0),
        (2.0, 1.0, 15.0),
    ]

    for r0, d, budget in test_cases:
        K_max_float = max_K_under_budget(r0, d, budget)
        K_max = int(K_max_float)
        L_K = arithmetic_progression_loss(r0, d, K_max)

        print(f"r_0={r0}%, d={d}%, Budget={budget}%:")
        print(f"  K_max = {K_max_float:.2f} → K={K_max}")
        print(f"  L_{K_max} = {L_K:.2f}% (< {budget}%)")
        print()

def verify_complete_cycle_expectation():
    """
    验证完整 cycle 期望的索引和终端项
    E[Total] = Σ(n=0 to K) (1-p)^n × p × (r_{n+1} × R - L_n)
             + P(K+1 losses) × (-L_K - r_K)
    """
    print("=== 完整 Cycle 期望验证 ===")
    print("参数: r_0=1%, d=0.5%, K=3, p=0.4, R=2.0\n")

    r0, d, K = 1.0, 0.5, 3
    p, R = 0.4, 2.0

    total_expectation = 0.0

    # 成功路径：前 n 次失败，第 n+1 次成功
    for n in range(K + 1):
        L_n = arithmetic_progression_loss(r0, d, n)
        r_next = arithmetic_position_size(r0, d, n)
        prob = ((1 - p) ** n) * p
        net = r_next * R - L_n
        contribution = prob * net
        total_expectation += contribution

        print(f"n={n}: P={(1-p)**n:.4f}×{p:.1f}={prob:.4f}, "
              f"r_{n}={r_next:.1f}%, L_{n}={L_n:.1f}%, "
              f"Net={net:.2f}%, E_contrib={contribution:.4f}%")

    # 终端失败路径：K+1 次全部失败
    L_K = arithmetic_progression_loss(r0, d, K)
    r_K = arithmetic_position_size(r0, d, K)
    P_terminal_failure = (1 - p) ** (K + 1)
    terminal_loss = -(L_K + r_K)
    terminal_contribution = P_terminal_failure * terminal_loss
    total_expectation += terminal_contribution

    print(f"\n终端失败: P={(1-p)**(K+1):.4f}, "
          f"Loss=-(L_{K} + r_{K})=-({L_K:.1f}% + {r_K:.1f}%)={terminal_loss:.2f}%, "
          f"E_contrib={terminal_contribution:.4f}%")

    print(f"\n总期望: E[Total] = {total_expectation:.4f}%")

    if total_expectation > 0:
        print("结论: 正期望（此参数下有利可图）")
    else:
        print("结论: 负期望（此参数下不利）")

    print()

def main():
    print("Progressive Probe Position Sizing - 数值验证\n")
    print("本脚本验证 mathematical-model.md 中的关键公式\n")
    print("=" * 60)
    print()

    verify_arithmetic_example()
    verify_geometric_example()
    verify_cycle_failure()
    verify_budget_constraint()
    verify_complete_cycle_expectation()

    print("=" * 60)
    print("\n所有数值例子验证完成。")
    print("\n重要提醒:")
    print("- P(cycle_failure) 不等于账户破产概率")
    print("- 多 cycle 破产风险需递归/Markov/Monte Carlo 建模")
    print("- 以上例子仅用于数学审计，不构成交易建议")
    print("- 实际应用需实证检验核心假设（止损序列是否预测趋势）")

if __name__ == "__main__":
    main()
