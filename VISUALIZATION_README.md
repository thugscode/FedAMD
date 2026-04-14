# Results Visualization Module

A comprehensive metrics tracking and visualization system for federated learning experiments, designed for the FedAMD framework.

## Overview

This module provides:

- **MetricsTracker**: Real-time tracking of training metrics (accuracy, loss, communication rounds)
- **ResultsVisualizer**: Beautiful plots for convergence, accuracy, loss, and efficiency analysis
- **ExperimentComparison**: Compare multiple algorithms side-by-side
- **Data Export**: Save metrics to JSON and CSV for further analysis

## Features

### 📊 Metrics Tracked
- Test and training accuracy
- Test and training loss
- Number of participating clients per round
- Communication costs
- Convergence statistics (best accuracy, convergence rounds)

### 📈 Visualization Types

1. **Accuracy Curves** - Test vs train accuracy over communication rounds
2. **Loss Curves** - Test vs train loss trends
3. **Convergence Analysis** - Best accuracy point and 95% convergence round highlighted
4. **Communication Efficiency** - Accuracy progress + client participation patterns
5. **Algorithm Comparison** - Side-by-side comparison of multiple experiments

### 💾 Data Management
- Save metrics to JSON (human-readable + structured)
- Export to CSV for spreadsheet analysis
- Load and analyze previous experiments
- Automatic experiment naming with timestamps

## Installation

The module is self-contained. Just ensure you have the required packages:

```bash
pip install matplotlib numpy scipy
# (Already in your requirements.txt)
```

## Quick Start

### Basic Usage

```python
from visualization import MetricsTracker, ResultsVisualizer

# Initialize tracker
tracker = MetricsTracker(experiment_name="FedAvg_exp1")

# Log configuration
tracker.log_config(
    method="FedAvg",
    dataset="FMNIST",
    num_clients=20,
    communication_rounds=200
)

# In your training loop, after each validation:
for round in range(num_rounds):
    # ... training code ...
    test_loss, test_acc = validate(model)
    
    # Log metrics
    tracker.log_round(
        round_num=round,
        test_loss=test_loss,
        test_acc=test_acc,
        num_clients=len(selected_clients)
    )

# Save and visualize
tracker.save_json()
tracker.save_csv()
tracker.print_summary()

visualizer = ResultsVisualizer()
visualizer.plot_all(tracker.metrics, experiment_name="FedAvg_exp1")
```

### Output Files

After running, you'll get:
```
results/
├── FedAvg_exp1_metrics.json      # Full metrics in JSON
├── FedAvg_exp1_metrics.csv       # Metrics in CSV
└── plots/
    ├── accuracy_FedAvg_exp1.png
    ├── loss_FedAvg_exp1.png
    ├── convergence_FedAvg_exp1.png
    └── efficiency_FedAvg_exp1.png
```

## Integration with Existing Code

### Option 1: Minimal Integration (3 lines)

Add to `main_fmnist.py`:

```python
from visualization import MetricsTracker, ResultsVisualizer

# At start of run() function:
tracker = MetricsTracker(f"{args.method}_experiment")
tracker.log_config(method=args.method, dataset=args.dataset, num_clients=args.num_clients)

# After each check_accuracy() call in training loop:
tracker.log_round(t, test_loss=test_loss, test_acc=test_acc, num_clients=len(part_list))

# After training completes:
tracker.save_json()
ResultsVisualizer().plot_all(tracker.metrics, tracker.experiment_name)
```

### Option 2: Full Integration

For complete tracking including training accuracy and loss, modify `algo/` files to return these metrics.

### Example: Comparing Algorithms

```python
from visualization import ExperimentComparison, ResultsVisualizer

# Load all saved experiments
comparator = ExperimentComparison(results_dir='./results')
comparator.load_all_experiments()

# Print comparison table
comparator.print_comparison()

# Visualize comparisons
experiments = {name: data['metrics'] for name, data in comparator.experiments.items()}
viz = ResultsVisualizer()
viz.plot_comparison(experiments, metric='test_acc')
viz.plot_comparison(experiments, metric='test_loss')
```

## API Reference

### MetricsTracker

```python
tracker = MetricsTracker(experiment_name="exp1", save_dir="./results")

# Configuration
tracker.log_config(method="FedAvg", dataset="FMNIST", ...)

# Logging metrics per round
tracker.log_round(
    round_num: int,           # Communication round number
    test_loss: float = None,  # Test loss
    test_acc: float = None,   # Test accuracy
    train_loss: float = None, # Training loss
    train_acc: float = None,  # Training accuracy
    num_clients: int = None,  # Num participating clients
    local_steps: int = None   # Local iterations
)

# Statistics
best_round, best_acc = tracker.get_best_accuracy()
convergence_round = tracker.get_convergence_round(threshold=0.95)
summary = tracker.summary()
tracker.print_summary()

# Export
tracker.save_json()  # Save to JSON
tracker.save_csv()   # Save to CSV
```

