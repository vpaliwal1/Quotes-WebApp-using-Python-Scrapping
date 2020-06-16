
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
app = Flask(__name__)


def listOfTuples(l1, l2):
    return list(map(lambda x, y:(x,y), l1, l2))

@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            quotes_url = "https://www.brainyquote.com/search_results?q=" + searchString
            html_content = requests.get(quotes_url)
            quotes_html = bs(html_content.content, "html.parser")
            quotes_line = quotes_html.find(id='quotesList')
            job_elems = quotes_line.find_all('div', class_='clearfix')
            quotes_list = []
            author_list = []
            results=[]
            for job in job_elems:
                quotes = job.find('a', title='view quote')
                author = job.find("a", title="view author")
                if None in (quotes, author):
                    continue
                quotes_list.append(quotes.text)
                author_list.append(author.text)
            data = listOfTuples(quotes_list,author_list)
            for i in range(26):
                quotes1= data[i][0]
                author1= data[i][1]

                mydict = {"Search": searchString, "Quotes": quotes1, 'Author': author1}
                results.append(mydict)
            return render_template('results.html', reviews=results)
        except:
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000,debug=True)