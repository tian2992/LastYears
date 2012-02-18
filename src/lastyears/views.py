from toiletrate import app

@app.route('/')
def hello():
	return("hello world")
