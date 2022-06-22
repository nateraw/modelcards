import logging
import tempfile
import uuid
from pathlib import Path

import pytest
import requests
from huggingface_hub import create_repo, delete_repo

from modelcards import CardData, ModelCard, RepoCard

from .hub_fixtures import HF_TOKEN, HF_USERNAME


@pytest.fixture
def repo_id(request):
    fn_name = request.node.name.lstrip("test_").replace("_", "-")
    repo_id = f"{HF_USERNAME}/{fn_name}-{uuid.uuid4()}"
    create_repo(repo_id, token=HF_TOKEN)
    yield repo_id
    delete_repo(repo_id, token=HF_TOKEN)


def test_load_repocard_from_file():
    sample_path = Path(__file__).parent / "samples" / "sample_simple.md"
    card = RepoCard.load(sample_path)
    assert card.data.to_dict() == {
        "language": ["en"],
        "license": "mit",
        "library_name": "pytorch-lightning",
        "tags": ["pytorch", "image-classification"],
        "datasets": ["beans"],
        "metrics": ["acc"],
    }
    assert card.text.strip().startswith(
        "# my-cool-model"
    ), "Card text not loaded properly"


def test_change_repocard_data():
    sample_path = Path(__file__).parent / "samples" / "sample_simple.md"
    card = RepoCard.load(sample_path)
    card.data.language = ["fr"]

    with tempfile.TemporaryDirectory() as tempdir:
        updated_card_path = Path(tempdir) / "updated.md"
        card.save(updated_card_path)

        updated_card = RepoCard.load(updated_card_path)
        assert updated_card.data.language == ["fr"], "Card data not updated properly"


def test_model_card_from_default_template():

    card = ModelCard.from_template(
        card_data=CardData(
            language="en",
            license="mit",
            library_name="pytorch",
            tags=["image-classification", "resnet"],
            datasets="imagenet",
            metrics=["acc", "f1"],
        ),
        model_id=None,
    )
    assert card.text.strip().startswith(
        "# MyModelName"
    ), "Default model name not set correctly"


def test_model_card_from_default_template_with_model_id():
    card = ModelCard.from_template(
        card_data=CardData(
            language="en",
            license="mit",
            library_name="pytorch",
            tags=["image-classification", "resnet"],
            datasets="imagenet",
            metrics=["acc", "f1"],
        ),
        model_id="my-cool-model",
    )
    assert card.text.strip().startswith(
        "# my-cool-model"
    ), "model_id not properly set in card template"


def test_model_card_from_custom_template():
    template_path = Path(__file__).parent / "samples" / "sample_template.md"
    card = ModelCard.from_template(
        card_data=CardData(
            language="en",
            license="mit",
            library_name="pytorch",
            tags="text-classification",
            datasets="glue",
            metrics="acc",
        ),
        template_path=template_path,
        some_data="asdf",
    )

    assert card.text.endswith(
        "asdf"
    ), "Custom template didn't set jinja variable correctly"


def test_model_card_data_must_be_dict():
    sample_path = Path(__file__).parent / "samples" / "sample_invalid_card_data.md"
    with pytest.raises(ValueError, match="repo card metadata block should be a dict"):
        ModelCard.load(sample_path)


def test_model_card_without_metadata(caplog):
    sample_path = Path(__file__).parent / "samples" / "sample_no_metadata.md"
    with caplog.at_level(logging.WARNING):
        card = ModelCard.load(sample_path)
    assert (
        "Repo card metadata block was not found. Setting CardData to empty."
        in caplog.text
    )
    assert card.data == CardData()


def test_model_card_with_invalid_model_index(caplog):
    """Test that when loading a card that has invalid model-index, no eval_results are added + it logs a warning"""
    sample_path = Path(__file__).parent / "samples" / "sample_invalid_model_index.md"
    with caplog.at_level(logging.WARNING):
        card = ModelCard.load(sample_path)
    assert "Invalid model-index. Not loading eval results into CardData." in caplog.text
    assert card.data.eval_results is None


def test_validate_modelcard(caplog):
    sample_path = Path(__file__).parent / "samples" / "sample_simple.md"
    card = RepoCard.load(sample_path)
    card.validate()

    card.data.license = "asdf"
    with pytest.raises(
        RuntimeError, match='- Error: YAML metadata schema issue on key "license"'
    ):
        card.validate()


def test_push_to_hub(repo_id):
    template_path = Path(__file__).parent / "samples" / "sample_template.md"
    card = ModelCard.from_template(
        card_data=CardData(
            language="en",
            license="mit",
            library_name="pytorch",
            tags="text-classification",
            datasets="glue",
            metrics="acc",
        ),
        template_path=template_path,
        some_data="asdf",
    )

    url = f"https://huggingface.co/{repo_id}/resolve/main/README.md"

    # Check this file doesn't exist (sanity check)
    with pytest.raises(requests.exceptions.HTTPError):
        r = requests.get(url)
        r.raise_for_status()

    # Push the card up to README.md in the repo
    card.push_to_hub(repo_id, token=HF_TOKEN)

    # No error should occur now, as README.md should exist
    r = requests.get(url)
    r.raise_for_status()


def test_push_and_create_pr(repo_id):
    template_path = Path(__file__).parent / "samples" / "sample_template.md"
    card = ModelCard.from_template(
        card_data=CardData(
            language="en",
            license="mit",
            library_name="pytorch",
            tags="text-classification",
            datasets="glue",
            metrics="acc",
        ),
        template_path=template_path,
        some_data="asdf",
    )

    url = f"https://huggingface.co/api/models/{repo_id}/discussions"
    r = requests.get(url)
    data = r.json()
    assert data["count"] == 0
    card.push_to_hub(repo_id, token=HF_TOKEN, create_pr=True)
    r = requests.get(url)
    data = r.json()
    assert data["count"] == 1
