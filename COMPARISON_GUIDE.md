# Experiment Comparison Tool - Complete Guide

## Overview

The **Experiment Comparison Tool** allows you to easily compare different federated learning algorithms (FedAvg, FedAMD, SCAFFOLD, etc.) side-by-side with:

- **Detailed metrics tables** - Compare best accuracy, convergence speed, loss, improvement
- **Visual comparisons** - Accuracy/loss curves, bar charts, speedup analysis, radar charts
- **Statistical analysis** - Rankings, strengths/weaknesses, insights
- **CSV export** - Load into Excel or other tools for further analysis
- **Text reports** - Formatted comparison reports

## Quick Start

### Load and Compare Experiments

```python
from comparison import ComparisonTool, ComparisonVisualizer

# Load all experiments
comp = ComparisonTool('./results')
num_loaded = comp.load_experiments()
print(f"Loaded {num_loaded} experiments")

# Compute statistics
stats = comp.compute_statistics()

# Print detailed report
comp.print_detailed_report()

# Print rankings
comp.print_rankings()

# Print analysis
comp.print_analysis()
```

### Generate Comparison Visualizations

```python
from comparison import ComparisonVisualizer

# Create visualizer
viz = ComparisonVisualizer()

# Load experiments for visualization
experiments = {}
for exp_name, data in comp.experiments.items():
    experiments[data['algorithm']] = data['metrics']

# Generate all plots
viz.plot_all_comparisons(experiments, comp.stats, baseline='FedAvg')
```

### Export Results

```python
# Export as CSV
comp.export_csv('./results/comparison_stats.csv')

# Export as text table
comp.export_comparison_table('./results/comparison_table.txt')
```

## Key Features

### 1. Detailed Statistics

```python
stats = comp.compute_statistics()

for algo_name, stat in stats.items():
    print(f"{algo_name}:")
    print(f"  Best Accuracy: {stat.best_accuracy:.4f}")
    print(f"  Final Accuracy: {stat.final_accuracy:.4f}")
    print(f"  Convergence @ 95%: {stat.convergence_round_95} rounds")
    print(f"  Improvement: {stat.improvement:.4f}")
```

### 2. Algorithm Rankings

```python
# Get rankings for different metrics
acc_ranking = comp.get_ranking('best_accuracy')
conv_ranking = comp.get_ranking('convergence_round_95')
imp_ranking = comp.get_ranking('improvement')

for rank, (algo, value) in enumerate(acc_ranking, 1):
    print(f"{rank}. {algo}: {value:.4f}")
```

### 3. Best Algorithm Detection

```python
# Best by accuracy
best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
print(f"Best accuracy: {best_algo} ({best_acc:.4f})")

# Best by convergence speed
best_algo, best_rounds = comp.get_best_algorithm('convergence_round_95')
print(f"Fastest convergence: {best_algo} ({best_rounds} rounds)")
```

### 4. Strengths & Weaknesses

```python
comp.print_analysis()

# Or get analysis dictionary
analysis = comp.identify_strengths_weaknesses()
for algo, info in analysis.items():
    print(f"{algo}:")
    print(f"  Strengths: {info['strengths']}")
    print(f"  Weaknesses: {info['weaknesses']}")
```

### 5. Comparison Summary

```python
summary = comp.get_comparison_summary()

print(f"Best by accuracy: {summary['best_by_accuracy']}")
print(f"Best by convergence: {summary['best_by_convergence_speed']}")
print(f"Best by improvement: {summary['best_by_improvement']}")
```

## Visualization Types

### 1. Accuracy Comparison
```python
viz.plot_accuracy_comparison(experiments)
```
- All algorithms on one plot
- Shows convergence trajectories
- Easy to see which reaches highest accuracy fastest

### 2. Loss Comparison
```python
viz.plot_loss_comparison(experiments)
```
- Test loss over rounds
- Identify overfitting (train vs test divergence)
- Compare optimizer effectiveness

### 3. Metrics Bar Charts
```python
viz.plot_metrics_comparison_bars(comp.stats)
```
- Best accuracy achieved
- Final accuracy
- Convergence speed (rounds to 95%)
- Accuracy improvement

### 4. Speedup Analysis
```python
viz.plot_speedup_analysis(comp.stats, baseline='FedAvg')
```
- Convergence speedup relative to baseline
- Shows how much faster/slower each algorithm is
- Useful for showing efficiency gains

### 5. Radar Chart
```python
viz.plot_convergence_radar(comp.stats)
```
- Multi-dimensional performance profile
- Peak accuracy, convergence speed, stability
- Visual profile of algorithm strengths

## Complete Workflow Example

