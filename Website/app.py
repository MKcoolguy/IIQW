from flask import Flask, render_template

#YOU CAN ONLY RUN THE APPLICATION FROM HERE

#Argument is the name of the application's module or package. __name__ is a convenient shortcut for this. 
#This is needed so flask knows where to look for resources such as templates and static files.
app = Flask(__name__)

#Use route() to tell flask what url should trigger our function
#The below function returns the html file we want to display in the user's browser
#Default content type is HTML
@app.route("/")
def index():
    return render_template('index.html')


#app.run() deploys the website
if __name__ == "__main__":
    app.run()
