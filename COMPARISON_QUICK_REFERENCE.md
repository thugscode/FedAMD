# Experiment Comparison Tool - Quick Reference

## 30-Second Start

```python
from comparison import ComparisonTool

comp = ComparisonTool('./results')
comp.load_experiments()
comp.print_detailed_report()
```

## Core Classes

### ComparisonTool
```python
comp = ComparisonTool('./results')

# Load
comp.load_experiments()                        # Load all *_metrics.json
comp.load_specific(filepath)                   # Load specific file

# Statistics
stats = comp.compute_statistics()              # Compute stats
df = comp.create_dataframe()                   # As DataFrame

# Queries
comp.get_best_algorithm('best_accuracy')       # (algo_name, value)
comp.get_ranking('best_accuracy')              # [(algo, value), ...]
comp.identify_strengths_weaknesses()           # Dict of analysis
comp.get_comparison_summary()                  # Full summary

# Print
comp.print_detailed_report()                   # Full report
comp.print_rankings()                          # All rankings
comp.print_analysis()                          # Strengths/weaknesses

# Export
comp.export_csv(filepath)                      # Export to CSV
comp.export_comparison_table(filepath)         # Export text table
```

### ComparisonVisualizer
```python
viz = ComparisonVisualizer()

# Plot
viz.plot_accuracy_comparison(experiments)      # Accuracy curves
viz.plot_loss_comparison(experiments)          # Loss curves
viz.plot_metrics_comparison_bars(stats)        # 4-panel bars
viz.plot_speedup_analysis(stats, baseline)     # Speedup chart
viz.plot_convergence_radar(stats)              # Radar chart

# All at once
viz.plot_all_comparisons(experiments, stats)   # Generate all
```

## Typical Workflow

```python
from comparison import ComparisonTool, ComparisonVisualizer

# 1. Load
comp = ComparisonTool('./results')
num = comp.load_experiments()
print(f"Loaded {num} experiments")

# 2. Analyze
comp.print_detailed_report()
comp.print_rankings()

# 3. Visualize
experiments = {d['algorithm']: d['metrics'] 
               for d in comp.experiments.values()}
viz = ComparisonVisualizer()
viz.plot_all_comparisons(experiments, comp.stats)

# 4. Export
comp.export_csv('comparison.csv')
comp.export_comparison_table('comparison.txt')

# 5. Share
best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
print(f"Best: {best_algo} with {best_acc:.4f}")
```

## Common Queries

```python
# Find best algorithm
best, acc = comp.get_best_algorithm('best_accuracy')
best, rounds = comp.get_best_algorithm('convergence_round_95')

# Get rankings
for rank, (algo, value) in enumerate(comp.get_ranking('best_accuracy'), 1):
    print(f"{rank}. {algo}: {value:.4f}")

# Understand strengths
analysis = comp.identify_strengths_weaknesses()
print(analysis['FedAvg']['strengths'])

# Get summary
summary = comp.get_comparison_summary()
print(summary['best_by_accuracy'])
```

## Metrics to Compare

| Metric | Meaning | Better |
|--------|---------|--------|
| best_accuracy | Peak accuracy | Higher |
| final_accuracy | Last round accuracy | Higher |
| avg_accuracy | Average accuracy | Higher |
| convergence_round_95 | Rounds to 95% of best | Lower |
| improvement | Final - Initial | Higher |
| avg_loss | Average loss | Lower |
| final_loss | Last round loss | Lower |

## Visualization Types

1. **Accuracy comparison** - All algorithms on same plot
2. **Loss comparison** - Test loss trajectories
3. **Metrics bar charts** - 4 metrics side-by-side
4. **Speedup analysis** - Relative to baseline algorithm
5. **Radar chart** - Multi-dimensional profile

## Output Files

