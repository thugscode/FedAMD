# Client Participation Analyzer - Complete Guide

## Overview

The **Client Participation Analyzer** is a comprehensive tool for analyzing how partial client participation affects convergence in federated learning. It helps you understand:

- **Impact of participation rates** on model accuracy and convergence speed
- **Robustness** of algorithms to varying participation levels
- **Communication efficiency** in relation to participation levels
- **Degradation** when participation is low vs high
- **Optimal participation rates** for each algorithm

## Why Client Participation Analysis Matters

In federated learning, not all clients participate in every round due to:
- Device availability/dropout
- Network connectivity issues
- Stragglers (slow devices)
- Battery constraints
- Privacy policies limiting participation

The Client Participation Analyzer helps answer:
- Which algorithms are most robust to dropouts?
- How much does performance degrade with 50% participation vs 100%?
- What's the minimum participation rate needed for good convergence?
- Which algorithm provides best accuracy per communication round?

## Installation & Setup

### 1. Ensure Metrics Are Tracked

First, enable client participation tracking in your training script:

```python
from visualization import MetricsTracker

tracker = MetricsTracker()
tracker.log_config(
    algorithm='FedAvg',
    num_clients=20,
    num_rounds=200,
    local_steps=5
)

# For each round:
participating_clients = selected_clients  # List of clients in this round
tracker.log_round(
    round_num=round_id,
    test_loss=test_loss,
    test_acc=test_accuracy,
    train_loss=train_loss,
    train_acc=train_accuracy,
    num_clients=len(participating_clients)  # KEY: participation tracking
)

# Save results
tracker.save_json()
tracker.save_csv()
```

### 2. Use the Analyzer

```python
from participation import ParticipationAnalyzer

analyzer = ParticipationAnalyzer('./results')
analyzer.load_all_experiments()
analyses = analyzer.analyze_participation_impact()
```

## Core Features

### 1. Participation Analysis

**What it measures:**
- Average participation rate across all rounds
- Minimum and maximum participation (worst and best cases)
- Consistency/variance of participation
- How these relate to convergence and accuracy

**Key method:**
```python
analyses = analyzer.analyze_participation_impact()

# Access results
for algo_name, analysis in analyses.items():
    print(f"{algo_name}:")
    print(f"  Avg participation: {analysis.avg_participation_rate:.1f}%")
    print(f"  Convergence rounds: {analysis.convergence_rounds}")
    print(f"  Final accuracy: {analysis.final_accuracy:.4f}")
    print(f"  Robustness: {analysis.robustness_score:.3f}")
```

### 2. Full vs Partial Participation Comparison

**What it measures:**
- Performance when ≥80% clients participate (full)
- Performance when <80% clients participate (partial)
- Accuracy degradation between the two

**Key method:**
```python
full_vs_partial = analyzer.analyze_full_vs_partial(threshold=0.8)

for algo, data in full_vs_partial.items():
    full = data['full_participation']
    partial = data['partial_participation']
    
    print(f"{algo}:")
    print(f"  Full (≥80%):   {full['avg_accuracy']:.4f}")
    print(f"  Partial (<80%): {partial['avg_accuracy']:.4f}")
    print(f"  Loss: {full['avg_accuracy'] - partial['avg_accuracy']:.4f}")
```

### 3. Participation-Accuracy Correlation

**What it measures:**
- How strongly does participation rate correlate with accuracy?
- High correlation = sensitive to dropouts
- Low correlation = robust to dropouts

**Key method:**
```python
impact = analyzer.get_participation_impact()

for algo, data in impact.items():
    corr = data['participation_accuracy_correlation']
    
    if corr > 0.7:
        print(f"{algo}: HIGH impact (sensitive to dropout)")
    elif corr < 0.3:
        print(f"{algo}: LOW impact (robust to dropout)")
```

### 4. Variance Analysis

**What it measures:**
- Variability of participation across rounds
- How does this variance affect accuracy progression?
- Algorithms with stable participation vs variable participation

**Key method:**
```python
variance = analyzer.get_participation_variance_impact()

for algo, data in variance.items():
    print(f"{algo}:")
    print(f"  Participation CV: {data['participation_cv']:.3f}")
    print(f"  Accuracy Std Dev: {data['accuracy_std']:.4f}")
```

### 5. Communication Efficiency

**What it measures:**
- How much accuracy is gained per communication round?
- Combines participation patterns with convergence speed
- Key for communication-constrained scenarios

**Calculation:**
```
Communication Efficiency = Final Accuracy / Total Communication Rounds
```

### 6. Robustness Scoring

