# Experiment Comparison Tool - Examples

from comparison import ComparisonTool, ComparisonVisualizer
import json


# ==========================================
# EXAMPLE 1: Basic Comparison
# ==========================================

def basic_comparison_example():
    """Load experiments and print detailed comparison."""
    
    print("\n" + "="*80)
    print("EXAMPLE 1: BASIC ALGORITHM COMPARISON")
    print("="*80)
    
    # Load experiments
    comp = ComparisonTool(results_dir='./results')
    num_loaded = comp.load_experiments()
    
    print(f"\nLoaded {num_loaded} experiments")
    print(f"Algorithms found: {', '.join(comp.algorithms.keys())}")
    
    # Compute statistics
    print("\nComputing statistics...")
    stats = comp.compute_statistics()
    
    # Print report
    comp.print_detailed_report()


# ==========================================
# EXAMPLE 2: Algorithm Rankings
# ==========================================

def rankings_example():
    """Show algorithm rankings for different metrics."""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: ALGORITHM RANKINGS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Print rankings
    comp.print_rankings()


# ==========================================
# EXAMPLE 3: Strengths & Weaknesses Analysis
# ==========================================

def analysis_example():
    """Identify strengths and weaknesses of each algorithm."""
    
    print("\n" + "="*80)
    print("EXAMPLE 3: ALGORITHM ANALYSIS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Print analysis
    comp.print_analysis()


# ==========================================
# EXAMPLE 4: Export Comparison Results
# ==========================================

def export_example():
    """Export comparison results to CSV and text."""
    
    print("\n" + "="*80)
    print("EXAMPLE 4: EXPORT RESULTS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Export as CSV
    csv_file = comp.export_csv('./results/algorithm_comparison.csv')
    print(f"✓ CSV exported: {csv_file}")
    
    # Export as text table
    txt_file = comp.export_comparison_table('./results/algorithm_comparison.txt')
    print(f"✓ Text table exported: {txt_file}")


# ==========================================
# EXAMPLE 5: Visualize Comparisons
# ==========================================

def visualization_example():
    """Generate comparison plots."""
    
    print("\n" + "="*80)
    print("EXAMPLE 5: GENERATE VISUALIZATIONS")
    print("="*80)
    
    # Load experiments
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Prepare experiments for visualization
    # Group by algorithm, use first experiment of each
    experiments = {}
    for exp_name, data in comp.experiments.items():
        algo = data['algorithm']
        if algo not in experiments:
            experiments[algo] = data['metrics']
    
    # Create visualizer and plot
    viz = ComparisonVisualizer()
    viz.plot_all_comparisons(experiments, comp.stats, baseline='FedAvg')


# ==========================================
# EXAMPLE 6: Get Best Algorithm
# ==========================================

def best_algorithm_example():
    """Find and display best algorithm by different metrics."""
    
    print("\n" + "="*80)
    print("EXAMPLE 6: FIND BEST ALGORITHM")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Best by different metrics
    print("\nBEST ALGORITHMS BY METRIC")
    print("-"*80)
    
    best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
    print(f"Best Accuracy:      {best_algo:<20} {best_acc:.4f}")
    
    best_algo, best_final = comp.get_best_algorithm('final_accuracy')
    print(f"Best Final Accuracy: {best_algo:<20} {best_final:.4f}")
    
    best_algo, best_conv = comp.get_best_algorithm('convergence_round_95')
    print(f"Fastest Convergence: {best_algo:<20} {best_conv} rounds")
    
    best_algo, best_imp = comp.get_best_algorithm('improvement')
    print(f"Largest Improvement: {best_algo:<20} {best_imp:.4f}")


# ==========================================
# EXAMPLE 7: Detailed Rankings
# ==========================================

def detailed_ranking_example():
    """Get detailed rankings for each metric."""
    
    print("\n" + "="*80)
    print("EXAMPLE 7: DETAILED RANKINGS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    metrics = ['best_accuracy', 'convergence_round_95', 'improvement']
    
    for metric in metrics:
        print(f"\nRanking by {metric}:")
        print("-"*60)
        
        ranking = comp.get_ranking(metric)
        for rank, (algo, value) in enumerate(ranking, 1):
            if isinstance(value, float):
                print(f"  {rank}. {algo:<20} {value:.4f}")
            else:
                print(f"  {rank}. {algo:<20} {value}")


# ==========================================
# EXAMPLE 8: Comparison Summary
# ==========================================

def summary_example():
    """Get comprehensive comparison summary."""
    
    print("\n" + "="*80)
    print("EXAMPLE 8: COMPARISON SUMMARY")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    summary = comp.get_comparison_summary()
    
    print(f"\nNumber of algorithms: {summary['num_algorithms']}")
    print(f"Number of experiments: {summary['num_experiments']}")
    
    print(f"\nBest by Accuracy: {summary['best_by_accuracy'][0]} ({summary['best_by_accuracy'][1]:.4f})")
    print(f"Best by Convergence Speed: {summary['best_by_convergence_speed'][0]} ({summary['best_by_convergence_speed'][1]} rounds)")
    print(f"Best by Improvement: {summary['best_by_improvement'][0]} ({summary['best_by_improvement'][1]:.4f})")


# ==========================================
# EXAMPLE 9: Load Specific Experiments
# ==========================================

def load_specific_example():
    """Load specific experiments by name."""
    
    print("\n" + "="*80)
    print("EXAMPLE 9: LOAD SPECIFIC EXPERIMENTS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    
    # Load specific files
    comp.load_specific('./results/FedAvg_metrics.json', name='FedAvg_run1')
    comp.load_specific('./results/FedAMD_metrics.json', name='FedAMD_run1')
    
    print(f"\nLoaded experiments: {', '.join(comp.experiments.keys())}")
    print(f"Algorithms: {', '.join(comp.algorithms.keys())}")


# ==========================================
# EXAMPLE 10: DataFrame for Analysis
# ==========================================

def dataframe_example():
    """Use pandas DataFrame for custom analysis."""
    
    print("\n" + "="*80)
    print("EXAMPLE 10: USE DATAFRAME FOR ANALYSIS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Get as DataFrame
    df = comp.create_dataframe()
    
    print("\nComparison DataFrame:")
    print(df.to_string())
    
    print("\n\nBasic Statistics:")
    print(df.describe())
    
    print("\n\nSorted by Best Accuracy:")
    print(df.sort_values('Best Accuracy', ascending=False))


# ==========================================
# EXAMPLE 11: Compare Specific Metrics
# ==========================================

def specific_metrics_example():
    """Compare only specific metrics of interest."""
    
    print("\n" + "="*80)
    print("EXAMPLE 11: COMPARE SPECIFIC METRICS")
    print("="*80)
    
    comp = ComparisonTool(results_dir='./results')
    comp.load_experiments()
    comp.compute_statistics()
    
    # Create table with specific metrics
    metrics = ['best_accuracy', 'convergence_round_95', 'improvement']
    table = comp.create_comparison_table(metrics=metrics)
    
    print("\n" + table)


# ==========================================
# EXAMPLE 12: Full Workflow
# ==========================================

def full_workflow_example():
    """Complete workflow: load, analyze, visualize, export."""
    
    print("\n" + "="*80)
    print("EXAMPLE 12: FULL COMPARISON WORKFLOW")
    print("="*80)
    
    # Step 1: Load experiments
    print("\n[1/6] Loading experiments...")
    comp = ComparisonTool(results_dir='./results')
    num_loaded = comp.load_experiments()
    print(f"✓ Loaded {num_loaded} experiments")
    
    # Step 2: Compute statistics
    print("\n[2/6] Computing statistics...")
    stats = comp.compute_statistics()
    print(f"✓ Statistics computed for {len(stats)} algorithms")
    
    # Step 3: Print report
    print("\n[3/6] Generating report...")
    comp.print_detailed_report()
    
    # Step 4: Export data
    print("\n[4/6] Exporting data...")
    comp.export_csv('./results/comparison_stats.csv')
    comp.export_comparison_table('./results/comparison_table.txt')
    print("✓ Data exported")
    
    # Step 5: Generate visualizations
    print("\n[5/6] Generating visualizations...")
    experiments = {}
    for exp_name, data in comp.experiments.items():
        algo = data['algorithm']
        if algo not in experiments:
            experiments[algo] = data['metrics']
    
    viz = ComparisonVisualizer()
    viz.plot_all_comparisons(experiments, comp.stats, baseline=list(comp.stats.keys())[0])
    
    # Step 6: Print summary
    print("\n[6/6] Final summary...")
    best_algo, best_acc = comp.get_best_algorithm('best_accuracy')
    print(f"\n✓ Comparison complete!")
    print(f"✓ Best algorithm: {best_algo} with accuracy {best_acc:.4f}")


# ==========================================
# MAIN: Run Examples
# ==========================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("EXPERIMENT COMPARISON TOOL - EXAMPLES")
    print("="*80)
    
    print("""
Available examples:
  1. basic_comparison_example()          - Load and print comparison
  2. rankings_example()                   - Show algorithm rankings
  3. analysis_example()                   - Analyze strengths/weaknesses
  4. export_example()                     - Export to CSV/text
  5. visualization_example()              - Generate comparison plots
  6. best_algorithm_example()             - Find best algorithm
  7. detailed_ranking_example()           - Detailed rankings
  8. summary_example()                    - Get summary
  9. load_specific_example()              - Load specific files
  10. dataframe_example()                 - Use pandas DataFrame
  11. specific_metrics_example()          - Compare specific metrics
  12. full_workflow_example()             - Complete workflow
  
Run any example:
  python examples_comparison.py
  
Then in Python:
  >>> basic_comparison_example()
  >>> rankings_example()
  >>> visualization_example()
  >>> full_workflow_example()
    """)
    
    print("\nNote: Make sure you have run experiments first!")
    print("Run main_fmnist.py with different algorithms to generate metrics files.")
