# modelcards

<a href="https://colab.research.google.com/github/nateraw/modelcards/blob/main/modelcards_demo.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

📝 Utility to create, edit, and publish model cards on the Hugging Face Hub.

This repo is just an idea for now! :)

## Usage

### Installation

```
pip install modelcards
```

### Examples

Load a model card from a Hugging Face Hub repo:

```python
from modelcards import ModelCard

card = ModelCard.load("nateraw/food")

# Access its card data
print(card.data)

# Update its card data
card.data.library_name = "transformers"

# Save it to a file
card.save("my_card.md")

# Or, push it to the hub directly to replace the existing card
card.push_to_hub("nateraw/food")
```

Make model cards from the [default model card template](https://github.com/nateraw/modelcards/blob/main/modelcards/modelcard_template.md). 👀 You can see what the resulting model card looks like at [this Hugging Face Hub repo](https://huggingface.co/nateraw/my-cool-model-with-card).
```python
from modelcards import CardData, ModelCard

repo_id = "nateraw/my-cool-model-with-card"

# Initialize card from default template, including card data defined above
card = ModelCard.from_template(
    card_data=CardData(  # Card metadata object that will be converted to YAML block
        language='en',
        license='mit',
        library_name='timm',
        tags=['image-classification', 'resnet'],
        datasets='imagenet',
        metrics=['accuracy', 'f1'],
    ),
    model_id=repo_id.split('/')[-1],  # Jinja template kwarg
    model_description="Some really helpful description...",  # Jinja template kwarg
)
```

The `modelcards.CardData` class is used above to define some card metadata. This metadata is leveraged by the Hugging Face Hub to:
- enable discoverability of your model through filters
- provide a standardized way to share your evaluation results (which are then automatically posted to Papers With Code)
- enable the inference API if your model is compatible with one of the available Inference API pipelines.
- And more!


You can also make your own template and supply that to the `from_template` method by using the `template_path` argument.

```python
from pathlib import Path

from modelcards import CardData, ModelCard

template_text = """
---
{{ card_data }}
---

# {{ model_id | default("CoolModel") }}

This model is part of `super_cool_models` package (which doesn't exist)! It is a fine tuned `cool-model` on the `{{ dataset_name }}`.

## Intended uses & limitations

This model doesn't exist, so you probably don't want to use it! This is just an example template. Please write a very thoughtful model card ❤️
"""

Path('my_template.md').write_text(template_text)

card = ModelCard.from_template(
    card_data=CardData(  # Card metadata object that will be converted to YAML block
        language='en',
        license='mit',
        library_name='super_cool_models',
        tags=['image-classification', 'cool-model'],
        datasets='awesome-dataset',
        metrics=['accuracy', 'f1'],
    ),
    template_path='my_template.md', # The template we just wrote!
    model_id='cool-model',  # Jinja template kwarg
    dataset_name='awesome-dataset', # Jinja template kwarg
)
```
