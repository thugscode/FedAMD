# Visualization Module - Quick Reference

## 30-Second Quick Start

```python
from visualization import MetricsTracker, ResultsVisualizer

# Initialize tracker
tracker = MetricsTracker()
tracker.log_config(algorithm='FedAvg', num_clients=20)

# Log each round
for round_num in range(200):
    # ... training ...
    tracker.log_round(round_num, test_loss=loss, test_acc=acc, 
                     train_loss=tr_loss, train_acc=tr_acc, num_clients=20)

# Save & visualize
tracker.save_json()
tracker.save_csv()
viz = ResultsVisualizer()
viz.plot_all(tracker.metrics, 'experiment_name')
```

## Core Classes

### MetricsTracker
Main class for logging training metrics.

**Key Methods:**
- `log_config(**kwargs)` - Store experiment configuration
- `log_round(round_num, test_loss, test_acc, train_loss, train_acc, num_clients)` - Log per-round metrics
- `save_json(filepath)` - Export to JSON
- `save_csv(filepath)` - Export to CSV
- `get_best_accuracy()` - Returns (round, accuracy)
- `get_convergence_round(threshold=0.95)` - Convergence analysis
- `summary()` - Get statistics dict
- `print_summary()` - Pretty-print statistics

### ResultsVisualizer
Create publication-quality plots.

**Key Methods:**
- `plot_accuracy_curves(metrics_dict, name, save)` - Test vs train accuracy
- `plot_loss_curves(metrics_dict, name, save)` - Test vs train loss
- `plot_convergence_analysis(metrics_dict, name, save)` - Best accuracy + 95% line
- `plot_communication_efficiency(metrics_dict, name, save)` - 2-panel plot
- `plot_comparison(experiments_dict, metric, save)` - Multi-algorithm comparison
- `plot_all(metrics_dict, name, save)` - Generate all plots

### ExperimentComparison
Compare multiple experiments.

**Key Methods:**
- `load_experiment(filepath, name)` - Load single JSON
- `load_all_experiments()` - Auto-load all *_metrics.json
- `compare_algorithms()` - Return comparison dict
- `print_comparison()` - Print formatted table

## Typical Workflow

```python
# 1. Initialize and log
tracker = MetricsTracker()
tracker.log_config(algorithm='FedAvg', num_clients=20, num_rounds=200)

for round_num in range(num_rounds):
    # ... training ...
    tracker.log_round(round_num, test_loss, test_acc, train_loss, train_acc, num_clients=20)

# 2. Save
tracker.save_json()      # → ./results/experiment_timestamp_metrics.json
tracker.save_csv()       # → ./results/experiment_timestamp_metrics.csv

# 3. Visualize
viz = ResultsVisualizer()
viz.plot_all(tracker.metrics, 'FedAvg')  # → ./results/plots/

# 4. Compare (optional)
comp = ExperimentComparison()
comp.load_all_experiments()
comp.print_comparison()
```

## Output Metrics

### Per-Round Metrics
- `test_accuracy` - Model accuracy on test set
- `test_loss` - Loss on test set
- `train_accuracy` - Model accuracy on training
- `train_loss` - Loss on training set
- `num_clients` - Clients participating this round
- `communication_rounds` - Global round number

### Summary Metrics (from `summary()`)
- `best_accuracy` - Highest accuracy achieved
- `convergence_round_95` - Rounds to 95% of best
- `final_accuracy` - Accuracy at last round
- `final_loss` - Loss at last round
- `num_rounds` -Total rounds completed
- `avg_test_accuracy` - Average across all rounds

## Visualization Types

1. **Accuracy Curves** - Test and train accuracy over time
2. **Loss Curves** - Test and train loss over time
3. **Convergence Analysis** - Identifies when convergence achieved
4. **Communication Efficiency** - Accuracy trends with client participation
5. **Comparison** - Multiple algorithms on one plot

## Supported Experiments

Expects JSON structure:
```json
{
  "experiment": "name",
  "algorithm": "FedAvg",
  "config": {...},
  "metrics": {
    "rounds": [1, 2, ...],
    "test_acc": [0.2, 0.3, ...],
    "test_loss": [2.3, 2.1, ...],
    "train_acc": [0.2, 0.3, ...],
    "train_loss": [2.3, 2.1, ...]
  }
}
```

## Common Use Cases

### 1. Track Single Experiment
```python
tracker = MetricsTracker('FedAvg_Run1')
for round in range(200):
    tracker.log_round(round, test_loss, test_acc, train_loss, train_acc)
tracker.save_json()
```