```
results/
├── comparison_stats.csv              # Statistics table
├── comparison_table.txt              # Text table
└── comparison_plots/
    ├── accuracy_comparison.png
    ├── loss_comparison.png
    ├── metrics_comparison_bars.png
    ├── speedup_vs_FedAvg.png
    └── convergence_radar.png
```

## File Structure

```
comparison/
├── __init__.py                      # Package exports
├── tool.py                          # ComparisonTool (600+ lines)
├── visualize.py                     # ComparisonVisualizer (400+ lines)
└── README.md
```

## Examples

```python
# Example 1: Find best algorithm
best_algo, _ = comp.get_best_algorithm('best_accuracy')
print(f"Recommended: {best_algo}")

# Example 2: Compare convergence speed
rankings = comp.get_ranking('convergence_round_95')
for rank, (algo, rounds) in enumerate(rankings, 1):
    print(f"{rank}. {algo}: {rounds} rounds")

# Example 3: Generate plots
experiments = {d['algorithm']: d['metrics'] for d in comp.experiments.values()}
viz = ComparisonVisualizer()
viz.plot_accuracy_comparison(experiments)

# Example 4: Export for Excel
comp.export_csv('comparison.csv')

# Example 5: Print analysis
comp.print_analysis()  # Identifies strengths/weaknesses
```

## Supported Ranking Metrics

```python
comp.get_ranking('best_accuracy')           # Highest wins
comp.get_ranking('final_accuracy')          # Highest wins
comp.get_ranking('avg_accuracy')            # Highest wins
comp.get_ranking('convergence_round_95')    # Lowest wins (faster)
comp.get_ranking('improvement')             # Highest wins
comp.get_ranking('avg_loss')                # Lowest wins (better)
comp.get_ranking('final_loss')              # Lowest wins (better)
```

## Data Flow

```
Experiment JSON files
        ↓
ComparisonTool.load_experiments()
        ↓
ComparisonTool.compute_statistics()
        ↓
┌───────────────────────────────────┐
│ print_detailed_report()           │
│ print_rankings()                  │
│ print_analysis()                  │
│ export_csv()                      │
│ export_comparison_table()         │
└───────────────────────────────────┘
        ↓
Results: Tables, CSV, Text, Analysis
```

## Performance

- Memory: ~1KB per metric
- Loading: <1 second for 10 experiments
- Statistics: <1 second
- Plotting: ~1-2 seconds for all plots
- Export: <100ms

## Tips

1. **Fair comparison** - Same number of rounds (T parameter)
2. **Multiple seeds** - Run 3+ times for statistical rigor
3. **Consistent naming** - Include algorithm name in experiment name
4. **Baseline** - Specify for speedup comparisons
5. **Export format** - CSV for Excel, text for reports, PNG for papers

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No experiments loaded | Check `*_metrics.json` in `./results/` |
| Empty tables | Call `comp.compute_statistics()` first |
| No data in plots | Ensure experiments have test_acc/test_loss |
| Rankings look odd | Check if metric is "lower" vs "higher" is better |

## Commands Quick List

```python
# Essentials
comp.print_detailed_report()        # Main report

# Analysis
comp.print_rankings()               # Ranked by all metrics
comp.print_analysis()               # Strengths/weaknesses
best, val = comp.get_best_algorithm()

# Visualizations
viz.plot_all_comparisons()          # Generate all plots

# Export
comp.export_csv()                   # CSV for Excel
comp.export_comparison_table()      # Text table
df = comp.create_dataframe()        # Pandas DataFrame
```

## Documentation Links

- **README**: [comparison/README.md](comparison/README.md)
- **Full Guide**: [COMPARISON_GUIDE.md](COMPARISON_GUIDE.md)
- **Examples**: [examples_comparison.py](examples_comparison.py)
- **Summary**: [COMPARISON_BUILD_SUMMARY.md](COMPARISON_BUILD_SUMMARY.md)

---

**Quick link to start**: Run `comp.print_detailed_report()` 🚀
