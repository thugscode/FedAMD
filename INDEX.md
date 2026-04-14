# FedAMD Analysis Toolkit - Complete Documentation Index

> **Navigation Hub** — Quick access to all documentation for the three analysis modules

---

## 📚 Documentation Structure

The FedAMD Analysis Toolkit includes **3 powerful modules** with **consistent documentation patterns**:

### Visualization Module
Track and visualize federated learning experiments with metrics, plots, and export options.
- **[VISUALIZATION_QUICK_REFERENCE.md](VISUALIZATION_QUICK_REFERENCE.md)** — 30-second quickstart + API cheat sheet
- **[VISUALIZATION_README.md](VISUALIZATION_README.md)** — Complete documentation + examples

### Comparison Module  
Compare algorithm performance across multiple experiments with side-by-side analysis and multi-algorithm visualizations.
- **[COMPARISON_QUICK_REFERENCE.md](COMPARISON_QUICK_REFERENCE.md)** — 30-second quickstart + API cheat sheet
- **[COMPARISON_GUIDE.md](COMPARISON_GUIDE.md)** — Complete documentation + examples
- **[COMPARISON_BUILD_SUMMARY.md](COMPARISON_BUILD_SUMMARY.md)** — Feature overview + technical details

### Participation Module
Analyze and visualize client participation patterns across training rounds with statistical insights.
- **[PARTICIPATION_QUICK_REFERENCE.md](PARTICIPATION_QUICK_REFERENCE.md)** — 30-second quickstart + API cheat sheet
- **[PARTICIPATION_GUIDE.md](PARTICIPATION_GUIDE.md)** — Complete documentation + examples
- **[PARTICIPATION_BUILD_SUMMARY.md](PARTICIPATION_BUILD_SUMMARY.md)** — Feature overview + technical details

---

## 🚀 Where to Start

Choose your path based on what you need:

| Goal | Start Here |
|------|-----------|
| **First time?** | [ANALYSIS_TOOLKIT_OVERVIEW.md](ANALYSIS_TOOLKIT_OVERVIEW.md) — Project overview |
| **Need examples?** | examples_visualization.py, examples_comparison.py, examples_participation.py |
| **Integrating into code?** | [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) — How to add to your training scripts |
| **30-second overview** | QUICK_REFERENCE for the module you need |
| **How does it work?** | The README file for your module |
| **Feature checklist** | BUILD_SUMMARY for your module |

---

## 📁 Complete File Structure

```
FedAMD/
│
├── 📊 VISUALIZATION MODULE
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── metrics.py              (263 lines)
│   │   └── plots.py                (319 lines)
│   ├── VISUALIZATION_QUICK_REFERENCE.md
│   └── VISUALIZATION_README.md
│
├── 📈 COMPARISON MODULE
│   ├── comparison/
│   │   ├── __init__.py
│   │   ├── tool.py                 (600+ lines)
│   │   └── visualize.py            (453 lines)
│   ├── COMPARISON_QUICK_REFERENCE.md
│   ├── COMPARISON_GUIDE.md
│   └── COMPARISON_BUILD_SUMMARY.md
│
├── 👥 PARTICIPATION MODULE
│   ├── participation/
│   │   ├── __init__.py
│   │   ├── analyzer.py             (535 lines)
│   │   └── visualize.py            (453 lines)
│   ├── PARTICIPATION_QUICK_REFERENCE.md
│   ├── PARTICIPATION_GUIDE.md
│   └── PARTICIPATION_BUILD_SUMMARY.md
│
├── 📖 SHARED DOCUMENTATION
│   ├── ANALYSIS_TOOLKIT_OVERVIEW.md    (main entry point)
│   ├── INTEGRATION_GUIDE.md            (add to training scripts)
│   ├── INDEX.md                        (this file)
│   ├── README.md                       (project readme)
│   └── LICENSE.md
│
├── 💡 EXAMPLES (1,200+ lines total)
│   ├── examples_visualization.py
│   ├── examples_comparison.py
│   └── examples_participation.py
│
└── 📁 OTHER
    ├── algo/
    ├── data_model/
    ├── main_fmnist.py
    └── requirements.txt
```

---

## 🎯 Documentation Roadmap

**New to the toolkit?**
1. Read [ANALYSIS_TOOLKIT_OVERVIEW.md](ANALYSIS_TOOLKIT_OVERVIEW.md) (5 min)
2. Pick a module and read its QUICK_REFERENCE (3 min each)
3. Run the corresponding example file (2 min)
4. Read the README for detailed API (10 min)

**Ready to integrate?**
1. Read [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) (5 min)
2. Copy the code snippets to your training scripts (5 min)
3. Run your experiment and check results/ directory

