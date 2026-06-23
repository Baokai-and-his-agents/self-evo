"""Report generation: Chinese markdown report and JSON results."""

from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json

from .engine import BacktestResult, CostModel
from .analysis import ConditionalStats, analyze_conditional_hypothesis, compare_policies_paired
from .data import DataManifest


def generate_markdown_report(
    results: Dict[str, BacktestResult],
    conditional_stats: List[ConditionalStats],
    manifest: DataManifest,
    cost_model: CostModel,
    config: dict,
    output_path: Path
):
    """Generate Chinese markdown report.

    Args:
        results: Dictionary mapping policy name to BacktestResult
        conditional_stats: Conditional probability statistics
        manifest: Data manifest
        cost_model: Cost model used
        config: Configuration dictionary
        output_path: Output file path
    """
    report_lines = []

    # Header
    report_lines.append("# 外汇仓位管理对照回测报告")
    report_lines.append("")
    report_lines.append(f"**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Issue:** #18")
    report_lines.append(f"**Worker:** fx-backtest-worker-01")
    report_lines.append("")

    # Data info
    report_lines.append("## 数据概况")
    report_lines.append("")
    report_lines.append(f"- **数据源:** {manifest.source}")
    report_lines.append(f"- **货币对:** {manifest.pair}")
    report_lines.append(f"- **时间框架:** {manifest.timeframe}")
    report_lines.append(f"- **数据期间:** {manifest.start_date.strftime('%Y-%m-%d')} 至 {manifest.end_date.strftime('%Y-%m-%d')}")
    report_lines.append(f"- **K线数量:** {manifest.num_bars}")
    report_lines.append(f"- **时区:** {manifest.timezone}")
    report_lines.append(f"- **数据类型:** {manifest.data_type}")
    report_lines.append(f"- **SHA256:** `{manifest.sha256}`")
    report_lines.append("")

    # Signal config
    report_lines.append("## 信号配置（预注册）")
    report_lines.append("")
    report_lines.append("以下参数在回测运行前固定，未在同一数据上优化：")
    report_lines.append("")
    signal_cfg = config.get('signal', {})
    report_lines.append(f"- **入场:** {signal_cfg.get('entry_period', 20)}-日 Donchian 通道突破")
    report_lines.append(f"- **退出:** {signal_cfg.get('exit_period', 10)}-日 Donchian 通道")
    report_lines.append(f"- **止损:** {signal_cfg.get('atr_stop_multiplier', 2.0)} × ATR({signal_cfg.get('atr_period', 14)})")
    report_lines.append("")
    report_lines.append("**警告:** 这些参数仅为说明性配置，不代表推荐参数或最优值。")
    report_lines.append("")

    # Cost model
    report_lines.append("## 成本模型")
    report_lines.append("")
    if cost_model.spread_pips == 0 and cost_model.commission_per_lot == 0:
        report_lines.append("**零成本场景** - 用于隔离仓位策略效果")
    else:
        report_lines.append("**保守成本场景:**")
        report_lines.append(f"- Spread: {cost_model.spread_pips} pips")
        report_lines.append(f"- Commission: ${cost_model.commission_per_lot} per lot")
        report_lines.append(f"- Slippage: {cost_model.slippage_pips} pips")
    report_lines.append("")

    # A/B/E/G Results
    report_lines.append("## 策略对照结果")
    report_lines.append("")
    report_lines.append("### 策略定义")
    report_lines.append("")
    report_lines.append("- **A (Fixed):** 固定 1% 风险，不随止损次数变化")
    report_lines.append("- **B (Arithmetic):** 止损后算术递增，r_n = min(1% + n×0.5%, 3%)，上限 K=5")
    report_lines.append("- **E (Confirm):** 固定 0.5% 试探，独立确认后放大至 2%")
    report_lines.append("- **G (Placebo):** 与 B 相同的仓位分布，但打乱 stop_count → size 映射（seed=42）")
    report_lines.append("")

    report_lines.append("### 收益与风险指标")
    report_lines.append("")
    report_lines.append("| 策略 | 交易数 | 胜率 | 总收益 | 最大回撤 | 平均R | 终止于K次 |")
    report_lines.append("|------|--------|------|--------|----------|-------|-----------|")

    for policy_name in ['A', 'B', 'E', 'G']:
        if policy_name not in results:
            continue
        r = results[policy_name]
        report_lines.append(
            f"| {policy_name} | {r.num_trades} | {r.win_rate:.2%} | "
            f"{r.total_return:+.2%} | {r.max_drawdown_pct:.2%} | "
            f"{r.avg_r:+.2f} | {r.max_stop_count_reached} |"
        )

    report_lines.append("")

    # Conditional probability
    report_lines.append("## 核心问题：条件概率分析")
    report_lines.append("")
    report_lines.append("**研究问题:** 连续止损次数是否预测下一次交易结果？")
    report_lines.append("")
    report_lines.append("### P(胜 | 连续止损=n)")
    report_lines.append("")
    report_lines.append("| 连续止损次数 n | 样本量 | 胜场 | 败场 | P(胜) | 95% CI |")
    report_lines.append("|----------------|--------|------|------|-------|---------|")

    for stat in conditional_stats[:8]:  # Show first 8 buckets
        if stat.n > 0:
            report_lines.append(
                f"| {stat.stop_count} | {stat.n} | {stat.num_wins} | {stat.num_losses} | "
                f"{stat.p_win:.3f} | [{stat.p_win_ci_low:.3f}, {stat.p_win_ci_high:.3f}] |"
            )
        else:
            report_lines.append(f"| {stat.stop_count} | 0 | - | - | - | - |")

    report_lines.append("")

    report_lines.append("### E[R | 连续止损=n]")
    report_lines.append("")
    report_lines.append("| 连续止损次数 n | 样本量 | 平均R | 95% CI |")
    report_lines.append("|----------------|--------|-------|---------|")

    for stat in conditional_stats[:8]:
        if stat.n > 0:
            report_lines.append(
                f"| {stat.stop_count} | {stat.n} | {stat.mean_r:+.3f} | "
                f"[{stat.mean_r_ci_low:+.3f}, {stat.mean_r_ci_high:+.3f}] |"
            )
        else:
            report_lines.append(f"| {stat.stop_count} | 0 | - | - |")

    report_lines.append("")

    # Hypothesis test
    hypothesis_result = analyze_conditional_hypothesis(conditional_stats)
    report_lines.append("### 假设检验结果")
    report_lines.append("")
    report_lines.append(f"**趋势:** {hypothesis_result.get('trend', 'N/A')}")
    report_lines.append("")
    report_lines.append(f"**解释:** {hypothesis_result.get('interpretation', 'N/A')}")
    report_lines.append("")

    # Paired comparisons
    if 'A' in results and 'B' in results:
        report_lines.append("## 配对比较")
        report_lines.append("")

        comparison_b_a = compare_policies_paired(results['A'], results['B'])
        report_lines.append("### B vs A (算术递增 vs 固定)")
        report_lines.append("")
        report_lines.append(f"- **平均PnL差异:** ${comparison_b_a.get('mean_pnl_diff', 0):.2f}")
        report_lines.append(f"- **95% CI:** [${comparison_b_a.get('pnl_diff_ci_low', 0):.2f}, ${comparison_b_a.get('pnl_diff_ci_high', 0):.2f}]")
        report_lines.append(f"- **总权益差异:** ${comparison_b_a.get('total_equity_diff', 0):.2f}")
        report_lines.append(f"- **解释:** {comparison_b_a.get('interpretation', 'N/A')}")
        report_lines.append("")

    if 'B' in results and 'G' in results:
        comparison_b_g = compare_policies_paired(results['B'], results['G'])
        report_lines.append("### B vs G (算术递增 vs 置换安慰剂)")
        report_lines.append("")
        report_lines.append(f"- **平均PnL差异:** ${comparison_b_g.get('mean_pnl_diff', 0):.2f}")
        report_lines.append(f"- **95% CI:** [${comparison_b_g.get('pnl_diff_ci_low', 0):.2f}, ${comparison_b_g.get('pnl_diff_ci_high', 0):.2f}]")
        report_lines.append(f"- **总权益差异:** ${comparison_b_g.get('total_equity_diff', 0):.2f}")
        report_lines.append(f"- **解释:** {comparison_b_g.get('interpretation', 'N/A')}")
        report_lines.append("")

    # Conclusions
    report_lines.append("## 结论与限制")
    report_lines.append("")
    report_lines.append("### 研究问题回答")
    report_lines.append("")

    if hypothesis_result.get('all_cis_overlap_baseline', True):
        report_lines.append("**连续止损次数不包含关于下一次交易结果的明显信息。** "
                          "各止损计数桶的胜率置信区间与基线（n=0）重叠，未观察到统计上显著的趋势。")
    else:
        report_lines.append("**观察到止损次数与后续交易结果之间的某些关联。** "
                          "但需注意样本量、多重比较问题和过拟合风险。")

    report_lines.append("")
    report_lines.append("### 策略比较")
    report_lines.append("")

    if 'B' in results and 'A' in results:
        if results['B'].final_equity > results['A'].final_equity:
            report_lines.append(f"- B (算术递增) 在本数据集上终值权益高于 A (固定仓位)，"
                              f"差异 ${results['B'].final_equity - results['A'].final_equity:.2f}")
        else:
            report_lines.append(f"- B (算术递增) 在本数据集上未优于 A (固定仓位)")

    report_lines.append("")
    report_lines.append("### 关键限制")
    report_lines.append("")
    report_lines.append("1. **数据限制:** " + manifest.notes if manifest.notes else "合成fixture数据，非真实历史")
    report_lines.append("2. **参数未优化:** 信号参数为预注册说明性配置，未在本数据上寻优")
    report_lines.append("3. **样本量:** 部分止损计数桶样本不足（n<10），置信区间宽泛")
    report_lines.append("4. **单一市场:** 仅测试一个货币对，泛化性未验证")
    report_lines.append("5. **成本假设:** 实际交易成本、滑点和执行质量可能显著不同")
    report_lines.append("6. **不构成投资建议:** 本研究为学术探索，不保证盈利，不建议实盘使用")
    report_lines.append("")

    # Write report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))


def save_json_results(
    results: Dict[str, BacktestResult],
    conditional_stats: List[ConditionalStats],
    manifest: DataManifest,
    output_path: Path
):
    """Save machine-readable JSON results.

    Args:
        results: Policy results
        conditional_stats: Conditional statistics
        manifest: Data manifest
        output_path: Output JSON path
    """
    data = {
        "manifest": manifest.to_dict(),
        "results": {name: result.to_dict() for name, result in results.items()},
        "conditional_stats": [stat.to_dict() for stat in conditional_stats],
        "generated_at": datetime.now().isoformat()
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
