from flask import Flask , render_template , request, redirect , flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hello my name is usman"
db = SQLAlchemy(app)
app.app_context().push()


class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"




@app.route('/', methods=['POST','GET'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    alltodo = Todo.query.all()
   
    return render_template('index.html', alltodo=alltodo)

@app.route('/show')
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is show page'


@app.route('/delete/<int:srno>')
def delete(srno):
    todo = Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/') 
    

@app.route('/update/<int:srno>',methods=['POST','GET'])
def update(srno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(srno=srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')



    todo = Todo.query.filter_by(srno=srno).first()
    return render_template('update.html', todo=todo)
    


@app.route('/login')
def login():
    

    return render_template('login.html')



@app.route('/register')
def register():
    

    return render_template('register.html')

@app.route('/home')
def home():
    

    return render_template('home.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/nust', methods=['GET', 'POST'])
def index():
    merit = None
    
    fields = [
        {"name": "Engineering", "min_merit": 75.0, "max_merit": 100.0},
        {"name": "Computer Science", "min_merit": 70.0, "max_merit": 100.0},
        {"name": "Business Studies", "min_merit": 60.0, "max_merit": 100.0},
        {"name": "Social Sciences", "min_merit": 55.0, "max_merit": 100.0},
        {"name": "Architecture", "min_merit": 65.0, "max_merit": 100.0},
        {"name": "Bio Sciences", "min_merit": 50.0, "max_merit": 100.0}
    ]
    chances = []

    if request.method == 'POST':
        try:
            matric = float(request.form.get('matric'))
            inter = float(request.form.get('inter'))
            net = float(request.form.get('net'))
            
            if 0 <= matric <= 1100 and 0 <= inter <= 1100 and 0 <= net <= 200:
                merit = (matric / 1100 * 10) + (inter / 1100 * 15) + (net / 200 * 75)
                merit = round(merit,4)
                
                for field in fields:
                    if field['min_merit'] <= merit <= field['max_merit']:
                        chances.append({
                            "name": field['name'],
                            "min_merit": field['min_merit'],
                            "max_merit": field['max_merit']
                        })
                        flash("Form Submitted")
            else:
                merit = "Please enter valid scores within the given ranges."
        except ValueError:
            merit = "Invalid input. Please enter valid numbers."
    
    return render_template('nust.html', merit=merit, chances=chances)




@app.route('/comsats', methods=['GET', 'POST'])
def comsats():
    merit = None
    fields = [
        {"name": "Engineering", "min_merit": 75.0, "max_merit": 100.0},
        {"name": "Computer Science", "min_merit": 70.0, "max_merit": 100.0},
        {"name": "Business Studies", "min_merit": 60.0, "max_merit": 100.0},
        {"name": "Social Sciences", "min_merit": 55.0, "max_merit": 100.0},
        {"name": "Architecture", "min_merit": 65.0, "max_merit": 100.0},
        {"name": "Bio Sciences", "min_merit": 50.0, "max_merit": 100.0}
    ]
    chances = []

    if request.method == 'POST':
        try:
            matric = float(request.form.get('matric'))
            inter = float(request.form.get('inter'))
            net = float(request.form.get('net'))
            
            if 0 <= matric <= 1100 and 0 <= inter <= 1100 and 0 <= net <= 200:
                merit = (matric / 1100 * 10) + (inter / 1100 * 40) + (net / 100 * 50)
                merit = round(merit,4)
                
                for field in fields:
                    if field['min_merit'] <= merit <= field['max_merit']:
                        chances.append({
                            "name": field['name'],
                            "min_merit": field['min_merit'],
                            "max_merit": field['max_merit']
                        })
            else:
                merit = "Please enter valid scores within the given ranges."
        except ValueError:
            merit = "Invalid input. Please enter valid numbers."
    
    return render_template('comsats.html', merit=merit, chances=chances)




@app.route('/merit')
def another_task():
    
    merit = request.args.get('merit', None)
    
    return render_template('merit.html', merit=merit)
        


@app.route('/ehome')
def ehome():
    

    return render_template('ehome.html')  




science_grade_points = {
    'A*': 100,
    'A': 95,
    'B': 85,
    'C': 75,
    'D': 65,
    'E': 55,
    'U': 0
}

arts_grade_points = {
    'A*': 90,
    'A': 85,
    'B': 75,
    'C': 65,
    'D': 55,
    'E': 45,
    'U': 0
}

@app.route('/olevel', methods=['GET', 'POST'])
def olevel():
    if request.method == 'POST':
        subjects = request.form.getlist('subject')
        grades = request.form.getlist('grade')
        
        total_points = 0
        for subject, grade in zip(subjects, grades):
            if subject == "science" and grade in science_grade_points:
                total_points += science_grade_points[grade]
            elif subject == "arts" and grade in arts_grade_points:
                total_points += arts_grade_points[grade]

        equivalence = round(total_points / len(grades), 2) if grades else 0
        return render_template('olevel.html', equivalence=equivalence)

    return render_template('olevel.html', equivalence=None)



if __name__ == "__main__":
    app.run(debug=True)
