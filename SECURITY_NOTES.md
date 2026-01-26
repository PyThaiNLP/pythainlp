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
Added three helper functions with comprehensive security validation:

1. `_is_within_directory()`: Validates that a path stays within the target directory
   - Uses `os.path.abspath()` to normalize paths and resolve `..` sequences
   - Prevents path traversal through relative paths
   - Does NOT follow symlinks (that's handled separately)

2. `_safe_extract_tar()`: Safely extracts tar archives
   - **Python 3.12+**: Uses built-in `tarfile.data_filter` for comprehensive protection
   - **Python 3.9-3.11**: Custom validation checking each member path
   - Validates regular file paths to prevent directory escape
   - Validates symlink targets to prevent symlinks pointing outside extraction directory
   - Handles both relative and absolute symlinks

3. `_safe_extract_zip()`: Safely extracts zip archives
   - Validates all member paths to prevent directory escape
   - Detects and validates symlinks in ZIP archives (Unix systems)
   - Checks symlink targets point within the extraction directory

**Symlink Attack Prevention:**
Archives can contain symlinks that point outside the extraction directory. An attacker could:
- Include a symlink `evil_link -> ../../etc`
- Then include a file `evil_link/passwd` which would overwrite `/etc/passwd`

The fix validates both:
- The symlink member path itself is within the directory
- The symlink target resolves to a location within the directory

These functions check each file in the archive before extraction and raise a `ValueError` if any file or symlink attempts to escape the target directory.

**Code Changes:**
```python
# Added validation function - handles path normalization
def _is_within_directory(directory: str, target: str) -> bool:
    """Check if target path is within directory (prevent path traversal)."""
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)
    if not abs_directory.endswith(os.sep):
        abs_directory += os.sep
    return abs_target.startswith(abs_directory) or abs_target == abs_directory.rstrip(os.sep)

# Safe tar extraction with symlink validation
def _safe_extract_tar(tar: tarfile.TarFile, path: str) -> None:
    """Safely extract tar archive, preventing path traversal attacks."""
    # Python 3.12+ uses built-in filter
    if hasattr(tarfile, 'data_filter'):
        try:
            tar.extractall(path=path, filter='data')
        except (tarfile.OutsideDestinationError, tarfile.LinkOutsideDestinationError) as e:
            raise ValueError(str(e))
    else:
        # Python 3.9-3.11: manual validation
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not _is_within_directory(path, member_path):
                raise ValueError(f"Attempted path traversal in tar file: {member.name}")
            
            # Validate symlink targets
            if member.issym() or member.islnk():
                link_target = member.linkname
                if not os.path.isabs(link_target):
                    member_dir = os.path.dirname(member_path)
                    link_target = os.path.join(member_dir, link_target)
                else:
                    link_target = os.path.join(path, link_target.lstrip(os.sep))
                
                if not _is_within_directory(path, link_target):
                    raise ValueError(
                        f"Symlink {member.name} points outside extraction directory: {member.linkname}"
                    )
        tar.extractall(path=path)

# Safe zip extraction with symlink validation
def _safe_extract_zip(zip_file: zipfile.ZipFile, path: str) -> None:
    """Safely extract zip archive, preventing path traversal attacks."""
    for member in zip_file.namelist():
        member_path = os.path.join(path, member)
        if not _is_within_directory(path, member_path):
            raise ValueError(f"Attempted path traversal in zip file: {member}")
        
        # Check for symlinks in ZIP (Unix systems)
        info = zip_file.getinfo(member)
        is_symlink = (info.external_attr >> 16) & 0o170000 == 0o120000
        
        if is_symlink:
            link_target = zip_file.read(member).decode('utf-8')
            if not os.path.isabs(link_target):
                member_dir = os.path.dirname(member_path)
                resolved_target = os.path.join(member_dir, link_target)
            else:
                resolved_target = os.path.join(path, link_target.lstrip(os.sep))
            
            if not _is_within_directory(path, resolved_target):
                raise ValueError(
                    f"Symlink {member} points outside extraction directory: {link_target}"
                )
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
