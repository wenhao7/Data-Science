from transformers import pipeline
from transformers import T5ForConditionalGeneration, T5Tokenizer
from extractive import remove_duplicates
import re

model = T5ForConditionalGeneration.from_pretrained("t5-base")
tokenizer = T5Tokenizer.from_pretrained("t5-base")

def get_hf_summary(chunks):
    summaries=[]
    for chunk in chunks:
        
        # Model input
        inputs = tokenizer.encode("summarize: " + chunk, return_tensors = "pt", max_length = 512, truncation = True)

        # Model output
        outputs = model.generate(inputs, max_length = 512, min_length = 80,
                                 length_penalty = 5.0, num_beams = 2,
                                 early_stopping = True)
        summary = tokenizer.decode(outputs[0])
        summary = summary.replace('<pad>', '').replace('</s>', '').strip()

        summaries.append(summary)
        
    summaries_nodup = remove_duplicates(' '.join(summaries))
    sentences = re.split('(?<=[.!?]) +', summaries_nodup)
    sentences = [sentence.capitalize() for sentence in sentences]   
    return sentences