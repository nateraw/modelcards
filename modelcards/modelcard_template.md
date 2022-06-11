---
{{ card_data }}
---

# {{ model_id | default("MyModelName", true)}}

## Table of Contents
- [Model Details](#model-details)
- [How To Get Started With the Model](#how-to-get-started-with-the-model)
- [Uses](#uses)
  - [Direct Use](#direct-use)
  - [Downstream Use](#downstream-use)
  - [Misuse and Out of Scope Use](#misuse-and-out-of-scope-use)
- [Limitations and Biases](#limitations-and-biases)
- [Training](#training)
  - [Training Data](#training-data)
  - [Training Procedure](#training-procedure)
- [Evaluation Results](#evaluation-results)
- [Environmental Impact](#environmental-impact)
- [Licensing Information](#licensing-information)
- [Citation Information](#citation-information)


## Model Details

<!-- Give an overview of your model, the relevant research paper, who trained it, etc.  -->

{{ model_description if model_description else "[More Information Needed]" }}

- Developed by: {{ authors if authors }}
- Language(s): {{ languages }}
- License: This model is licensed under the {{ license }}{{ " license" if "license" not in license.lower() }}
- Resources for more information:
{{ "  - [Research Paper](" + paper_url + ")" if paper_url }}
{{ "  - [GitHub Repo](" + github_url + ")" if github_url }}


## How to Get Started with the Model

Use the code below to get started with the model.

```python
# A nice code snippet here that describes how to use the model...
```

## Uses

#### Direct Use

<!-- Describe what kind of tasks this model can be used for directly or problems it can solve. -->

[More Information Needed]

#### Downstream Use

<!-- Describe how this model could be leveraged by a downstream model (if applicable) -->

[More Information Needed]

#### Misuse and Out-of-scope Use

<!-- Describe ways in which this model ***should not*** be used. -->

[More Information Needed]

## Limitations and Biases

<!-- Describe limitations and biases of this model or models of it's type. -->

**CONTENT WARNING: Readers should be aware this section contains content that is disturbing, offensive, and can propogate historical and current stereotypes.**

[More Information Needed]

## Training

#### Training Data

<!-- Describe the dataset used to train this model. -->
<!-- Refer to data card if dataset is provided and exists on the hub -->

See the data card for additional information.

#### Training Procedure

<!-- Describe the preprocessing, hardware used, training hyperparameters, etc. -->

[More Information Needed]

## Evaluation Results

<!-- Describe evaluation results of this model across any datasets it was evaluated on. -->

[More Information Needed]

## Environmental Impact

<!-- Provide information to document the environmental impact of this model -->

You can estimate carbon emissions using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700)

- **Hardware Type:**
- **Hours used:**
- **Cloud Provider:**
- **Compute Region:**
- **Carbon Emitted:** {{ emissions if emissions }}


## Citation Information

```bibtex
{{ bibtex_citations if bibtex_citations }}
```
