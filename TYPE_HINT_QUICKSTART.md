# Type Hint Coverage Analysis - Quick Start

This is a quick reference guide for the type hint coverage analysis tools.

## TL;DR

**Overall Status:** 82.22% of functions have complete type hints ✅

**What to do:**
1. Check `TYPE_HINT_ANALYSIS.md` for the full report
2. Use CSV files in `docs/type_hint_analysis/` for detailed analysis
3. Focus on improving coverage in: `transliterate`, `classify`, `el`, `chat`, `wangchanberta`

## Running the Analysis

```bash
# From repository root
python3 build_tools/analysis/type_hint_analyzer.py

# Generate CSV files
python3 build_tools/analysis/generate_csv.py

# Copy CSV files to docs
cp /tmp/*.csv docs/type_hint_analysis/
```

## Quick Stats by Submodule

| Coverage | Submodules |
|----------|------------|
| 💚 100% | cli, lm, morpheme, parse, tokenizeicu, tools, transliterateicu, word_vector, ancient |
| ✅ 95%+ | corpus (97%), tag (97%), soundex (96%), spell (95%) |
| 👍 80-94% | util (94%), phayathaibert (89%), benchmarks (87%), tokenize (84%), translate (84%) |
| ⚠️ 50-79% | khavee (77%), summarize (70%), ulmfit (68%), augment (62%), generate (53%), wsd (50%) |
| ❌ <50% | **transliterate (48%)**, **wangchanberta (44%)**, **coref (40%)**, **chat (25%)**, **classify (20%)**, **el (20%)** |

## Priority Items to Fix

### High Priority
✅ None! All critical public APIs have type hints.

### Medium Priority (51 functions without hints, 43 incomplete)
Key items:
- `pythainlp.corpus.util.tokenize` (991 references)
- `pythainlp.classify.param_free.GzipModel.train` (164 references)
- Many `__init__` methods missing `-> None` return type

### Low Priority (21 without, 13 incomplete)
Private functions or rarely used functions.

## Examples of Issues

### Missing Type Hints
```python
# Before
def tokenize(text):
    return newmm.segment(text, custom_dict=trie)

# After
def tokenize(text: str) -> List[str]:
    return newmm.segment(text, custom_dict=trie)
```

### Incomplete Type Hints
```python
# Before
def train(self):
    temp_list = []
    ...
    return temp_list

# After
def train(self) -> List[int]:
    temp_list = []
    ...
    return temp_list
```

### Missing Return Type on __init__
```python
# Before
def __init__(self, model_path: str):
    self.model = load(model_path)

# After  
def __init__(self, model_path: str) -> None:
    self.model = load(model_path)
```

## Data Files

All detailed data is available in:
- **Main Report:** `TYPE_HINT_ANALYSIS.md`
- **CSV Data:** `docs/type_hint_analysis/`
  - `submodule_summary.csv` - Statistics by submodule
  - `functions_no_hints.csv` - Functions without type hints
  - `functions_incomplete_hints.csv` - Functions with incomplete hints
- **JSON Data:** `/tmp/type_hint_analysis.json` (generated during analysis)

## Using CSV Files

```bash
# View functions in transliterate submodule
csvgrep -c Submodule -m "transliterate" docs/type_hint_analysis/functions_no_hints.csv | csvlook

# Sort by references (most used first)
csvsort -c References -r docs/type_hint_analysis/functions_no_hints.csv | head -20 | csvlook

# Count by priority
csvcut -c Priority docs/type_hint_analysis/functions_no_hints.csv | tail -n +2 | sort | uniq -c
```

## Recommendations

1. **Quick wins:** Add `-> None` to all `__init__` methods (many incomplete hints are this)
2. **Focus on:** transliterate, classify, el, chat submodules
3. **Maintain:** Keep 100% coverage in new code
4. **Gradual:** Improve legacy code during maintenance

## Tools

- `build_tools/analysis/type_hint_analyzer.py` - Main analyzer
- `build_tools/analysis/generate_csv.py` - CSV generator
- `build_tools/analysis/README.md` - Detailed tool documentation

---

**Last Updated:** 2026-02-03