### 2. Visualize Results
```python
viz = ResultsVisualizer()
viz.plot_accuracy_curves(metrics_dict, 'FedAvg')
viz.plot_loss_curves(metrics_dict, 'FedAvg')
viz.plot_all(metrics_dict, 'FedAvg')
```

### 3. Get Convergence Info
```python
tracker = MetricsTracker()
# ... log metrics ...
best_round, best_acc = tracker.get_best_accuracy()
conv_round = tracker.get_convergence_round(0.95)
print(f"Converged in round {conv_round}")
```

### 4. Compare Multiple Experiments
```python
comp = ExperimentComparison()
comp.load_experiment('./results/fedavg_metrics.json', 'FedAvg')
comp.load_experiment('./results/fedadapt_metrics.json', 'FedAdapt')
comp.print_comparison()
```

## Output Files

When metrics are saved:
- `*_metrics.json` - Complete metrics with timestamps
- `*_metrics.csv` - Spreadsheet-compatible format

When plots are generated:
- `accuracy_curves.png` - Accuracy plot
- `loss_curves.png` - Loss plot
- `convergence_analysis.png` - Convergence plot
- `communication_efficiency.png` - Efficiency plot
- `comparison.png` - Algorithm comparison

## Interpretation Guide

### Convergence
- **Fast convergence**: Reaches 95% of best accuracy in <50 rounds
- **Medium convergence**: 50-150 rounds
- **Slow convergence**: >150 rounds

### Accuracy Plateau
- **Early plateau**: Reaches best accuracy before 100 rounds
- **Late plateau**: Reaches best accuracy after 100 rounds

### Communication Efficiency
- **High efficiency**: Quick accuracy improvement per round
- **Low efficiency**: Slow improvement, more rounds needed

## Troubleshooting

**No plots generated:**
- Check: `mkdir -p ./results/plots`
- Ensure matplotlib installed: `pip install matplotlib`

**Missing metrics:**
- Ensure all fields logged in `log_round()`
- Check: None values in metrics arrays

**JSON files not created:**
- Check: `./results/` directory exists
- Verify: `tracker.save_json()` called

## API Reference

### MetricsTracker
```python
MetricsTracker(experiment_name=None, save_dir='./results')
.log_config(**kwargs) → None
.log_round(round_num, test_loss, test_acc, train_loss, train_acc, num_clients=None) → None
.save_json(filepath=None) → str
.save_csv(filepath=None) → str
.get_best_accuracy() → (int, float)
.get_convergence_round(threshold=0.95) → int
.summary() → Dict[str, Any]
.print_summary() → None
```

### ResultsVisualizer
```python
ResultsVisualizer(figsize=(12,8), style='seaborn-v0_8-darkgrid')
.plot_accuracy_curves(metrics_dict, name, save=True) → None
.plot_loss_curves(metrics_dict, name, save=True) → None
.plot_convergence_analysis(metrics_dict, name, save=True) → None
.plot_communication_efficiency(metrics_dict, name, save=True) → None
.plot_comparison(experiments_dict, metric, save=True) → None
.plot_all(metrics_dict, name, save=True) → None
```

### ExperimentComparison
```python
ExperimentComparison(results_dir='./results')
.load_experiment(filepath, name=None) → bool
.load_all_experiments(pattern='*_metrics.json') → int
.compare_algorithms() → Dict
.print_comparison() → None
```

## Advanced Usage

**Access raw metrics:**
```python
metrics = tracker.metrics
rounds = metrics['rounds']
accuracies = metrics['test_acc']
```

**Custom analysis:**
```python
stats = tracker.summary()
print(f"Best: {stats['best_accuracy']:.4f}")
print(f"Final: {stats['final_accuracy']:.4f}")
print(f"Converged: {stats['convergence_round_95']} rounds")
```

**Batch plot generation:**
```python
for algo in ['FedAvg', 'FedAdapt', 'SCAFFOLD']:
    comp.load_experiment(f'./results/{algo}_metrics.json', algo)
comp.print_comparison()
```

## Related Documentation

- [VISUALIZATION_README.md](VISUALIZATION_README.md) - Complete guide
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - How to integrate
- [examples_visualization.py](examples_visualization.py) - Working examples
- [ANALYSIS_TOOLKIT_OVERVIEW.md](ANALYSIS_TOOLKIT_OVERVIEW.md) - Toolkit overview
