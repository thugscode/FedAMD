# participation/ - Client Participation Analysis Module

**Analyze the impact of partial client participation on convergence in federated learning.**

## What It Does

This module helps you understand:
- How client dropout/participation affects convergence
- Which algorithms are robust to varying participation 
- Performance differences between high and low participation scenarios
- Optimal participation rates for each algorithm

## Quick Start

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

## Files

- **analyzer.py** - Core ParticipationAnalyzer class and data structures
- **visualize.py** - ParticipationVisualizer with 6 plot types
- **__init__.py** - Module exports

## Key Classes

### ParticipationAnalyzer
Load experiment data and analyze participation impact:
- `load_all_experiments()` - Load all JSON files from results dir
- `analyze_participation_impact()` - Compute participation statistics
- `analyze_full_vs_partial()` - Compare high vs low participation
- `print_participation_report()` - Print formatted analysis
- `export_participation_metrics()` - Save to JSON

### ParticipationVisualizer  
Create 6 types of participation visualizations:
1. **Participation Over Time** - Round-by-round participation rates
2. **Accuracy vs Participation** - Scatter with trend lines
3. **Variance Impact** - How variance affects performance
4. **Full vs Partial** - High vs low participation comparison
5. **Robustness Profiles** - Multi-metric robustness view
6. **Heatmap** - Accuracy at different participation levels

## Key Metrics

Per-algorithm metrics returned by `analyze_participation_impact()`:

| Metric | Meaning |
|--------|---------|
| `avg_participation_rate` | Average % of clients participating |
| `participation_consistency` | Std dev of participation (σ) |
| `convergence_rounds` | Rounds to reach 95% best accuracy |
| `final_accuracy` | Final model accuracy achieved |
| `communication_efficiency` | Accuracy gained per communication round |
| `robustness_score` | Stability under varying participation (0-1) |

## Supported Experiments

Expects JSON files with:
```json
{
  "algorithm": "FedAvg",
  "config": {"num_clients": 20, ...},
  "metrics": {
    "test_acc": [...],
    "test_loss": [...],
    "client_participation": [...]
  }
}
```

The `client_participation` field is required (number of clients in each round).

## Common Usage Patterns

**Find most robust algorithm:**
```python
best = max(analyses.items(), key=lambda x: x[1].robustness_score)
print(f"Most robust: {best[0]}")
```

**Compare efficiency:**
```python
for algo, analysis in analyses.items():
    print(f"{algo}: {analysis.communication_efficiency:.6f}")
```

**Check degradation with low participation:**
```python
result = analyzer.analyze_full_vs_partial(threshold=0.8)
for algo, data in result.items():
    full = data['full_participation']['avg_accuracy']
    partial = data['partial_participation']['avg_accuracy']
    print(f"{algo}: Loss = {full - partial:.4f}")
```

## Visualizations Generated

When using `plot_all_participation_visualizations()`:
- `participation_over_time.png`
- `accuracy_vs_participation.png`
- `participation_variance_impact.png`
- `full_vs_partial_participation.png`
- `robustness_profiles.png`
- `participation_impact_heatmap.png`

All saved to `./results/participation_plots/`

## Data Structures

### ParticipationAnalysis
Aggregated statistics for one algorithm:
```python
@dataclass
class ParticipationAnalysis:
    algorithm_name: str
    total_clients: int
    avg_participation_rate: float       # %
    min_participation_rate: float       # %
    max_participation_rate: float       # %
    participation_consistency: float    # σ
    convergence_rounds: int
    final_accuracy: float
    communication_efficiency: float
    robustness_score: float            # 0-1
```

### ParticipationMetrics
Per-round metrics (not currently used by analyzer, reserved for future):
```python
@dataclass
class ParticipationMetrics:
    round_num: int
    num_clients_participating: int
    total_clients: int
    participation_rate: float          # %
    test_accuracy: float
    test_loss: float
    accumulated_communication_rounds: int
```

## Advanced Features

**Full vs Partial Threshold:**
```python
# Compare with different threshold (default 80%)
result = analyzer.analyze_full_vs_partial(threshold=0.9)
```

**Custom Threshold for Recommendations:**
```python
recommendations = analyzer.get_participation_recommendations()
```

**Optimal Participation Estimation:**
```python
optimal = analyzer.get_optimal_participation_rate()
for algo, rate in optimal.items():
    print(f"{algo}: Recommended {rate:.1f}%")
```

**Participation-Accuracy Correlation:**
```python
impact = analyzer.get_participation_impact()
for algo, data in impact.items():
    corr = data['participation_accuracy_correlation']
    if corr < 0.3:
        print(f"{algo}: Robust to dropout")
```

## Integration with Training

To enable participation tracking in your training script:

```python
from visualization import MetricsTracker

tracker = MetricsTracker()
tracker.log_config(algorithm='FedAvg', num_clients=20, ...)

for round_num in range(num_rounds):
    selected = random_client_selection()  # Get participating clients
    # ... training ...
    tracker.log_round(
        round_num=round_num,
        test_loss=loss,
        test_acc=acc,
        train_loss=train_loss,
        train_acc=train_acc,
        num_clients=len(selected)  # Log participation count
    )

tracker.save_json()
```

## Output Export

**JSON Export:**
```python
analyzer.export_participation_metrics('./results/participation_analysis.json')
```

Exports all analyses, full/partial comparisons, variance impact, and optimal rates.

## See Also

- **PARTICIPATION_GUIDE.md** - Comprehensive usage guide
- **PARTICIPATION_QUICK_REFERENCE.md** - 30-second quick start
- **examples_participation.py** - 12 working examples
- **visualization/** - Single-experiment metrics tracking
- **comparison/** - Multi-algorithm comparison tool

## Notes

- Requires matplotlib 3.8+ for visualizations
- Requires numpy 1.24+ for statistical computations
- All existing requirements (pandas, torch, etc.) remain
- No new dependencies needed beyond core tools
