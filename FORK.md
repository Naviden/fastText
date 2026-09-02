# About this fork

fastText Modern is an independently maintained fork of
[facebookresearch/fastText](https://github.com/facebookresearch/fastText). It
focuses on keeping the native library and Python bindings buildable and easy to
install on current platforms.

## Identity and compatibility

- The Python distribution is named `fasttext-modern`.
- The Python import remains `fasttext` for source compatibility.
- This project is not affiliated with or endorsed by Meta.
- fastText and Meta names and marks belong to their respective owners. Their
  use here identifies the upstream project and compatibility target.

## License and attribution

The upstream source is licensed under the MIT License. The original
[LICENSE](LICENSE), copyright notices, and Git history are preserved. New
contributions to this repository are made under the same MIT License.

## Models and datasets

This repository and its Python distributions contain source code only. Linked
pretrained models and datasets are provided by third parties or the upstream
project and may have separate terms. They are not relicensed or redistributed
by fastText Modern.

## Maintenance policy

The fork follows upstream bug fixes when they remain compatible with the goals
of this project. Fork releases use their own version numbers and changelog, and
changes are tested on the supported Python and native-platform matrix before
release.
