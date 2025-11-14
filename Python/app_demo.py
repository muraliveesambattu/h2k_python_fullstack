from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # return "<h1>Welcome to Flask! Thi is From ME</h1>"
    return  render_template('home.html')
@app.route('/about')
def about():
    # return "<h1>Message from About page </h1>"
    return render_template('about.html')

@app.route('/contact')
def contact():
    # return "<h1>Message from Contact page </h1>"
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)