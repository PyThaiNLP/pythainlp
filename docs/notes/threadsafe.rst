Thread safety
=============

Summary
-------

PyThaiNLP's core word tokenization engines are designed with thread-safety
in mind. Internal implementations (``mm``, ``newmm``, ``newmm-safe``,
``longest``, ``icu``) are thread-safe.

For engines that wrap external libraries (``attacut``, ``budoux``, ``deepcut``,
``nercut``, ``nlpo3``, ``oskut``, ``sefr_cut``, ``tltk``, ``wtsplit``), the
wrapper code is thread-safe, but we cannot guarantee thread-safety of the
underlying external libraries themselves.

Thread safety implementation
-----------------------------

**Internal implementations (fully thread-safe):**

- ``mm``, ``newmm``, ``newmm-safe``: Stateless implementation,
  all data is local
- ``longest``: uses lock-protected check-then-act for
  the management of global cache shared across threads
- ``icu``: each thread gets its own ``BreakIterator`` instance

**External library wrappers (wrapper code is thread-safe):**

- ``attacut``: uses lock-protected check-then-act for
  the management of global cache; underlying library thread-safety not guaranteed
- ``budoux``: uses lock-protected lazy initialization of parser;
  underlying library thread-safety not guaranteed
- ``deepcut``, ``nercut``, ``nlpo3``, ``tltk``: Stateless wrapper,
  underlying library thread-safety not guaranteed
- ``oskut``, ``sefr_cut``, ``wtsplit``: use lock-protected model
  loading when switching models/engines; underlying library thread-safety not guaranteed

Usage in multi-threaded applications
-------------------------------------

Using a tokenization engine safely in multi-threaded contexts:

.. code-block:: python

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

Performance considerations
--------------------------

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

Best practices
--------------

1. **For high-throughput applications**: Consider using stateless engines like
   ``newmm`` or ``mm`` for optimal performance.

2. **For custom dictionaries**: The ``longest`` engine with custom dictionaries
   maintains a cache per dictionary object. Reuse dictionary objects across
   threads to maximize cache efficiency.

3. **For process pools**: All engines work correctly with multiprocessing as
   each process has its own memory space.

4. **IMPORTANT: Do not modify custom dictionaries during tokenization**:
   
   - Create your custom Trie/dictionary before starting threads
   - Never call ``trie.add()`` or ``trie.remove()`` while tokenization is in progress
   - If you need to update the dictionary,
     create a new Trie instance and pass it to subsequent tokenization calls
   - The Trie data structure itself is NOT thread-safe for concurrent modifications

Example of safe custom dictionary usage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

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

    # Wait for all threads to finish
    for t in threads:
        t.join()

Example of UNSAFE usage (DO NOT DO THIS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # UNSAFE: Modifying dictionary while threads are using it
    custom_dict = dict_trie(thai_words())

    def unsafe_worker(text, custom_dict):
        result = word_tokenize(text, engine="newmm", custom_dict=custom_dict)
        # DANGER: Modifying the shared dictionary
        custom_dict.add("คำใหม่")  # This is NOT thread-safe!
        return result

Testing
-------

Comprehensive thread safety tests are available in:

- ``tests/core/test_tokenize_thread_safety.py``

The test suite includes:

- Concurrent tokenization with multiple threads
- Race condition testing with multiple dictionaries
- Verification of result consistency across threads
- Stress testing with up to 200 concurrent operations (20 threads × 10 iterations)

Maintenance notes
-----------------

When adding new tokenization engines to PyThaiNLP:

1. **Avoid global mutable state** whenever possible
2. If caching is necessary, use thread-safe locks
3. If per-thread state is needed, use ``threading.local()``
4. Always add thread safety tests for new engines
5. Document thread safety guarantees in docstrings

Related files
-------------

- Core implementation: ``pythainlp/tokenize/core.py``
- Engine implementations: ``pythainlp/tokenize/*.py``
- Tests: ``tests/core/test_tokenize_thread_safety.py``

See also
--------

- :doc:`installation` - For using PyThaiNLP in distributed computing environments
  like Apache Spark, including configuration of data directories for distributed operations
