---
{{card_data}}
---

{% set lm_task_entries = {
    'text_generation': {
        'direct_use': "The model can be used for text generation.", 
        'downstream_use': "To learn more about this task and potential downstream uses, see the Hugging Face [text generation docs](https://huggingface.co/tasks/text-generation)", 
        'misuse': "The model was not trained to be factual or true representations of people or events, and therefore using the models to generate such content is out-of-scope for the abilities of this model."
    },
    'question_answering': {
        'direct_use': "The model can be used for question answering.", 
        'downstream_use': "Potential types of question answering include extractive QA, open generative QA, and closed generative QA. To learn more about this task and potential downstream uses, see the Hugging Face [question answering docs](https://huggingface.co/tasks/question-answering)", 
        'misuse': "The model was not trained to be factual or true representations of people or events, and therefore using the models to generate such content is out-of-scope for the abilities of this model."
    },
    'fill_mask': {
        'direct_use': "The model can be used for masked language modeling.", 
        'downstream_use': "Masked language modeling are sometimes used to train large models for domain-specific problems. To learn more about this task and potential downstream uses, see the Hugging Face [fill mask docs](https://huggingface.co/tasks/fill-mask)", 
        'misuse': "The model was not trained to be factual or true representations of people or events, and therefore using the models to generate such content is out-of-scope for the abilities of this model."
    },
    'sentence_similarity': {
        'direct_use': "The model can be used for sentence similarity, the task of determining how similar two texts are.", 
        'downstream_use': "Potential downstream use cases may include information retreival and clustering or grouping. To learn more about sentence similarity and potential downstream uses, see the Hugging Face [sentence similarity docs](https://huggingface.co/tasks/sentence-similarity)", 
        'misuse': ""
    },
    'summarization': {
        'direct_use': "The model can be used for summarization.", 
        'downstream_use': "To learn more about summarization and potential downstream uses, see the Hugging Face [summarization docs](https://huggingface.co/tasks/summarization).", 
        'misuse': "The model was not trained to be factual or true representations of people or events, and therefore using the models to generate such content is out-of-scope for the abilities of this model."
    },
    'text_classification': {
        'direct_use': "The model can be used for text classification, the task of assigning a label or class to a given text.", 
        'downstream_use': "Potential downstream use cases include sentiment analysis, natural language inference, and assessing grammatical correctness. To learn more about text classification and other potential downstream uses, see the Hugging Face [text classification docs](https://huggingface.co/tasks/text-classification).", 
        'misuse': ""
    },
    'token_classification': {
        'direct_use': "The model can be used for token classification, a natural language understanding task in which a label is assigned to some tokens in a text.", 
        'downstream_use': "Potential downstream use cases include Named Entity Recognition (NER) and Part-of-Speech (PoS) tagging. To learn more about token classification and other potential downstream use cases, see the Hugging Face [token classification docs](https://huggingface.co/tasks/token-classification).", 
        'misuse': ""
    },
    'translation': {
        'direct_use': "The model can be used for translation, the task of converting text from one language to another.", 
        'downstream_use': "Potential downstream use cases include use cases that leverage conversational agents across different languages. To learn more about translation and other potential downstream use cases, see the Hugging Face [translation docs](https://huggingface.co/tasks/translation).", 
        'misuse': ""
    },
} %}

{% set task_list = [
    'text_generation', 
    'question_answering', 
    'fill_mask', 
    'sentence_similarity', 
    'summarization', 
    'text_classification',
    'token_classification', 
    'translation'
] %}


# Model Card for {{ model_id }}

<!-- Provide a quick summary of what the model is/does. [Optional] -->
{{ model_summary }}

{% if model_card_user == "policymaker" %}
<details>
<summary> Click to expand policymaker version of model card </summary>

# Table of Contents 

