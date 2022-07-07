import re
import tempfile
from pathlib import Path
from typing import Optional, Union

import jinja2
import requests
import yaml
from huggingface_hub import hf_hub_download, upload_file
from huggingface_hub.utils.logging import get_logger

from .card_data import DatasetCardData, ModelCardData

TEMPLATE_MODELCARD_PATH = Path(__file__).parent / "modelcard_template.md"
REGEX_YAML_BLOCK = re.compile(r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r]")


logger = get_logger(__name__)


def parse_repocard_content(content, return_text=False):
    """Parse repocard metadata dict and (optionally) the accompanying
    card content from a string.

    Args:
        content (_type_): _description_
        return_text (bool, optional): _description_. Defaults to False.

    Raises:
        ValueError: When the repocard metadata is found but is not a dict

    Returns:
        If `return_text` is False:

        `dict`: the metadata dict loaded from YAML header.

        If `return_text` is True:

        (`dict`, `str): Both the metadata dict and card text content.

    Example:
        >>> from modelcards.cards import parse_repo_content

        >>> # Some string content we want to parse
        >>> content = '''
        ... ---
        ... language: en
        ... license: mit
        ... ---
        ... # My Cool Card!
        ... '''

        >>> # Return just metadata dict
        >>> metadata = parse_repocard_content(content)
        >>> assert metadata == {'language': 'en', 'license': 'mit'}

        >>> # Return both metadata dict and text
        >>> metadata, text = parse_repocard_content(content, return_text=True)
        >>> assert text == "# My Cool Card!"
        >>> assert metadata == {'language': 'en', 'license': 'mit'}
    """
    match = REGEX_YAML_BLOCK.search(content)
    if match:
        # Metadata found in the YAML block
        yaml_block = match.group(1)
        text = content[match.end() :]
        metadata = yaml.safe_load(yaml_block)

        # The YAML block's data should be a dictionary
        if not isinstance(metadata, dict):
            raise ValueError("repo card metadata block should be a dict")
    else:
        # Model card without metadata... create empty metadata
        logger.warning("Repo card metadata block was not found.")
        metadata = {}
        text = content

    if return_text:
        return metadata, text

    return metadata


