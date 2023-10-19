# Word Tokenization Benchmark for Thai (obsolete)

A framework for benchmarking tokenization algorithms for Thai.
It has a command-line interface that allows users to conveniently execute the benchmarks
as well as a module interface for later use in their development pipelines.


## Metrics
<div align="center">
    <img src="https://i.imgur.com/jVBOLa2.png"/>
</div>


### Character-Level (CL)
- True Positive (TP): no. of starting characters that are correctly predicted.
- True Negative (TN): no. of non-starting characters that are correctly predicted.
- False Positive (FP): no. of non-starting characters that are wrongly predicted as starting characters.
- False Negative (FN): no. of starting characters that are wrongly predicted as non-starting characters.
- Precision: TP / (TP + FP)
- Recall: TP / (TP+FN)
- f1: ...


### Word-Level (WL)
- Correctly Tokenized Words (CTW): no. of words in reference that are correctly tokenized.
- Precision: CTW / no. words in reference solution
- Recall: CTW / no. words in sample
-**** f1: ...


## Benchmark Results

| Vendor | Approach | Datasets |
|---|---|---|
| DeepCut | CNN | [![](https://img.shields.io/badge/BEST:val-WL:f1(0.9732)-yellow.svg)][res-BEST-val-DeepCut] [![](https://img.shields.io/badge/THNC-WL:f1(0.6323)-yellow.svg)][res-THNC-DeepCut] [![](https://img.shields.io/badge/Orchid-WL:f1(0.6638)-yellow.svg)][res-Orchid-DeepCut] [![](https://img.shields.io/badge/WiseSight160-WL:f1(0.8042)-yellow.svg)][res-WiseSight160-DeepCut] |
| PyThaiNLP-newmm | dictionary-based | [![](https://img.shields.io/badge/BEST:val-WL:f1(0.6836)-yellow.svg)][res-BEST-val-PyThaiNLP-newmm] [![](https://img.shields.io/badge/THNC-WL:f1(0.7338)-yellow.svg)][res-THNC-PyThaiNLP-newmm] [![](https://img.shields.io/badge/Orchid-WL:f1(0.7223)-yellow.svg)][res-Orchid-PyThaiNLP-newmm] [![](https://img.shields.io/badge/WiseSight160-WL:f1(0.7248)-yellow.svg)][res-WiseSight160-PyThaiNLP-newmm] |
| Sertis-BiGRU | Bi-directional RNN | [![](https://img.shields.io/badge/BEST:val-WL:f1(0.9251)-yellow.svg)][res-BEST-val-Sertis-BiGRU] [![](https://img.shields.io/badge/WiseSight160-WL:f1(0.8115)-yellow.svg)][res-WiseSight160-Sertis-BiGRU] |

[res-BEST-val-DeepCut]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=BEST-val-DeepCut
[res-THNC-DeepCut]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=THNC-DeepCut
[res-Orchid-DeepCut]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=Orchid-DeepCut
[res-WiseSight160-DeepCut]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=WiseSight160-DeepCut
[res-BEST-val-PyThaiNLP-newmm]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=BEST-val-PyThaiNLP-newmm
[res-THNC-PyThaiNLP-newmm]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=THNC-PyThaiNLP-newmm
[res-Orchid-PyThaiNLP-newmm]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=Orchid-PyThaiNLP-newmm
[res-WiseSight160-PyThaiNLP-newmm]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=WiseSight160-PyThaiNLP-newmm
[res-BEST-val-Sertis-BiGRU]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=BEST-val-Sertis-BiGRU
[res-WiseSight160-Sertis-BiGRU]: https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name=WiseSight160-Sertis-BiGRU


## Installation (WIP)
```
pip ...
```

## Usages (to be updated)

1. Command-line Interface
    ```
    PYTHONPATH=`pwd` python scripts/thai-tokenisation-benchmark.py \
    --test-file ./data/best-2010/TEST_100K_ANS.txt \
    --input ./data/best-2010-syllable.txt

    # Sample output
    Benchmarking ./data/best-2010-deepcut.txt against ./data/best-2010/TEST_100K_ANS.txt with 2252 samples in total
    ============== Benchmark Result ==============
                    metric       mean±std       min    max
             char_level:tp    47.82±47.22  1.000000  354.0
             char_level:tn  144.19±145.97  1.000000  887.0
             char_level:fp      1.34±2.02  0.000000   23.0
             char_level:fn      0.70±1.19  0.000000   14.0
      char_level:precision      0.96±0.08  0.250000    1.0
         char_level:recall      0.98±0.04  0.500000    1.0
             char_level:f1      0.97±0.06  0.333333    1.0
      word_level:precision      0.92±0.14  0.000000    1.0
         word_level:recall      0.93±0.12  0.000000    1.0
             word_level:f1      0.93±0.13  0.000000    1.0
    ```

2. Module Interface
    ```
    from pythainlp.benchmarks import word_tokenisation as bwt

    ref_samples = array of reference tokenised samples
    tokenised_samples = array of tokenised samples, aka. from your algorithm

    # dataframe contains metrics for each sample
    df = bwt.benchmark(ref_samples, tokenised_samples)
    ```

## Related Work
- [Thai Tokenizers Docker][docker]: collection of Docker containers of pre-built Thai tokenizers.


## Development
```
# unitests
$ TEST_VERBOSE=1 PYTHONPATH=. python tests/__init__.py
```

## Acknowledgement
This project was initially started by [Pattarawat Chormai][pat], while he was interning at [Dr. Attapol Thamrongrattanarit][ate]'s lab.

[docker]: https://github.com/PyThaiNLP/docker-thai-tokenizers
[ate]: https://attapol.github.io
[pat]: https://pat.chormai.org
