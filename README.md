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

card = ModelCard.load("nateraw/rare-puppers")

# Access its card data
print(card.data)

# Update its card data
card.data["library_name"] = "timm"

# Save it to a file
card.save("my_card.md")

# Or, push it to the hub directly to replace the existing card
card.push_to_hub("nateraw/rare-puppers")
```

Make model cards from the [default model card template](https://github.com/nateraw/modelcards/blob/main/modelcards/modelcard_template.md).

```python
from modelcards import ModelCard

repo_id = "nateraw/my-cool-model-with-card"

# Write/overwrite the model card in that repo
card = ModelCard.from_template(
    language='en',
    license='mit',
    library_name='timm',
    tags=['image-classification', 'resnet'],
    dataset='imagenet',
    metrics=['acc', 'f1'],
    model_id=repo_id.split('/')[-1],  # Included in the template
    model_description="Some really helpful description...",  # Included in the template
)
```

👀 You can see what the resulting model card here looks like at [this Hugging Face Hub repo](https://huggingface.co/nateraw/my-cool-model-with-card).

Note: you can make your own template and supply that to the `from_template` method by using the `template_path` argument.

## TODOs

- [ ] Support evaluation metrics
- [ ] Data validation on card data
