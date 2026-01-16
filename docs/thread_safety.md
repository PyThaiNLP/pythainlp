# Thread Safety in PyThaiNLP Word Tokenization

## Summary

As of this implementation, all standard word tokenization engines in PyThaiNLP's
core and compact dependency sets are thread-safe and can be safely used in
multi-threaded applications.

## Thread Safety Implementation

### Engines with Explicit Thread Safety Mechanisms

#### 1. `longest` Engine
- **Issue**: Global `_tokenizers` cache shared across threads
- **Solution**: Added `threading.Lock()` to protect cache access
- **Pattern**: Lock-protected check-then-act for cache management
- **File**: `pythainlp/tokenize/longest.py`

#### 2. `attacut` Engine (Extra Dependency)
- **Issue**: Global `_tokenizers` cache shared across threads
- **Solution**: Added `threading.Lock()` to protect cache access
- **Pattern**: Lock-protected check-then-act for cache management
- **File**: `pythainlp/tokenize/attacut.py`

#### 3. `icu` Engine (Compact Dependency)
- **Issue**: Global `BreakIterator` object modified by `setText()`
- **Solution**: Replaced global object with thread-local storage
- **Pattern**: Each thread gets its own `BreakIterator` instance
- **File**: `pythainlp/tokenize/pyicu.py`

### Engines That Are Inherently Thread-Safe

These engines use no global mutable state and are naturally thread-safe:

- **newmm**: Stateless implementation, all data is local
- **newmm-safe**: Stateless implementation, all data is local
- **mm** (multi_cut): Stateless implementation, all data is local

## Testing

Comprehensive thread safety tests are available in:
- `tests/core/test_tokenize_thread_safety.py`

The test suite includes:
- Concurrent tokenization with multiple threads
- Race condition testing with multiple dictionaries
- Verification of result consistency across threads
- Stress testing with 5000+ concurrent operations

## Usage in Multi-threaded Applications

All tokenization engines can now be safely used in multi-threaded contexts:

```python
import threading
from pythainlp.tokenize import word_tokenize

def tokenize_worker(text, results, index):
    # Thread-safe for all engines
    results[index] = word_tokenize(text, engine="longest")

texts = ["ผมรักประเทศไทย", "วันนี้อากาศดี", "เขาไปโรงเรียน"]
results = [None] * len(texts)
threads = []

for i, text in enumerate(texts):
    thread = threading.Thread(target=tokenize_worker, args=(text, results, i))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# All results are correctly populated
print(results)
```

## Performance Considerations

1. **Lock-based synchronization** (longest, attacut):
   - Minimal overhead for cache access
   - Cache lookups are very fast
   - Lock contention is minimal in typical usage

2. **Thread-local storage** (icu):
   - Each thread maintains its own instance
   - No synchronization overhead after initialization
   - Slightly higher memory usage (one instance per thread)

3. **Stateless engines** (newmm, mm):
   - Zero synchronization overhead
   - Best performance in multi-threaded scenarios
   - Recommended for high-throughput applications

## Best Practices

1. **For high-throughput applications**: Consider using stateless engines like
   `newmm` or `mm` for optimal performance.

2. **For custom dictionaries**: The `longest` engine with custom dictionaries
   maintains a cache per dictionary object. Reuse dictionary objects across
   threads to maximize cache efficiency.

3. **For process pools**: All engines work correctly with multiprocessing as
   each process has its own memory space.

## Maintenance Notes

When adding new tokenization engines to PyThaiNLP:

1. **Avoid global mutable state** whenever possible
2. If caching is necessary, use thread-safe locks
3. If per-thread state is needed, use `threading.local()`
4. Always add thread safety tests for new engines
5. Document thread safety guarantees in docstrings

## Related Files

- Core implementation: `pythainlp/tokenize/core.py`
- Engine implementations: `pythainlp/tokenize/*.py`
- Tests: `tests/core/test_tokenize_thread_safety.py`
- Stress tests: Available in PR discussion/comments
