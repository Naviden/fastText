# Contributing to fastText Modern
We want to make contributing to this project as easy and transparent as possible.

## Issues
We use GitHub issues to track public bugs. Please ensure your description is clear and has sufficient instructions to be able to reproduce the issue.

### Reproducing issues
Please make sure that the issue you mention is not a result of one of the existing third-party libraries. For example, please do not post an issue if you encountered an error within a third-party Python library. We can only help you with errors which can be directly reproduced either with our C++ code or the corresponding Python bindings. If you do find an error, please post detailed steps to reproduce it. If we can't reproduce your error, we can't help you fix it.

## Pull Requests
For substantial changes, please open an issue before submitting a pull request.
Small, well-scoped fixes may be submitted directly.

To create a pull request:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code is formatted consistently with the surrounding code.

## Tests
First, you will need to make sure you have the required data. For that, please have a look at the fetch_test_data.sh script under tests. Next run the tests using the runtests.py script passing a path to the directory containing the datasets.

## License
By contributing to fastText Modern, you agree that your contributions will be
licensed under the repository's MIT License. No separate contributor license
agreement is required by this fork.
