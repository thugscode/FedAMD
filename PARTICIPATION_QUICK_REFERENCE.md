# Client Participation Analyzer - Quick Reference

## 30-Second Quick Start

```python
from participation import ParticipationAnalyzer, ParticipationVisualizer

# Load and analyze
analyzer = ParticipationAnalyzer('./results')
analyzer.load_all_experiments()
analyzer.analyze_participation_impact()
analyzer.print_participation_report()

# Visualize
visualizer = ParticipationVisualizer('./results/participation_plots')
visualizer.plot_all_participation_visualizations(
    analyzer.experiments, 
    analyzer.get_participation_variance_impact(),
    analyzer.analyze_full_vs_partial(),
    analyzer.analyses
)
```

## Core Classes

### ParticipationAnalyzer
Main analysis tool for understanding participation impact on convergence.

**Key Methods:**
- `load_all_experiments(pattern='*_metrics.json')` - Load all JSON files
- `analyze_participation_impact()` - Compute participation statistics
- `analyze_full_vs_partial(threshold=0.8)` - Compare full vs partial participation
- `get_participation_impact()` - Get participation-accuracy correlation
- `print_participation_report()` - Print formatted analysis
- `print_recommendations()` - Get algorithm recommendations
- `export_participation_metrics(filepath)` - Save analysis to JSON

### ParticipationVisualizer
Create publication-quality visualizations of participation analysis.

**Visualization Types:**
1. **Participation Over Time** - Show participation rate trends
2. **Accuracy vs Participation** - Scatter plot with trend lines
3. **Variance Impact** - How variance affects performance
4. **Full vs Partial** - Side-by-side performance comparison
5. **Robustness Profiles** - Multi-metric robustness visualization
6. **Heatmap** - Accuracy at different participation levels

## Typical Workflow

```python
# 1. Initialize and load
analyzer = ParticipationAnalyzer('./results')
analyzer.load_all_experiments()

# 2. Core analysis
analyzer.analyze_participation_impact()
analyzer.print_participation_report()

# 3. Deep dives
analyzer.print_full_vs_partial_analysis()  # Compare participation levels
analyzer.print_participation_impact()      # Correlation analysis
analyzer.print_recommendations()           # Get recommendations

# 4. Visualize
visualizer = ParticipationVisualizer('./results/participation_plots')
visualizer.plot_participation_over_time(analyzer.experiments)
visualizer.plot_accuracy_vs_participation(analyzer.experiments)

# 5. Export
analyzer.export_participation_metrics()
```

## Output Metrics

### Per-Algorithm Metrics (ParticipationAnalysis)
- `avg_participation_rate` - Average % of clients participating
- `min_participation_rate` - Minimum participation (worst case)
- `max_participation_rate` - Maximum participation (best case)
- `participation_consistency` - Std dev of participation (σ)
- `convergence_rounds` - Rounds to reach 95% of best accuracy
- `final_accuracy` - Final model accuracy
- `communication_efficiency` - Accuracy per communication round
- `robustness_score` - Stability under varying participation (0-1)

### Full vs Partial Metrics
- `full_participation_avg` - Average accuracy with ≥80% clients
- `partial_participation_avg` - Average accuracy with <80% clients
- `degradation` - Accuracy loss from partial participation

### Variance Metrics
- `participation_cv` - Coefficient of variation in participation
- `accuracy_std` - Standard deviation of accuracy
- `participation_accuracy_correlation` - How correlated are they?

## Supported Experiments

Expects JSON files with structure:
```json
{
  "experiment": "experiment_name",
  "algorithm": "FedAvg",
  "config": {
    "num_clients": 20,
    ...
  },
  "metrics": {
    "rounds": [1, 2, 3, ...],
    "test_acc": [0.2, 0.3, 0.5, ...],
    "test_loss": [2.3, 2.1, 1.5, ...],
    "client_participation": [15, 18, 20, ...],
    ...
  }
}
```

## Common Use Cases

### 1. Find Most Robust Algorithm
```python
best = max(analyses.items(), key=lambda x: x[1].robustness_score)
print(f"Most robust: {best[0]} (score: {best[1].robustness_score})")
```

### 2. Compare Efficiency
```python
for algo, analysis in sorted(analyses.items()):
    eff = analysis.communication_efficiency
    print(f"{algo}: {eff:.6f}")
```

