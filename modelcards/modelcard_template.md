---
{{card_data}}
---

# {{ model_id | default("MyModelName", true)}}

## Model description

{{ model_description | default("The model description provides basic details about the model. This includes the architecture, version, if it was introduced in a paper, if an original implementation is available, the author, and general information about the model. Any copyright should be attributed here. General information about training procedures, parameters, and important disclaimers can also be mentioned in this section.", true)}}

## Intended uses & limitations

#### How to use

```python
# You can include sample code which will be formatted
```

#### Limitations and bias

Provide examples of latent issues and potential remediations.

## Training data

Describe the data you used to train the model.
If you initialized it with pre-trained weights, add a link to the pre-trained model card or repository with description of the pre-training data.

## Training procedure

Preprocessing, hardware used, hyperparameters...

## Eval results

Provide some evaluation results.

### BibTeX entry and citation info

```bibtex
@inproceedings{...,
  year={2020}
}
```
