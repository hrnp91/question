from flask import Flask, url_for, request, render_template;
from app import app;
import redis;
r = redis.StrictRedis(host='homeautomation.redis.cache.windows.net',password='8I5nu00AIqALRs6M0Dhruvzmy66k6DlDrgJq2n1rOqA=', port=6380,ssl=True,charset="utf-8", decode_responses=True);

@app.route('/')
def hello():
   

    createLink = "<a href='" + url_for('create') + "'>Create a question</a>";
    return """<html> 
                 <head> 
                       <title>Hello Hiren </title>
                 </head>       
                 <body>
                 """ + createLink + """
                 </body>
           </html>""";

 # server/create
@app.route('/create', methods = ['GET', 'POST'])

def create():
     if  request.method == 'GET':
         #send the user the form
         return render_template('Createquestion.html');
     elif request.method == 'POST':
          #read for data and save it
          title = request.form['title'];
          question = request.form['question'];
          answer = request.form['answer'];
          #store data in data store
          r.set(title +':question',question);
          r.set(title +':answer',answer);
          #add code here
          return render_template('createdquestion.html', question = question);
     else:
          return "<h2>Invalid Request</h2>";

#server/question/<title>

@app.route('/question/<title>', methods = ['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        #send user the form
        question = r.get(title+':question');
        #read question from data store
        #add code here
        
        return render_template('answerquestion.html', question = question);
    elif request.method == 'POST' :
        # User has attempted answer, check if they are correct

        submittedanswer = request.form['submittedanswer'];

        #read answer from data store
        #add code 

        answer = r.get(title+':answer');

        if submittedanswer == answer:
            return "Correct!"
           # return render_template('correct.html');
        else:
            return render_template('Incorrect.html', submittedanswer = submittedanswer, answer = answer);
         
    else:
       return '<h2>  I nvalid request </h2>';