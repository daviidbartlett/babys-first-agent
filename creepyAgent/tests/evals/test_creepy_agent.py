from importlib import import_module

import pytest

from deepeval import assert_test
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.tracing import next_retriever_span

from metrics import RETRIEVER_SPAN_METRICS, SINGLE_TURN_TRACE_METRICS


ai_app = import_module("ai_app")


dataset = EvaluationDataset()
dataset.add_goldens_from_json_file(file_path="tests/evals/dataset.json")


@pytest.mark.parametrize("golden", dataset.goldens)
def test_creepy_agent(golden: Golden):
    with next_retriever_span(metrics=RETRIEVER_SPAN_METRICS):
        ai_app.run_traced_ai_app(golden.input)
    assert_test(golden=golden, metrics=SINGLE_TURN_TRACE_METRICS)
