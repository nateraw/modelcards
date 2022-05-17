import tempfile
from pathlib import Path

import pytest

from modelcards import ModelCard, RepoCard


def test_load_repocard_from_file():
    sample_path = Path(__file__).parent / 'samples' / "sample_1.md"
    card = RepoCard.load(sample_path)
    assert card.data.to_dict() == {
        'language': ['en'],
        'license': 'mit',
        'library_name': 'pytorch-lightning',
        'tags': ['pytorch', 'image-classification'],
        'datasets': ['beans'],
        'metrics': ['acc'],
    }
    assert card.text.strip().startswith("# my-cool-model"), "Card text not loaded properly"


def test_change_repocard_data():
    sample_path = Path(__file__).parent / 'samples' / "sample_1.md"
    card = RepoCard.load(sample_path)
    card.data.language = ['fr']

    with tempfile.TemporaryDirectory() as tempdir:
        updated_card_path = Path(tempdir) / "updated.md"
        card.save(updated_card_path)

        updated_card = RepoCard.load(updated_card_path)
        assert updated_card.data.language == ['fr'], "Card data not updated properly"


def test_model_card_from_default_template():

    card = ModelCard.from_template(
        language='en',
        license='mit',
        library_name='pytorch',
        tags=['image-classification', 'resnet'],
        datasets='imagenet',
        metrics=['acc', 'f1'],
        model_id=None,
    )
    assert card.text.strip().startswith("# MyModelName"), "Default model name not set correctly"


def test_model_card_from_default_template_with_model_id():
    card = ModelCard.from_template(
        language='en',
        license='mit',
        library_name='pytorch',
        tags=['image-classification', 'resnet'],
        datasets='imagenet',
        metrics=['acc', 'f1'],
        model_id="my-cool-model",
    )
    assert card.text.strip().startswith("# my-cool-model"), "model_id not properly set in card template"


def test_model_card_from_custom_template():
    template_path = Path(__file__).parent / 'samples' / "sample_template.md"
    card = ModelCard.from_template(
        language='en',
        license='mit',
        library_name='pytorch',
        tags="text-classification",
        datasets='glue',
        metrics='acc',
        template_path=template_path,
        some_data='asdf',
    )

    assert card.text.endswith('asdf'), "Custom template didn't set jinja variable correctly"