**What it measures:**
- How stable is the algorithm under varying participation?
- Accounts for participation variance and impact on accuracy
- Score from 0 (fragile) to 1 (very robust)

**Interpretation:**
- **> 0.8**: Excellent robustness
- **0.5-0.8**: Good robustness
- **< 0.5**: Fair robustness, sensitive to perturbations

## Output Metrics

### ParticipationAnalysis Dataclass

```python
@dataclass
class ParticipationAnalysis:
    algorithm_name: str           # Algorithm name
    total_clients: int            # Total in system
    avg_participation_rate: float # Average % participating
    min_participation_rate: float # Minimum participation
    max_participation_rate: float # Maximum participation
    participation_consistency: float  # Std dev of participation
    convergence_rounds: int       # Rounds to 95% best accuracy
    final_accuracy: float         # Final model accuracy
    communication_efficiency: float # Accuracy per round
    robustness_score: float       # 0-1 scale, higher is better
```

### Exported JSON Structure

```json
{
  "participation_analysis": {
    "FedAvg": {
      "total_clients": 20,
      "avg_participation_rate": 85.5,
      "min_participation_rate": 60.0,
      "max_participation_rate": 100.0,
      "participation_consistency": 10.5,
      "convergence_rounds": 45,
      "final_accuracy": 0.8234,
      "communication_efficiency": 0.00548,
      "robustness_score": 0.876
    }
  },
  "full_vs_partial": { ... },
  "participation_impact": { ... },
  "optimal_rates": { ... }
}
```

## Visualizations

### 1. Participation Over Time
Shows how client participation changes across training rounds for each algorithm.

**Insight:** Identify algorithms that maintain consistent participation vs those with variable participation.

### 2. Accuracy vs Participation
Scatter plot showing relationship between participation rate (x-axis) and accuracy (y-axis).

**Insight:** See how sensitive each algorithm is to participation changes.

### 3. Participation Variance Impact
Two-panel visualization:
- Left: Final accuracy vs participation coefficient of variation
- Right: How participation changes across rounds

**Insight:** Understand impact of participation variability on performance.

### 4. Full vs Partial Participation Comparison
Bar charts comparing average and best accuracy:
- Green bars: Full participation (≥80%)
- Red bars: Partial participation (<80%)

**Insight:** Quantify performance degradation with lower participation.

### 5. Robustness Profiles
Four-panel visualization:
- Robustness scores
- Communication efficiency
- Participation consistency
- Average participation needed

**Insight:** Comprehensive view of each algorithm's participation profile.

### 6. Participation Impact Heatmap
Color-coded grid showing accuracy at different participation rate ranges.

**Insight:** Quickly identify which participation levels affect which algorithms.

## Usage Patterns

### Pattern 1: Basic Analysis

```python
from participation import ParticipationAnalyzer

analyzer = ParticipationAnalyzer('./results')
analyzer.load_all_experiments()
analyzer.analyze_participation_impact()
analyzer.print_participation_report()
```

**Output:** Summary report showing participation stats, convergence impact, efficiency.

### Pattern 2: Identify Robust Algorithms

```python
analyses = analyzer.analyze_participation_impact()

# Find most robust
best = max(analyses.items(), key=lambda x: x[1].robustness_score)
print(f"Most robust: {best[0]}")

# Find most efficient
best = max(analyses.items(), key=lambda x: x[1].communication_efficiency)
print(f"Most efficient: {best[0]}")
```

### Pattern 3: Performance Degradation Analysis

```python
full_vs_partial = analyzer.analyze_full_vs_partial(threshold=0.80)

for algo, data in full_vs_partial.items():
    full_acc = data['full_participation']['avg_accuracy']
    partial_acc = data['partial_participation']['avg_accuracy']
    degradation = (full_acc - partial_acc) / full_acc * 100
    print(f"{algo}: {degradation:.1f}% degradation with low participation")
```

### Pattern 4: Dropout Sensitivity

```python
impact = analyzer.get_participation_impact()

for algo, data in impact.items():
    corr = data['participation_accuracy_correlation']
    if corr < 0.3:
        print(f"{algo}: Robust to dropouts")
    else:
        print(f"{algo}: Sensitive to dropouts, correlation={corr:.3f}")
```

### Pattern 5: Optimal Configuration

```python
analyzer.print_recommendations()
optimal_rates = analyzer.get_optimal_participation_rate()

for algo, rate in sorted(optimal_rates.items()):
    current = analyzer.analyses[algo].avg_participation_rate
    savings = current - rate
    print(f"{algo}: Can reduce participation by {savings:.1f}% without hurting accuracy")
```