```python
from comparison import ComparisonTool, ComparisonVisualizer

# Step 1: Load experiments
comp = ComparisonTool('./results')
comp.load_experiments()

# Step 2: Compute statistics
stats = comp.compute_statistics()

# Step 3: Print reports
comp.print_detailed_report()
comp.print_rankings()
comp.print_analysis()

# Step 4: Export data
comp.export_csv('comparison_stats.csv')
comp.export_comparison_table('comparison_table.txt')

# Step 5: Visualize
viz = ComparisonVisualizer()

# Prepare data
experiments = {}
for exp_name, data in comp.experiments.items():
    algo = data['algorithm']
    if algo not in experiments:
        experiments[algo] = data['metrics']

# Generate plots
viz.plot_all_comparisons(experiments, comp.stats, baseline='FedAvg')

# Step 6: Get insights
print("\n=== KEY INSIGHTS ===")
best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
print(f"Best accuracy: {best_algo} with {best_acc:.4f}")

print("\nAccuracy Rankings:")
for rank, (algo, acc) in enumerate(comp.get_ranking('best_accuracy'), 1):
    print(f"  {rank}. {algo}: {acc:.4f}")

print("\nConvergence Rankings:")
for rank, (algo, rounds) in enumerate(comp.get_ranking('convergence_round_95'), 1):
    print(f"  {rank}. {algo}: {rounds} rounds")
```

## Output Examples

### Console Output

```
================================================================================
FEDERATED LEARNING ALGORITHM COMPARISON REPORT
================================================================================

Dataset: Multiple experiments
Total experiments: 3
Algorithms compared: 3

SUMMARY METRICS
--------------------------------------------------------------------------------
Algorithm            Best Acc        Final Acc      Convergence    
--------------------------------------------------------------------------------
FedAvg               0.9543          0.9543         200            
FedAMD               0.9621          0.9621         156            
SCAFFOLD             0.9489          0.9489         200            
--------------------------------------------------------------------------------


DETAILED STATISTICS PER ALGORITHM
================================================================================

FedAvg
--------------------------------------------------------------------------------
  Number of experiments:        1
  Best accuracy:                0.9543
  Final accuracy:               0.9543
  Average accuracy:             0.9543
  Accuracy improvement:         0.5043
  Best achieved at round:       200
  Convergence at 95%:           200 rounds
  Average loss:                 0.2134
  Final loss:                   0.1234
  Average total rounds:         200

================================================================================
ALGORITHM RANKINGS
================================================================================

Best Accuracy (Higher is Better)
------------------------------------------------------------
  1. FedAMD                 0.9621
  2. FedAvg                 0.9543
  3. SCAFFOLD               0.9489

Convergence Speed (Lower is Better)
------------------------------------------------------------
  1. FedAMD                    156
  2. FedAvg                    200
  3. SCAFFOLD                  200

================================================================================
ALGORITHM ANALYSIS: STRENGTHS & WEAKNESSES
================================================================================

FedAvg
--------------------------------------------------------------------------------
  Strengths:
    ✓ Balanced performance
  Weaknesses:
    ✗ None identified
  Rankings:
    - Best Accuracy:    #2
    - Convergence:      #2
    - Improvement:      #1

FedAMD
--------------------------------------------------------------------------------
  Strengths:
    ✓ Highest accuracy
    ✓ Fastest convergence
  Weaknesses:
    ✗ None identified
  Rankings:
    - Best Accuracy:    #1
    - Convergence:      #1
    - Improvement:      #2

SCAFFOLD
--------------------------------------------------------------------------------
  Strengths:
    ✓ Balanced performance
  Weaknesses:
    ✗ Lowest accuracy
    ✗ Slowest convergence
  Rankings:
    - Best Accuracy:    #3
    - Convergence:      #3
    - Improvement:      #3
```

### Generated Plots

1. **accuracy_comparison.png** - All algorithms' accuracy curves
2. **loss_comparison.png** - Test loss comparison
3. **metrics_comparison_bars.png** - 4-panel comparison (best acc, final acc, convergence, improvement)
4. **speedup_vs_FedAvg.png** - Speedup relative to baseline
5. **convergence_radar.png** - Multi-dimensional performance profile

### CSV Output

```
Algorithm,Num Experiments,Best Accuracy,Final Accuracy,Avg Accuracy,Best Round,Convergence Round (95%),Avg Loss,Final Loss,Total Rounds,Improvement
FedAvg,1,0.9543,0.9543,0.9543,200,200,0.2134,0.1234,200,0.5043
FedAMD,1,0.9621,0.9621,0.9621,156,156,0.1890,0.1087,200,0.5121
SCAFFOLD,1,0.9489,0.9489,0.9489,200,200,0.2567,0.1456,200,0.4989
```

