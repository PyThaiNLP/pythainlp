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
- **deepcut**: Delegates to external library (deepcut package)

### Default Dictionary Loading

The default word dictionary is loaded lazily using `@lru_cache` on the
`word_dict_trie()` function. The caching mechanism itself is thread-safe:

- First thread to request the dictionary triggers loading
- Subsequent threads receive the cached Trie instance
- All threads share the same default Trie object

This is safe because:
1. The tokenizers only **read** from the Trie (using `.prefixes()` and `__contains__`)
2. They never modify the Trie after creation
3. Python's GIL ensures dictionary reads are atomic
4. The default Trie is never modified after initial creation

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

4. **IMPORTANT: Do not modify custom dictionaries during tokenization**:
   - Create your custom Trie/dictionary before starting threads
   - Never call `trie.add()` or `trie.remove()` while tokenization is in progress
   - If you need to update the dictionary, create a new Trie instance and pass it to subsequent tokenization calls
   - The Trie data structure itself is NOT thread-safe for concurrent modifications

### Example of Safe Custom Dictionary Usage

```python
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus.common import thai_words
from pythainlp.util import dict_trie
import threading

# SAFE: Create dictionary once before threading
custom_words = set(thai_words())
custom_words.add("คำใหม่")
custom_dict = dict_trie(custom_words)

texts = ["ผมรักประเทศไทย", "วันนี้อากาศดี", "เขาไปโรงเรียน"]

def worker(text, custom_dict):
    # SAFE: Only reading from the dictionary
    return word_tokenize(text, engine="newmm", custom_dict=custom_dict)

# All threads share the same dictionary (read-only)
threads = []
for text in texts:
    t = threading.Thread(target=worker, args=(text, custom_dict))
    threads.append(t)
    t.start()
```

### Example of UNSAFE Usage (DO NOT DO THIS)

```python
# UNSAFE: Modifying dictionary while threads are using it
custom_dict = dict_trie(thai_words())

def unsafe_worker(text, custom_dict):
    result = word_tokenize(text, engine="newmm", custom_dict=custom_dict)
    # DANGER: Modifying the shared dictionary
    custom_dict.add("คำใหม่")  # This is NOT thread-safe!
    return result
```

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
