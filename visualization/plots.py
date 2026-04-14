# Visualization plotting utilities for federated learning results

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import json


class ResultsVisualizer:
    """Create visualizations for federated learning metrics."""
    
    def __init__(self, figsize: tuple = (12, 8), style: str = 'seaborn-v0_8-darkgrid'):
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
            pass  # Fallback if style not available
        
        self.colors = plt.cm.Set2(np.linspace(0, 1, 8))
        self.save_dir = Path('./results/plots')
        self.save_dir.mkdir(parents=True, exist_ok=True)
    
    def plot_accuracy_curves(self, metrics_dict: Dict, experiment_name: str = None, 
                            save: bool = True) -> plt.Figure:
        """
        Plot test and training accuracy over communication rounds.
        
        Args:
            metrics_dict: Dictionary with 'rounds', 'test_acc', 'train_acc' keys
            experiment_name: Name for the plot
            save: Whether to save the figure
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        rounds = metrics_dict.get('rounds', [])
        test_acc = metrics_dict.get('test_acc', [])
        train_acc = metrics_dict.get('train_acc', [])
        
        # Filter out None values
        test_acc_clean = [(r, a) for r, a in zip(rounds, test_acc) if a is not None]
        train_acc_clean = [(r, a) for r, a in zip(rounds, train_acc) if a is not None]
        
        if test_acc_clean:
            rounds_t, acc_t = zip(*test_acc_clean)
            ax.plot(rounds_t, acc_t, marker='o', linewidth=2.5, label='Test Accuracy', 
                   color=self.colors[0], markersize=6)
        
        if train_acc_clean:
            rounds_tr, acc_tr = zip(*train_acc_clean)
            ax.plot(rounds_tr, acc_tr, marker='s', linewidth=2, label='Train Accuracy', 
                   color=self.colors[1], markersize=5, alpha=0.8)
        
        ax.set_xlabel('Communication Rounds', fontsize=12, fontweight='bold')
        ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
        ax.set_title(experiment_name or 'Accuracy Over Communication Rounds', 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, loc='lower right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f"accuracy_{experiment_name or 'default'}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Accuracy plot saved to {filename}")
        
        return fig
    
    def plot_loss_curves(self, metrics_dict: Dict, experiment_name: str = None, 
                        save: bool = True) -> plt.Figure:
        """
        Plot training and test loss over communication rounds.
        
        Args:
            metrics_dict: Dictionary with 'rounds', 'train_loss', 'test_loss' keys
            experiment_name: Name for the plot
            save: Whether to save the figure
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        rounds = metrics_dict.get('rounds', [])
        train_loss = metrics_dict.get('train_loss', [])
        test_loss = metrics_dict.get('test_loss', [])
        
        # Filter out None values
        train_loss_clean = [(r, l) for r, l in zip(rounds, train_loss) if l is not None]
        test_loss_clean = [(r, l) for r, l in zip(rounds, test_loss) if l is not None]
        
        if train_loss_clean:
            rounds_tr, loss_tr = zip(*train_loss_clean)
            ax.plot(rounds_tr, loss_tr, marker='s', linewidth=2, label='Train Loss', 
                   color=self.colors[2], markersize=5)
        
        if test_loss_clean:
            rounds_t, loss_t = zip(*test_loss_clean)
            ax.plot(rounds_t, loss_t, marker='o', linewidth=2.5, label='Test Loss', 
                   color=self.colors[3], markersize=6)
        
        ax.set_xlabel('Communication Rounds', fontsize=12, fontweight='bold')
        ax.set_ylabel('Loss', fontsize=12, fontweight='bold')
        ax.set_title(experiment_name or 'Loss Over Communication Rounds', 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, loc='upper right')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f"loss_{experiment_name or 'default'}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Loss plot saved to {filename}")
        
        return fig
    
    def plot_comparison(self, experiments: Dict[str, Dict], metric: str = 'test_acc', 
                       save: bool = True) -> plt.Figure:
        """
        Compare multiple experiments on the same plot.
        
        Args:
            experiments: Dictionary of {exp_name: metrics_dict}
            metric: Metric to plot ('test_acc', 'train_acc', 'test_loss', etc.)
            save: Whether to save the figure
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for idx, (exp_name, metrics) in enumerate(experiments.items()):
            rounds = metrics.get('rounds', [])
            values = metrics.get(metric, [])
            
            # Filter out None values
            values_clean = [(r, v) for r, v in zip(rounds, values) if v is not None]
            
            if values_clean:
                rounds_c, vals_c = zip(*values_clean)
                ax.plot(rounds_c, vals_c, marker='o', linewidth=2.5, 
                       label=exp_name, color=self.colors[idx % len(self.colors)], 
                       markersize=6)
        
        xlabel = 'Communication Rounds'
        ylabel = metric.replace('_', ' ').title()
        
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
        ax.set_title(f'Algorithm Comparison: {ylabel}', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f"comparison_{metric}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Comparison plot saved to {filename}")
        
        return fig
    
    def plot_convergence_analysis(self, metrics_dict: Dict, experiment_name: str = None, 
                                 save: bool = True) -> plt.Figure:
        """
        Plot convergence analysis with best accuracy and convergence round highlighted.
        
        Args:
            metrics_dict: Dictionary with metrics
            experiment_name: Name for the plot
            save: Whether to save the figure
                
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        rounds = metrics_dict.get('rounds', [])
        test_acc = metrics_dict.get('test_acc', [])
        
        # Filter out None values
        test_acc_clean = [(r, a) for r, a in zip(rounds, test_acc) if a is not None]
        
        if not test_acc_clean:
            print("No test accuracy data available")
            return fig
        
        rounds_t, acc_t = zip(*test_acc_clean)
        
        # Plot accuracy
        ax.plot(rounds_t, acc_t, marker='o', linewidth=2.5, label='Test Accuracy', 
               color=self.colors[0], markersize=7)
        
        # Find and mark best accuracy
        best_idx = np.argmax(acc_t)
        best_round = rounds_t[best_idx]
        best_acc = acc_t[best_idx]
        
        ax.plot(best_round, best_acc, marker='*', markersize=20, color='red', 
               label=f'Best: {best_acc:.4f} @ Round {best_round}', zorder=5)
        
        # Mark 95% convergence
        target_acc = best_acc * 0.95
        convergence_found = False
        for r, a in zip(rounds_t, acc_t):
            if a >= target_acc:
                ax.axvline(x=r, color='green', linestyle='--', alpha=0.7, 
                          label=f'95% Convergence @ Round {r}')
                convergence_found = True
                break
        
        ax.set_xlabel('Communication Rounds', fontsize=12, fontweight='bold')
        ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
        ax.set_title(experiment_name or 'Convergence Analysis', 
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=10, loc='lower right')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1.05])
        
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f"convergence_{experiment_name or 'default'}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Convergence plot saved to {filename}")
        
        return fig
    
    def plot_communication_efficiency(self, metrics_dict: Dict, experiment_name: str = None,
                                     save: bool = True) -> plt.Figure:
        """
        Plot communication efficiency metrics.
        
        Args:
            metrics_dict: Dictionary with metrics
            experiment_name: Name for the plot
            save: Whether to save the figure
        
        Returns:
            matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        rounds = metrics_dict.get('rounds', [])
        test_acc = metrics_dict.get('test_acc', [])
        client_participation = metrics_dict.get('client_participation', [])
        
        # Filter out None values
        test_acc_clean = [(r, a) for r, a in zip(rounds, test_acc) if a is not None]
        
        if test_acc_clean:
            rounds_t, acc_t = zip(*test_acc_clean)
            ax1.plot(rounds_t, acc_t, marker='o', linewidth=2.5, color=self.colors[0])
            ax1.set_xlabel('Communication Rounds', fontsize=11, fontweight='bold')
            ax1.set_ylabel('Test Accuracy', fontsize=11, fontweight='bold')
            ax1.set_title('Accuracy Progress', fontsize=12, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim([0, 1.05])
        
        # Client participation
        if client_participation:
            part_clean = [(r, p) for r, p in zip(rounds, client_participation) if p is not None]
            if part_clean:
                rounds_p, part_p = zip(*part_clean)
                ax2.bar(rounds_p, part_p, color=self.colors[1], alpha=0.7, edgecolor='black')
                ax2.set_xlabel('Communication Rounds', fontsize=11, fontweight='bold')
                ax2.set_ylabel('Number of Participating Clients', fontsize=11, fontweight='bold')
                ax2.set_title('Client Participation', fontsize=12, fontweight='bold')
                ax2.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle(experiment_name or 'Communication Efficiency', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save:
            filename = self.save_dir / f"efficiency_{experiment_name or 'default'}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Efficiency plot saved to {filename}")
        
        return fig
    
    def plot_all(self, metrics_dict: Dict, experiment_name: str = None, save: bool = True):
        """
        Generate all plots for an experiment.
        
        Args:
            metrics_dict: Dictionary with metrics
            experiment_name: Name for the plots
            save: Whether to save figures
        """
        print(f"\nGenerating visualizations for {experiment_name}...")
        self.plot_accuracy_curves(metrics_dict, experiment_name, save)
        self.plot_loss_curves(metrics_dict, experiment_name, save)
        self.plot_convergence_analysis(metrics_dict, experiment_name, save)
        self.plot_communication_efficiency(metrics_dict, experiment_name, save)
        print("✓ All visualizations generated!\n")
