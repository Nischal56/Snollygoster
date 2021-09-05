from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get("username")
    full_name = request.form.get('full_name')
    return username + '   ' +  full_name

if __name__ == "__main__":
    app.run(debug=True)

