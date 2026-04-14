# Visualization Module - Architecture Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR TRAINING SCRIPT                         │
│              (main_fmnist.py / main_emnist.py)                 │
│                                                                 │
│  for t in range(T):                                             │
│      loss, acc = train_and_validate()                           │
│      tracker.log_round(t, loss, acc)  ← Add 1 line             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────────┐
│         VISUALIZATION MODULE (visualization/)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐                                       │
│  │  MetricsTracker      │                                       │
│  ├──────────────────────┤                                       │
│  │ • log_round()        │ ← Collects metrics                   │
│  │ • log_config()       │                                       │
│  │ • save_json()        │ → JSON file                          │
│  │ • save_csv()         │ → CSV file                           │
│  │ • summary()          │ → Statistics                         │
│  └──────────────────────┘                                       │
│         │                                                       │
│         ├→ metrics.json                                         │
│         ├→ metrics.csv                                          │
│         │                                                       │
│         ↓                                                       │
│  ┌──────────────────────┐                                       │
│  │ ResultsVisualizer    │                                       │
│  ├──────────────────────┤                                       │
│  │ • plot_accuracy_curves()                                    │
│  │ • plot_loss_curves()                                        │
│  │ • plot_convergence()                                        │
│  │ • plot_efficiency()                                         │
│  │ • plot_comparison()                                         │
│  │ • plot_all()         │ ← Creates plots                      │
│  └──────────────────────┘                                       │
│         │                                                       │
│         ↓                                                       │
│  ┌──────────────────────┐                                       │
│  │ExperimentComparison  │                                       │
│  ├──────────────────────┤                                       │
│  │ • load_all_exps()    │ ← Load multiple JSON files           │
│  │ • compare()          │ → Comparison statistics              │
│  │ • print_comparison() │ → Comparison table                   │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────────┐
│              OUTPUT FILES (results/ directory)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  results/                                                       │
│  ├── FedAvg_metrics.json         (Full metrics JSON)            │
│  ├── FedAvg_metrics.csv          (Spreadsheet format)           │
│  ├── FedAdapt_metrics.json                                      │
│  ├── FedAdapt_metrics.csv                                       │
│  └── plots/                                                     │
│      ├── accuracy_FedAvg.png                                    │
│      ├── loss_FedAvg.png                                        │
│      ├── convergence_FedAvg.png                                 │
│      ├── efficiency_FedAvg.png                                  │
│      ├── accuracy_FedAdapt.png                                  │
│      ├── loss_FedAdapt.png                                      │
│      ├── convergence_FedAdapt.png                               │
│      ├── efficiency_FedAdapt.png                                │
│      ├── comparison_test_acc.png   (Algorithm comparison)       │
│      └── comparison_test_loss.png                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────┐
│  Training Loop          │
│                         │
│  Round 0: loss, acc     │───┐
│  Round 1: loss, acc     │   │
│  Round 2: loss, acc     │   │
│  ...                    │   │
│  Round 200: loss, acc   │   │
└─────────────────────────┘   │
                               │
                               ↓
                    ┌──────────────────────┐
                    │  MetricsTracker      │
                    │  .log_round()        │
                    └──────────────────────┘
                               │
                    ┌──────────┴──────────┬────────────┐
                    │                     │            │
                    ↓                     ↓            ↓
          ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐
          │ Internal Storage │  │   JSON Export    │  │   CSV Export    │
          │  (in memory)     │  │  (JSON file)     │  │  (CSV file)     │
          └──────────────────┘  └──────────────────┘  └─────────────────┘
                    │
                    ↓
          ┌──────────────────┐
          │ResultsVisualizer │
          │ .plot_all()      │
          └──────────────────┘
                    │
           ┌────────┼────────┬──────────┬──────────┐
           ↓        ↓        ↓          ↓          ↓
         ┌──┐    ┌──┐    ┌───┐     ┌───┐      ┌───┐
         │ac│    │lo│    │co│     │ef│     │co│
         │cu│    │ss│    │nv│     │fi│     │mp│
         │racy│  │  │    │gr│     │cy│     │ar│
         └──┘    └──┘    └───┘     └───┘      └───┘
```

## Integration Points in main_fmnist.py

```python
# main_fmnist.py

