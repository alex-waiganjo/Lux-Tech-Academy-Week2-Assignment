from asyncio import tasks
from turtle import update
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

class Crud(db.Model): 
 id = db.Column(db.Integer,primary_key=True)
 content=db.Column(db.String(200),nullable=False)
 date_created = db.Column(db.DateTime,default=datetime.utcnow)

 def __repr__(self):
     return '<Task %r>' %self.id


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        form_data = request.form['note']
        new_content = Crud(content=form_data)
        try:
            db.session.add(new_content)        
            db.session.commit()   
            return redirect('/')           
        except:
           return "There was an Error"
    else:  
         data = Crud.query.order_by(Crud.date_created).all()
         return render_template('index.html',html_data=data)
    
@app.route('/delete/<int:id>')
def Delete(id):
    delete_id = Crud.query.get_or_404(id)
    db.session.delete(delete_id)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:id>',methods=['GET','POST'])
def Update(id):
    task = Crud.get(id)
    if request.method == 'POST':   
        task.content = request.form['note']
        try:
            db.session.commit()
            return redirect('/')    
        except:
         return "There was an Error"  
    else:
     return render_template('update.html',task=task)
#  The error lies in the update section 
     
       
if __name__ == '__main__':
        app.run(debug=True)
    