class RepoCard:

    repo_type: str

    def __init__(self, content: str):
        """Initialize a RepoCard from string content. The content should be a
        Markdown file with a YAML block at the beginning and a Markdown body.

        Args:
            content (`str`): The content of the Markdown file.

        Raises:
            ValueError: When the content of the repo card metadata is not found.
            ValueError: When the content of the repo card metadata is not a dictionary.
        """
        self.content = content
        metadata, self.text = parse_repocard_content(content, return_text=True)
        self.data = (
            ModelCardData(**metadata)
            if self.repo_type == "model"
            else DatasetCardData(**metadata)
        )

    def __str__(self):
        return f"---\n{self.data.to_yaml()}\n---\n{self.text}"

    def save(self, filepath: Union[Path, str]):
        r"""Save a RepoCard to a file.

        Args:
            filepath (`Union[Path, str]`): Filepath to the markdown file to save.

        Example:
            >>> from modelcards import RepoCard
            >>> card = RepoCard("---\nlanguage: en\n---\n# This is a test repo card")
            >>> card.save("/tmp/test.md")
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(str(self), encoding="utf-8")

    @classmethod
    def load(cls, repo_id_or_path: Union[str, Path], repo_type=None, token=None):
        """Initialize a RepoCard from a Hugging Face Hub repo's README.md or a local filepath.

        Args:
            repo_id_or_path (`Union[str, Path]`):
                The repo ID associated with a Hugging Face Hub repo or a local filepath.
            repo_type (`str`, *optional*):
                The type of Hugging Face repo to push to. Defaults to None, which will use
                use "model". Other options are "dataset" and "space".
            token (`str`, *optional*):
                Authentication token, obtained with `huggingface_hub.HfApi.login` method. Will default to
                the stored token.

        Returns:
            `modelcards.RepoCard`: The RepoCard (or subclass) initialized from the repo's
                README.md file or filepath.

        Example:
            >>> from modelcards import RepoCard
            >>> card = RepoCard.load("nateraw/food")
            >>> assert card.data.tags == ["generated_from_trainer", "image-classification", "pytorch"]
        """

        if Path(repo_id_or_path).exists():
            card_path = Path(repo_id_or_path)
        else:
            card_path = hf_hub_download(
                repo_id_or_path, "README.md", repo_type=repo_type, use_auth_token=token
            )

        return cls(Path(card_path).read_text(encoding="utf-8"))

    def validate(self, repo_type="model"):
        """Validates card against Hugging Face Hub's model card validation logic.
        Using this function requires access to the internet, so it is only called
        internally by `modelcards.ModelCard.push_to_hub`.

        Args:
            repo_type (`str`, *optional*):
                The type of Hugging Face repo to push to. Defaults to None, which will use
                use "model". Other options are "dataset" and "space".
        """

        # TODO - compare against repo types constant in huggingface_hub if we move this object there.
        if repo_type not in ["model", "space", "dataset"]:
            raise RuntimeError(
                "Provided repo_type '{repo_type}' should be one of ['model', 'space',"
                " 'dataset']."
            )

        body = {
            "repoType": repo_type,
            "content": str(self),
        }
        headers = {"Accept": "text/plain"}

        try:
            r = requests.post(
                "https://huggingface.co/api/validate-yaml", body, headers=headers
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            if r.status_code == 400:
                raise RuntimeError(r.text)
            else:
                raise exc

    def push_to_hub(
        self,
        repo_id,
        token=None,
        # repo_type=None,
        commit_message=None,
        commit_description=None,
        revision=None,
        create_pr=None,
    ):
        """Push a RepoCard to a Hugging Face Hub repo.

        Args:
            repo_id (`str`):
                The repo ID of the Hugging Face Hub repo to push to. Example: "nateraw/food".
            token (`str`, *optional*):
                Authentication token, obtained with `huggingface_hub.HfApi.login` method. Will default to
                the stored token.
            repo_type (`str`, *optional*):
                The type of Hugging Face repo to push to. Defaults to None, which will use
                use "model". Other options are "dataset" and "space".
            commit_message (`str`, *optional*):
                The summary / title / first line of the generated commit
            commit_description (`str`, *optional*)
                The description of the generated commit
            revision (`str`, *optional*):
                The git revision to commit from. Defaults to the head of the
                `"main"` branch.
            create_pr (`bool`, *optional*):
                Whether or not to create a Pull Request with this commit. Defaults to `False`.
        Returns:
            `str`: URL of the commit which updated the card metadata.
        """
        # NOTE - removing this fo good soon
        # repo_name = repo_id.split("/")[-1]

        # if self.data.model_name and self.data.model_name != repo_name:
        #     logger.warning(
        #         f"Set model name {self.data.model_name} in CardData does not match "
        #         f"repo name {repo_name}. Updating model name to match repo name."
        #     )
        #     self.data.model_name = repo_name

        # Validate card before pushing to hub
        self.validate(repo_type=self.repo_type)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "README.md"
            tmp_path.write_text(str(self))
            url = upload_file(
                path_or_fileobj=str(tmp_path),
                path_in_repo="README.md",
                repo_id=repo_id,
                token=token,
                repo_type=self.repo_type,
                identical_ok=True,
                commit_message=commit_message,
                commit_description=commit_description,
                create_pr=create_pr,
                revision=revision,
            )
        return url

    @classmethod
    def from_template(cls, card_data, template_path, **template_kwargs):
        """Initialize a RepoCard from a template.

        Args:
            card_data (`modelcards.CardData`):
                The {Model|Dataset}CardData to use for the template.
            template_path (`str`):
                The path to the template file.
            **template_kwargs (`dict`):
                Keyword arguments to pass to the template.
        Returns:
            `modelcards.RepoCard`: The RepoCard initialized from the template.
        """
        template_path = Path(template_path)
        if not template_path.exists():
            raise RuntimeError(f"Template file {template_path} does not exist.")

        content = jinja2.Template(Path(template_path).read_text()).render(
            card_data=card_data.to_yaml(), **template_kwargs
        )
        return cls(content)


class ModelCard(RepoCard):

    repo_type = "model"

    @classmethod
    def from_template(
        cls,
        card_data: ModelCardData,
        template_path: Optional[str] = TEMPLATE_MODELCARD_PATH,
        **template_kwargs,
    ):
        """Initialize a ModelCard from a template. By default, it uses the default template.

        Templates are Jinja2 templates that can be customized by passing keyword arguments.

        Args:
            card_data (`modelcards.CardData`):
                A modelcards.CardData instance containing the metadata you want to include in the YAML
                header of the model card on the Hugging Face Hub.
            template_path (`str`, *optional*):
                A path to a markdown file with optional Jinja template variables that can be filled
                in with `template_kwargs`. Defaults to the default template which can be found here:
                https://github.com/nateraw/modelcards/blob/main/modelcards/modelcard_template.md

        Returns:
            `modelcards.ModelCard`: A ModelCard instance with the specified card data and content from the
            template.

        Example:
            >>> from modelcards import ModelCard, CardData, EvalResult

            >>> # Using the Default Template
            >>> card_data = CardData(
            ...     language='en',
            ...     license='mit',
            ...     library_name='timm',
            ...     tags=['image-classification', 'resnet'],
            ...     datasets='beans',
            ...     metrics=['accuracy'],
            ... )
            >>> card = ModelCard.from_template(
            ...     card_data,
            ...     model_description='This model does x + y...'
            ... )

            >>> # Including Evaluation Results
            >>> card_data = CardData(
            ...     language='en',
            ...     tags=['image-classification', 'resnet'],
            ...     eval_results=[
            ...         EvalResult(
            ...             task_type='image-classification',
            ...             dataset_type='beans',
            ...             dataset_name='Beans',
            ...             metric_type='accuracy',
            ...             metric_value=0.9,
            ...         ),
            ...     ],
            ...     model_name='my-cool-model',
            ... )
            >>> card = ModelCard.from_template(card_data)

            >>> # Using a Custom Template
            >>> card_data = CardData(
            ...     language='en',
            ...     tags=['image-classification', 'resnet']
            ... )
            >>> card = ModelCard.from_template(
            ...     card_data=card_data,
            ...     template_path='./modelcards/modelcard_template.md',
            ...     custom_template_var='custom value',  # will be replaced in template if it exists
            ... )

        """
        return super().from_template(card_data, template_path, **template_kwargs)


class DatasetCard(RepoCard):

    repo_type = "dataset"
