# Client Participation Visualization
# Visualize participation impact on convergence and performance

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np


class ParticipationVisualizer:
    """Visualize client participation and its impact on convergence."""
    
    def __init__(self, output_dir: str = './results/participation_plots'):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory for output plots
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = plt.cm.Set2(np.linspace(0, 1, 8))
    
    def plot_participation_over_time(self, experiments_dict: Dict, save: bool = True) -> None:
        """
        Plot client participation rate over time for all algorithms.
        
        Args:
            experiments_dict: Dictionary of experiment data
            save: Whether to save plot
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        color_idx = 0
        for experiment_name, exp_data in experiments_dict.items():
            metrics = exp_data.get('metrics', {})
            client_participation = metrics.get('client_participation', [])
            config = exp_data.get('config', {})
            
            total_clients = config.get('num_clients', 20)
            
            if not client_participation:
                continue
            
            # Convert to participation rates
            participation_rates = []
            for num_part in client_participation:
                if num_part is not None:
                    rate = (num_part / total_clients * 100) if total_clients > 0 else 0
                    participation_rates.append(rate)
                else:
                    participation_rates.append(None)
            
            rounds = range(1, len(participation_rates) + 1)
            ax.plot(rounds, participation_rates, label=experiment_name, 
                   marker='o', markersize=3, linewidth=2, 
                   color=self.colors[color_idx % len(self.colors)])
            color_idx += 1
        
        ax.set_xlabel('Round', fontsize=12, fontweight='bold')
        ax.set_ylabel('Client Participation Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Client Participation Over Time', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        ax.set_ylim([0, 105])
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'participation_over_time.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_accuracy_vs_participation(self, experiments_dict: Dict, save: bool = True) -> None:
        """
        Plot relationship between participation and accuracy.
        
        Args:
            experiments_dict: Dictionary of experiment data
            save: Whether to save plot
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        color_idx = 0
        for experiment_name, exp_data in experiments_dict.items():
            metrics = exp_data.get('metrics', {})
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            config = exp_data.get('config', {})
            
            total_clients = config.get('num_clients', 20)
            
            if not client_participation or not test_acc:
                continue
            
            # Convert to participation rates
            participation_rates = []
            valid_accs = []
            
            for num_part, acc in zip(client_participation, test_acc):
                if num_part is not None and acc is not None:
                    rate = (num_part / total_clients * 100) if total_clients > 0 else 0
                    participation_rates.append(rate)
                    valid_accs.append(acc)
            
            if participation_rates and valid_accs:
                ax.scatter(participation_rates, valid_accs, label=experiment_name, 
                          s=50, alpha=0.6, color=self.colors[color_idx % len(self.colors)])
                
                # Fit trend line
                z = np.polyfit(participation_rates, valid_accs, 1)
                p = np.poly1d(z)
                x_range = np.linspace(min(participation_rates), max(participation_rates), 100)
                ax.plot(x_range, p(x_range), '--', linewidth=1.5, 
                       color=self.colors[color_idx % len(self.colors)], alpha=0.5)
                
                color_idx += 1
        
        ax.set_xlabel('Client Participation Rate (%)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Test Accuracy', fontsize=12, fontweight='bold')
        ax.set_title('Accuracy vs Client Participation', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='best', fontsize=10)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'accuracy_vs_participation.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_participation_variance_impact(self, variance_impact: Dict, save: bool = True) -> None:
        """
        Plot impact of participation variance on performance.
        
        Args:
            variance_impact: Dictionary with variance analysis
            save: Whether to save plot
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        algos = list(variance_impact.keys())
        participation_cvs = [variance_impact[a]['participation_cv'] for a in algos]
        final_accs = [variance_impact[a]['final_accuracy'] for a in algos]
        
        # Plot 1: Participation CV vs Final Accuracy
        colors = self.colors[:len(algos)]
        bars1 = ax1.bar(range(len(algos)), final_accs, color=colors, alpha=0.7, edgecolor='black')
        ax1_twin = ax1.twinx()
        ax1_twin.plot(range(len(algos)), participation_cvs, 'ro-', linewidth=2, markersize=8, label='Part. CV')
        
        ax1.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Final Accuracy', fontsize=11, fontweight='bold')
        ax1_twin.set_ylabel('Participation Coefficient of Variation', fontsize=11, fontweight='bold', color='red')
        ax1.set_title('Participation Variance Impact on Performance', fontsize=13, fontweight='bold')
        ax1.set_xticks(range(len(algos)))
        ax1.set_xticklabels(algos, rotation=45, ha='right')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for i, (bar, acc) in enumerate(zip(bars1, final_accs)):
            ax1.text(bar.get_x() + bar.get_width()/2, acc + 0.01, f'{acc:.3f}', 
                    ha='center', va='bottom', fontsize=9)
        
        # Plot 2: Participation progression for each algorithm
        for i, algo in enumerate(algos):
            participation = variance_impact[algo]['participation_progression']
            ax2.plot(participation, label=algo, linewidth=2, 
                    color=colors[i], marker='o', markersize=4)
        
        ax2.set_xlabel('Round', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Participating Clients', fontsize=12, fontweight='bold')
        ax2.set_title('Participation Progression Over Time', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='best', fontsize=10)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'participation_variance_impact.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_full_vs_partial_participation(self, full_vs_partial: Dict, save: bool = True) -> None:
        """
        Plot comparison of full vs partial participation performance.
        
        Args:
            full_vs_partial: Dictionary with full/partial analysis
            save: Whether to save plot
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        algos = list(full_vs_partial.keys())
        
        full_avg = [full_vs_partial[a]['full_participation']['avg_accuracy'] 
                   for a in algos]
        partial_avg = [full_vs_partial[a]['partial_participation']['avg_accuracy'] 
                      for a in algos]
        
        full_best = [full_vs_partial[a]['full_participation']['best_accuracy'] 
                    for a in algos]
        partial_best = [full_vs_partial[a]['partial_participation']['best_accuracy'] 
                       for a in algos]
        
        x = np.arange(len(algos))
        width = 0.35
        
        # Average accuracy
        bars1 = axes[0].bar(x - width/2, full_avg, width, label='Full Participation', 
                           alpha=0.8, color='#2ecc71', edgecolor='black')
        bars2 = axes[0].bar(x + width/2, partial_avg, width, label='Partial Participation', 
                           alpha=0.8, color='#e74c3c', edgecolor='black')
        
        axes[0].set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Average Accuracy', fontsize=12, fontweight='bold')
        axes[0].set_title('Average Accuracy: Full vs Partial Participation', fontsize=13, fontweight='bold')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(algos, rotation=45, ha='right')
        axes[0].legend(fontsize=10)
        axes[0].grid(True, alpha=0.3, axis='y')
        
        # Best accuracy
        bars3 = axes[1].bar(x - width/2, full_best, width, label='Full Participation', 
                           alpha=0.8, color='#3498db', edgecolor='black')
        bars4 = axes[1].bar(x + width/2, partial_best, width, label='Partial Participation', 
                           alpha=0.8, color='#f39c12', edgecolor='black')
        
        axes[1].set_xlabel('Algorithm', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Best Accuracy', fontsize=12, fontweight='bold')
        axes[1].set_title('Best Accuracy: Full vs Partial Participation', fontsize=13, fontweight='bold')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels(algos, rotation=45, ha='right')
        axes[1].legend(fontsize=10)
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'full_vs_partial_participation.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_robustness_profiles(self, analyses: Dict, save: bool = True) -> None:
        """
        Plot robustness profiles for each algorithm.
        
        Args:
            analyses: Dictionary of ParticipationAnalysis objects
            save: Whether to save plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        algos = sorted(list(analyses.keys()))
        colors = self.colors[:len(algos)]
        
        # Robustness scores
        robustness = [analyses[a].robustness_score for a in algos]
        axes[0, 0].barh(algos, robustness, color=colors, alpha=0.7, edgecolor='black')
        axes[0, 0].set_xlabel('Robustness Score', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Algorithm Robustness (to Participation Variance)', fontsize=12, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3, axis='x')
        for i, v in enumerate(robustness):
            axes[0, 0].text(v + 0.02, i, f'{v:.3f}', va='center', fontsize=9)
        
        # Communication efficiency
        comm_eff = [analyses[a].communication_efficiency for a in algos]
        axes[0, 1].barh(algos, comm_eff, color=colors, alpha=0.7, edgecolor='black')
        axes[0, 1].set_xlabel('Communication Efficiency', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Communication Efficiency (Accuracy/Round)', fontsize=12, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        for i, v in enumerate(comm_eff):
            axes[0, 1].text(v + max(comm_eff)*0.01, i, f'{v:.6f}', va='center', fontsize=9)
        
        # Participation consistency
        consistency = [analyses[a].participation_consistency for a in algos]
        axes[1, 0].barh(algos, consistency, color=colors, alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Participation Std Dev', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Participation Variability', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        for i, v in enumerate(consistency):
            axes[1, 0].text(v + max(consistency)*0.02, i, f'{v:.2f}', va='center', fontsize=9)
        
        # Average participation rate
        avg_part = [analyses[a].avg_participation_rate for a in algos]
        axes[1, 1].barh(algos, avg_part, color=colors, alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('Average Participation Rate (%)', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Average Client Participation Needed', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='x')
        axes[1, 1].set_xlim([0, 105])
        for i, v in enumerate(avg_part):
            axes[1, 1].text(v + 2, i, f'{v:.1f}%', va='center', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'robustness_profiles.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_participation_impact_heatmap(self, experiments_dict: Dict, bins: int = 5, save: bool = True) -> None:
        """
        Create heatmap showing accuracy at different participation levels.
        
        Args:
            experiments_dict: Dictionary of experiment data
            bins: Number of participation rate bins
            save: Whether to save plot
        """
        fig, axes = plt.subplots(figsize=(12, 6))
        
        # Collect data per algorithm
        algo_data = {}
        
        for experiment_name, exp_data in experiments_dict.items():
            metrics = exp_data.get('metrics', {})
            algorithm = exp_data.get('algorithm', 'unknown')
            config = exp_data.get('config', {})
            
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            
            total_clients = config.get('num_clients', 20)
            
            if not client_participation or not test_acc:
                continue
            
            if algorithm not in algo_data:
                algo_data[algorithm] = {'participation': [], 'accuracy': []}
            
            for num_part, acc in zip(client_participation, test_acc):
                if num_part is not None and acc is not None:
                    rate = (num_part / total_clients * 100) if total_clients > 0 else 0
                    algo_data[algorithm]['participation'].append(rate)
                    algo_data[algorithm]['accuracy'].append(acc)
        
        # Create heatmap
        algos = sorted(list(algo_data.keys()))
        bin_edges = np.linspace(0, 100, bins + 1)
        heatmap_data = np.zeros((len(algos), bins))
        
        for i, algo in enumerate(algos):
            participation = algo_data[algo]['participation']
            accuracy = algo_data[algo]['accuracy']
            
            for j in range(bins):
                mask = (np.array(participation) >= bin_edges[j]) & (np.array(participation) < bin_edges[j+1])
                if np.any(mask):
                    heatmap_data[i, j] = np.mean(np.array(accuracy)[mask])
                else:
                    heatmap_data[i, j] = np.nan
        
        im = axes.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        # Set labels
        axes.set_xticks(range(bins))
        axes.set_xticklabels([f'{bin_edges[j]:.0f}-{bin_edges[j+1]:.0f}%' for j in range(bins)], 
                            rotation=45, ha='right')
        axes.set_yticks(range(len(algos)))
        axes.set_yticklabels(algos)
        
        axes.set_xlabel('Participation Rate Range', fontsize=12, fontweight='bold')
        axes.set_ylabel('Algorithm', fontsize=12, fontweight='bold')
        axes.set_title('Accuracy Heatmap for Different Participation Rates', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=axes)
        cbar.set_label('Average Accuracy', fontsize=11, fontweight='bold')
        
        # Add annotations
        for i in range(len(algos)):
            for j in range(bins):
                if not np.isnan(heatmap_data[i, j]):
                    axes.text(j, i, f'{heatmap_data[i, j]:.2f}', 
                             ha='center', va='center', color='black', fontsize=9)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / 'participation_impact_heatmap.png'
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filepath}")
        plt.show()
    
    def plot_all_participation_visualizations(self, experiments_dict: Dict, 
                                             variance_impact: Dict, 
                                             full_vs_partial: Dict,
                                             analyses: Dict,
                                             save: bool = True) -> None:
        """
        Generate all participation visualizations.
        
        Args:
            experiments_dict: Dictionary of experiment data
            variance_impact: Dictionary with variance analysis
            full_vs_partial: Dictionary with full/partial analysis
            analyses: Dictionary of ParticipationAnalysis objects
            save: Whether to save plots
        """
        print("\nGenerating participation visualizations...\n")
        
        self.plot_participation_over_time(experiments_dict, save)
        self.plot_accuracy_vs_participation(experiments_dict, save)
        self.plot_participation_variance_impact(variance_impact, save)
        self.plot_full_vs_partial_participation(full_vs_partial, save)
        self.plot_robustness_profiles(analyses, save)
        self.plot_participation_impact_heatmap(experiments_dict, save=save)
        
        print("\n✓ All participation visualizations generated!")
