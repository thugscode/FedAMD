# Integration Example: Modified main_fmnist.py with Visualization
# This shows the minimal changes needed to add metrics tracking

# NOTE: This is a TEMPLATE showing what to modify in main_fmnist.py
# It shows the key changes to add visualization tracking with ~20 lines of code

"""
INTEGRATION STEPS:

1. Add import at the top of main_fmnist.py:
   from visualization import MetricsTracker, ResultsVisualizer

2. In the run() function, add these 3 lines after initialization:
   tracker = MetricsTracker(f"{args.method}_{args.dataset}")
   tracker.log_config(method=args.method, dataset=args.dataset, num_clients=args.num_clients,
                      num_participants=args.num_part, lr=args.lr, batch_size=args.bsz)

3. In the training loop (after check_accuracy call), add:
   tracker.log_round(t, test_loss=test_loss, test_acc=test_acc, num_clients=len(part_list))

4. After training loop completes, add:
   tracker.save_json()
   tracker.save_csv()
   tracker.print_summary()
   visualizer = ResultsVisualizer()
   visualizer.plot_all(tracker.metrics, experiment_name=tracker.experiment_name)
"""


# ============ BEFORE (Original Code) ============

def run_original(workers, model, args, data_ratio_pairs, data_ratio_pairs_full_batch, test_data, cpu, gpu):
    """Original run function from main_fmnist.py"""
    worker_num = len(workers)
    model = model.cuda(gpu)
    
    hist_acc = []
    
    for t in range(args.T):  # Communication rounds
        # ... training code ...
        
        test_loss, test_acc = check_accuracy(t, test_loader, model, device)
        hist_acc.append(test_acc)
        
        print(f"Round {t}, Test Acc: {test_acc:.4f}")
    
    # Results stored only in hist_acc list


# ============ AFTER (With Visualization) ============

def run_with_visualization(workers, model, args, data_ratio_pairs, data_ratio_pairs_full_batch, test_data, cpu, gpu):
    """
    Modified run function showing minimal integration of visualization module.
    
    Changes:
    - 3 lines to initialize tracker
    - 1 line per round to log metrics  
    - 5 lines at end to save and visualize
    Total: ~9 lines added (very minimal!)
    """
    from visualization import MetricsTracker, ResultsVisualizer  # NEW: Add import
    
    worker_num = len(workers)
    model = model.cuda(gpu)
    
    # NEW: Initialize metrics tracker (3 lines)
    tracker = MetricsTracker(
        experiment_name=f"{args.method}_{args.dataset}_T{args.T}",
        save_dir='./results'
    )
    tracker.log_config(
        method=args.method,
        dataset=args.dataset, 
        num_clients=args.num_clients,
        num_participants=args.num_part,
        communication_rounds=args.T,
        local_epochs=args.K,
        learning_rate=args.lr,
        batch_size=args.bsz,
        non_iid=args.non_iid
    )
    
    hist_acc = []
    
    for t in range(args.T):  # Communication rounds
        # ... existing training code ...
        
        test_loss, test_acc = check_accuracy(t, test_loader, model, device)
        hist_acc.append(test_acc)
        
        # NEW: Log metrics for this round (1 line)
        tracker.log_round(
            round_num=t,
            test_loss=test_loss,
            test_acc=test_acc,
            num_clients=len(part_list)  # Select list of current round
        )
        
        print(f"Round {t}, Test Acc: {test_acc:.4f}")
    
    # NEW: Save and visualize results (5 lines)
    print("\n" + "="*60)
    print("SAVING RESULTS AND GENERATING VISUALIZATIONS...")
    tracker.save_json()
    tracker.save_csv()
    tracker.print_summary()
    
    visualizer = ResultsVisualizer()
    visualizer.plot_all(tracker.metrics, experiment_name=tracker.experiment_name)
    print("="*60 + "\n")


# ============ COMPARISON ALGORITHM TEST ============

def test_comparison_example():
    """
    After running multiple experiments (FedAvg, FedAdapt, SCAFFOLD, etc.),
    compare them with a few lines of code.
    """
    from visualization import ExperimentComparison, ResultsVisualizer
    
    # Load all experiments from results directory
    comparator = ExperimentComparison(results_dir='./results')
    comparator.load_all_experiments()
    
    # Print comparison table
    print("\nALGORITHM COMPARISON:")
    comparator.print_comparison()
    
    # Create comparison plots
    experiments = {}
    for exp_name, data in comparator.experiments.items():
        experiments[exp_name] = data['metrics']
    
    viz = ResultsVisualizer()
    print("\nGenerating comparison plots...")
    viz.plot_comparison(experiments, metric='test_acc', save=True)
    viz.plot_comparison(experiments, metric='test_loss', save=True)
    print("✓ Comparison plots saved to results/plots/\n")


