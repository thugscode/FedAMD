# Experiment Comparison Tool

Easily compare federated learning algorithms side-by-side with comprehensive metrics, statistical analysis, and beautiful visualizations.

## What It Does

Compare different algorithms (FedAvg, FedAMD, SCAFFOLD, etc.) with:

✅ **Detailed comparison tables** - Best accuracy, loss, convergence speed, improvement  
✅ **Algorithm rankings** - Ranked by any metric  
✅ **Visual comparisons** - Accuracy curves, loss curves, bar charts, speedup analysis, radar charts  
✅ **Statistical analysis** - Strengths/weaknesses identification, rankings, insights  
✅ **Data export** - CSV for spreadsheets, text tables for reports  
✅ **Pandas integration** - Load as DataFrame for custom analysis  

## Quick Start (3 Lines)

```python
from comparison import ComparisonTool

comp = ComparisonTool('./results')
comp.load_experiments()
comp.print_detailed_report()
```

That's it! Your comparison results appear instantly.

## Installation

Module is self-contained. No new dependencies needed (uses matplotlib, pandas, numpy - already in requirements.txt).

## Usage Examples

### Load and Compare
```python
from comparison import ComparisonTool, ComparisonVisualizer

# Load experiments
comp = ComparisonTool('./results')
comp.load_experiments()

# Compute statistics
stats = comp.compute_statistics()

# Print detailed report
comp.print_detailed_report()

# Print rankings
comp.print_rankings()

# Print analysis
comp.print_analysis()
```

### Generate Visualizations
```python
# Prepare experiments for visualization
experiments = {}
for exp_name, data in comp.experiments.items():
    algo = data['algorithm']
    if algo not in experiments:
        experiments[algo] = data['metrics']

# Create all comparison plots
viz = ComparisonVisualizer()
viz.plot_all_comparisons(experiments, comp.stats, baseline='FedAvg')
```

### Export Results
```python
# Export as CSV
comp.export_csv('comparison_stats.csv')

# Export as text table
comp.export_comparison_table('comparison_table.txt')

# Export as DataFrame
df = comp.create_dataframe()
```

### Find Best Algorithm
```python
# Best by accuracy
best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
print(f"Best: {best_algo} with {best_acc:.4f} accuracy")

# Best by convergence speed
best_algo, best_rounds = comp.get_best_algorithm('convergence_round_95')
print(f"Fastest: {best_algo} in {best_rounds} rounds")

# Get all rankings
for rank, (algo, acc) in enumerate(comp.get_ranking('best_accuracy'), 1):
    print(f"{rank}. {algo}: {acc:.4f}")
```

## Features

### 1. Comprehensive Statistics

For each algorithm:
- Best accuracy achieved
- Final accuracy (at last round)
- Average accuracy (across experiment)
- Convergence speed (rounds to 95% of best)
- Loss metrics (average and final)
- Accuracy improvement (final - initial)
- Number of experiments

### 2. Algorithm Rankings

Rank algorithms by:
- Best accuracy (higher is better)
- Final accuracy (higher is better)  
- Convergence speed (lower is better)
- Accuracy improvement (higher is better)
- Average loss (lower is better)

### 3. Strengths & Weaknesses Analysis

Automatically identifies:
- What each algorithm does best
- Where it falls short
- Comparative rankings on each metric
- Overall performance profile

### 4. Visualizations

**5 comparison plot types:**
1. **Accuracy comparison** - All algorithms' accuracy curves
2. **Loss comparison** - Test loss over rounds
3. **Metrics bar charts** - Side-by-side metric comparison
4. **Speedup analysis** - Convergence speedup relative to baseline
5. **Radar chart** - Multi-dimensional performance profile

### 5. Data Export

- **CSV format** - Load into Excel, Python, R
- **Text tables** - Copy into reports/presentations
- **pandas DataFrame** - Custom analysis in Python

## API Reference

### ComparisonTool

```python
tool = ComparisonTool(results_dir='./results')

# Load experiments
tool.load_experiments(pattern='*_metrics.json')
tool.load_specific(filepath, name='custom_name')

# Compute statistics
stats = tool.compute_statistics()

# Queries
best_algo, value = tool.get_best_algorithm('best_accuracy')
ranking = tool.get_ranking('best_accuracy')
analysis = tool.identify_strengths_weaknesses()

# Export
df = tool.create_dataframe()
tool.export_csv(filepath)
tool.export_comparison_table(filepath)
summary = tool.get_comparison_summary()

# Print
tool.print_detailed_report()
tool.print_rankings()
tool.print_analysis()
```

### ComparisonVisualizer

```python
viz = ComparisonVisualizer(figsize=(14, 10))

# Individual plots
viz.plot_accuracy_comparison(experiments)
viz.plot_loss_comparison(experiments)
viz.plot_metrics_comparison_bars(stats_dict)
viz.plot_speedup_analysis(stats_dict, baseline='FedAvg')
viz.plot_convergence_radar(stats_dict)

# All at once
viz.plot_all_comparisons(experiments, stats_dict, baseline='FedAvg')
```

## Output Examples

