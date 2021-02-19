from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import mysql.connector

app = Flask(__name__)

#to get current time
now = datetime.now()


#MySql Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="todolist_flask"
)

@app.route('/')
def main():
    return render_template('Add_Task.html')

@app.route('/Add_List')
def for_list():
    return render_template('Add_List.html')

@app.route('/Add_Group')
def for_group():
    return render_template('Add_Group.html')

@app.route('/ToDoList')
def todo():

    cur = mydb.cursor()

    cur.execute("SELECT * FROM tasks")

    tasks  = cur.fetchall()

    cur.close()

    return render_template('ToDoList.html',data=tasks)

def __repr__(self):
    return '<Task %r>' %self.id

@app.route('/delete/<int:id>')
def delete(id):

    task_to_delete = "DELETE FROM tasks WHERE id="+str(id)

    query = mydb.cursor()

    query.execute(task_to_delete)

    return 'Task Deleted Successfully'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    mycursor = mydb.cursor()

    if request.method == 'POST':

        todo = request.form
        task = todo['task']
        add_date = now.strftime('%Y-%m-%d %H:%M:%S')
        due_date = todo['dueDate']
        due_time = todo['dueTime']

        if "important" in todo:
            important = todo['important']

        else:
            important = 'No'

        description = todo['descr']

        mycursor.execute(
            """UPDATE tasks SET task=%s,adddate=%s,duedate=%s,duetime=%s,important=%s,description=%s Where id="""+str(id),(task,add_date,due_date,due_time,important,description))

        mydb.commit()

        return redirect(url_for('Update'))



@app.route('/', methods=['POST', 'GET'])
def db():

        mycursor=mydb.cursor()

        if request.method == 'POST':

            todo=request.form
            task=todo['task']
            add_date = now.strftime('%Y-%m-%d %H:%M:%S')
            due_date=todo['dueDate']
            due_time=todo['dueTime']

            if "important" in todo:
                important=todo['important']

            else:
                important = 'No'

            description=todo['descr']


            mycursor.execute('insert into tasks(task,adddate,duedate,duetime,important,description)values(%s,%s,%s,%s,%s,%s)',(task,add_date,due_date,due_time,str(important),description))

            mydb.commit()

            mycursor.close()

            return "Values added successfully"

if __name__ == "__main__":
    app.run(debug=True)