# ============ EXACT CODE TO ADD TO main_fmnist.py ============

"""
Here's the EXACT code to add/modify in main_fmnist.py:

1. AT THE TOP OF THE FILE, add import:
---
from visualization import MetricsTracker, ResultsVisualizer
---

2. IN THE run() FUNCTION, after parameter definitions, add:
---
# Initialize metrics tracking
tracker = MetricsTracker(
    experiment_name=f"{args.method}_{args.dataset}",
    save_dir='./results'
)
tracker.log_config(
    method=args.method,
    dataset=args.dataset,
    num_clients=args.num_clients,
    num_participants=args.num_part,
    communication_rounds=args.T,
    local_epochs=args.K,
    learning_rate=args.lr,
    batch_size=args.bsz,
    non_iid=args.non_iid
)
---

3. IN THE TRAINING LOOP, after check_accuracy() call, add:
---
# Replace this line:
# print(epoch, batch_idx, len(loader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
#       % (test_loss / (batch_idx + 1), 100. * correct / total, correct, total))

# With this:
tracker.log_round(
    round_num=t,
    test_loss=test_loss,
    test_acc=test_acc,
    num_clients=len(part_list)
)
print(epoch, batch_idx, len(loader), 'Loss: %.3f | Acc: %.3f%% (%d/%d)'
      % (test_loss / (batch_idx + 1), 100. * correct / total, correct, total))
---

4. AT THE END OF training loop (after for t in range(args.T):), add:
---
# Save results and generate visualizations
print("\\n" + "="*60)
print("Saving experiment results...")
tracker.save_json()
tracker.save_csv()
tracker.print_summary()

print("\\nGenerating visualizations...")
visualizer = ResultsVisualizer()
visualizer.plot_all(tracker.metrics, experiment_name=tracker.experiment_name)
print("="*60 + "\\n")
---

That's it! Now your experiments will automatically:
✓ Track all metrics per round
✓ Generate beautiful plots
✓ Save results as JSON + CSV
✓ Print summary statistics
✓ Allow for easy algorithm comparison
"""


# ============ EXPECTED OUTPUT ============

"""
When you run with visualization tracking, you'll see:

$ python main_fmnist.py --method FedAvg --T 200

Round 0, Test Acc: 0.4512
Round 1, Test Acc: 0.5823
...
Round 199, Test Acc: 0.9234

============================================================
Saving experiment results...
✓ Metrics saved to ./results/FedAvg_FMNIST_metrics.json
✓ Metrics saved to ./results/FedAvg_FMNIST_metrics.csv

============================================================
Experiment: FedAvg_FMNIST
Algorithm: FedAvg
Total Rounds: 200
Best Accuracy: 0.9234 (Round 156)
Final Accuracy: 0.9234
Avg Test Loss: 0.2134
============================================================

Generating visualizations...
✓ Accuracy plot saved to ./results/plots/accuracy_FedAvg_FMNIST.png
✓ Loss plot saved to ./results/plots/loss_FedAvg_FMNIST.png
✓ Convergence plot saved to ./results/plots/convergence_FedAvg_FMNIST.png
✓ Efficiency plot saved to ./results/plots/efficiency_FedAvg_FMNIST.png

============================================================

Files created:
results/
├── FedAvg_FMNIST_metrics.json
├── FedAvg_FMNIST_metrics.csv
└── plots/
    ├── accuracy_FedAvg_FMNIST.png
    ├── loss_FedAvg_FMNIST.png
    ├── convergence_FedAvg_FMNIST.png
    └── efficiency_FedAvg_FMNIST.png
"""


# ============ RUNNING EXPERIMENTS ============

"""
Example workflow:

# 1. Run multiple algorithms
python main_fmnist.py --method FedAvg --T 200
python main_fmnist.py --method FedAdapt --T 200  
python main_fmnist.py --method SCAFFOLD --T 200

# 2. Compare them (add this to main script or run separately)
python -c "
from visualization import ExperimentComparison, ResultsVisualizer
comp = ExperimentComparison()
comp.load_all_experiments()
comp.print_comparison()

experiments = {n: d['metrics'] for n, d in comp.experiments.items()}
viz = ResultsVisualizer()
viz.plot_comparison(experiments, 'test_acc')
"

# 3. Results appear in:
#    - ./results/*.json (raw data)
#    - ./results/plots/*.png (visualizations)
"""