### Console Output
```
================================================================================
FEDERATED LEARNING ALGORITHM COMPARISON REPORT
================================================================================

SUMMARY METRICS
────────────────────────────────────────────────────────────────────────────────
Algorithm            Best Acc        Final Acc      Convergence    
────────────────────────────────────────────────────────────────────────────────
FedAvg               0.9543          0.9543         200            
FedAMD               0.9621          0.9621         156            
SCAFFOLD             0.9489          0.9489         200            
────────────────────────────────────────────────────────────────────────────────
```

### Generated Plots (in results/comparison_plots/)
```
accuracy_comparison.png           - All algorithms' accuracy curves
loss_comparison.png               - Test loss comparison
metrics_comparison_bars.png       - 4-panel metric comparison
speedup_vs_FedAvg.png            - Convergence speedup analysis
convergence_radar.png            - Multi-dimensional profile
```

### CSV Export
```
Algorithm,Best Accuracy,Final Accuracy,Convergence Round (95%),Improvement
FedAvg,0.9543,0.9543,200,0.5043
FedAMD,0.9621,0.9621,156,0.5121
SCAFFOLD,0.9489,0.9489,200,0.4989
```

## Typical Workflow

```python
from comparison import ComparisonTool, ComparisonVisualizer

# Step 1: Load
comp = ComparisonTool('./results')
comp.load_experiments()

# Step 2: Analyze
comp.print_detailed_report()
comp.print_rankings()
comp.print_analysis()

# Step 3: Visualize
exp_data = {d['algorithm']: d['metrics'] 
            for d in comp.experiments.values()}
viz = ComparisonVisualizer()
viz.plot_all_comparisons(exp_data, comp.stats)

# Step 4: Export
comp.export_csv('comparison.csv')
comp.export_comparison_table('comparison.txt')

# Step 5: Share insights
best, acc = comp.get_best_algorithm('best_accuracy')
print(f"Recommendation: Use {best} for best accuracy ({acc:.4f})")
```

## Common Use Cases

### Use Case 1: Choose Best Algorithm
```python
best_algo, _ = comp.get_best_algorithm('best_accuracy')
print(f"Recommended algorithm: {best_algo}")
```

### Use Case 2: Compare Convergence Speed
```python
rankings = comp.get_ranking('convergence_round_95')
for rank, (algo, rounds) in enumerate(rankings, 1):
    print(f"{rank}. {algo}: {rounds} rounds")
```

### Use Case 3: Generate Comparison Table for Paper
```python
comp.print_detailed_report()
comp.export_comparison_table('table.txt')
viz.plot_all_comparisons(...)
```

### Use Case 4: Analyze Hyperparameter Impact
```python
# Run same algorithm with different LRs
# Load all and compare
comp.load_experiments()
comp.print_rankings()  # See which LR works best
```

### Use Case 5: Identify Algorithm Strengths
```python
comp.print_analysis()  # Shows what each algorithm excels at
```

## File Structure

```
comparison/
├── __init__.py              - Module exports
├── tool.py                  - ComparisonTool class (600+ lines)
└── visualize.py             - ComparisonVisualizer (400+ lines)

results/
├── algorithm1_metrics.json
├── algorithm2_metrics.json
├── comparison_stats.csv     - Exported statistics
├── comparison_table.txt     - Text comparison table
└── comparison_plots/
    ├── accuracy_comparison.png
    ├── loss_comparison.png
    ├── metrics_comparison_bars.png
    ├── speedup_vs_*.png
    └── convergence_radar.png
```

## Supported Metrics for Comparison

- `best_accuracy` - Peak accuracy achieved
- `final_accuracy` - Accuracy at last round
- `avg_accuracy` - Average across experiment
- `convergence_round_95` - Rounds to 95% of best
- `improvement` - Final minus initial accuracy
- `avg_loss` - Average test loss
- `final_loss` - Test loss at last round

## Tips & Tricks

1. **Fair comparison**: Use same number of rounds (same T parameter)
2. **Statistical rigor**: Run multiple seeds for robustness
3. **Consistent naming**: Name experiments with algorithm name
4. **Baseline comparison**: Specify baseline for speedup analysis
5. **Export for sharing**: CSV format great for collaborators
6. **Custom analysis**: Use DataFrame for flexibility

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No experiments loaded | Check files are `*_metrics.json` in results/ directory |
| Empty tables | Ensure ComparisonTool.compute_statistics() was called |
| Plots have no data | Verify experiments have test_acc/test_loss fields |
| Rankings look wrong | Check if metric is "lower is better" vs "higher is better" |

## Requirements

- matplotlib (for plots)
- pandas (for DataFrame export)
- numpy (for statistics)
- json (standard library)

All already in project requirements.txt ✓

## Related Tools

- **MetricsTracker** (visualization/metrics.py) - Track single experiment
- **ResultsVisualizer** (visualization/plots.py) - Plot single experiment
- **ExperimentComparison** (visualization/metrics.py) - Basic comparison

## See Also

- [COMPARISON_GUIDE.md](COMPARISON_GUIDE.md) - Detailed usage guide
- [examples_comparison.py](examples_comparison.py) - 12 working examples
- [VISUALIZATION_README.md](VISUALIZATION_README.md) - Related visualization tools

---

**Ready to compare your algorithms!** 🚀
