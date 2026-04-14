# Client Participation Analyzer - Examples
# Demonstrate usage of the participation analysis tools

from participation import ParticipationAnalyzer, ParticipationVisualizer
import json

print("="*80)
print("CLIENT PARTICIPATION ANALYZER - USAGE EXAMPLES")
print("="*80)

# ==================== EXAMPLE 1: Basic Setup ====================
print("\n" + "="*80)
print("EXAMPLE 1: Basic Setup and Loading Experiments")
print("="*80)

# Initialize analyzer
analyzer = ParticipationAnalyzer('./results')

# Load all experiments
num_loaded = analyzer.load_all_experiments()
print(f"\n✓ Loaded {num_loaded} experiment(s)")

# Or load a specific experiment
# analyzer.load_experiment('./results/fedavg_metrics.json', 'FedAvg_Run1')
# analyzer.load_experiment('./results/fedadapt_metrics.json', 'FedAdapt_Run1')


# ==================== EXAMPLE 2: Participation Analysis ====================
print("\n" + "="*80)
print("EXAMPLE 2: Analyze Participation Impact")
print("="*80)

# Analyze participation impact
print("\n→ Analyzing participation impact...")
analyses = analyzer.analyze_participation_impact()

print(f"\n✓ Analyzed {len(analyses)} algorithm(s)")

# Print detailed report
analyzer.print_participation_report()


# ==================== EXAMPLE 3: Full vs Partial Participation ====================
print("="*80)
print("EXAMPLE 3: Compare Full vs Partial Participation")
print("="*80)

# Analyze full vs partial participation
print("\n→ Comparing full vs partial participation (threshold: 80%)...")
analyzer.print_full_vs_partial_analysis(threshold=0.8)


# ==================== EXAMPLE 4: Participation Impact Correlation ====================
print("="*80)
print("EXAMPLE 4: Participation-Accuracy Correlation")
print("="*80)

# Analyze correlation between participation and accuracy
print("\n→ Computing participation-accuracy correlation...")
analyzer.print_participation_impact()


# ==================== EXAMPLE 5: Variance Analysis ====================
print("="*80)
print("EXAMPLE 5: Participation Variance Impact")
print("="*80)

# Get participation variance impact
variance_impact = analyzer.get_participation_variance_impact()

print("\n→ Participation variance analysis:")
for algo, data in sorted(variance_impact.items()):
    print(f"\n{algo}:")
    print(f"  Participation CV: {data['participation_cv']:.3f}")
    print(f"  Accuracy Std Dev: {data['accuracy_std']:.4f}")
    print(f"  Final Accuracy:   {data['final_accuracy']:.4f}")


# ==================== EXAMPLE 6: Recommendations ====================
print("\n" + "="*80)
print("EXAMPLE 6: Participation Recommendations")
print("="*80)

# Get recommendations
print("\n→ Generating recommendations...")
analyzer.print_recommendations()


# ==================== EXAMPLE 7: Optimal Participation Rates ====================
print("="*80)
print("EXAMPLE 7: Optimal Participation Rates")
print("="*80)

# Get optimal participation rates
print("\n→ Estimating optimal participation rates...")
analyzer.print_optimal_rates()


# ==================== EXAMPLE 8: Visualization ====================
print("="*80)
print("EXAMPLE 8: Create Visualizations")
print("="*80)

# Initialize visualizer
visualizer = ParticipationVisualizer('./results/participation_plots')

print("\n→ Generating all participation visualizations...")

# Plot 1: Participation over time
visualizer.plot_participation_over_time(analyzer.experiments, save=True)

# Plot 2: Accuracy vs Participation
visualizer.plot_accuracy_vs_participation(analyzer.experiments, save=True)

# Plot 3: Participation variance impact
variance_data = analyzer.get_participation_variance_impact()
if variance_data:
    visualizer.plot_participation_variance_impact(variance_data, save=True)

# Plot 4: Full vs partial participation
full_vs_partial = analyzer.analyze_full_vs_partial()
if full_vs_partial:
    visualizer.plot_full_vs_partial_participation(full_vs_partial, save=True)

# Plot 5: Robustness profiles
if analyses:
    visualizer.plot_robustness_profiles(analyses, save=True)

