# Changelog

All notable changes to fastText Modern are documented here.

## [0.10.0] - 2026-09-02

### Added

- Prebuilt CPython 3.10 through 3.14 wheels for Linux x86-64, Windows x86-64,
  macOS x86-64, and macOS Apple Silicon.
- Cross-platform native CMake validation and packaging tests.
- Trusted Publishing release automation for PyPI.

### Changed

- Renamed the Python distribution to `fasttext-modern`; the import remains
  `fasttext`.
- Raised the native compiler baseline to C++17 and CMake 3.16.
- Made host-specific CPU optimization opt-in for portable binaries.
- Declared Python 3.10 through 3.14 support and pybind11 3.x builds.

### Fixed

- NumPy 2 compatibility for prediction and evaluation arrays.
- Windows shared/static library and Python binding portability issues.
- Default thread selection on single-core systems.

[0.10.0]: https://github.com/Naviden/fastText/releases/tag/v0.10.0