# ========== POINT 1: Import ==========
from visualization import MetricsTracker, ResultsVisualizer


def run(workers, model, args, ...):
    
    # ========== POINT 2: Initialize Tracker ==========
    tracker = MetricsTracker(f"{args.method}_{args.dataset}")
    tracker.log_config(
        method=args.method,
        dataset=args.dataset,
        num_clients=args.num_clients,
        ...
    )
    
    # ========== POINT 3: Training Loop ==========
    for t in range(args.T):
        # ... existing training code ...
        
        # After validation:
        test_loss, test_acc = check_accuracy(...)
        
        # ========== POINT 4: Log Metrics ==========
        tracker.log_round(t, test_loss=test_loss, test_acc=test_acc, 
                         num_clients=len(part_list))
        
    # ========== POINT 5: Save & Visualize ==========
    tracker.save_json()
    tracker.save_csv()
    tracker.print_summary()
    
    visualizer = ResultsVisualizer()
    visualizer.plot_all(tracker.metrics, tracker.experiment_name)
```

## Class Hierarchy

```
┌─────────────────────────────────┐
│   MetricsTracker                │
├─────────────────────────────────┤
│ Properties:                     │
│ - experiment_name               │
│ - metrics (dict)                │
│ - config (dict)                 │
│ - algorithm                     │
│                                 │
│ Methods:                        │
│ + log_config(**kwargs)          │
│ + log_round(...)                │
│ + add_communication_cost(...)   │
│ + get_best_accuracy()           │
│ + get_convergence_round()       │
│ + summary()                     │
│ + print_summary()               │
│ + save_json()                   │
│ + save_csv()                    │
└─────────────────────────────────┘


┌─────────────────────────────────┐
│   ResultsVisualizer             │
├─────────────────────────────────┤
│ Properties:                     │
│ - figsize                       │
│ - colors                        │
│ - save_dir                      │
│                                 │
│ Methods:                        │
│ + plot_accuracy_curves()        │
│ + plot_loss_curves()            │
│ + plot_convergence_analysis()   │
│ + plot_communication_efficiency│
│ + plot_comparison()             │
│ + plot_all()                    │
└─────────────────────────────────┘


┌─────────────────────────────────┐
│   ExperimentComparison          │
├─────────────────────────────────┤
│ Properties:                     │
│ - results_dir                   │
│ - experiments (dict)            │
│                                 │
│ Methods:                        │
│ + load_experiment()             │
│ + load_all_experiments()        │
│ + compare_algorithms()          │
│ + print_comparison()            │
└─────────────────────────────────┘
```

## JSON Output Structure

```json
{
  "experiment": "FedAvg_FMNIST_20240414_103045",
  "algorithm": "FedAvg",
  "config": {
    "method": "FedAvg",
    "dataset": "FMNIST",
    "num_clients": 20,
    "num_participants": 10,
    "communication_rounds": 200,
    "local_epochs": 5,
    "learning_rate": 0.01,
    "batch_size": 64,
    "non_iid": true,
    "dirichlet_alpha": 0.1
  },
  "metrics": {
    "rounds": [0, 1, 2, ..., 199],
    "test_loss": [2.3, 1.8, 1.2, ..., 0.24],
    "test_acc": [0.45, 0.58, 0.72, ..., 0.95],
    "train_loss": [2.5, 1.9, 1.3, ..., 0.20],
    "train_acc": [0.40, 0.55, 0.70, ..., 0.96],
    "client_participation": [10, 10, 9, ..., 10],
    "local_updates": [5, 5, 5, ..., 5],
    "communication_cost": []
  },
  "best_accuracy": [156, 0.9543],
  "convergence_round": 45,
  "timestamp": "2024-04-14T10:30:45.123456"
}
```

## Workflow for Algorithm Comparison

```
┌──────────────────────────────────────────────────────────────┐
│ Run Multiple Algorithms (Sequential)                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  $ python main_fmnist.py --method FedAvg --T 200            │
│  ✓ Generates: FedAvg_FMNIST_metrics.json                   │
│                                                              │
│  $ python main_fmnist.py --method FedAdapt --T 200          │
│  ✓ Generates: FedAdapt_FMNIST_metrics.json                 │
│                                                              │
│  $ python main_fmnist.py --method SCAFFOLD --T 200          │
│  ✓ Generates: SCAFFOLD_FMNIST_metrics.json                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Load and Compare (ExperimentComparison)                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  comp = ExperimentComparison()                              │
│  comp.load_all_experiments()   # Load all .json files       │
│  comp.print_comparison()       # Print table                │
│                                                              │
│  Output table:                                              │
│  ┌────────────┬─────────────┬──────────────┬────────────┐  │
│  │ Algorithm  │ Best Acc    │ Final Acc    │ Rounds     │  │
│  ├────────────┼─────────────┼──────────────┼────────────┤  │
│  │ FedAvg     │ 0.9543      │ 0.9543       │ 200        │  │
│  │ FedAdapt   │ 0.9621      │ 0.9521       │ 200        │  │
│  │ SCAFFOLD   │ 0.9489      │ 0.9412       │ 200        │  │
│  └────────────┴─────────────┴──────────────┴────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ Create Comparison Plots (ResultsVisualizer)                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  exps = {...}  # {exp_name: metrics}                        │
│  viz = ResultsVisualizer()                                  │
│  viz.plot_comparison(exps, metric='test_acc')              │
│  viz.plot_comparison(exps, metric='test_loss')             │
│                                                              │
│  Output:                                                    │
│  ✓ comparison_test_acc.png   (All algorithms on one plot)   │
│  ✓ comparison_test_loss.png  (All algorithms on one plot)   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────────┐
                    │ Analysis & Insights│
                    ├───────────────────┤
                    │ • Which is faster │
                    │ • Which converges │
                    │ • Trade-offs      │
                    │ • Statistical     │
                    │   significance    │
                    └───────────────────┘
