from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///beauty.db'
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300),nullable=False)
    text = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Review %r>' % self.id


@app.route('/')
@app.route('/index')
def index():
    return render_template ("index.html")

@app.route('/about')
def about():
    return render_template ("about.html")

@app.route('/create_review',methods=['POST', 'GET'])
def create_review():
    if request.method == "POST":
        name = request.form['name']
        text = request.form['text']

        review = Review(name=name,text=text)

        try:
            db.session.add(review)
            db.session.commit()
            return redirect('/reviews')
        except:
            return "Ошибка при добавлении отзыва"

    else:
        return render_template ("create_review.html")

@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.date.desc()).all()
    return render_template("reviews.html",reviews=reviews)

@app.route('/reviews/<int:id>')
def review_detail(id):
    review=Review.query.get(id)
    return render_template("review_detail.html",review=review)

@app.route('/service')
def service():
    return render_template ("service.html")


if __name__ == '__main__':
    app.run(debug=True)