# Plot 6: Participation impact heatmap
visualizer.plot_participation_impact_heatmap(analyzer.experiments, bins=5, save=True)

# Plot all at once
visualizer.plot_all_participation_visualizations(
    analyzer.experiments,
    variance_data,
    full_vs_partial,
    analyses,
    save=True
)


# ==================== EXAMPLE 9: Export Results ====================
print("="*80)
print("EXAMPLE 9: Export Analysis Results")
print("="*80)

print("\n→ Exporting participation analysis...")
export_path = analyzer.export_participation_metrics('./results/participation_analysis.json')
print(f"✓ Exported to: {export_path}")

# Manual export - access the data directly
participation_data = {
    'analyses': {
        algo: {
            'total_clients': a.total_clients,
            'avg_participation_rate': a.avg_participation_rate,
            'convergence_rounds': a.convergence_rounds,
            'final_accuracy': a.final_accuracy,
            'robustness_score': a.robustness_score
        }
        for algo, a in analyses.items()
    },
    'full_vs_partial': full_vs_partial,
    'variance_impact': {
        algo: {
            'participation_cv': data['participation_cv'],
            'accuracy_std': data['accuracy_std'],
            'final_accuracy': data['final_accuracy']
        }
        for algo, data in variance_data.items()
    }
}

print("\nExportable data structure:")
print(json.dumps(participation_data, indent=2)[:500] + "...")


# ==================== EXAMPLE 10: Custom Analysis ====================
print("\n" + "="*80)
print("EXAMPLE 10: Custom Analysis Workflow")
print("="*80)

# Get best algorithm by robustness
best_robustness = max(analyses.items(), key=lambda x: x[1].robustness_score)
print(f"\nMost robust algorithm: {best_robustness[0]} (score: {best_robustness[1].robustness_score:.3f})")

# Get algorithm with best efficiency
best_efficiency = max(analyses.items(), key=lambda x: x[1].communication_efficiency)
print(f"Best efficiency: {best_efficiency[0]} (score: {best_efficiency[1].communication_efficiency:.6f})")

# Get algorithms by participation requirement
low_participation = [a for a, data in analyses.items() if data.avg_participation_rate < 50]
high_participation = [a for a, data in analyses.items() if data.avg_participation_rate >= 80]

print(f"\nLow participation algorithms (<50%): {low_participation if low_participation else 'None'}")
print(f"High participation algorithms (≥80%): {high_participation if high_participation else 'None'}")


# ==================== EXAMPLE 11: Detailed Analysis ====================
print("\n" + "="*80)
print("EXAMPLE 11: Detailed Algorithm Analysis")
print("="*80)

for algo_name, analysis in sorted(analyses.items()):
    print(f"\n{algo_name}")
    print("-" * 60)
    print(f"  Total Clients:             {analysis.total_clients}")
    print(f"  Avg Participation:         {analysis.avg_participation_rate:.1f}%")
    print(f"  Participation Range:       {analysis.min_participation_rate:.1f}% - {analysis.max_participation_rate:.1f}%")
    print(f"  Participation Consistency: σ = {analysis.participation_consistency:.2f}")
    print(f"  Convergence Rounds:        {analysis.convergence_rounds}")
    print(f"  Final Accuracy:            {analysis.final_accuracy:.4f}")
    print(f"  Communication Efficiency:  {analysis.communication_efficiency:.6f}")
    print(f"  Robustness Score:          {analysis.robustness_score:.3f}")


# ==================== EXAMPLE 12: Impact Metrics ====================
print("\n" + "="*80)
print("EXAMPLE 12: Participation Impact Metrics")
print("="*80)

impact = analyzer.get_participation_impact()

print("\nParticipation-Accuracy Correlation (by Algorithm):")
print("-" * 60)
for algo, data in sorted(impact.items()):
    corr = data['participation_accuracy_correlation']
    
    if not np.isnan(corr):
        if corr > 0.7:
            impact_level = "HIGH (sensitive to dropout)"
        elif corr > 0.3:
            impact_level = "MODERATE"
        else:
            impact_level = "LOW (robust to dropout)"
        
        print(f"{algo:<20} Correlation: {corr:>7.3f}  Impact: {impact_level}")


print("\n" + "="*80)
print("✓ EXAMPLES COMPLETED")
print("="*80)

# Import numpy for the script
import numpy as np