```

## File Organization

```
FedAMD/
│
├── visualization/                  ← NEW MODULE
│   ├── __init__.py
│   ├── metrics.py                  (263 lines)
│   └── plots.py                    (323 lines)
│
├── algo/                           (EXISTING)
│   ├── fedavg.py
│   ├── fedadapt.py
│   ├── ...
│
├── data_model/                     (EXISTING)
│
├── main_fmnist.py                  (EXISTING - modified +9 lines)
├── main_emnist.py                  (EXISTING - can modify same way)
│
├── VISUALIZATION_README.md         ← NEW DOCS
├── INTEGRATION_GUIDE.md            ← NEW DOCS
├── QUICK_REFERENCE.md              ← NEW DOCS
├── BUILD_SUMMARY.md                ← NEW DOCS
├── ARCHITECTURE.md                 ← You are here
│
├── examples_visualization.py        ← NEW EXAMPLES
│
└── results/                        ← OUTPUT DIRECTORY
    ├── FedAvg_metrics.json
    ├── FedAvg_metrics.csv
    ├── FedAdapt_metrics.json
    ├── FedAdapt_metrics.csv
    │
    └── plots/
        ├── accuracy_FedAvg.png
        ├── loss_FedAvg.png
        ├── convergence_FedAvg.png
        ├── efficiency_FedAvg.png
        ├── accuracy_FedAdapt.png
        ├── loss_FedAdapt.png
        │
        └── comparison_*.png
```

## Timing & Performance

```
┌────────────────────────────────────────────────────────────┐
│ Performance Metrics (per 200 round experiment)            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Memory usage:   ~1KB per metric × 200 rounds = 10KB       │
│ JSON save:      ~100ms                                    │
│ CSV save:       ~100ms                                    │
│ Plot generation:~5 sec (4 plots)                          │
│ Total overhead: <0.1% of typical training time            │
│                                                            │
│ Negligible impact on training performance!                │
└────────────────────────────────────────────────────────────┘
```

## Extension Points

```
Future enhancements can be added at these points:

1. Custom Metrics
   └─ TrackerTracker.add_custom_metric(name, value)

2. New Plot Types
   └─ ResultsVisualizer.plot_custom()

3. Export Formats
   └─ MetricsTracker.save_parquet()
   └─ MetricsTracker.save_xlsx()

4. Statistical Analysis
   └─ ExperimentComparison.statistical_test()

5. Dashboard Generation
   └─ ResultsVisualizer.generate_html_dashboard()
```

This modular architecture makes it easy to add features without breaking existing code!

---

*Visualization Module Architecture Guide | April 2024*
