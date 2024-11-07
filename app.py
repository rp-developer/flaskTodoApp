from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configure the SQLite database (or another database URI if preferred)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("list.html", tasks=tasks)
@app.route("/addtask")
def addtask():
    return render_template("addtasks.html")
@app.post("/submit")
def submit():
    userinput = request.form.get("userinput")
    newTask = Task(content=userinput)
    db.session.add(newTask)
    db.session.commit()
    return redirect(url_for("index"))
if __name__ == "__main__":
    app.run(debug=True)
    
@app.post("/remove/<int:task_id>")
def remove(task_id):
    task = Task.query.get(task_id)
    
    if task:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return "Task not found", 404
