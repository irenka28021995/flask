from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' %self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/cafe')
def cafe():
    return render_template("cafe.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"



@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:

            db.session.commit()
            return redirect('/posts')
        except:
            return "Произошла ошибка"

    else:
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)




@app.route('/create-article', methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Произошла ошибка"

    else:
        return render_template("create-article.html")

@app.route('/picca')
def picca():
    return render_template("picca.html")





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