**Want complete understanding?**
1. Read all three QUICK_REFERENCE files (9 min)
2. Read all three README/GUIDE files (30 min)
3. Explore all three example files (15 min)
4. Study the BUILD_SUMMARY files for architecture (10 min)

---

## 📊 Module Overview

### Visualization: Track & Visualize Experiments
```python
from visualization import MetricsTracker, ResultsVisualizer

tracker = MetricsTracker("experiment_name")
tracker.log_round(round_num, test_loss=loss, test_acc=acc)
tracker.save_json() and tracker.save_csv()
ResultsVisualizer().plot_all(tracker.metrics, "experiment_name")
```

**Outputs:**
- JSON/CSV metrics export
- Accuracy & loss curves
- Convergence analysis
- Communication efficiency plots

---

### Comparison: Compare Multiple Algorithms
```python
from comparison import ComparisonTool

tool = ComparisonTool()
tool.load_experiments(["FedAvg", "FedAdapt", "SCAFFOLD"])
tool.plot_comparison()
tool.export_table()
```

**Outputs:**
- Side-by-side algorithm comparison
- Performance tables & statistics
- Multi-algorithm visualization plots

---

### Participation: Analyze Client Participation
```python
from participation import ParticipationAnalyzer

analyzer = ParticipationAnalyzer("experiment_name")
analyzer.load_data()
analyzer.analyze()
analyzer.plot_insights()
```

**Outputs:**
- Participation histograms
- Trends over rounds
- Client availability patterns
- Statistical summaries

---

## 🔍 Quick Reference Links

| What | Where |
|------|-------|
| Project overview | [ANALYSIS_TOOLKIT_OVERVIEW.md](ANALYSIS_TOOLKIT_OVERVIEW.md) |
| Integration instructions | [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) |
| Visualization quick start | [VISUALIZATION_QUICK_REFERENCE.md](VISUALIZATION_QUICK_REFERENCE.md) |
| Visualization full guide | [VISUALIZATION_README.md](VISUALIZATION_README.md) |
| Comparison quick start | [COMPARISON_QUICK_REFERENCE.md](COMPARISON_QUICK_REFERENCE.md) |
| Comparison full guide | [COMPARISON_GUIDE.md](COMPARISON_GUIDE.md) |
| Participation quick start | [PARTICIPATION_QUICK_REFERENCE.md](PARTICIPATION_QUICK_REFERENCE.md) |
| Participation full guide | [PARTICIPATION_GUIDE.md](PARTICIPATION_GUIDE.md) |
| Working examples (viz) | examples_visualization.py |
| Working examples (comp) | examples_comparison.py |
| Working examples (part) | examples_participation.py |

---

## 📝 All Documentation Files (13 total)

**Shared Guides (5 files):**
- ANALYSIS_TOOLKIT_OVERVIEW.md
- INTEGRATION_GUIDE.md
- INDEX.md (this file)
- README.md
- LICENSE.md

**Visualization (2 files):**
- VISUALIZATION_QUICK_REFERENCE.md
- VISUALIZATION_README.md

**Comparison (3 files):**
- COMPARISON_QUICK_REFERENCE.md
- COMPARISON_GUIDE.md
- COMPARISON_BUILD_SUMMARY.md

**Participation (3 files):**
- PARTICIPATION_QUICK_REFERENCE.md
- PARTICIPATION_GUIDE.md
- PARTICIPATION_BUILD_SUMMARY.md

---

## ✅ Each Module Provides

| Feature | Visualization | Comparison | Participation |
|---------|---------------|-----------|---------------|
| Track metrics | ✅ | — | — |
| Visualize trends | ✅ | ✅ | ✅ |
| Compare algorithms | — | ✅ | — |
| Export data | ✅ | ✅ | ✅ |
| Statistical analysis | ✅ | ✅ | ✅ |
| Publication plots | ✅ | ✅ | ✅ |

---

## 🚀 Next Steps

1. **Understand the toolkit**: Read [ANALYSIS_TOOLKIT_OVERVIEW.md](ANALYSIS_TOOLKIT_OVERVIEW.md)
2. **See it in action**: Run any examples_*.py file
3. **Integrate into code**: Follow [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
4. **Learn your module**: Read the appropriate QUICK_REFERENCE + README

---

## ❓ Need Help?

Check the relevant QUICK_REFERENCE or README for your module — each contains:
- Common usage patterns
- Complete API reference
- Code examples
- Troubleshooting tips
- FAQs  
A: Yes, the module is flexible about what you log

**Q: Do I need to modify existing code significantly?**  
A: No! Just add 9 lines. Fully backward compatible.
