# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 5.3.x   | :white_check_mark: |
| 5.2.x   | :white_check_mark: |
| 5.1.x   | :x:                |
| 5.0.x   | :x:                |
| 4.0.x   | :x:                |
| 3.1.x   | :x:                |
| 3.0.x   | :x:                |
| 2.3.x   | :x:                |
| 2.2.x   | :x:                |
| 2.1.x   | :x:                |
| 2.0.x   | :x:                |
| < 2.0   | :x:                |

## Verify release files

Releases after version 5.3.8 attach these files to each
[GitHub release](https://github.com/PyThaiNLP/pythainlp/releases):

- the wheel and the source distribution (sdist), as published on PyPI;
- the software bill of materials (SBOM), `pythainlp-<version>.spdx3.json`,
  byte-identical to the SBOM embedded in the wheel at
  `.dist-info/sboms/` ([PEP 770][]);
- a [Sigstore][] bundle (`<file>.sigstore.json`) for each of the three
  files above.

Each of the three files also has a GitHub artifact attestation
(build provenance).

To verify a downloaded file, put `<file>` and `<file>.sigstore.json`
in the same directory, then run:

```sh
pip install sigstore
python -m sigstore verify github <file> \
  --cert-identity https://github.com/PyThaiNLP/pythainlp/.github/workflows/pypi-publish.yml@refs/tags/v<version>
gh attestation verify <file> -R PyThaiNLP/pythainlp \
  --signer-workflow PyThaiNLP/pythainlp/.github/workflows/pypi-publish.yml \
  --source-ref refs/tags/v<version>
```

`<file>` is the wheel, the sdist, or the SBOM.

[PEP 770]: https://peps.python.org/pep-0770/
[Sigstore]: https://www.sigstore.dev/

## Future Security Recommendations

The following security improvements are planned for future releases:

- Migrate from pickle to a safer serialization format such as JSON or
  [MessagePack][].
- Upgrade the hashing algorithm for integrity verification from MD5 to SHA-256
  or SHA-3.
- Implement digital signatures for corpus files to ensure authenticity.
- Add version tracking to the corpus to prevent rollback attacks.

[MessagePack]: https://msgpack.org/
