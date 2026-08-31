"""Regression tests for the Python API on NumPy 2.x."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest

import numpy as np


def load_fasttext_module():
    """Load FastText.py without requiring the compiled extension."""
    binding = types.ModuleType("fasttext_pybind")
    binding.loss_name = types.SimpleNamespace()
    binding.model_name = types.SimpleNamespace(supervised="supervised")
    previous_binding = sys.modules.get("fasttext_pybind")
    sys.modules["fasttext_pybind"] = binding

    module_path = (
        Path(__file__).parents[1]
        / "python"
        / "fasttext_module"
        / "fasttext"
        / "FastText.py"
    )
    spec = importlib.util.spec_from_file_location("fasttext_numpy_test", module_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    finally:
        if previous_binding is None:
            sys.modules.pop("fasttext_pybind", None)
        else:
            sys.modules["fasttext_pybind"] = previous_binding
    return module


FastText = load_fasttext_module()


class FakeMeter:
    def scoreVsTrue(self, label_id):
        return [(0.9, True), (0.1, False)]

    def precisionRecallCurve(self):
        return [(1.0, 0.5), (0.5, 1.0)]


class FakeModel:
    def get_label_id(self, label):
        return 0


class FakePredictor:
    def predict(self, text, k, threshold, on_unicode_error):
        return [(0.75, "__label__positive")]


class NumpyCompatibilityTest(unittest.TestCase):
    def test_default_thread_count_is_always_positive(self):
        self.assertGreaterEqual(FastText.unsupervised_default["thread"], 1)

    def test_meter_results_allow_numpy_to_copy(self):
        meter = FastText._Meter(FakeModel(), FakeMeter())

        scores, truth = meter.score_vs_true("__label__positive")
        precision, recall = meter.precision_recall_curve()

        np.testing.assert_array_equal(scores, [0.9, 0.1])
        np.testing.assert_array_equal(truth, [True, False])
        np.testing.assert_array_equal(precision, [1.0, 0.5])
        np.testing.assert_array_equal(recall, [0.5, 1.0])

    def test_predict_probabilities_allow_numpy_to_copy(self):
        model = object.__new__(FastText._FastText)
        model.f = FakePredictor()

        labels, probabilities = model.predict("example")

        self.assertEqual(labels, ("__label__positive",))
        np.testing.assert_array_equal(probabilities, [0.75])


if __name__ == "__main__":
    unittest.main()
