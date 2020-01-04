from flask import Flask, render_template, request, send_file, abort
import requests
import datetime
import os

app = Flask(__name__)
API_KEY = 'wd2dtVwJNn1UkcMlTIR1zpaaGH23vCPJrW5IGSt4'
Token = 'GO6of8KnDETXY5miOJDp4PkAQnhMKRzc'

@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    global date,base
    base =request.base_url
    date = request.args.get('date')
    [y , m, d] = date.split('-')
    d1 = datetime.date(int(y), int(m), int(d))
    d2 = datetime.date.today()

    if d1 > d2:
        abort(404)

    if d1 <= d2:
        title = 'Here are your results:'
        results = eval(requests.get(
            'https://api.nasa.gov/planetary/apod?api_key='+API_KEY+'&date=' + date).content.decode(
            'utf-8'))
        return render_template('results.html',
                               the_title=title,
                               the_image=results['url'],
                               the_results=results['explanation'])


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to NASA apod app:')


@app.route('/pdf' , methods=['POST' , 'GET'])
def download() -> 'html':
    global date,base
    #base = 'https://flask-nasa-apod-v2.herokuapp.com/search4'
    url = base+'?date='+date+'&pdf=True'
    command = "curl -H 'Authentication: Token "+Token+"' \
    -d 'url="+url+"' \
    'https://htmlpdfapi.com/api/v1/pdf' > "+date+".pdf"
    os.system(command)
    file = send_file(date+'.pdf', mimetype='text/pdf', attachment_filename=date+'.pdf', as_attachment=True)
    os.remove(date+".pdf")
    return file


if __name__ == '__main__':
    app.run(debug=True)

