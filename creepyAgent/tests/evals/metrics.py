from deepeval.metrics import AnswerRelevancyMetric, ContextualRelevancyMetric, GEval
from deepeval.test_case import SingleTurnParams


# Keep metrics in one module so eval files stay focused on app execution.
#
# TaskCompletionMetric and StepEfficiencyMetric were dropped: they require the
# judge model to reason over the full trace and emit a complex structured JSON
# schema, which the local llama3.1 judge could not reliably produce (DeepEval
# itself errored with "Evaluation LLM outputted an invalid JSON"). Sticking to
# metrics that need a single, simpler JSON verdict keeps the local judge usable.
GROUNDED_CITATION_METRIC = GEval(
    name="GroundedCitation",
    criteria=(
        "Determine whether the actual output is grounded strictly in the retrieved "
        "notes (no invented facts beyond what the notes/retrieval context contain) "
        "and explicitly cites which note(s) it drew from. If the retrieval context "
        "does not contain relevant information, the output should say it doesn't "
        "know instead of guessing."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.RETRIEVAL_CONTEXT,
    ],
)

SINGLE_TURN_TRACE_METRICS = [
    AnswerRelevancyMetric(),
    GROUNDED_CITATION_METRIC,
]

# Component-level metrics are span-specific. Name each list after the exact
# component/span it evaluates rather than sharing one generic list.
RETRIEVER_SPAN_METRICS = [
    ContextualRelevancyMetric(),
]
