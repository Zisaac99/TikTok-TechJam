from application import app


#Handles http://127.0.0.1:5000/hello
@app.route('/') 
def hello_world(): 
    return "<h1>Hello World</h1>"

