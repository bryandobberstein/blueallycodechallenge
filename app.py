from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/blueallyapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(20))
    status = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=False)
    assignee = db.Column(db.String(30), nullable=False)
    percent_complete = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(300))
    requester = db.Column(db.Integer, db.ForeignKey('user.id'))
    summary = db.Column(db.Text)
    justification = db.Column(db.Text)
    

    def __init__(self, title, start_date, status, active, assignee, percent_complete, notes, requester, summary, justification):
        self.title = title
        self.start_date = start_date
        self.status = status
        self.assignee = assignee
        self.percent_complete = percent_complete
        self.active = active
        self.notes = notes
        self.requester = requester
        self.summary = summary
        self.justification = justification
        
    
    
        

    def __str__(self):
        user_details = User.query.filter_by(id = self.requester)
        user_items = [item.__str__() for item in user_details]
        return ({
            "id": self.id,
            "title": self.title,
            "start_date": self.start_date,
            "status": self.status,
            "assignee": self.assignee,
            "percent_complete": self.percent_complete,
            "active": self.active,
            "details": {
                "requester": user_items,
                "summary": self.summary,
                "justification": self.justification
            },
            "notes": self.notes
        })

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    entries = db.relationship('Entry', backref='user', lazy=True)

    def __init__(self, name, department):
        self.name = name
        self.department = department

    def __str__(self):
        return({
            "name": self.name,
            "deparment": self.department
        })

#VIEWS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = User(name = request.form['name'], department = request.form['department'])
        db.session.add(user)
        details = Entry(
            title = request.form['title'],
            start_date = request.form['start_date'],
            status  = request.form['status'],
            assignee  = request.form['assignee'],
            percent_complete = request.form['percent_complete'],
            active  = request.form['active'],
            notes  = request.form['notes'],
            requester = user.id,
            summary  = request.form['summary'],
            justification  = request.form['justification'],
        )
        db.session.add(details)
        db.session.commit()
    clicked = False
    entry = Entry.query.all()
    jentry = [e.__str__() for e in entry]
    return render_template('index.html', entries=jentry, clicked=clicked)

@app.route('/delete', method = ['POST'])
def delete():
    to_go = Entry.query.filter_by(id = request.form['detail.id'])
    db.session.delete(to_go)
    return redirect('/')

@app.route('/update', methods = ['POST'])
def update():
    to_up = Entry.query.filter_by(id = request.form['detail.id'])
    to_up.title = request.form['title']
    to_up.start_date = request.form['start_date']
    to_up.status  = request.form['status']
    to_up.assignee  = request.form['assignee']
    to_up.percent_complete = request.form['percent_complete']
    to_up.active  = request.form['active']
    to_up.notes  = request.form['notes']
    to_up.requester = request.form['detail.id']
    to_up.summary  = request.form['summary']
    to_up.justification  = request.form['justification']
    db.session.commit()
    return redirect('/')


@app.route('/<clicked>', methods=['GET'])
def click(clicked):
    if clicked == 'true':
        clicked = True
    else:
        clicked = False
    entry = Entry.query.all()
    jentry = [e.__str__() for e in entry]
    return render_template('index.html', entries=jentry, clicked=clicked)
    
        

if __name__ == '__main__':
    app.run(debug=True)
