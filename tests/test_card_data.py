from pathlib import Path

import pytest

from modelcards import ModelCard
from modelcards.card_data import (
    CardData,
    EvalResult,
    eval_results_to_model_index,
    model_index_to_eval_results,
)


def test_eval_results_to_model_index():
    sample_path = Path(__file__).parent / "samples" / "sample_simple_model_index.md"
    sample_card = ModelCard.load(sample_path)

    eval_results = [
        EvalResult(
            task_type="image-classification",
            dataset_type="beans",
            dataset_name="Beans",
            metric_type="acc",
            metric_value=0.9,
        ),
    ]

    model_index = eval_results_to_model_index("my-cool-model", eval_results)

    assert model_index == sample_card.data.to_dict()["model-index"]


def test_model_index_to_eval_results():
    model_index = [
        {
            "name": "my-cool-model",
            "results": [
                {
                    "task": {
                        "type": "image-classification",
                    },
                    "dataset": {
                        "type": "cats_vs_dogs",
                        "name": "Cats vs. Dogs",
                    },
                    "metrics": [
                        {
                            "type": "acc",
                            "value": 0.85,
                        },
                        {
                            "type": "f1",
                            "value": 0.9,
                        },
                    ],
                },
                {
                    "task": {
                        "type": "image-classification",
                    },
                    "dataset": {
                        "type": "beans",
                        "name": "Beans",
                    },
                    "metrics": [
                        {
                            "type": "acc",
                            "value": 0.9,
                        }
                    ],
                },
            ],
        }
    ]
    model_name, eval_results = model_index_to_eval_results(model_index)

    assert len(eval_results) == 3
    assert model_name == "my-cool-model"
    assert eval_results[0].dataset_type == "cats_vs_dogs"
    assert eval_results[1].metric_type == "f1"
    assert eval_results[1].metric_value == 0.9
    assert eval_results[2].task_type == "image-classification"
    assert eval_results[2].dataset_type == "beans"


def test_card_data_requires_model_name_for_eval_results():
    with pytest.raises(
        ValueError, match="`eval_results` requires `model_name` to be set."
    ):
        CardData(
            eval_results=[
                EvalResult(
                    task_type="image-classification",
                    dataset_type="beans",
                    dataset_name="Beans",
                    metric_type="acc",
                    metric_value=0.9,
                ),
            ],
        )

    data = CardData(
        model_name="my-cool-model",
        eval_results=[
            EvalResult(
                task_type="image-classification",
                dataset_type="beans",
                dataset_name="Beans",
                metric_type="acc",
                metric_value=0.9,
            ),
        ],
    )

    model_index = eval_results_to_model_index(data.model_name, data.eval_results)

    assert model_index[0]["name"] == "my-cool-model"
    assert model_index[0]["results"][0]["task"]["type"] == "image-classification"


def test_abitrary_incoming_card_data():
    data = CardData(
        model_name="my-cool-model",
        eval_results=[
            EvalResult(
                task_type="image-classification",
                dataset_type="beans",
                dataset_name="Beans",
                metric_type="acc",
                metric_value=0.9,
            ),
        ],
        some_abitrary_kwarg="some_value",
    )

    assert data.some_abitrary_kwarg == "some_value"

    data_dict = data.to_dict()
    assert data_dict["some_abitrary_kwarg"] == "some_value"