### 3. Identify Low-Participation Algorithms
```python
low_part = [a for a, d in analyses.items() if d.avg_participation_rate < 50]
print(f"Can work with <50%: {low_part}")
```

### 4. Analyze Participation-Accuracy Correlation
```python
impact = analyzer.get_participation_impact()
for algo, data in impact.items():
    corr = data['participation_accuracy_correlation']
    print(f"{algo}: {corr:.3f} correlation")
```

### 5. Full vs Partial Comparison
```python
result = analyzer.analyze_full_vs_partial(threshold=0.8)
for algo, data in result.items():
    full_acc = data['full_participation']['avg_accuracy']
    partial_acc = data['partial_participation']['avg_accuracy']
    loss = full_acc - partial_acc
    print(f"{algo}: Loss = {loss:.4f}")
```

## Output Files

When visualizations are saved:
- `participation_over_time.png` - Participation trends
- `accuracy_vs_participation.png` - Accuracy-participation relationship
- `participation_variance_impact.png` - Variance effect on performance
- `full_vs_partial_participation.png` - Full vs partial comparison
- `robustness_profiles.png` - Multi-metric robustness view
- `participation_impact_heatmap.png` - Accuracy at different rates

When metrics are exported:
- `participation_analysis.json` - Complete analysis data

## Interpretation Guide

### Robustness Score
- **> 0.8**: Excellent - Very stable even with participation variance
- **0.5-0.8**: Good - Relatively stable
- **< 0.5**: Fair - Noticeably affected by participation changes

### Communication Efficiency
- **> 0.005**: Excellent - High accuracy per communication round
- **0.002-0.005**: Good - Reasonable efficiency
- **< 0.002**: Fair - Requires more communication rounds

### Participation-Accuracy Correlation
- **> 0.7**: High impact - Sensitive to client dropout
- **0.3-0.7**: Moderate - Some impact from dropout
- **< 0.3**: Low impact - Robust to client dropout

### Participation Consistency (σ)
- **Low (σ < 2)**: Stable participation levels
- **Medium (σ 2-5)**: Variable but manageable
- **High (σ > 5)**: Highly variable, may affect reliability

## Advanced Usage

### Access Internal Data
```python
# Direct experiment data
experiments = analyzer.experiments  # Dict of experiment data

# Analysis results
analyses = analyzer.analyses  # Dict of ParticipationAnalysis

# Participation impact
impact = analyzer.get_participation_impact()

# Variance impact
variance = analyzer.get_participation_variance_impact()

# Full vs partial
full_vs_partial = analyzer.analyze_full_vs_partial()

# Recommendations
recs = analyzer.get_participation_recommendations()

# Optimal rates
optimal = analyzer.get_optimal_participation_rate()
```

### Custom Metrics
```python
# Access individual algorithm analysis
analysis = analyzer.analyses['FedAvg']
print(f"Final accuracy: {analysis.final_accuracy}")
print(f"Convergence: {analysis.convergence_rounds} rounds")
print(f"Participation range: {analysis.min_participation_rate:.1f}% - {analysis.max_participation_rate:.1f}%")
```

### Custom Visualizations
```python
# Use ParticipationVisualizer components separately
visualizer = ParticipationVisualizer()

# Single visualization
visualizer.plot_participation_over_time(experiments, save=True)

# Or create custom analysis visualization
import matplotlib.pyplot as plt
# ... plot custom metrics
```

## Troubleshooting

**No experiments loaded:**
- Check directory path exists
- Verify JSON files match `*_metrics.json` pattern
- Ensure JSON has required fields: `metrics.client_participation`, `metrics.test_acc`

**Missing participation data:**
- ParticipationAnalyzer requires `client_participation` in metrics
- Add to training script: `tracker.log_round(..., num_clients=...)` 
- See INTEGRATION_GUIDE.md for how to enable tracking

**Correlations showing NaN:**
- Need at least 2 rounds of data
- Ensure both participation and accuracy are logged
- Check for None values in data

**Visualizations not displaying:**
- Check output directory: `mkdir -p ./results/participation_plots`
- Verify matplotlib is installed: `pip install matplotlib`
- Try `plt.show()` after plot calls
