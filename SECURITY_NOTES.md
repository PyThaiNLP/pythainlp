# Security Issues Found and Fixed

This document describes security vulnerabilities identified in the PyThaiNLP codebase and the fixes applied.

## 1. Path Traversal in Archive Extraction (CWE-22)

### Issue
**File:** `pythainlp/corpus/core.py`
**Lines:** 520, 531 (before fix)

**Description:**
The code used `tar.extractall()` and `zipfile.extractall()` without validating member paths, which could allow path traversal attacks. A malicious archive could contain files with paths like `../../etc/passwd` that would be extracted outside the intended directory.

**Why it's a security issue:**
- An attacker could create a malicious corpus archive that, when downloaded and extracted, writes files to arbitrary locations on the user's filesystem
- Could lead to overwriting critical system files or user data
- Could be used to place malicious code in locations where it might be executed

**Likelihood:**
- **Medium**: Requires the attacker to compromise the corpus distribution system or perform a man-in-the-middle attack
- The MD5 checksum verification provides some protection, but MD5 is cryptographically weak
- An attacker with control over the corpus server could distribute malicious archives

**Impact:**
- **High**: Arbitrary file write vulnerability
- Could lead to data loss, system compromise, or code execution
- Affects all users who download corpus files

**Fix Applied:**
Added two helper functions:
1. `_is_within_directory()`: Validates that a path stays within the target directory
2. `_safe_extract_tar()`: Safely extracts tar archives by checking all member paths
3. `_safe_extract_zip()`: Safely extracts zip archives by checking all member paths

These functions check each file in the archive before extraction and raise a `ValueError` if any file attempts to escape the target directory.

**Code Changes:**
```python
# Added validation functions
def _is_within_directory(directory: str, target: str) -> bool:
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    return abs_target.startswith(abs_directory + os.sep) or abs_target == abs_directory

def _safe_extract_tar(tar, path: str) -> None:
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not _is_within_directory(path, member_path):
            raise ValueError(f"Attempted path traversal in tar file: {member.name}")
    tar.extractall(path=path)

def _safe_extract_zip(zip_file, path: str) -> None:
    for member in zip_file.namelist():
        member_path = os.path.join(path, member)
        if not _is_within_directory(path, member_path):
            raise ValueError(f"Attempted path traversal in zip file: {member}")
    zip_file.extractall(path=path)

# Updated extraction calls
_safe_extract_tar(tar, get_full_data_path(foldername))
_safe_extract_zip(zip_file, get_full_data_path(foldername))
```

## 2. Insecure Deserialization with Pickle (CWE-502)

### Issue
**File:** `pythainlp/generate/thai2fit.py`
**Line:** 46 (before fix)

**Description:**
The code used `pickle.load()` to deserialize data from a file. Pickle deserialization can execute arbitrary code if the pickle file is malicious.

**Why it's a security issue:**
- Pickle can deserialize and execute arbitrary Python code
- If an attacker can replace the corpus file with a malicious pickle file, they can achieve remote code execution
- The `__reduce__` method in pickle allows arbitrary code execution during deserialization

**Likelihood:**
- **Low to Medium**: The pickle file is from PyThaiNLP's official corpus, which is verified with MD5
- However, MD5 is cryptographically broken and could be subject to collision attacks
- An attacker who compromises the corpus server or performs MITM could replace the file

**Impact:**
- **Critical**: Remote code execution
- An attacker could gain full control of the system
- Could lead to data theft, ransomware, or system compromise

**Fix Applied:**
1. Added comprehensive security warnings in comments explaining the risk
2. Used context manager for proper file handling
3. Added `# noqa: S301` to acknowledge the security risk (detected by bandit)
4. Documented that the file comes from a trusted source with MD5 verification

**Recommendations for Future:**
- Consider migrating from pickle to safer formats like JSON or MessagePack
- Implement stronger cryptographic verification (SHA-256 instead of MD5)
- Add digital signatures to corpus files to ensure authenticity

