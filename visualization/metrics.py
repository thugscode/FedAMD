# Author: Visualization Module
# Federated Learning Results Metrics Tracker

import json
import csv
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class MetricsTracker:
    """Track and store training metrics for federated learning experiments."""
    
    def __init__(self, experiment_name: str = None, save_dir: str = './results'):
        """
        Initialize metrics tracker.
        
        Args:
            experiment_name: Name of the experiment (auto-generated if None)
            save_dir: Directory to save metrics and logs
        """
        self.experiment_name = experiment_name or f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Metrics storage
        self.metrics = {
            'rounds': [],           # Communication rounds
            'train_loss': [],       # Training loss per round
            'test_loss': [],        # Test loss per round
            'test_acc': [],         # Test accuracy per round
            'train_acc': [],        # Training accuracy per round
            'client_participation': [],  # Number of clients participated
            'local_updates': [],    # Local iterations per round
            'communication_cost': []  # Communication cost per round
        }
        
        self.config = {}  # Store experiment configuration
        self.algorithm = None
        self.round_counter = 0
        
    def log_config(self, **kwargs):
        """Log experiment configuration."""
        self.config.update(kwargs)
        if 'method' in kwargs:
            self.algorithm = kwargs['method']
    
    def log_round(self, round_num: int, test_loss: float = None, test_acc: float = None,
                  train_loss: float = None, train_acc: float = None, 
                  num_clients: int = None, local_steps: int = None):
        """
        Log metrics for a single communication round.
        
        Args:
            round_num: Communication round number
            test_loss: Test loss
            test_acc: Test accuracy
            train_loss: Average training loss
            train_acc: Average training accuracy
            num_clients: Number of participating clients
            local_steps: Number of local update steps
        """
        self.round_counter = round_num
        
        self.metrics['rounds'].append(round_num)
        self.metrics['test_loss'].append(test_loss if test_loss is not None else None)
        self.metrics['test_acc'].append(test_acc if test_acc is not None else None)
        self.metrics['train_loss'].append(train_loss if train_loss is not None else None)
        self.metrics['train_acc'].append(train_acc if train_acc is not None else None)
        self.metrics['client_participation'].append(num_clients)
        self.metrics['local_updates'].append(local_steps)
    
    def add_communication_cost(self, round_num: int, cost: float):
        """Add communication cost for a round."""
        if round_num < len(self.metrics['rounds']):
            self.metrics['communication_cost'].append(cost)
    
    def get_best_accuracy(self) -> Tuple[int, float]:
        """Get best test accuracy and at which round."""
        accs = [a for a in self.metrics['test_acc'] if a is not None]
        if not accs:
            return None, None
        best_acc = max(accs)
        best_round = self.metrics['test_acc'].index(best_acc)
        return best_round, best_acc
    
    def get_convergence_round(self, threshold: float = 0.95) -> int:
        """Get round at which accuracy reaches threshold (normalized to [0, 1])."""
        accs = self.metrics['test_acc']
        best_acc = max([a for a in accs if a is not None])
        target = best_acc * threshold
        
        for round_num, acc in enumerate(accs):
            if acc is not None and acc >= target:
                return round_num
        return None
    
    def save_json(self) -> str:
        """Save metrics to JSON file."""
        output_file = self.save_dir / f"{self.experiment_name}_metrics.json"
        data = {
            'experiment': self.experiment_name,
            'algorithm': self.algorithm,
            'config': self.config,
            'metrics': self.metrics,
            'best_accuracy': self.get_best_accuracy(),
            'convergence_round': self.get_convergence_round(),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Metrics saved to {output_file}")
        return str(output_file)
    
    def save_csv(self) -> str:
        """Save metrics to CSV file."""
        output_file = self.save_dir / f"{self.experiment_name}_metrics.csv"
        
        # Get max length
        max_len = max(len(v) for v in self.metrics.values())
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.metrics.keys())
            
            for i in range(max_len):
                row = []
                for key in self.metrics.keys():
                    val = self.metrics[key][i] if i < len(self.metrics[key]) else ''
                    row.append(val)
                writer.writerow(row)
        
        print(f"✓ Metrics saved to {output_file}")
        return str(output_file)
    
    def summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        accs = [a for a in self.metrics['test_acc'] if a is not None]
        losses = [l for l in self.metrics['test_loss'] if l is not None]
        
        summary = {
            'algorithm': self.algorithm,
            'total_rounds': len(self.metrics['rounds']),
            'best_accuracy': max(accs) if accs else None,
            'final_accuracy': accs[-1] if accs else None,
            'best_round': self.get_best_accuracy()[0],
            'convergence_round_95': self.get_convergence_round(0.95),
            'avg_loss': sum(losses) / len(losses) if losses else None,
            'final_loss': losses[-1] if losses else None
        }
        return summary
    
    def print_summary(self):
        """Print summary statistics."""
        summary = self.summary()
        print("\n" + "="*60)
        print(f"Experiment: {self.experiment_name}")
        print(f"Algorithm: {summary['algorithm']}")
        print(f"Total Rounds: {summary['total_rounds']}")
        print(f"Best Accuracy: {summary['best_accuracy']:.4f} (Round {summary['best_round']})")
        print(f"Final Accuracy: {summary['final_accuracy']:.4f}")
        print(f"Avg Test Loss: {summary['avg_loss']:.4f}")
        print("="*60 + "\n")


class ExperimentComparison:
    """Compare multiple experiments."""
    
    def __init__(self, results_dir: str = './results'):
        self.results_dir = Path(results_dir)
        self.experiments = {}
    
    def load_experiment(self, filepath: str, name: str = None):
        """Load an experiment from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        exp_name = name or data.get('experiment', 'unnamed')
        self.experiments[exp_name] = data
        return exp_name
    
    def load_all_experiments(self):
        """Load all JSON files in results directory."""
        for json_file in self.results_dir.glob('*_metrics.json'):
            with open(json_file, 'r') as f:
                data = json.load(f)
                exp_name = data.get('experiment', json_file.stem)
                self.experiments[exp_name] = data
    
    def compare_algorithms(self) -> Dict[str, Dict]:
        """Compare key metrics across algorithms."""
        comparison = {}
        
        for exp_name, data in self.experiments.items():
            algo = data.get('algorithm', 'unknown')
            metrics = data.get('metrics', {})
            summary = data.get('summary', {})
            
            accs = [a for a in metrics.get('test_acc', []) if a is not None]
            
            comparison[algo] = {
                'experiments': comparison.get(algo, {}).get('experiments', 0) + 1,
                'best_accuracy': max(accs) if accs else None,
                'final_accuracy': accs[-1] if accs else None,
                'total_rounds': len(metrics.get('rounds', []))
            }
        
        return comparison
    
    def print_comparison(self):
        """Print comparison table."""
        comparison = self.compare_algorithms()
        
        print("\n" + "="*80)
        print(f"{'Algorithm':<20} {'Best Acc':<15} {'Final Acc':<15} {'Total Rounds':<15}")
        print("="*80)
        
        for algo, metrics in sorted(comparison.items()):
            best = f"{metrics['best_accuracy']:.4f}" if metrics['best_accuracy'] else "N/A"
            final = f"{metrics['final_accuracy']:.4f}" if metrics['final_accuracy'] else "N/A"
            rounds = metrics['total_rounds']
            print(f"{algo:<20} {best:<15} {final:<15} {rounds:<15}")
        
        print("="*80 + "\n")
