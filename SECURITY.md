# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 5.2.x   | :white_check_mark: |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :x:                |
| 3.1.x   | :x:                |
| 3.0.x   | :x:                |
| 2.3.x   | :x:                |
| 2.2.x   | :x:                |
| 2.1.x   | :x:                |
| 2.0.x   | :x:                |
| < 2.0   | :x:                |

## Future Security Recommendations

The following security improvements are planned for future releases:

- Migrate from pickle to a safer serialization format such as JSON or
  [MessagePack][].
- Upgrade the hashing algorithm for integrity verification from MD5 to SHA-256
  or SHA-3.
- Implement digital signatures for corpus files to ensure authenticity.
- Add version tracking to the corpus to prevent rollback attacks.

[MessagePack]: https://msgpack.org/