1. [Model Details](#model-details)
2. [Uses](#uses)
3. [Bias, Risks, and Limitations](#bias-risks-and-limitations)
4. [Model Examination](#model-examination)
5. [Environmental Impact](#environmental-impact)
6. [Citation](#citation)
7. [Glossary](#glossary-optional)
8. [More Information](#more-information-optional)
9. [Model Card Authors](#model-card-authors-optional)
10. [Model Card Contact](#model-card-contact)

</details>

{% endif %}


#  Table of Contents

1. [Model Details](#model-details)
2. [Uses](#uses)
3. [Bias, Risks, and Limitations](#bias-risks-and-limitations)
4. [Training Details](#training-details)
5. [Evaluation](#evaluation)
6. [Model Examination](#model-examination)
7. [Environmental Impact](#environmental-impact)
8. [Technical Specifications](#technical-specifications-optional)
9. [Citation](#citation)
10. [Glossary](#glossary-optional)
11. [More Information](#more-information-optional)
12. [Model Card Authors](#model-card-authors-optional)
13. [Model Card Contact](#model-card-contact)
14. [How To Get Started With the Model](#how-to-get-started-with-the-model)


# Model Details

## Model Description

<!-- Provide a longer summary of what this model is/does. -->
{{ model_description }}

- **Developed by:** {{ developers | join(', ') | default("More information needed", true)}}
- **Shared by [Optional]:** {{ shared_by | join(', ') | default("More information needed", true)}}
- **Model type:** {{ model_type | default("Language model", true)}}
- **Language(s) (NLP):** {{ card_data.language | join(', ') | default("More information needed", true)}}
- **License:** {{ card_data.license | default("More information needed", true)}}
- **Related Models:** {{ related_models | join(', ') | default("More information needed", true)}}
    - **Parent Model:** {{ parent_model | default("More information needed", true)}}
- **Resources for more information:** {{ more_resources | default("More information needed", true)}}
{{ "    - [GitHub Repo]({0})".format(repo_link) if repo_link }}
{{ "    - [Associated Paper]({0})".format(paper_link) if paper_link }} 
{{ "    - [Blog Post]({0})".format(blog_link) if blog_link }}

# Uses

<!-- Address questions around how the model is intended to be used, including the foreseeable users of the model and those affected by the model. -->

## Direct Use

<!-- This section is for the model use without fine-tuning or plugging into a larger ecosystem/app. -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->
{% if direct_use is defined %}
{{ direct_use }}
{% elif model_task in task_list %}
{{ lm_task_entries[model_task]['direct_use'] }}
{% else %}
More information needed.
{% endif %}

## Downstream Use [Optional]

<!-- This section is for the model use when fine-tuned for a task, or when plugged into a larger ecosystem/app -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->
{% if downstream_use is defined %} 
{{ downstream_use }}
{% elif model_task in task_list %} 
{{ lm_task_entries[model_task]['downstream_use'] }}
{% else %} 
More information needed.
{% endif %}

## Out-of-Scope Use

<!-- This section addresses misuse, malicious use, and uses that the model will not work well for. -->
<!-- If the user enters content, print that. If not, but they enter a task in the list, use that. If neither, say "more info needed." -->
{% if out_of_scope_use is defined %}
{{ out_of_scope_use }}
{% elif model_task in task_list %}
The model should not be used to intentionally create hostile or alienating environments for people. {{ lm_task_entries[model_task]['misuse'] }}
{% else %}
More information needed.
{% endif %}

# Bias, Risks, and Limitations

<!-- This section is meant to convey both technical and sociotechnical limitations. -->
{% if bias_risks_limiations is defined %}
{{ bias_risks_limitations }}
{% else %}
Significant research has explored bias and fairness issues with language models (see, e.g., [Sheng et al. (2021)](https://aclanthology.org/2021.acl-long.330.pdf) and [Bender et al. (2021)](https://dl.acm.org/doi/pdf/10.1145/3442188.3445922)). Predictions generated by the model may include disturbing and harmful stereotypes across protected classes; identity characteristics; and sensitive, social, and occupational groups.
{% endif %}

## Recommendations

<!-- This section is meant to convey recommendations with respect to the bias, risk, and technical limitations. -->

{% if bias_recommendations is defined %}
{{ bias_recommendations }}
{% else %}
Users (both direct and downstream) should be made aware of the risks, biases and limitations of the model. More information needed for further recomendations.
{% endif %}

# Training Details

## Training Data

<!-- This should link to a Data Card, perhaps with a short stub of information on what the training data is all about as well as documentation related to data pre-processing or additional filtering. -->

{{ training_data | default("More information on training data needed", true)}}
{{ "See the associated [dataset card]({0}) for further details.".format(training_datacard_link) if training_data_card_link }}

## Training Procedure

<!-- This relates heavily to the Technical Specifications. Content here should link to that section when it is relevant to the training procedure. -->

### Preprocessing

{{ preprocessing | default("More information needed", true)}}

### Speeds, Sizes, Times

<!-- This section provides information about throughput, start/end time, checkpoint size if relevant, etc. -->

{{ speeds_sizes_times | default("More information needed", true)}}
 
# Evaluation

<!-- This section describes the evaluation protocols and provides the results. -->

## Testing Data, Factors & Metrics

### Testing Data

<!-- This should link to a Data Card if possible. -->

{{ testing_data | default("More information needed", true)}}
{{ "See the associated [dataset card]({0}) for further details.".format(testing_datacard_link) if testing_data_card_link }}

### Factors

<!-- These are the things the evaluation is disaggregating by, e.g., subpopulations or domains. -->

{{ testing_factors | default("More information needed", true)}}

### Metrics

<!-- These are the evaluation metrics being used, ideally with a description of why. -->

{{ testing_metrics | default("More information needed", true)}}

## Results 

{{ results | default("More information needed", true)}}

# Model Examination

{{ model_examination | default("More information needed", true)}}

# Environmental Impact

<!-- Total emissions (in grams of CO2eq) and additional considerations, such as electricity usage, go here. Edit the suggested text below accordingly -->

Carbon emissions can be estimated using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700).

- **Hardware Type:** {{ hardware | default("More information needed", true)}}
- **Hours used:** {{ hours_used | default("More information needed", true)}}
- **Cloud Provider:** {{ cloud_provider | default("More information needed", true)}}
- **Compute Region:** {{ cloud_region | default("More information needed", true)}}
- **Carbon Emitted:** {{ co2_eq_emissions | default("More information needed", true)}}

# Technical Specifications [optional]

## Model Architecture and Objective

{{ model_specs | default("More information needed", true)}}

## Compute Infrastructure

{{ compute_infrastructure | default("More information needed", true)}}

### Hardware

{{ hardware | default("More information needed", true)}}

### Software

{{ software | default("More information needed", true)}}

# Citation

<!-- If there is a paper or blog post introducing the model, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

{{ citation_bibtex | default("More information needed", true)}}

**APA:**

{{ citation_apa | default("More information needed", true)}}

# Glossary [optional]

<!-- If relevant, include terms and calculations in this section that can help readers understand the model or model card. -->

{{ glossary | default("More information needed", true)}}

# More Information [optional]

{{ more_information | default("More information needed", true)}}

# Model Card Authors [optional]

<!-- This section provides another layer of transparency and accountability. Whose views is this model card representing? How many voices were included in its construction? Etc. -->

{{ model_card_authors | join(', ') | default("More information needed", true)}}

# Model Card Contact

{{ model_card_contact | join(', ') | default("More information needed", true)}}

# How to Get Started with the Model

Use the code below to get started with the model.

<details>
<summary> Click to expand </summary>

{{ get_started_code | default("More information needed", true)}}

</details>