# Text Summarizer
This project contains a simple web application that summarises text provided in its input. If user chooses to provide a URL as input, the app will scrape and summarize the provided webpage.

Two kinds of text summarization approaches are provided here:
- Extractive Summarization
  - Sentence importances are calculated based on the weighted frequencies of the words they contained, most important sentences of each paragraph will be kept in the summary.
  - Approach generates a subset of sentences from original text and does not "interpret" or "understand" the important aspects of the text.
- Abstractive Summarization
  - Algorithm "interpret" the input text and generates a suitable summary, leading to sentences that are different from the input
  - Project uses [Google's T5 model](https://huggingface.co/docs/transformers/en/model_doc/t5) that has been pretrained for text-to-text tasks including text summarization

# Demo Images
### Pasting a few paragraphs about Python and requesting the application for an extractive summary.
![form_python](/Text%20Summarizer/static/images/form_python_extractive.PNG)

### Extractive summary for Python
![summary_python](/Text%20Summarizer/static/images/summary_python_extractive.PNG)

### Pasting a link to Wikipedia page about Bears, indicating that this is a URL and requesting for both extractive and abstractive summaries
![form_bear](/Text%20Summarizer/static/images/form_bear_both.PNG)

### Extractive and abstractive summaries for Wikipedia Bear page
![summary_bear_input](/Text%20Summarizer/static/images/summary_bear_input.PNG)
![summary_bear_both](/Text%20Summarizer/static/images/summary_bear_both.PNG)
