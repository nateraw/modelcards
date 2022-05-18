import re
import tempfile
from pathlib import Path
from typing import List, Optional, Union

import jinja2
import yaml
from huggingface_hub import hf_hub_download, upload_file
from huggingface_hub.utils.logging import get_logger

from .card_data import CardData, EvalResult, model_index_to_eval_results

TEMPLATE_MODELCARD_PATH = Path(__file__).parent / "modelcard_template.md"
REGEX_YAML_BLOCK = re.compile(
    r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r]([\S\s].*)", re.DOTALL
)

logger = get_logger(__name__)


class RepoCard:
    def __init__(self, content: str):
        """Initialize a RepoCard from string content. The content should be a
        Markdown file with a YAML block at the beginning and a Markdown body.

        Args:
            content (str): The content of the Markdown file.

        Raises:
            ValueError: When the content of the repo card metadata is not found.
            ValueError: When the content of the repo card metadata is not a dictionary.
        """
        self.content = content
        match = REGEX_YAML_BLOCK.search(content)
        if match:
            # Metadata found in the YAML block
            yaml_block = match.group(1)
            self.text = match.group(2)
            data_dict = yaml.safe_load(yaml_block)

            # The YAML block's data should be a dictionary
            if not isinstance(data_dict, dict):
                raise ValueError("repo card metadata block should be a dict")
        else:
            # Model card without metadata... create empty metadata
            logger.warning(
                "Repo card metadata block was not found. Setting CardData to empty."
            )
            data_dict = {}
            self.text = content

        model_index = data_dict.pop("model-index", None)
        if model_index:
            try:
                model_name, eval_results = model_index_to_eval_results(model_index)
                data_dict["model_name"] = model_name
                data_dict["eval_results"] = eval_results
            except KeyError:
                logger.warning(
                    "Invalid model-index. Not loading eval results into CardData."
                )

        self.data = CardData(**data_dict)

    def __str__(self):
        return f"---\n{self.data.to_yaml()}\n---\n{self.text}"

    def save(self, filepath: Union[Path, str]):
        r"""Save a RepoCard to a file.

        Args:
            filepath (Union[Path, str]): Filepath to the markdown file to save.

        Example:
            >>> from modelcards import RepoCard
            >>> card = RepoCard("---\nlanguage: en\n---\n# This is a test repo card")
            >>> card.save("/tmp/test.md")
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(str(self))

    @classmethod
    def load(cls, repo_id_or_path: Union[str, Path]):
        """Initialize a RepoCard from a Hugging Face Hub repo's README.md or a local filepath.

        Args:
            repo_id_or_path (Union[str, Path]):
                The repo ID associated with a Hugging Face Hub repo or a local filepath.

        Returns:
            modelcards.RepoCard: The RepoCard (or subclass) initialized from the repo's
                README.md file or filepath.

        Example:
            >>> from modelcards import RepoCard
            >>> card = RepoCard.load("nateraw/food")
            >>> assert card.data.tags == ["generated_from_trainer", "image-classification", "pytorch"]
        """
        if Path(repo_id_or_path).exists():
            card_path = Path(repo_id_or_path)
        else:
            card_path = hf_hub_download(repo_id_or_path, "README.md")

        return cls(Path(card_path).read_text())

    def push_to_hub(self, repo_id, repo_type=None):
        """Push a RepoCard to a Hugging Face Hub repo.

        Args:
            repo_id (str):
                The repo ID of the Hugging Face Hub repo to push to. Example: "nateraw/food".
            repo_type (str, optional):
                The type of Hugging Face repo to push to. Defaults to None, which will use
                use "model". Other options are "dataset" and "space".
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir) / "README.md"
            tmp_path.write_text(str(self))
            upload_file(
                path_or_fileobj=str(tmp_path),
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type=repo_type,
                identical_ok=True,
            )


