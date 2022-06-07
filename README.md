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

Make model cards from the [default model card template](https://github.com/nateraw/modelcards/blob/main/modelcards/modelcard_template.md).

```python
from modelcards import CardData, ModelCard

repo_id = "nateraw/my-cool-model-with-card"

# Card metadata that will be included as a YAML block at the top of the card.
card_data = CardData(
    language='en',
    license='mit',
    library_name='timm',
    tags=['image-classification', 'resnet'],
    datasets='imagenet',
    metrics=['acc', 'f1'],
)

# Initialize card from default template, including card data defined above
card = ModelCard.from_template(
    card_data,
    model_id=repo_id.split('/')[-1],  # Jinja template kwarg
    model_description="Some really helpful description...",  # Jinja template kwarg
)
```

👀 You can see what the resulting model card here looks like at [this Hugging Face Hub repo](https://huggingface.co/nateraw/my-cool-model-with-card).

Note: you can make your own template and supply that to the `from_template` method by using the `template_path` argument.
