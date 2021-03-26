from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        FA1 = request.form['FA1']
        print(FA1)

    return render_template('app.html')

if __name__=='__main__':
    app.run(debug=True)