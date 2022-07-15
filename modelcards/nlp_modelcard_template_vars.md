---
model_id: # Required, name of the model (often the model on the HF Hub). Can be parsed from the repo_id.
model_summary: # Optional, a quick summary of what the model is/does. Example: "DistilGPT2 (short for Distilled-GPT2) is an English-language model  pre-trained with the supervision of the smallest version of Generative Pre-trained Transformer 2 (GPT-2)."
model_card_user: # Optional. Can be used to generate "Click to expand" sections with selected content from the model card based on the audience.
developers: # Optional, list of people who developed the model. Example: ['Person1', 'Person2']
shared_by: # Optional, list of people who shared the model. Example: ['Person3', 'Person4']
model_type: # Optional. Defaults to "Language model."
language: # Required, language(s) of the model. Also part of the model card metadata.
license: # Required, license associated with the model. Also part of the model card metatadata. Example: apache-2.0 or any license from https://hf.co/docs/hub/repositories-licenses
model_task: # Optional, task associated with the model. If value is one of the options from https://huggingface.co/tasks for NLP models, using underscores (e.g., "text_generation"), model card content in the "Uses" section can be auto-populated unless overriden.
related_models: # Optional, list of related models on the HF hub. Example: ['gpt2', 'distilgpt2']
parent_model: # Optional. If the model is a distilled model, can be used to indicate which model is the "parent" model (e.g., gpt2 for distilgpt2)
repo_link: # Optional, link to GitHub repository with code/other content related to the model.
paper_link: # Optional, link to academic paper or report related to the model. 
blog_link: # Optional, link to blog or website content related to the model.
direct_use: # Optional. If specified, content will be used to populate the "Direct Use" subsection of the model card. Example: "This model can be used for sentence summarization."
downstream_use: # Optional. If specified, content will be used to populate the "Downstream Use" subsection of the model card. Example: "This model can be used for downstream tasks that leverage text generation capabilities, including in chatbots, writing assistants, and related research projects." 
out_of_scope_use: # Optional. If specified, content will be used to populate the "Out of Scope Use" subsection of the model card. Example: "This model should not be used in biomedical settings or settings related to legal systems."
bias_risks_limitations: # Optional. If specified, content will be used to populate the "Bias, Risks, and Limitations" section of the model card. 
bias_recommendations: # Optional. If specified, content will be used to populate the "Recommendations" subsection of the "Bias, Risks, and Limitations" section of the model card. 
training_data: # Optional. If specified, content will be used to populate the "Training Data" subsection of the model card. 
training_datacard_link: # Optional, link to dataset card on the Hugging Face Hub associated with the training data (or some portion of the training data) for the model. 
preprocessing: # Optional. If specified, content will be used to populate the "Preprocessing" subsection of the model card's "Training Details" section.
speeds_sizes_times: # Optional. If specified, content will be used to populate the "Speeds, Sizes and Times" subsection of the model card's "Training Details" section.
testing_data: # Optional. If specified, content will be used to populate the "Testing Data" subsection of the model card. 
testing_datacard_link: # Optional, link to dataset card on the Hugging Face Hub associated with the testing data (or some portion of the testing data) for the model. 
testing_factors: # Optional. If specified, content will be used to populate the "Testing Factors" subsection of the model card. Testing factors are the variables the evaluation is disaggregating by, e.g., subpopulations or domains.
testing_metrics: # Optional. If specified, content will be used to populate the "Testing Metrics" subsection of the model card. This section should include the evaluation metrics used, ideally with a description of why.
testing_results: # Optional. If specified, content will be used to populate the "Results" subsection of the model card's "Evaluation" section.
model_examination: # Optional. If specified, content will be used to populate the "Model Examination" section of the model card.
hours_used: # Optional, time (in hours) training/fine-tuning the model. If specified, content will be used to populate part of the "Environmental Impact" section and can be used to calculate CO2 emissions.
cloud_provider: # Optional, cloud provider utilized for model development. If specified, content will be used to populate part of the "Environmental Impact" section and can be used to calculate CO2 emissions.
cloud_region: # Optional, cloud region utilized for model development. If specified, content will be used to populate part of the "Environmental Impact" section and can be used to calculate CO2 emissions.
co2_eq_emissions: # Optional, estimated CO2 emissions associated with training/fine-tuning the model. Can be computed using https://mlco2.github.io/impact#compute or another method. Should be reported in grams.
model_specs: # Optional, details related to the architecture and objective used to develop the model. If specified, content will be used to populate the "Model Architecture and Objective" subsection of the "Technical Specifications" section.
compute_infrastructure: # Optional, details related to the compute infrastructure used to develop the model. If specified, content will be used to populate the "Compute Infrastructure" subsection of the "Technical Specifications" section.
hardware: # Optional. If specified, content will be used to populate the "Hardware" subsection of the "Technical Specifications" section and the associated content in the "Environmental Impact section."
software: # Optional. If specified, content will be used to populate the "Software" subsection of the "Technical Specifications" section.
citation_bibtex: # Optional, bibtex formatted citation of associated paper. If specified, content will be used to populate the "Citation" section.
citation_apa: # Optional, APA formatted citation of associated paper. If specified, content will be used to populate the "Citation" section.
glossary: # Optional, could include terms or calculations used in the model card or helpful for understanding the model. If specified, content will be used to populate the "Glossary" section.
more_information: # Optional, additional context or resources about the model. If specified, content will be used to populate the "More Information" section.
model_card_authors: # Optional. If specified, content will be used to populate the "Model Card Authors" section. Example: "This model card was written by the team at X."
model_card_contact: # Optional, list of contacts for the model. If specified, content will be used to populate the "Model Card Contact" section.
get_started_code: # Optional, code snippets for using the model. If specified, content will be used to populate the "How to Get Started with the Model" section.
---

This markdown file contains the spec for the NLP model card template variables that can be used to partially auto-generate model cards for NLP models. For model card metadata, see https://github.com/huggingface/hub-docs/blame/main/modelcard.md. 