class ModelCard(RepoCard):
    @classmethod
    def from_template(
        cls,
        language: Optional[Union[str, List[str]]] = None,
        license: Optional[str] = None,
        library_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        datasets: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        eval_results: Optional[Union[List[EvalResult], EvalResult]] = None,
        model_name: Optional[str] = None,
        template_path: Optional[str] = TEMPLATE_MODELCARD_PATH,
        **template_kwargs,
    ):
        """Initialize a ModelCard from a template. By default, it uses the default template.

        Templates are Jinja2 templates that can be customized by passing keyword arguments.

        Args:
            language (Optional[Union[str, List[str]]], optional):
                Language of model's training data or metadata. Example: 'en' Defaults to None.
            license (Optional[str], optional):
                License of this model. Example: apache-2.0 or any license from
                https://hf.co/docs/hub/model-repos#list-of-license-identifiers. Defaults to None.
            library_name (Optional[str], optional):
                Name of library used by this model. Example: keras or any library from
                https://github.com/huggingface/huggingface_hub/blob/main/js/src/lib/interfaces/Libraries.ts.
                Defaults to None.
            tags (Optional[List[str]], optional):
                List of tags to add to your model that can be used when filtering on the Hugging
                Face Hub. Defaults to None.
            datasets (Optional[Union[str, List[str]]], optional):
                Dataset or list of datasets that were used to train this model. Should be a dataset ID
                found on https://hf.co/datasets. Defaults to None.
            metrics (Optional[Union[str, List[str]]], optional):
                List of metrics used to evaluate this model. Should be a metric name that can be found
                at https://hf.co/metrics. Example: 'accuracy'. Defaults to None.
            eval_results (Optional[Union[List[EvalResult], EvalResult]], optional):
                List of `modelcards.EvalResult` that define evaluation results of the model. If provided,
                model_name kwarg must be provided. Defaults to None.
            model_name (Optional[str], optional):
                A name for this model. Required if you provide `eval_results`. It is used along with
                `eval_results` to construct the `model-index` within the card's metadata. The name
                you supply here is what will be used on PapersWithCode's leaderboards. Defaults to None.
            template_path (Optional[str], optional):
                A path to a markdown file with optional Jinja template variables that can be filled
                in with `template_kwargs`. Defaults to the default template which can be found here:
                https://github.com/nateraw/modelcards/blob/main/modelcards/modelcard_template.md

        Returns:
            modelcards.ModelCard: A ModelCard instance with the specified card data and content from the
            template.

        Example:
            >>> from modelcards import ModelCard

            >>> # Using the Default Template
            >>> card = ModelCard.from_template(
            ...     language='en',
            ...     license='mit',
            ...     library_name='timm',
            ...     tags=['image-classification', 'resnet'],
            ...     datasets='imagenet',
            ...     metrics=['accuracy'],
            ... )

            >>> # Including Evaluation Results
            >>> card = ModelCard.from_template(
            ...     language='en',
            ...     tags=['image-classification', 'resnet'],
            ...     eval_results=[
            ...         EvalResult(
            ...             task_type='image-classification',
            ...             dataset_type='beans',
            ...             dataset_name='Beans',
            ...             metric_type='acc',
            ...             metric_value=0.9,
            ...         ),
            ...     ],
            ...     model_name='my-cool-model',
            ... )

            >>> # Using a Custom Template
            >>> card = ModelCard.from_template(
            ...     language='en',
            ...     tags=['image-classification', 'resnet'],
            ...     template_path='./modelcards/modelcard_template.md',
            ...     custom_template_var='custom value',  # will be replaced in template
            ... )

        """
        card_data = CardData(
            language=language,
            license=license,
            library_name=library_name,
            tags=tags,
            datasets=datasets,
            metrics=metrics,
            eval_results=eval_results,
            model_name=model_name,
        )
        content = jinja2.Template(Path(template_path).read_text()).render(
            card_data=card_data.to_yaml(), **template_kwargs
        )
        return cls(content)