## Integration with Training Scripts

### For main_fmnist.py or main_emnist.py:

```python
# Add imports
from visualization import MetricsTracker

# Initialize tracker before training
tracker = MetricsTracker()
tracker.log_config(
    algorithm=alg_name,
    num_clients=num_clients,
    num_rounds=num_rounds,
    local_steps=local_epochs,
    dataset='FMNIST'
)

# In training loop, log each round:
# selected_indices = np.random.choice(range(num_clients), size=selected_clients, replace=False)
# ... training ...
tracker.log_round(
    round_num=round_num,
    test_loss=test_loss,
    test_acc=test_acc,
    train_loss=train_loss,
    train_acc=train_acc,
    num_clients=len(selected_indices)  # Track participation
)

# After training
tracker.save_json()
tracker.save_csv()
```

Then run the analyzer:
```bash
python examples_participation.py
```

## Advanced: Custom Analysis

### Create Custom Metrics

```python
# Access raw data
for exp_name, exp_data in analyzer.experiments.items():
    metrics = exp_data['metrics']
    participation = metrics['client_participation']
    accuracy = metrics['test_acc']
    
    # Custom metric: Accuracy drop per 1% participation drop
    contribution = []
    for i in range(1, len(participation)):
        part_drop = participation[i-1] - participation[i]
        acc_drop = accuracy[i-1] - accuracy[i]
        if part_drop > 0:
            contribution.append(acc_drop / part_drop)
    
    print(f"Avg contribution: {np.mean(contribution):.4f}")
```

### Combine with Other Analyses

```python
from comparison import ComparisonTool

# Use comparison tool
comp = ComparisonTool('./results')
comp.load_experiments()
comp_analyses = comp.compute_statistics()

# Cross-reference with participation
participation_analyzer = ParticipationAnalyzer('./results')
participation_analyzer.load_all_experiments()
part_analyses = participation_analyzer.analyze_participation_impact()

for algo in comp_analyses.keys():
    comp_acc = comp_analyses[algo].best_accuracy
    part_rob = part_analyses[algo].robustness_score
    print(f"{algo}: Accuracy={comp_acc:.4f}, Robustness={part_rob:.3f}")
```

## Common Questions

**Q: How is robustness score calculated?**
A: It's based on how stable the algorithm is under varying participation levels. Higher consistency = higher robustness (though the metric is inverted to indicate how well it maintains performance despite variance).

**Q: What participation levels should I test?**
A: Start with 100%, 80%, 60%, 40%, 20%, 10% participation rates. The analyzer will characterize your actual participation patterns.

**Q: Why does my algorithm show low efficiency?**
A: It may require many communication rounds. Try `analyzer.get_optimal_participation_rate()` to see if you can reduce participation without hurting accuracy.

**Q: How do I interpret negative correlation?**
A: Negative correlation (and NaN values) indicate insufficient data or issues with logging. Ensure `client_participation` is logged in every round.

## Troubleshooting

### Issue: No Experiments Loaded
```
Solution: Ensure JSON files are in ./results/ directory with names like *_metrics.json
```

### Issue: ParticipationAnalysis Shows Zero Values
```
Solution: Check that client_participation is logged in metrics:
  tracker.log_round(..., num_clients=len(participating_clients))
```

### Issue: Correlations Show NaN
```
Solution: Need at least 2 rounds of data and valid participation values.
Check: len(experiment_data['metrics']['client_participation']) > 1
```

### Issue: Visualizations Not Saving
```
Solution: Create output directory:
  mkdir -p ./results/participation_plots
  
And ensure matplotlib is installed:
  pip install matplotlib
```

## Performance Considerations

- **Multiple algorithms**: Runtime scales linearly with number of experiments
- **Long training runs**: With 1,000+ rounds, plot generation may take 1-2 seconds
- **Large heatmaps**: 10+ bin heatmaps with many algorithms can be memory-intensive

Typical performance:
- Load 5 experiments: <100ms
- Analyze participation: <500ms
- Generate 6 visualizations: 3-5 seconds
- Export JSON: <100ms

## Next Steps

1. **Enable participation tracking** in your training scripts
2. **Run experiments** with different algorithms
3. **Use ParticipationAnalyzer** to load and analyze results
4. **Generate visualizations** for presentations/papers
5. **Use recommendations** to optimize your federated learning setup

## See Also

- [Visualization Module](VISUALIZATION_README.md) - Track single-experiment metrics
- [Comparison Tool](COMPARISON_GUIDE.md) - Compare algorithms across all metrics
- [Integration Guide](INTEGRATION_GUIDE.md) - How to integrate into training scripts
