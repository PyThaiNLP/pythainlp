#!python3
# -*- coding: utf-8 -*-

import json
import os

MARKDOWN_TEMPLATE = """
| Vendor | Approach | Datasets | 
|---|---|---|
{content}
"""

ROW_TEMPLATE = """
| {vendor} | {desc} | {datasets} |
"""

REF_KEY = "res-{ds}-{method}"

REF_TEMPLATE = """
[{key}]: {url}
"""

RESULT_DIR = os.environ['TOKENISATION_BENCHMARK_RESULT_DIR']

URL_TEMPLATE = "https://pythainlp.github.io/tokenization-benchmark-visualization/?experiment-name={ds}-{method}"

BADGE_TEMPLATE = "[![](https://img.shields.io/badge/{ds}-WL:f1({f1:.4f})-yellow.svg)][{key}]"

desc = {
    'DeepCut': 'CNN',
    'Sertis-BiGRU': 'Bi-directional RNN',
    'PyThaiNLP-newmm': 'dictionary-based'
}

results = {
    'DeepCut': {
        'datasets': [
            {
                'ds': 'BEST-val',
                'file': 'eval-details-best-features-window-1--sampling-0-ms-5_tokenised-deepcut-deepcut.json'
            },
            {
                'ds': 'THNC',
                'file': 'eval-details-thai-literature_tokenised-deepcut-deepcut.json'
            },
            {
                'ds': 'Orchid',
                'file': 'eval-details-orchid_tokenised-deepcut-deepcut.json'
            },
            {
                'ds': 'WiseSight160',
                'file': 'eval-details-wisesight-160-samples-tokenised_tokenised-deepcut-deepcut.json'
            }
        ]
    },
    'PyThaiNLP-newmm': {
        'datasets': [
            {
                'ds': 'BEST-val',
                'file': 'eval-details-best-features-window-1--sampling-0-ms-5_tokenised-pythainlp-newmm.json'
            },
            {
                'ds': 'THNC',
                'file': 'eval-details-thai-literature_tokenised-pythainlp-newmm.json'
            },
            {
                'ds': 'Orchid',
                'file': 'eval-details-orchid_tokenised-pythainlp-newmm.json'
            },
            {
                'ds': 'WiseSight160',
                'file': 'eval-details-wisesight-160-samples-tokenised_tokenised-pythainlp-newmm.json'
            }
        ]
    },
    'Sertis-BiGRU': {
        'datasets': [
            {
                'ds': 'BEST-val',
                'file': 'eval-details-best-features-window-1--sampling-0-ms-5_tokenised-sertis-sertis.json'
            },
            {
                'ds': 'WiseSight160',
                'file': 'eval-details-wisesight-160-samples-tokenised_tokenised-sertis-sertis.json'
            }
        ]
    }
}

content = ""

rows = []
references = []
for k, v in sorted(results.items(), key=lambda (k, v): k):
    res = []
    for ds in v['datasets']:
        dsk, dsf = ds['ds'], ds['file']

        with open("%s/%s" % (RESULT_DIR, dsf), "r") as f:
            dd = json.load(f)
            f1 = dd['metrics']['word_level:f1']['mean']

        key = REF_KEY.format(ds=dsk, method=k)
        res.append(BADGE_TEMPLATE.format(ds=dsk.replace("-", ":"), f1=f1, key=key))
        url = URL_TEMPLATE.format(ds=dsk, method=k)
        references.append(REF_TEMPLATE.format(key=key, url=url).strip())

    row = ROW_TEMPLATE.format(vendor=k, desc=desc[k], datasets=" ".join(res)).strip()
    rows.append(row)

print("-------- TABLE ----------")
print(MARKDOWN_TEMPLATE.format(content="\n".join(rows)))

print("")

print("\n".join(references))
