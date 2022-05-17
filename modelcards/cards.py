import re
import tempfile
from pathlib import Path
from typing import List, Optional, Union

import jinja2
import yaml
from huggingface_hub import hf_hub_download, upload_file

from .card_data import CardData, EvalResult, model_index_to_eval_results

TEMPLATE_MODELCARD_PATH = Path(__file__).parent / "modelcard_template.md"
REGEX_YAML_BLOCK = re.compile(
    r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r]([\S\s].*)", re.DOTALL
)


class RepoCard:
    def __init__(self, content: str):
        self.content = content
        match = REGEX_YAML_BLOCK.search(content)
        if match:
            yaml_block = match.group(1)
            self.text = match.group(2)
            data_dict = yaml.safe_load(yaml_block)
            if not isinstance(data_dict, dict):
                raise ValueError("repo card metadata block should be a dict")
        else:
            raise ValueError("could not find yaml block in repo card")

        model_index = data_dict.pop("model-index", None)
        if model_index:
            (
                data_dict["model_name"],
                data_dict["eval_results"],
            ) = model_index_to_eval_results(model_index)
        self.data = CardData(**data_dict)

    def __str__(self):
        return f"---\n{self.data.to_yaml()}\n---\n{self.text}"

    def save(self, filepath: Union[Path, str]):
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(str(self))

    @classmethod
    def load(cls, repo_id_or_path: Union[str, Path]):
        if Path(repo_id_or_path).exists():
            card_path = Path(repo_id_or_path)
        else:
            card_path = hf_hub_download(repo_id_or_path, "README.md")

        return cls(Path(card_path).read_text())

    def push_to_hub(self, repo_id, repo_type=None):
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
