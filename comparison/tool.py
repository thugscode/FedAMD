# Experiment Comparison Tool
# Compare federated learning algorithms side-by-side with detailed metrics

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import pandas as pd


@dataclass
class AlgorithmStats:
    """Statistics for a single algorithm across experiments."""
    name: str
    num_experiments: int
    best_accuracy: float
    final_accuracy: float
    avg_accuracy: float
    best_round: int
    convergence_round_95: int
    avg_loss: float
    final_loss: float
    total_rounds: int
    improvement: float  # final - initial
    accuracy_trajectory: List[float]
    loss_trajectory: List[float]


class ComparisonTool:
    """Comprehensive tool for comparing federated learning algorithms."""
    
    def __init__(self, results_dir: str = './results'):
        """
        Initialize comparison tool.
        
        Args:
            results_dir: Directory containing experiment JSON files
        """
        self.results_dir = Path(results_dir)
        self.experiments = {}
        self.algorithms = {}
        self.stats = {}
    
    def load_experiments(self, pattern: str = '*_metrics.json') -> int:
        """
        Load all experiments matching pattern from results directory.
        
        Args:
            pattern: Glob pattern for JSON files (default: all metrics files)
            
        Returns:
            Number of experiments loaded
        """
        for json_file in self.results_dir.glob(pattern):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    exp_name = data.get('experiment', json_file.stem)
                    algorithm = data.get('algorithm', 'unknown')
                    
                    self.experiments[exp_name] = data
                    
                    if algorithm not in self.algorithms:
                        self.algorithms[algorithm] = []
                    self.algorithms[algorithm].append(exp_name)
            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")
        
        return len(self.experiments)
    
    def load_specific(self, filepath: str, name: str = None) -> bool:
        """
        Load a specific experiment from file.
        
        Args:
            filepath: Path to JSON file
            name: Optional custom name for experiment
            
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                exp_name = name or data.get('experiment', Path(filepath).stem)
                algorithm = data.get('algorithm', 'unknown')
                
                self.experiments[exp_name] = data
                
                if algorithm not in self.algorithms:
                    self.algorithms[algorithm] = []
                self.algorithms[algorithm].append(exp_name)
                
                return True
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return False
    
    def compute_statistics(self) -> Dict[str, AlgorithmStats]:
        """
        Compute comprehensive statistics for each algorithm.
        
        Returns:
            Dictionary of {algorithm_name: AlgorithmStats}
        """
        self.stats = {}
        
        for algo_name, exp_names in self.algorithms.items():
            accs_list = []
            losses_list = []
            best_accs = []
            convergence_rounds = []
            total_rounds_list = []
            
            for exp_name in exp_names:
                exp = self.experiments[exp_name]
                metrics = exp.get('metrics', {})
                
                accs = [a for a in metrics.get('test_acc', []) if a is not None]
                losses = [l for l in metrics.get('test_loss', []) if l is not None]
                
                if accs:
                    accs_list.append(accs)
                    best_accs.append(max(accs))
                    convergence_rounds.append(exp.get('convergence_round', 0))
                    total_rounds_list.append(len(metrics.get('rounds', [])))
                
                if losses:
                    losses_list.append(losses)
            
            # Calculate statistics
            if best_accs:
                best_accuracy = np.mean(best_accs)
                std_best = np.std(best_accs)
                
                # Average trajectory
                min_len = min(len(traj) for traj in accs_list) if accs_list else 0
                if min_len > 0:
                    avg_trajectory = np.mean([traj[:min_len] for traj in accs_list], axis=0).tolist()
                else:
                    avg_trajectory = []
                
                # Loss trajectory
                min_loss_len = min(len(traj) for traj in losses_list) if losses_list else 0
                if min_loss_len > 0:
                    avg_loss_trajectory = np.mean([traj[:min_loss_len] for traj in losses_list], axis=0).tolist()
                else:
                    avg_loss_trajectory = []
                
                # Get final values from first experiment
                first_exp = self.experiments[exp_names[0]]
                first_accs = [a for a in first_exp.get('metrics', {}).get('test_acc', []) if a is not None]
                first_losses = [l for l in first_exp.get('metrics', {}).get('test_loss', []) if l is not None]
                
                stats = AlgorithmStats(
                    name=algo_name,
                    num_experiments=len(exp_names),
                    best_accuracy=best_accuracy,
                    final_accuracy=first_accs[-1] if first_accs else 0,
                    avg_accuracy=np.mean(accs_list) if accs_list else 0,
                    best_round=int(np.mean([first_accs.index(max(first_accs)) for first_accs in accs_list if first_accs])) if accs_list else 0,
                    convergence_round_95=int(np.mean(convergence_rounds)) if convergence_rounds else 0,
                    avg_loss=np.mean(losses_list) if losses_list else 0,
                    final_loss=first_losses[-1] if first_losses else 0,
                    total_rounds=int(np.mean(total_rounds_list)) if total_rounds_list else 0,
                    improvement=first_accs[-1] - first_accs[0] if len(first_accs) > 1 else 0,
                    accuracy_trajectory=avg_trajectory,
                    loss_trajectory=avg_loss_trajectory
                )
                self.stats[algo_name] = stats
        
        return self.stats
    
    def create_comparison_table(self, metrics: List[str] = None) -> str:
        """
        Create formatted comparison table.
        
        Args:
            metrics: List of metrics to include. Defaults to key metrics.
            
        Returns:
            Formatted table string
        """
        if not self.stats:
            self.compute_statistics()
        
        if not metrics:
            metrics = ['best_accuracy', 'final_accuracy', 'convergence_round_95', 'improvement']
        
        # Find max widths
        algo_width = max(len(name) for name in self.stats.keys()) + 2
        algo_width = max(algo_width, 12)
        col_width = 15
        
        # Create table
        lines = []
        
        # Header
        header = f"{'Algorithm':<{algo_width}}"
        for metric in metrics:
            header += f"{metric:<{col_width}}"
        lines.append(header)
        lines.append("=" * len(header))
        
        # Data rows
        for algo_name, stats in sorted(self.stats.items()):
            row = f"{algo_name:<{algo_width}}"
            for metric in metrics:
                value = getattr(stats, metric, 'N/A')
                if isinstance(value, float):
                    if metric == 'improvement':
                        row += f"{value:>14.4f} "
                    else:
                        row += f"{value:>14.4f} "
                else:
                    row += f"{value:>14} "
            lines.append(row)
        
        return "\n".join(lines)
    
    def export_comparison_table(self, filepath: str = None, metrics: List[str] = None) -> str:
        """
        Export comparison table to text file.
        
        Args:
            filepath: Output file path. If None, creates in results/
            metrics: List of metrics to include
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = self.results_dir / 'comparison_table.txt'
        
        table = self.create_comparison_table(metrics)
        
        with open(filepath, 'w') as f:
            f.write("ALGORITHM COMPARISON REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Experiments loaded: {len(self.experiments)}\n")
            f.write(f"Algorithms compared: {len(self.stats)}\n\n")
            f.write(table)
        
        print(f"✓ Comparison table saved to {filepath}")
        return str(filepath)
    
    def create_dataframe(self) -> pd.DataFrame:
        """
        Create pandas DataFrame for easy analysis.
        
        Returns:
            DataFrame with algorithm statistics
        """
        if not self.stats:
            self.compute_statistics()
        
        data = []
        for algo_name, stats in self.stats.items():
            data.append({
                'Algorithm': stats.name,
                'Num Experiments': stats.num_experiments,
                'Best Accuracy': stats.best_accuracy,
                'Final Accuracy': stats.final_accuracy,
                'Avg Accuracy': stats.avg_accuracy,
                'Best Round': stats.best_round,
                'Convergence Round (95%)': stats.convergence_round_95,
                'Avg Loss': stats.avg_loss,
                'Final Loss': stats.final_loss,
                'Total Rounds': stats.total_rounds,
                'Improvement': stats.improvement
            })
        
        return pd.DataFrame(data)
    
    def export_csv(self, filepath: str = None) -> str:
        """
        Export comparison statistics to CSV.
        
        Args:
            filepath: Output file path
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = self.results_dir / 'comparison_statistics.csv'
        
        df = self.create_dataframe()
        df.to_csv(filepath, index=False)
        
        print(f"✓ Comparison statistics saved to {filepath}")
        return str(filepath)
    
    def print_detailed_report(self):
        """Print detailed comparison report."""
        if not self.stats:
            self.compute_statistics()
        
        print("\n" + "="*80)
        print("FEDERATED LEARNING ALGORITHM COMPARISON REPORT")
        print("="*80)
        print(f"\nDataset: Multiple experiments")
        print(f"Total experiments: {len(self.experiments)}")
        print(f"Algorithms compared: {len(self.stats)}\n")
        
        # Summary table
        print("SUMMARY METRICS")
        print("-"*80)
        print(f"{'Algorithm':<20} {'Best Acc':<15} {'Final Acc':<15} {'Convergence':<15}")
        print("-"*80)
        
        for algo_name, stats in sorted(self.stats.items()):
            print(f"{algo_name:<20} {stats.best_accuracy:>13.4f}  {stats.final_accuracy:>13.4f}  "
                  f"{stats.convergence_round_95:>13}")
        
        print("-"*80)
        
        # Detailed statistics
        print("\n\nDETAILED STATISTICS PER ALGORITHM")
        print("="*80)
        
        for algo_name, stats in sorted(self.stats.items()):
            print(f"\n{algo_name}")
            print("-"*80)
            print(f"  Number of experiments:        {stats.num_experiments}")
            print(f"  Best accuracy:                {stats.best_accuracy:.4f}")
            print(f"  Final accuracy:               {stats.final_accuracy:.4f}")
            print(f"  Average accuracy:             {stats.avg_accuracy:.4f}")
            print(f"  Accuracy improvement:         {stats.improvement:.4f}")
            print(f"  Best achieved at round:       {stats.best_round}")
            print(f"  Convergence at 95%:           {stats.convergence_round_95} rounds")
            print(f"  Average loss:                 {stats.avg_loss:.4f}")
            print(f"  Final loss:                   {stats.final_loss:.4f}")
            print(f"  Average total rounds:         {stats.total_rounds}")
        
        print("\n" + "="*80 + "\n")
    
    def get_best_algorithm(self, metric: str = 'best_accuracy') -> Tuple[str, float]:
        """
        Get best algorithm for a given metric.
        
        Args:
            metric: Metric to compare ('best_accuracy', 'convergence_round_95', etc.)
            
        Returns:
            Tuple of (algorithm_name, metric_value)
        """
        if not self.stats:
            self.compute_statistics()
        
        if metric == 'convergence_round_95':
            # Lower is better for convergence round
            best = min(self.stats.items(), key=lambda x: x[1].convergence_round_95)
        else:
            # Higher is better for accuracy
            best = max(self.stats.items(), key=lambda x: getattr(x[1], metric))
        
        return best[0], getattr(best[1], metric)
    
    def get_ranking(self, metric: str = 'best_accuracy') -> List[Tuple[str, float]]:
        """
        Get algorithms ranked by metric.
        
        Args:
            metric: Metric to rank by
            
        Returns:
            List of (algorithm_name, metric_value) sorted by rank
        """
        if not self.stats:
            self.compute_statistics()
        
        if metric == 'convergence_round_95':
            # Lower is better
            ranking = sorted(self.stats.items(), 
                            key=lambda x: x[1].convergence_round_95)
        else:
            # Higher is better for accuracy and improvement
            ranking = sorted(self.stats.items(), 
                            key=lambda x: getattr(x[1], metric), reverse=True)
        
        return [(name, getattr(stats, metric)) for name, stats in ranking]
    
    def print_rankings(self):
        """Print algorithm rankings for all key metrics."""
        if not self.stats:
            self.compute_statistics()
        
        metrics = [
            ('best_accuracy', 'Best Accuracy (Higher is Better)', False),
            ('final_accuracy', 'Final Accuracy (Higher is Better)', False),
            ('improvement', 'Accuracy Improvement (Higher is Better)', False),
            ('convergence_round_95', 'Convergence Speed (Lower is Better)', True),
            ('avg_loss', 'Average Loss (Lower is Better)', True)
        ]
        
        print("\n" + "="*80)
        print("ALGORITHM RANKINGS")
        print("="*80)
        
        for metric, description, reverse in metrics:
            print(f"\n{description}")
            print("-"*60)
            
            if reverse:
                sorted_items = sorted(self.stats.items(),
                                     key=lambda x: getattr(x[1], metric))
            else:
                sorted_items = sorted(self.stats.items(),
                                     key=lambda x: getattr(x[1], metric), reverse=True)
            
            for rank, (algo_name, stats) in enumerate(sorted_items, 1):
                value = getattr(stats, metric)
                if isinstance(value, float):
                    print(f"  {rank}. {algo_name:<20} {value:.4f}")
                else:
                    print(f"  {rank}. {algo_name:<20} {value}")
        
        print("\n" + "="*80 + "\n")
    
    def identify_strengths_weaknesses(self) -> Dict[str, Dict]:
        """
        Identify strengths and weaknesses of each algorithm.
        
        Returns:
            Dictionary with strengths/weaknesses for each algorithm
        """
        if not self.stats:
            self.compute_statistics()
        
        analysis = {}
        
        for algo_name, stats in self.stats.items():
            ranking = self.get_ranking()
            
            strengths = []
            weaknesses = []
            
            # Check rankings
            best_acc_rank = next(i for i, (n, _) in enumerate(self.get_ranking('best_accuracy'), 1) if n == algo_name)
            convergence_rank = next(i for i, (n, _) in enumerate(self.get_ranking('convergence_round_95'), 1) if n == algo_name)
            improvement_rank = next(i for i, (n, _) in enumerate(self.get_ranking('improvement'), 1) if n == algo_name)
            
            # Identify strengths
            if best_acc_rank == 1:
                strengths.append("Highest accuracy")
            if convergence_rank == 1:
                strengths.append("Fastest convergence")
            if improvement_rank == 1:
                strengths.append("Largest improvement")
            
            if not strengths:
                if best_acc_rank <= 2:
                    strengths.append(f"High accuracy (rank {best_acc_rank})")
                if convergence_rank <= 2:
                    strengths.append(f"Fast convergence (rank {convergence_rank})")
            
            # Identify weaknesses
            num_algos = len(self.stats)
            if best_acc_rank == num_algos:
                weaknesses.append("Lowest accuracy")
            if convergence_rank == num_algos:
                weaknesses.append("Slowest convergence")
            if improvement_rank == num_algos:
                weaknesses.append("Smallest improvement")
            
            analysis[algo_name] = {
                'strengths': strengths if strengths else ['Balanced performance'],
                'weaknesses': weaknesses if weaknesses else ['None identified'],
                'best_accuracy_rank': best_acc_rank,
                'convergence_rank': convergence_rank,
                'improvement_rank': improvement_rank
            }
        
        return analysis
    
    def print_analysis(self):
        """Print algorithm strengths and weaknesses analysis."""
        analysis = self.identify_strengths_weaknesses()
        
        print("\n" + "="*80)
        print("ALGORITHM ANALYSIS: STRENGTHS & WEAKNESSES")
        print("="*80)
        
        for algo_name, info in sorted(analysis.items()):
            print(f"\n{algo_name}")
            print("-"*60)
            print(f"  Strengths:")
            for strength in info['strengths']:
                print(f"    ✓ {strength}")
            print(f"  Weaknesses:")
            for weakness in info['weaknesses']:
                print(f"    ✗ {weakness}")
            print(f"  Rankings:")
            print(f"    - Best Accuracy:    #{info['best_accuracy_rank']}")
            print(f"    - Convergence:      #{info['convergence_rank']}")
            print(f"    - Improvement:      #{info['improvement_rank']}")
        
        print("\n" + "="*80 + "\n")
    
    def get_comparison_summary(self) -> Dict:
        """
        Get comprehensive comparison summary.
        
        Returns:
            Dictionary with all comparison metrics
        """
        if not self.stats:
            self.compute_statistics()
        
        best_by_accuracy, best_acc = self.get_best_algorithm('best_accuracy')
        best_by_convergence, best_conv = self.get_best_algorithm('convergence_round_95')
        best_by_improvement, best_imp = self.get_best_algorithm('improvement')
        
        return {
            'num_algorithms': len(self.stats),
            'num_experiments': len(self.experiments),
            'best_by_accuracy': (best_by_accuracy, best_acc),
            'best_by_convergence_speed': (best_by_convergence, best_conv),
            'best_by_improvement': (best_by_improvement, best_imp),
            'all_rankings': {
                'accuracy': self.get_ranking('best_accuracy'),
                'convergence': self.get_ranking('convergence_round_95'),
                'improvement': self.get_ranking('improvement')
            },
            'strengths_weaknesses': self.identify_strengths_weaknesses()
        }
