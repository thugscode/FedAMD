# Comparison Tool Visualizations
# Create comparison plots for federated learning algorithms

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np


class ComparisonVisualizer:
    """Create visualization plots for algorithm comparisons."""
    
    def __init__(self, figsize: tuple = (14, 10), style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.
        
        Args:
            figsize: Default figure size
            style: Matplotlib style
        """
        self.figsize = figsize
        try:
            plt.style.use(style)
        except:
            pass
        
        self.colors = plt.cm.Set3(np.linspace(0, 1, 12))
        self.save_dir = Path('./results/comparison_plots')
        self.save_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_accuracy_comparison(self, experiments: Dict[str, Dict], save: bool = True) -> plt.Figure:
        """
        Plot accuracy comparison for all algorithms.
        
        Args:
            experiments: Dictionary of {algorithm: metrics_dict}
            save: Whether to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for idx, (algo_name, metrics) in enumerate(experiments.items()):
            rounds = metrics.get('rounds', [])
            test_acc = metrics.get('test_acc', [])
            
            # Filter out None values
            acc_clean = [(r, a) for r, a in zip(rounds, test_acc) if a is not None]
            
            if acc_clean:
                rounds_c, acc_c = zip(*acc_clean)
                ax.plot(rounds_c, acc_c, marker='o', linewidth=2.5, label=algo_name,
                       color=self.colors[idx % len(self.colors)], markersize=5, alpha=0.8)
        
        ax.set_xlabel('Communication Rounds', fontsize=13, fontweight='bold')
        ax.set_ylabel('Test Accuracy', fontsize=13, fontweight='bold')
        ax.set_title('Algorithm Accuracy Comparison', fontsize=15, fontweight='bold')
        ax.legend(fontsize=11, loc='lower right', framealpha=0.95)
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / 'accuracy_comparison.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Accuracy comparison saved to {filename}")
        
        return fig
    
    def plot_loss_comparison(self, experiments: Dict[str, Dict], save: bool = True) -> plt.Figure:
        """
        Plot loss comparison for all algorithms.
        
        Args:
            experiments: Dictionary of {algorithm: metrics_dict}
            save: Whether to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for idx, (algo_name, metrics) in enumerate(experiments.items()):
            rounds = metrics.get('rounds', [])
            test_loss = metrics.get('test_loss', [])
            
            # Filter out None values
            loss_clean = [(r, l) for r, l in zip(rounds, test_loss) if l is not None]
            
            if loss_clean:
                rounds_c, loss_c = zip(*loss_clean)
                ax.plot(rounds_c, loss_c, marker='s', linewidth=2.5, label=algo_name,
                       color=self.colors[idx % len(self.colors)], markersize=5, alpha=0.8)
        
        ax.set_xlabel('Communication Rounds', fontsize=13, fontweight='bold')
        ax.set_ylabel('Test Loss', fontsize=13, fontweight='bold')
        ax.set_title('Algorithm Loss Comparison', fontsize=15, fontweight='bold')
        ax.legend(fontsize=11, loc='upper right', framealpha=0.95)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / 'loss_comparison.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Loss comparison saved to {filename}")
        
        return fig
    
    def plot_metrics_comparison_bars(self, stats_dict: Dict, save: bool = True) -> plt.Figure:
        """
        Create bar chart comparing key metrics across algorithms.
        
        Args:
            stats_dict: Dictionary of {algorithm_name: AlgorithmStats}
            save: Whether to save the figure
            
        Returns:
            matplotlib Figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        algo_names = list(stats_dict.keys())
        colors_list = self.colors[:len(algo_names)]
        
        # Best Accuracy
        best_accs = [stats_dict[name].best_accuracy for name in algo_names]
        axes[0, 0].bar(algo_names, best_accs, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[0, 0].set_ylabel('Accuracy', fontsize=11, fontweight='bold')
        axes[0, 0].set_title('Best Accuracy Achieved', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylim([0, 1.05])
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(best_accs):
            axes[0, 0].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
        
        # Final Accuracy
        final_accs = [stats_dict[name].final_accuracy for name in algo_names]
        axes[0, 1].bar(algo_names, final_accs, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[0, 1].set_ylabel('Accuracy', fontsize=11, fontweight='bold')
        axes[0, 1].set_title('Final Accuracy', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylim([0, 1.05])
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(final_accs):
            axes[0, 1].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
        
        # Convergence Rounds (95%)
        conv_rounds = [stats_dict[name].convergence_round_95 for name in algo_names]
        axes[1, 0].bar(algo_names, conv_rounds, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[1, 0].set_ylabel('Rounds', fontsize=11, fontweight='bold')
        axes[1, 0].set_title('Convergence Speed (95% of Best)', fontsize=12, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(conv_rounds):
            axes[1, 0].text(i, v + 1, f'{int(v)}', ha='center', fontweight='bold')
        
        # Accuracy Improvement
        improvements = [stats_dict[name].improvement for name in algo_names]
        axes[1, 1].bar(algo_names, improvements, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[1, 1].set_ylabel('Improvement', fontsize=11, fontweight='bold')
        axes[1, 1].set_title('Accuracy Improvement (Final - Initial)', fontsize=12, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        for i, v in enumerate(improvements):
            axes[1, 1].text(i, v + 0.01, f'{v:.3f}', ha='center', fontweight='bold')
        
        # Rotate x labels
        for ax in axes.flat:
            ax.set_xticklabels(algo_names, rotation=45, ha='right')
        
        plt.suptitle('Algorithm Metrics Comparison', fontsize=15, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / 'metrics_comparison_bars.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Metrics comparison (bars) saved to {filename}")
        
        return fig
    
    def plot_speedup_analysis(self, stats_dict: Dict, baseline: str = None, 
                             save: bool = True) -> plt.Figure:
        """
        Plot speedup relative to baseline algorithm.
        
        Args:
            stats_dict: Dictionary of {algorithm_name: AlgorithmStats}
            baseline: Baseline algorithm name (defaults to first algorithm)
            save: Whether to save the figure
            
        Returns:
            matplotlib Figure object
        """
        if baseline is None:
            baseline = list(stats_dict.keys())[0]
        
        if baseline not in stats_dict:
            print(f"Warning: Baseline algorithm '{baseline}' not found")
            return None
        
        baseline_conv = stats_dict[baseline].convergence_round_95
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        algo_names = []
        speedups = []
        colors_list = []
        
        for idx, (algo_name, stats) in enumerate(sorted(stats_dict.items())):
            if stats.convergence_round_95 > 0:
                speedup = baseline_conv / stats.convergence_round_95
            else:
                speedup = 1.0
            
            algo_names.append(algo_name)
            speedups.append(speedup)
            
            # Color baseline differently
            if algo_name == baseline:
                colors_list.append('red')
            else:
                colors_list.append(self.colors[idx % len(self.colors)])
        
        bars = ax.bar(algo_names, speedups, color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add baseline line
        ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Baseline', alpha=0.7)
        
        ax.set_ylabel('Speedup Factor', fontsize=12, fontweight='bold')
        ax.set_title(f'Convergence Speedup (Relative to {baseline})', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_xticklabels(algo_names, rotation=45, ha='right')
        
        # Add value labels
        for i, (bar, speedup) in enumerate(zip(bars, speedups)):
            height = bar.get_height()
            label = f'{speedup:.2f}x'
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                   label, ha='center', va='bottom', fontweight='bold')
        
        plt.legend(fontsize=11)
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f'speedup_vs_{baseline}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Speedup analysis saved to {filename}")
        
        return fig
    
    def plot_convergence_radar(self, stats_dict: Dict, save: bool = True) -> plt.Figure:
        """
        Create radar chart comparing algorithm characteristics.
        
        Args:
            stats_dict: Dictionary of {algorithm_name: AlgorithmStats}
            save: Whether to save the figure
            
        Returns:
            matplotlib Figure object
        """
        from math import pi
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Normalize metrics
        max_acc = max(s.best_accuracy for s in stats_dict.values())
        max_conv_rounds = max(s.convergence_round_95 for s in stats_dict.values())
        
        # Categories
        categories = ['Peak Accuracy', 'Convergence Speed', 'Stability']
        N = len(categories)
        
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=11)
        ax.set_ylim(0, 1)
        
        # Plot each algorithm
        for idx, (algo_name, stats) in enumerate(sorted(stats_dict.items())):
            values = [
                stats.best_accuracy / max_acc,  # Normalized accuracy
                1 - (stats.convergence_round_95 / max_conv_rounds),  # Inverse of convergence rounds
                stats.improvement  # Stability (improvement consistency)
            ]
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2.5, label=algo_name,
                   color=self.colors[idx % len(self.colors)], markersize=8)
            ax.fill(angles, values, alpha=0.15, color=self.colors[idx % len(self.colors)])
        
        ax.set_title('Algorithm Performance Profile', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
        ax.grid(True)
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / 'convergence_radar.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Radar chart saved to {filename}")
        
        return fig
    
    def plot_all_comparisons(self, experiments: Dict[str, Dict], stats_dict: Dict, 
                            baseline: str = None, save: bool = True):
        """
        Generate all comparison plots.
        
        Args:
            experiments: Dictionary of {algorithm: metrics_dict}
            stats_dict: Dictionary of {algorithm_name: AlgorithmStats}
            baseline: Baseline algorithm for speedup comparison
            save: Whether to save figures
        """
        print("\n" + "="*70)
        print("GENERATING COMPARISON VISUALIZATIONS")
        print("="*70)
        
        self.plot_accuracy_comparison(experiments, save)
        self.plot_loss_comparison(experiments, save)
        self.plot_metrics_comparison_bars(stats_dict, save)
        self.plot_speedup_analysis(stats_dict, baseline=baseline, save=save)
        
        try:
            self.plot_convergence_radar(stats_dict, save)
        except Exception as e:
            print(f"Note: Radar chart skipped ({e})")
        
        print("\n✓ All comparison visualizations generated!")
        print(f"✓ Saved to: {self.save_dir}\n")
        print("="*70 + "\n")