## API Reference

### ComparisonTool

```python
tool = ComparisonTool(results_dir='./results')

# Loading
tool.load_experiments(pattern='*_metrics.json')  # Load all matching
tool.load_specific(filepath, name='custom_name')  # Load one

# Statistics
stats = tool.compute_statistics()  # Compute all stats
df = tool.create_dataframe()  # Get as DataFrame

# Queries
best_algo, value = tool.get_best_algorithm('best_accuracy')
ranking = tool.get_ranking('best_accuracy')
analysis = tool.identify_strengths_weaknesses()

# Export
tool.export_csv(filepath)  # Export to CSV
tool.export_comparison_table(filepath)  # Export text table
summary = tool.get_comparison_summary()  # Get summary dict

# Print
tool.print_detailed_report()
tool.print_rankings()
tool.print_analysis()
```

### ComparisonVisualizer

```python
viz = ComparisonVisualizer(figsize=(14, 10))

# Individual plots
viz.plot_accuracy_comparison(experiments, save=True)
viz.plot_loss_comparison(experiments, save=True)
viz.plot_metrics_comparison_bars(stats_dict, save=True)
viz.plot_speedup_analysis(stats_dict, baseline='FedAvg', save=True)
viz.plot_convergence_radar(stats_dict, save=True)

# All at once
viz.plot_all_comparisons(experiments, stats_dict, baseline='FedAvg')
```

## Metrics Explained

| Metric | Meaning | Lower/Higher Better |
|--------|---------|-------------------|
| Best Accuracy | Highest accuracy achieved | Higher |
| Final Accuracy | Accuracy at last round | Higher |
| Avg Accuracy | Average across experiment | Higher |
| Best Round | At which round best accuracy reached | Lower |
| Convergence @ 95% | Rounds to reach 95% of best accuracy | Lower |
| Avg Loss | Average test loss | Lower |
| Final Loss | Test loss at last round | Lower |
| Improvement | Final - Initial accuracy | Higher |

## Common Use Cases

### 1. Choose Best Algorithm
```python
best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
print(f"Use {best_algo} for highest accuracy: {best_acc:.4f}")
```

### 2. Find Fastest Converging
```python
best_algo, best_rounds = comp.get_best_algorithm('convergence_round_95')
print(f"{best_algo} converges fastest in {best_rounds} rounds")
```

### 3. Compare Communication Cost
- Algorithms with lower convergence_round_95 need fewer communication rounds
- Multiply by local_epochs to get total gradient computations
- Compare vs. algorithm accuracy improvement

### 4. Generate Report for Paper
```python
comp.print_detailed_report()  # For main text
comp.export_comparison_table('table.txt')  # For table
viz.plot_all_comparisons(...)  # For figures
```

### 5. Identify Hyperparameter Impact
- Run same algorithm with different hyperparameters
- Load all experiments
- Compare to see which hyperparameters work best

## Tips & Best Practices

1. **Consistent naming**: Use algorithm name in experiment name
   - Good: `FedAvg_FMNIST_lr0.01`
   - Bad: `exp1_exp2_exp3`

2. **Fair comparison**: Same number of rounds (T parameter)

3. **Statistical significance**: Run multiple seeds for robustness

4. **Normalize metrics**: Different datasets may have different scales

5. **Document baselines**: Always note your baseline algorithm

6. **Track hyperparameters**: Save config in JSON for reproducibility

## Files Structure

```
comparison/
├── __init__.py         # Module exports
├── tool.py            # ComparisonTool class (600+ lines)
└── visualize.py       # ComparisonVisualizer class (400+ lines)

results/
├── FedAvg_metrics.json
├── FedAMD_metrics.json
├── SCAFFOLD_metrics.json
├── comparison_table.txt        # Comparison tables
├── comparison_stats.csv        # CSV export
└── comparison_plots/           # Visualizations
    ├── accuracy_comparison.png
    ├── loss_comparison.png
    ├── metrics_comparison_bars.png
    ├── speedup_vs_FedAvg.png
    └── convergence_radar.png
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No experiments loaded | Check file format is `*_metrics.json` in results/ |
| Empty comparison tables | Ensure experiments have computed statistics |
| Plots not showing labels | Check algorithm names in experiment JSON |
| CSV empty | Verify statistics computed before export |

## Future Enhancements

- Interactive web dashboard
- Statistical significance testing (t-tests)
- Hyperparameter sensitivity analysis
- Automated best algorithm recommendation
- Performance prediction models

---

**Ready to compare your algorithms!** 🚀
