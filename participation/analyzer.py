# Client Participation Analyzer
# Analyze impact of partial client participation on convergence

import json
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

import numpy as np


@dataclass
class ParticipationAnalysis:
    """Analysis of participation impact on convergence."""
    algorithm_name: str
    total_clients: int
    avg_participation_rate: float
    min_participation_rate: float
    max_participation_rate: float
    participation_consistency: float  # std dev of participation
    convergence_rounds: int
    final_accuracy: float
    communication_efficiency: float  # accuracy per communication round
    robustness_score: float  # stability under varying participation


class ParticipationAnalyzer:
    """Analyze impact of client participation on convergence."""
    
    def __init__(self, results_dir: str = './results'):
        """
        Initialize analyzer.
        
        Args:
            results_dir: Directory containing experiment JSON files
        """
        self.results_dir = Path(results_dir)
        self.experiments = {}
        self.analyses = {}
    
    def load_experiment(self, filepath: str, name: str = None) -> bool:
        """
        Load an experiment JSON file.
        
        Args:
            filepath: Path to JSON file
            name: Optional custom name
            
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                exp_name = name or data.get('experiment', Path(filepath).stem)
                self.experiments[exp_name] = data
                return True
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return False
    
    def load_all_experiments(self, pattern: str = '*_metrics.json') -> int:
        """
        Load all experiments from directory.
        
        Args:
            pattern: Glob pattern for JSON files
            
        Returns:
            Number of experiments loaded
        """
        for json_file in self.results_dir.glob(pattern):
            self.load_experiment(json_file)
        return len(self.experiments)
    
    def analyze_participation_impact(self) -> Dict[str, ParticipationAnalysis]:
        """
        Analyze how client participation affects convergence.
        
        Returns:
            Dictionary of {algorithm_name: ParticipationAnalysis}
        """
        self.analyses = {}
        
        for exp_name, exp_data in self.experiments.items():
            metrics = exp_data.get('metrics', {})
            algorithm = exp_data.get('algorithm', 'unknown')
            config = exp_data.get('config', {})
            
            # Extract participation data
            rounds = metrics.get('rounds', [])
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            test_loss = metrics.get('test_loss', [])
            
            # Clean data
            accs = [a for a in test_acc if a is not None]
            
            if not accs or not client_participation:
                continue
            
            # Calculate statistics
            total_clients = config.get('num_clients', 20)
            
            # Participation rates
            participation_rates = []
            for num_participating in client_participation:
                if num_participating is not None and total_clients > 0:
                    rate = (num_participating / total_clients) * 100
                    participation_rates.append(rate)
            
            if not participation_rates:
                continue
            
            avg_participation = np.mean(participation_rates)
            min_participation = np.min(participation_rates)
            max_participation = np.max(participation_rates)
            participation_consistency = np.std(participation_rates)
            
            # Convergence metrics
            best_acc = max(accs)
            convergence_round = len(accs)
            for i, acc in enumerate(accs):
                if acc >= 0.95 * best_acc:
                    convergence_round = i
                    break
            
            final_accuracy = accs[-1] if accs else 0
            
            # Communications efficiency
            total_communications = len(client_participation)
            communication_efficiency = final_accuracy / total_communications if total_communications > 0 else 0
            
            # Robustness score (how stable under varying participation)
            # Higher consistency = higher robustness (unexpected, so inverse)
            robustness = 1.0 - (participation_consistency / 100.0)
            
            analysis = ParticipationAnalysis(
                algorithm_name=algorithm,
                total_clients=total_clients,
                avg_participation_rate=avg_participation,
                min_participation_rate=min_participation,
                max_participation_rate=max_participation,
                participation_consistency=participation_consistency,
                convergence_rounds=convergence_round,
                final_accuracy=final_accuracy,
                communication_efficiency=communication_efficiency,
                robustness_score=max(0, robustness)
            )
            
            if algorithm not in self.analyses:
                self.analyses[algorithm] = analysis
            else:
                # Average if multiple experiments for same algorithm
                prev = self.analyses[algorithm]
                self.analyses[algorithm] = ParticipationAnalysis(
                    algorithm_name=algorithm,
                    total_clients=total_clients,
                    avg_participation_rate=(prev.avg_participation_rate + avg_participation) / 2,
                    min_participation_rate=min(prev.min_participation_rate, min_participation),
                    max_participation_rate=max(prev.max_participation_rate, max_participation),
                    participation_consistency=(prev.participation_consistency + participation_consistency) / 2,
                    convergence_rounds=(prev.convergence_rounds + convergence_round) // 2,
                    final_accuracy=(prev.final_accuracy + final_accuracy) / 2,
                    communication_efficiency=(prev.communication_efficiency + communication_efficiency) / 2,
                    robustness_score=(prev.robustness_score + robustness) / 2
                )
        
        return self.analyses
    
    def get_participation_impact(self) -> Dict[str, Dict]:
        """
        Get impact of participation rate on convergence.
        
        Returns:
            Dictionary with participation impact analysis
        """
        impact = {}
        
        for exp_name, exp_data in self.experiments.items():
            metrics = exp_data.get('metrics', {})
            algorithm = exp_data.get('algorithm', 'unknown')
            
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            
            accs = [a for a in test_acc if a is not None]
            if not accs or not client_participation:
                continue
            
            # Calculate correlation between participation and accuracy
            valid_pairs = [(p, a) for p, a in zip(client_participation, accs) 
                          if p is not None and a is not None]
            
            if len(valid_pairs) > 1:
                parts, accs_valid = zip(*valid_pairs)
                correlation = np.corrcoef(parts, accs_valid)[0, 1]
                
                impact[algorithm] = {
                    'participation_accuracy_correlation': correlation,
                    'avg_participation': np.mean([p for p in client_participation if p is not None]),
                    'final_accuracy': accs[-1] if accs else 0,
                    'best_accuracy': max(accs) if accs else 0
                }
        
        return impact
    
    def analyze_full_vs_partial(self, threshold: float = 0.8) -> Dict[str, Dict]:
        """
        Compare performance with full vs partial participation.
        
        Args:
            threshold: Participation threshold (0.8 = 80% considered 'full')
            
        Returns:
            Dictionary comparing full vs partial participation
        """
        results = {}
        
        for exp_name, exp_data in self.experiments.items():
            metrics = exp_data.get('metrics', {})
            algorithm = exp_data.get('algorithm', 'unknown')
            config = exp_data.get('config', {})
            
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            
            total_clients = config.get('num_clients', 20)
            
            if not client_participation or not test_acc:
                continue
            
            # Categorize rounds
            full_participation_accs = []
            partial_participation_accs = []
            
            for num_part, acc in zip(client_participation, test_acc):
                if num_part is not None and acc is not None:
                    participation_rate = num_part / total_clients if total_clients > 0 else 0
                    
                    if participation_rate >= threshold:
                        full_participation_accs.append(acc)
                    else:
                        partial_participation_accs.append(acc)
            
            # Calculate metrics
            if full_participation_accs:
                full_avg_acc = np.mean(full_participation_accs)
                full_best_acc = max(full_participation_accs)
            else:
                full_avg_acc = None
                full_best_acc = None
            
            if partial_participation_accs:
                partial_avg_acc = np.mean(partial_participation_accs)
                partial_best_acc = max(partial_participation_accs)
            else:
                partial_avg_acc = None
                partial_best_acc = None
            
            if algorithm not in results:
                results[algorithm] = {
                    'full_participation': {
                        'avg_accuracy': full_avg_acc,
                        'best_accuracy': full_best_acc,
                        'num_rounds': len(full_participation_accs)
                    },
                    'partial_participation': {
                        'avg_accuracy': partial_avg_acc,
                        'best_accuracy': partial_best_acc,
                        'num_rounds': len(partial_participation_accs)
                    },
                    'degradation': {
                        'avg_accuracy': (full_avg_acc - partial_avg_acc) if (full_avg_acc and partial_avg_acc) else None,
                        'best_accuracy': (full_best_acc - partial_best_acc) if (full_best_acc and partial_best_acc) else None
                    }
                }
        
        return results
    
    def get_participation_variance_impact(self) -> Dict[str, Dict]:
        """
        Analyze impact of participation variance on convergence.
        
        Returns:
            Dictionary with variance impact analysis
        """
        variance_impact = {}
        
        for exp_name, exp_data in self.experiments.items():
            metrics = exp_data.get('metrics', {})
            algorithm = exp_data.get('algorithm', 'unknown')
            
            client_participation = metrics.get('client_participation', [])
            test_acc = metrics.get('test_acc', [])
            
            accs = [a for a in test_acc if a is not None]
            
            if not accs or not client_participation:
                continue
            
            # Calculate participation variance
            valid_participation = [p for p in client_participation if p is not None]
            if len(valid_participation) < 2:
                continue
            
            participation_std = np.std(valid_participation)
            participation_mean = np.mean(valid_participation)
            participation_cv = participation_std / participation_mean if participation_mean > 0 else 0
            
            # Accuracy variance
            accuracy_std = np.std(accs)
            accuracy_mean = np.mean(accs)
            
            if algorithm not in variance_impact:
                variance_impact[algorithm] = {
                    'participation_std': participation_std,
                    'participation_cv': participation_cv,
                    'accuracy_std': accuracy_std,
                    'accuracy_progression': accs,
                    'participation_progression': valid_participation,
                    'final_accuracy': accs[-1] if accs else 0
                }
        
        return variance_impact
    
    def print_participation_report(self):
        """Print participation impact report."""
        if not self.analyses:
            self.analyze_participation_impact()
        
        print("\n" + "="*80)
        print("CLIENT PARTICIPATION IMPACT ANALYSIS")
        print("="*80)
        
        print("\nPARTICIPATION STATISTICS")
        print("-"*80)
        print(f"{'Algorithm':<20} {'Avg Participation':<20} {'Min':<10} {'Max':<10}")
        print("-"*80)
        
        for algo_name, analysis in sorted(self.analyses.items()):
            avg_part = analysis.avg_participation_rate
            min_part = analysis.min_participation_rate
            max_part = analysis.max_participation_rate
            print(f"{algo_name:<20} {avg_part:>17.1f}% {min_part:>9.1f}% {max_part:>9.1f}%")
        
        print("\nCONVERGENCE IMPACT")
        print("-"*80)
        print(f"{'Algorithm':<20} {'Convergence Rounds':<20} {'Final Accuracy':<20}")
        print("-"*80)
        
        for algo_name, analysis in sorted(self.analyses.items()):
            print(f"{algo_name:<20} {analysis.convergence_rounds:<20} {analysis.final_accuracy:>18.4f}")
        
        print("\nCOMMUNICATION EFFICIENCY (Accuracy per Communication Round)")
        print("-"*80)
        
        for algo_name, analysis in sorted(self.analyses.items()):
            eff = analysis.communication_efficiency
            print(f"{algo_name:<20} {eff:.6f}")
        
        print("\nROBUSTNESS TO PARTICIPATION VARIANCE")
        print("-"*80)
        
        for algo_name, analysis in sorted(self.analyses.items()):
            robustness = analysis.robustness_score
            consistency = analysis.participation_consistency
            print(f"{algo_name:<20} Robustness: {robustness:.3f}  Consistency Std: {consistency:.3f}")
        
        print("\n" + "="*80 + "\n")
    
    def print_full_vs_partial_analysis(self, threshold: float = 0.8):
        """Print full vs partial participation analysis."""
        results = self.analyze_full_vs_partial(threshold)
        
        print("\n" + "="*80)
        print(f"FULL VS PARTIAL PARTICIPATION ANALYSIS (Threshold: {threshold*100:.0f}%)")
        print("="*80)
        
        for algo_name, data in sorted(results.items()):
            print(f"\n{algo_name}")
            print("-"*80)
            
            full = data['full_participation']
            partial = data['partial_participation']
            deg = data['degradation']
            
            print(f"Full Participation (≥{threshold*100:.0f}%):")
            print(f"  Average Accuracy: {full['avg_accuracy']:.4f}" if full['avg_accuracy'] else "  Average Accuracy: N/A")
            print(f"  Best Accuracy:    {full['best_accuracy']:.4f}" if full['best_accuracy'] else "  Best Accuracy:    N/A")
            print(f"  Rounds:           {full['num_rounds']}")
            
            print(f"Partial Participation (<{threshold*100:.0f}%):")
            print(f"  Average Accuracy: {partial['avg_accuracy']:.4f}" if partial['avg_accuracy'] else "  Average Accuracy: N/A")
            print(f"  Best Accuracy:    {partial['best_accuracy']:.4f}" if partial['best_accuracy'] else "  Best Accuracy:    N/A")
            print(f"  Rounds:           {partial['num_rounds']}")
            
            print(f"Degradation:")
            if deg['avg_accuracy']:
                print(f"  Average Accuracy: {deg['avg_accuracy']:.4f} ({-deg['avg_accuracy']/full['avg_accuracy']*100:.1f}%)" if full['avg_accuracy'] else "  Average Accuracy: N/A")
            if deg['best_accuracy']:
                print(f"  Best Accuracy:    {deg['best_accuracy']:.4f}" if deg['best_accuracy'] else "  Best Accuracy:    N/A")
        
        print("\n" + "="*80 + "\n")
    
    def print_participation_impact(self):
        """Print participation impact analysis."""
        impact = self.get_participation_impact()
        
        print("\n" + "="*80)
        print("PARTICIPATION-ACCURACY CORRELATION")
        print("="*80)
        
        print(f"\n{'Algorithm':<20} {'Correlation':<20} {'Avg Participation':<20}")
        print("-"*80)
        
        for algo_name, data in sorted(impact.items()):
            corr = data['participation_accuracy_correlation']
            avg_part = data['avg_participation']
            
            if not np.isnan(corr):
                print(f"{algo_name:<20} {corr:>18.3f}  {avg_part:>18.1f} clients")
            else:
                print(f"{algo_name:<20} {'N/A':>18}  {avg_part:>18.1f} clients")
        
        print("\nInterpretation:")
        print("  Correlation > 0.7: High impact of participation on accuracy")
        print("  Correlation 0.3-0.7: Moderate impact")
        print("  Correlation < 0.3: Low impact (robust to dropout)")
        
        print("\n" + "="*80 + "\n")
    
    def get_participation_recommendations(self) -> Dict[str, str]:
        """
        Generate recommendations based on participation analysis.
        
        Returns:
            Dictionary of {algorithm: recommendation}
        """
        if not self.analyses:
            self.analyze_participation_impact()
        
        recommendations = {}
        
        for algo_name, analysis in self.analyses.items():
            rec = f"{algo_name}: "
            
            # Based on robustness
            if analysis.robustness_score > 0.8:
                rec += "Highly robust to participation variance. "
            elif analysis.robustness_score > 0.5:
                rec += "Moderately robust to participation variance. "
            else:
                rec += "Sensitive to participation variance. "
            
            # Based on efficiency
            if analysis.communication_efficiency > 0.004:
                rec += "Excellent communication efficiency. "
            elif analysis.communication_efficiency > 0.002:
                rec += "Good communication efficiency. "
            else:
                rec += "Lower communication efficiency. "
            
            # Based on participation rate needed
            if analysis.avg_participation_rate > 80:
                rec += "Requires high participation rate."
            elif analysis.avg_participation_rate > 50:
                rec += "Works with moderate participation rates."
            else:
                rec += "Can work with very low participation rates."
            
            recommendations[algo_name] = rec
        
        return recommendations
    
    def print_recommendations(self):
        """Print participation recommendations for each algorithm."""
        recommendations = self.get_participation_recommendations()
        
        print("\n" + "="*80)
        print("ALGORITHM RECOMMENDATIONS BASED ON PARTICIPATION IMPACT")
        print("="*80)
        
        for algo_name, rec in sorted(recommendations.items()):
            print(f"\n{algo_name}")
            print("-"*80)
            print(rec)
        
        print("\n" + "="*80 + "\n")
    
    def get_optimal_participation_rate(self) -> Dict[str, float]:
        """
        Estimate optimal participation rate for each algorithm.
        
        Returns:
            Dictionary of {algorithm: optimal_rate}
        """
        if not self.analyses:
            self.analyze_participation_impact()
        
        optimal_rates = {}
        
        for algo_name, analysis in self.analyses.items():
            # Optimal = balance between efficiency and accuracy
            # Consider participation vs communication rounds vs accuracy
            
            efficiency_factor = analysis.communication_efficiency
            accuracy_factor = analysis.final_accuracy
            convergence_factor = 1.0 / (analysis.convergence_rounds + 1)
            
            # Weighted combination
            overall_score = (efficiency_factor * 0.3 + 
                            accuracy_factor * 0.5 + 
                            convergence_factor * 0.2)
            
            # Estimate optimal participation based on analysis
            optimal_participation = min(100, max(20, analysis.avg_participation_rate * 0.9))
            
            optimal_rates[algo_name] = optimal_participation
        
        return optimal_rates
    
    def print_optimal_rates(self):
        """Print optimal participation rates."""
        optimal = self.get_optimal_participation_rate()
        
        print("\n" + "="*80)
        print("ESTIMATED OPTIMAL PARTICIPATION RATES")
        print("="*80)
        
        print(f"\n{'Algorithm':<20} {'Current Avg':<20} {'Recommended':<20} {'Potential Savings':<20}")
        print("-"*80)
        
        for algo_name, opt_rate in sorted(optimal.items()):
            if algo_name in self.analyses:
                current = self.analyses[algo_name].avg_participation_rate
                savings = current - opt_rate
                print(f"{algo_name:<20} {current:>18.1f}% {opt_rate:>18.1f}% {savings:>18.1f}%")
        
        print("\nNote: Recommended rates aim to maintain accuracy while reducing participation overhead.")
        print("\n" + "="*80 + "\n")
    
    def export_participation_metrics(self, filepath: str = None) -> str:
        """
        Export participation metrics to JSON.
        
        Args:
            filepath: Output file path
            
        Returns:
            Path to saved file
        """
        if filepath is None:
            filepath = self.results_dir / 'participation_analysis.json'
        
        if not self.analyses:
            self.analyze_participation_impact()
        
        export_data = {
            'participation_analysis': {
                algo: {
                    'total_clients': analysis.total_clients,
                    'avg_participation_rate': analysis.avg_participation_rate,
                    'min_participation_rate': analysis.min_participation_rate,
                    'max_participation_rate': analysis.max_participation_rate,
                    'participation_consistency': analysis.participation_consistency,
                    'convergence_rounds': analysis.convergence_rounds,
                    'final_accuracy': analysis.final_accuracy,
                    'communication_efficiency': analysis.communication_efficiency,
                    'robustness_score': analysis.robustness_score
                }
                for algo, analysis in self.analyses.items()
            },
            'full_vs_partial': self.analyze_full_vs_partial(),
            'participation_impact': self.get_participation_impact(),
            'optimal_rates': self.get_optimal_participation_rate()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Participation analysis exported to {filepath}")
        return str(filepath)
