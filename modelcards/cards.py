import re
import tempfile
from pathlib import Path
from typing import List, Optional, Union

import jinja2
import yaml
from huggingface_hub import hf_hub_download, upload_file

TEMPLATE_MODELCARD_PATH = Path(__file__).parent / "modelcard_template.md"
REGEX_YAML_BLOCK = re.compile(r"---[\n\r]+([\S\s]*?)[\n\r]+---[\n\r]([\S\s].*)", re.DOTALL)


class RepoCard:
    def __init__(self, content: str):
        self.content = content
        match = REGEX_YAML_BLOCK.search(content)
        if match:
            yaml_block = match.group(1)
            self.text = match.group(2)
            self.data = yaml.safe_load(yaml_block)
            if not isinstance(self.data, dict):
                raise ValueError("repo card metadata block should be a dict")
        else:
            raise ValueError("could not find yaml block in repo card")

    def __str__(self):
        return f"---\n{yaml.dump(self.data, sort_keys=False)}\n---\n{self.text}"

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
                path_in_repo='README.md',
                repo_id=repo_id,
                repo_type=repo_type,
                identical_ok=True,
            )


class ModelCard(RepoCard):
    @classmethod
    def from_template(
        cls,
        language: Union[str, List[str]] = None,
        license: str = None,
        library_name: Optional[str] = None,
        tags: List[str] = None,
        dataset: List[str] = None,
        metrics: List[str] = None,
        template_path: str = TEMPLATE_MODELCARD_PATH,
        **template_kwargs,
    ):
        if type(language) == str:
            language = [language]
        if type(tags) == str:
            tags = [tags]
        if type(dataset) == str:
            dataset = [dataset]
        if type(metrics) == str:
            metrics = [metrics]

        card_data = {
            'language': language,
            'license': license,
            'library_name': library_name,
            'tags': tags,
            'dataset': dataset,
            'metrics': metrics,
        }
        content = jinja2.Template(Path(template_path).read_text()).render(
            card_data=yaml.dump(card_data, sort_keys=False).strip(), **template_kwargs
        )
        return cls(content)
