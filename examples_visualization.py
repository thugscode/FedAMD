# Example Usage of the Visualization Module
# Shows how to integrate metrics tracking into federated learning training

from visualization import MetricsTracker, ResultsVisualizer, ExperimentComparison
import json


# ==========================================
# EXAMPLE 1: Basic Usage with Training Loop
# ==========================================

def train_with_metrics(args):
    """
    Example of how to integrate MetricsTracker into your training loop.
    This would replace the existing training logic in main_fmnist.py
    """
    
    # Initialize metrics tracker
    tracker = MetricsTracker(
        experiment_name=f"{args.method}_T{args.T}_K{args.K}",
        save_dir='./results'
    )
    
    # Log experiment configuration
    tracker.log_config(
        method=args.method,
        dataset=args.dataset,
        num_clients=args.num_clients,
        num_participants=args.num_part,
        communication_rounds=args.T,
        local_epochs=args.K,
        learning_rate=args.lr,
        batch_size=args.bsz,
        non_iid=args.non_iid,
        dirichlet_alpha=args.dir_alpha if args.dirichlet else None
    )
    
    # Training loop
    for t in range(args.T):  # Communication rounds
        # ... your training code here ...
        
        # After each round, log metrics:
        test_loss, test_acc = check_accuracy(t, test_loader, model, device)  # Your existing function
        
        # Log round metrics
        tracker.log_round(
            round_num=t,
            test_loss=test_loss,
            test_acc=test_acc,
            train_loss=avg_train_loss,  # Compute during training
            train_acc=avg_train_acc,     # Compute during training
            num_clients=len(part_list),  # Number of selected clients
            local_steps=args.K
        )
        
        print(f"Round {t}: Test Acc = {test_acc:.4f}, Test Loss = {test_loss:.4f}")
    
    # Save results
    tracker.save_json()
    tracker.save_csv()
    tracker.print_summary()
    
    # Visualize results
    visualizer = ResultsVisualizer()
    visualizer.plot_all(tracker.metrics, experiment_name=tracker.experiment_name)
    
    return tracker


# ==========================================
# EXAMPLE 2: Comparing Multiple Algorithms
# ==========================================

def compare_algorithms_example():
    """
    Example of comparing different federated learning algorithms.
    Run multiple experiments and compare them.
    """
    
    # Assuming you've run experiments for FedAvg, FedAdapt, SCAFFOLD, etc.
    comparator = ExperimentComparison(results_dir='./results')
    
    # Load all experiments
    comparator.load_all_experiments()
    
    # Print comparison table
    comparator.print_comparison()
    
    # Load specific experiments for visualization
    experiments = {}
    for exp_name, data in comparator.experiments.items():
        experiments[exp_name] = data['metrics']
    
    # Compare accuracy
    visualizer = ResultsVisualizer()
    visualizer.plot_comparison(experiments, metric='test_acc', save=True)
    visualizer.plot_comparison(experiments, metric='test_loss', save=True)


# ==========================================
# EXAMPLE 3: Advanced Metrics Analysis
# ==========================================

def advanced_analysis_example(results_file: str):
    """
    Load and analyze saved results in detail.
    """
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    metrics = data['metrics']
    config = data['config']
    
    # Get statistics
    test_accs = [a for a in metrics['test_acc'] if a is not None]
    test_losses = [l for l in metrics['test_loss'] if l is not None]
    
    print(f"\n{'='*60}")
    print(f"Experiment Analysis: {data['experiment']}")
    print(f"{'='*60}")
    print(f"Algorithm: {config.get('method', 'Unknown')}")
    print(f"Dataset: {config.get('dataset', 'Unknown')}")
    print(f"\nAccuracy Statistics:")
    print(f"  Initial Acc: {test_accs[0]:.4f}" if test_accs else "  Initial Acc: N/A")
    print(f"  Final Acc:   {test_accs[-1]:.4f}" if test_accs else "  Final Acc: N/A")
    print(f"  Best Acc:    {max(test_accs):.4f}" if test_accs else "  Best Acc: N/A")
    print(f"  Avg Acc:     {sum(test_accs)/len(test_accs):.4f}" if test_accs else "  Avg Acc: N/A")
    
    print(f"\nLoss Statistics:")
    print(f"  Initial Loss: {test_losses[0]:.4f}" if test_losses else "  Initial Loss: N/A")
    print(f"  Final Loss:   {test_losses[-1]:.4f}" if test_losses else "  Final Loss: N/A")
    print(f"  Avg Loss:     {sum(test_losses)/len(test_losses):.4f}" if test_losses else "  Avg Loss: N/A")
    
    print(f"\nTraining Config:")
    print(f"  Communication Rounds: {config.get('communication_rounds', 'N/A')}")
    print(f"  Local Epochs: {config.get('local_epochs', 'N/A')}")
    print(f"  Num Clients: {config.get('num_clients', 'N/A')}")
    print(f"  Participants/Round: {config.get('num_participants', 'N/A')}")
    print(f"  Non-IID: {config.get('non_iid', 'N/A')}")
    
    if config.get('non_iid') and config.get('dirichlet_alpha'):
        print(f"  Dirichlet Alpha: {config.get('dirichlet_alpha', 'N/A')}")
    
    print(f"{'='*60}\n")


# ==========================================
# EXAMPLE 4: Minimal Integration Template
# ==========================================

def minimal_integration_template():
    """
    Minimal code template to add to your existing training script.
    
    Just 3 lines to add at the start of training:
        tracker = MetricsTracker(f"{args.method}_experiment")
        tracker.log_config(method=args.method, dataset=args.dataset, ...)
    
    One line in each training round (after validation):
        tracker.log_round(t, test_loss, test_acc, train_loss, train_acc, 
                         num_clients=len(selected_clients), local_steps=args.K)
    
    And at the end:
        tracker.save_json()
        tracker.print_summary()
        ResultsVisualizer().plot_all(tracker.metrics, tracker.experiment_name)
    """
    
    code = '''
# Add this to your training script:

from visualization import MetricsTracker, ResultsVisualizer

# Initialize tracker at start of training
tracker = MetricsTracker(experiment_name=f"{args.method}_{args.dataset}")
tracker.log_config(method=args.method, dataset=args.dataset, num_clients=args.num_clients, ...)

# Inside your training loop (after each validation):
for t in range(args.T):
    # ... your training code ...
    test_loss, test_acc = check_accuracy(t, test_loader, model, device)
    
    # Log metrics
    tracker.log_round(t, test_loss=test_loss, test_acc=test_acc, 
                     num_clients=len(participating_clients))

# After training completes:
tracker.save_json()
tracker.save_csv()
tracker.print_summary()

# Generate visualizations
visualizer = ResultsVisualizer()
visualizer.plot_all(tracker.metrics, experiment_name=tracker.experiment_name)
    '''
    
    print(code)


if __name__ == '__main__':
    # Run examples
    print("Visualization Module Examples\n")
    
    print("=" * 70)
    print("MINIMAL INTEGRATION TEMPLATE")
    print("=" * 70)
    minimal_integration_template()
    
    print("\n" + "=" * 70)
    print("NOTE: To use these examples:")
    print("=" * 70)
    print("1. Run your training with integrated MetricsTracker")
    print("2. Results will be saved to ./results/")
    print("3. Plots will be saved to ./results/plots/")
    print("4. Use ExperimentComparison to compare multiple algorithms")
    print("\nExample commands:")
    print("  python main_fmnist.py --method FedAvg --T 200")
    print("  python main_fmnist.py --method FedAdapt --T 200")
    print("  # Then run compare_algorithms_example() to see comparisons")
