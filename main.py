from flask import Flask, render_template , request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Maaq.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Route definitions go here
@app.route('/' , methods=['GET','POST'])
def todos():
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        Maaq= ToDo(title=title, desc=desc)
        db.session.add(Maaq)
        db.session.commit()
    allTodo = ToDo.query.all()
    return render_template('index.html' , allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = ToDo.query.all()
    print(allTodo)
    return 'This is the products!'

@app.route('/update/<int:sno>' , methods=['GET','POST'] )
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        Maaq = ToDo.query.filter_by(sno=sno).first()
        Maaq.title=title
        Maaq.desc=desc
        db.session.add(Maaq)
        db.session.commit()
        return redirect('/')
    Maaq = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html' , Maaq=Maaq)


@app.route('/delete/<int:sno>')
def delete(sno):
    Maaq = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(Maaq)
    db.session.commit()
    return redirect('/')

@app.route('/about')  # Add route for About page
def about():
    return render_template('base.html')

if __name__ == '__main__':
    # Ensure that the application context is pushed before creating tables
    with app.app_context():
        # Create the database tables
        db.create_all()

    # Run the Flask application
    app.run(debug=True)