### ResultsVisualizer

```python
viz = ResultsVisualizer(figsize=(12, 8))

# Individual plots
viz.plot_accuracy_curves(metrics_dict, experiment_name="exp1", save=True)
viz.plot_loss_curves(metrics_dict, experiment_name="exp1", save=True)
viz.plot_convergence_analysis(metrics_dict, experiment_name="exp1", save=True)
viz.plot_communication_efficiency(metrics_dict, experiment_name="exp1", save=True)

# All plots at once
viz.plot_all(metrics_dict, experiment_name="exp1", save=True)

# Compare experiments
experiments = {
    "FedAvg": metrics_dict_1,
    "FedAdapt": metrics_dict_2,
    "SCAFFOLD": metrics_dict_3
}
viz.plot_comparison(experiments, metric='test_acc')
viz.plot_comparison(experiments, metric='test_loss')
```

### ExperimentComparison

```python
comp = ExperimentComparison(results_dir='./results')

# Load experiments
comp.load_experiment('path/to/metrics.json', name='FedAvg')
comp.load_all_experiments()

# Compare
comparison = comp.compare_algorithms()
comp.print_comparison()
```

## JSON Output Format

The JSON file contains:
```json
{
  "experiment": "FedAvg_exp1",
  "algorithm": "FedAvg",
  "config": {
    "method": "FedAvg",
    "dataset": "FMNIST",
    "num_clients": 20,
    ...
  },
  "metrics": {
    "rounds": [0, 1, 2, ...],
    "test_acc": [0.5, 0.6, 0.7, ...],
    "test_loss": [2.3, 1.8, 1.2, ...],
    "train_acc": [...],
    "train_loss": [...],
    "client_participation": [10, 10, 9, ...],
    ...
  },
  "best_accuracy": [150, 0.9543],
  "convergence_round": 45,
  "timestamp": "2024-04-14T10:30:45.123456"
}
```

## Advanced Usage

### Custom Analysis

```python
import json

# Load results
with open('results/FedAvg_metrics.json') as f:
    data = json.load(f)

metrics = data['metrics']
test_accs = [a for a in metrics['test_acc'] if a is not None]

# Compute custom metrics
convergence_speed = data['convergence_round']
final_accuracy = test_accs[-1]
improvement = test_accs[-1] - test_accs[0]

print(f"Convergence Speed: {convergence_speed} rounds")
print(f"Final Accuracy: {final_accuracy:.4f}")
print(f"Improvement: {improvement:.4f}")
```

### Batch Processing

```python
from pathlib import Path
from visualization import ResultsVisualizer
import json

# Process all experiments in a directory
results_dir = Path('./results')
viz = ResultsVisualizer()

for json_file in results_dir.glob('*_metrics.json'):
    with open(json_file) as f:
        data = json.load(f)
    
    exp_name = data['experiment']
    print(f"Processing {exp_name}...")
    viz.plot_all(data['metrics'], experiment_name=exp_name)
```

## Tips & Best Practices

1. **Consistent Naming**: Use descriptive experiment names including algorithm name and key hyperparameters
   - Good: `FedAvg_FMNIST_lr0.01_c10`
   - Bad: `exp1`

2. **Log Configuration Early**: Call `log_config()` at the start to capture experimental setup

3. **Regular Logging**: Call `log_round()` after each validation to capture complete trajectory

4. **Save Incrementally**: Consider saving metrics periodically for long-running experiments

5. **Organize Results**: Create subdirectories for different experiments or datasets

## Troubleshooting

**Q: Plots not showing/saving?**
- Check that `results/plots/` directory has write permissions
- Ensure matplotlib backend is configured correctly

**Q: Missing metrics in JSON?**
- Verify `log_round()` is called after each training round
- Check that metrics passed to `log_round()` are not None

**Q: Comparison plots show no data?**
- Ensure experiments are loaded with `load_all_experiments()`
- Check that JSON files have correct format

**Q: Memory issues with long training?**
- The module stores all metrics in memory; this is fine for ≤10,000 rounds
- For longer runs, consider periodic checkpointing

## Files Structure

```
visualization/
├── __init__.py              # Module exports
├── metrics.py               # MetricsTracker & ExperimentComparison
└── plots.py                 # ResultsVisualizer

examples_visualization.py     # Usage examples and templates

results/
├── *_metrics.json           # Experiment results (JSON)
├── *_metrics.csv            # Experiment results (CSV)
└── plots/
    ├── accuracy_*.png
    ├── loss_*.png
    ├── convergence_*.png
    ├── efficiency_*.png
    └── comparison_*.png
```

## Future Enhancements

Potential additions:
- Interactive web dashboard (Plotly/Dash)
- Real-time metric streaming during training
- Statistical significance testing
- Hyperparameter sensitivity analysis plots
- Communication efficiency metrics
- Convergence rate analysis

## License

Same as FedAMD project

## Questions?

See `examples_visualization.py` for detailed usage examples.
