from flask import Flask, request, jsonify, render_template
import re
from extractive import read_article, read_text, preprocess, score_sentences, build_summary, chunk_text, remove_duplicates
from abstractive import get_hf_summary
app = Flask(__name__)
# @app.route('/')
# @app.route('/index2')
# def index():
#     name = 'Rosalia'
#     return render_template('index2.html', title='Welcome', username=name)



@app.route('/')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    # if request.method == 'POST':
    #     form_data = request.form
    #     return render_template('data.html',form_data = form_data)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        summary_data = dict()
        summary_data['url'] = 'N/A'
        summary_data['extractive_summary'] = ['N/A']
        summary_data['abstractive_summary'] = ['N/A']
        if 'url' in form_data.keys():
            url = form_data['input']
            summary_data['url'] = url
            article_text = read_article(url)
        else:
            article_text = read_text(form_data['input'])
        summary_data['article_text'] = article_text
        chunks = preprocess(article_text)
        
        if 'extractive' in form_data.keys():
            summaries = score_sentences(chunks, article_text, 4)
            extractive_sentences=build_summary(summaries)
            summary_data['extractive_summary'] = extractive_sentences
        
        if 'abstractive' in form_data.keys():
            abstractive_sentences = get_hf_summary(chunks)
            summary_data['abstractive_summary'] = abstractive_sentences       
        summary_data['extractive_summary'] = ' '.join(summary_data['extractive_summary'])
        summary_data['abstractive_summary'] = ' '.join(summary_data['abstractive_summary'])
        return render_template('data.html', summary_data=summary_data)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)