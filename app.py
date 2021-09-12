from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField
import random
import string
import apiscrape

app=Flask(__name__)
app.config['SECRET_KEY']=''.join(random.choice(string.ascii_uppercase + string.digits))
host="127.0.0.1"


class SearchForm(FlaskForm):
    searchTerm=StringField("Search Query")
    categoryList=SelectMultipleField('Categories',choices=apiscrape.indexerList(1))
    indexerList = SelectMultipleField('Categories', choices=apiscrape.indexerList(2))

@app.route('/',methods=['GET','POST'])
def searchform():
    form=SearchForm()
    if form.is_submitted():
        df=apiscrape.searchQuery(form.searchTerm.data,form.categoryList.data,form.indexerList.data)
        if df[0] is not "Empty":
            return render_template('search.html', form=form,
                                   results=df[0].to_html(index=False, escape=False, table_id="searchOutput",
                                                         classes="table table-striped", border=0), indexerstatus=df[1])
        return render_template('search.html',form=form,results="No results found")
    return render_template('search.html',form=form)
if __name__=='__main__':
    app.run(host=host)