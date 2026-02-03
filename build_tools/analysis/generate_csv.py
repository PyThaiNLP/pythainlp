#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2026 PyThaiNLP Project
# SPDX-License-Identifier: Apache-2.0
"""
Generate detailed CSV report from type hint analysis
"""
import json
import csv

# Load the JSON data
with open('/tmp/type_hint_analysis.json', 'r') as f:
    data = json.load(f)

# Create CSV for functions without type hints
with open('/tmp/functions_no_hints.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Function Name', 'Submodule', 'Scope', 'Priority', 'References', 'Test Suite', 'File', 'Line'])
    
    for func in data['functions_no_hints']:
        parts = func['name'].split('.')
        submodule = parts[1] if len(parts) > 2 and parts[0] == 'pythainlp' else parts[0]
        
        writer.writerow([
            func['name'],
            submodule,
            func['scope'],
            func['priority'],
            func['references'],
            func['test_suite'],
            func['file'],
            func['line']
        ])

# Create CSV for functions with incomplete type hints
with open('/tmp/functions_incomplete_hints.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Function Name', 'Submodule', 'Scope', 'Priority', 'Params Hinted', 'Has Return', 'References', 'Test Suite', 'File', 'Line'])
    
    for func in data['functions_incomplete_hints']:
        parts = func['name'].split('.')
        submodule = parts[1] if len(parts) > 2 and parts[0] == 'pythainlp' else parts[0]
        
        writer.writerow([
            func['name'],
            submodule,
            func['scope'],
            func['priority'],
            func['params'],
            func['return'],
            func['references'],
            func['test_suite'],
            func['file'],
            func['line']
        ])

# Create summary CSV by submodule
with open('/tmp/submodule_summary.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Submodule', 'Total', 'Complete', 'Incomplete', 'None', '% Complete'])
    
    for submodule, counts in sorted(data['by_submodule'].items()):
        total = counts['complete'] + counts['incomplete'] + counts['none']
        pct = (counts['complete'] / total * 100) if total > 0 else 0
        
        writer.writerow([
            submodule,
            total,
            counts['complete'],
            counts['incomplete'],
            counts['none'],
            f"{pct:.2f}%"
        ])

print("CSV files generated:")
print("  /tmp/functions_no_hints.csv")
print("  /tmp/functions_incomplete_hints.csv")
print("  /tmp/submodule_summary.csv")
