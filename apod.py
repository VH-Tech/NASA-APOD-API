from flask import Flask, render_template, request, send_file, abort
import requests
import pdfkit
import os
import datetime

app = Flask(__name__)
API_KEY= 'wd2dtVwJNn1UkcMlTIR1zpaaGH23vCPJrW5IGSt4'


@app.route('/search4', methods=['POST', 'GET'])
def do_search() -> 'html':
    global date,base
    base =request.base_url
    print(base)
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
    global date
    pdfkit.from_url(base+'?date='+date+'&pdf=True', date+'.pdf')
    file = send_file(date+'.pdf', mimetype='text/pdf', attachment_filename=date+'.pdf', as_attachment=True)
    os.remove(date+".pdf")
    return file


if __name__ == '__main__':
    app.run(debug=True)





