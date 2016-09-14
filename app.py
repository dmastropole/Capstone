from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
  return render_template('main.html')

@app.route('/about_tool')
def about_tool():
  return render_template('about_tool.html')

@app.route('/about_me')
def about_me():
  return render_template('about_me.html')

if __name__ == '__main__':
  app.run(debug=True)