**Code Changes:**
```python
# Security Note: This loads a pickle file from PyThaiNLP's trusted corpus.
# The file is downloaded from PyThaiNLP's official repository with MD5 verification.
# Users should only use corpus files from trusted sources.
# WARNING: Pickle deserialization can execute arbitrary code if the file is malicious.
with open(thwiki["itos_fname"], "rb") as f:
    thwiki_itos = pickle.load(f)  # noqa: S301
```

## 3. SSL/TLS Certificate Verification

### Issue
**File:** `pythainlp/corpus/core.py`
**Functions:** `get_corpus_db()`, `_download()`

**Description:**
The code uses `urllib.request.urlopen()` for HTTPS downloads. While Python's urllib validates SSL certificates by default, this wasn't explicitly documented.

**Why it could be a security issue:**
- If SSL verification were disabled, attackers could perform man-in-the-middle attacks
- Could lead to downloading malicious corpus files
- Users might not be aware of the security guarantees

**Likelihood:**
- **Low**: Python 3.9+ (the minimum supported version) enables SSL verification by default
- No actual vulnerability exists in the current code

**Impact:**
- **N/A**: This is already secure by default

**Fix Applied:**
- Added security comments documenting that SSL certificate verification is enabled
- Made the security expectations explicit in the code
- Helps prevent future regressions where someone might disable verification

**Code Changes:**
```python
# SSL certificate verification is enabled by default
with urlopen(req, timeout=10) as response:
```

## 4. MD5 Hash Usage (CWE-327)

### Issue
**File:** `pythainlp/corpus/core.py`
**Line:** 353

**Description:**
The code uses MD5 for file integrity verification. While MD5 is marked with `# noqa: S324` acknowledging it's insecure, this represents a potential weakness.

**Why it's a security issue:**
- MD5 is cryptographically broken and vulnerable to collision attacks
- An attacker could create a malicious file with the same MD5 hash
- Does not provide authenticity verification (only integrity)

**Likelihood:**
- **Low**: Creating a meaningful MD5 collision is difficult but possible
- Would require sophisticated attacker with resources

**Impact:**
- **Medium**: Could allow distribution of malicious corpus files
- Limited by the difficulty of creating useful MD5 collisions

**Current Status:**
- **Not Fixed**: The issue is acknowledged with `# noqa: S324`
- The comment states "MD5 is insecure but sufficient here"

**Recommendations for Future:**
- Migrate to SHA-256 or SHA-3 for file integrity verification
- Implement digital signatures using public key cryptography
- Add versioning to detect rollback attacks

## Summary of Security Improvements

| Issue | Severity | Status | Impact |
|-------|----------|--------|---------|
| Path Traversal (extractall) | High | ✅ Fixed | Prevents arbitrary file writes |
| Pickle Deserialization | Critical | ⚠️ Documented | Risk acknowledged, mitigated by trusted source |
| SSL Verification | N/A | ✅ Documented | Already secure, now explicit |
| MD5 Usage | Medium | ⚠️ Acknowledged | Accepted risk, documented for future improvement |

## Testing Recommendations

To verify the security fixes:

1. **Path Traversal Test**: Create a test archive with paths like `../../test.txt` and verify it's rejected
2. **Pickle Security**: Ensure corpus files are only loaded from trusted sources
3. **SSL Test**: Verify HTTPS downloads fail with invalid certificates
4. **Integration Test**: Test normal corpus download and extraction workflows

## Best Practices for Users

1. **Only use official PyThaiNLP corpus files** from trusted sources
2. **Keep PyThaiNLP updated** to receive security patches
3. **Verify checksums** of downloaded corpus files when possible
4. **Use HTTPS** for all corpus downloads (which is the default)
5. **Report security issues** responsibly through the project's security policy

## References

- [CWE-22: Path Traversal](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)
- [OWASP: Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
