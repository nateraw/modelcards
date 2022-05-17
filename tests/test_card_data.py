from modelcards import ModelCard
from modelcards.card_data import CardData, EvalResult, eval_results_to_model_index, model_index_to_eval_results
from pathlib import Path


def test_eval_results_to_model_index():
    sample_path = Path(__file__).parent / 'samples' / "sample_simple_model_index.md"
    sample_card = ModelCard.load(sample_path)
    
    eval_results = [
        EvalResult(
            name='my-cool-model',
            task_type='image-classification',
            dataset_type='beans',
            dataset_name='Beans',
            metric_type='acc',
            metric_value=0.9,
        ),
    ]

    model_index = eval_results_to_model_index(eval_results)

    assert model_index == sample_card.data.to_dict()['model-index']


def test_model_index_to_eval_results():
    model_index = [
        {
            'name': 'my-cool-model',
            'results': [
                {
                    'task': {
                        'type': 'image-classification',

                    },
                    'dataset': {
                        'type': 'cats_vs_dogs',
                        'name': 'Cats vs. Dogs',
                    },
                    'metrics': [
                        {
                            'type': 'acc',
                            'value': 0.85,
                        },
                        {
                            'type': 'f1',
                            'value': 0.9,
                        }
                    ]
                },
                {
                    'task': {
                        'type': 'image-classification',
                    },
                    'dataset': {
                        'type': 'beans',
                        'name': 'Beans',
                    },
                    'metrics': [
                        {
                            'type': 'acc',
                            'value': 0.9,
                        }
                    ]
                },
            ]
        }
    ]
    eval_results = model_index_to_eval_results(model_index)
    assert len(eval_results) == 3
    
    assert all([e.name == 'my-cool-model' for e in eval_results])
    assert eval_results[0].dataset_type == 'cats_vs_dogs'
    assert eval_results[1].metric_type == 'f1'
    assert eval_results[1].metric_value == 0.9
    assert eval_results[2].name == 'my-cool-model'
    assert eval_results[2].task_type == 'image-classification'
    assert eval_results[2].dataset_type == 'beans'