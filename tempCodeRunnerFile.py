from ai_command import model,load_model
from flask import Flask,render_template,request,redirect,url_for,session
from io import StringIO
import pandas as pd


app = Flask(__name__)
app.secret_key = 'gH4@KpRvLz9Yq2E7'

train_data = None
train_ratio = None
n_estimator = None
finding_col = None
mpae = None

@app.route('/', methods=['GET', 'POST'])
def index(val_found:bool=True):
    global train_data
    global train_ratio
    global n_estimator
    global finding_col
    if request.method == "POST":
        if request.files.get('csv') is None or request.files['csv'].filename == '':
            val_found = False
        else:
            csv_file = request.files['csv']
            csv_data = pd.read_csv(StringIO(csv_file.stream.read().decode('utf-8')))
            n_estimator = int(request.form.get('n_estimator'))
            finding_col = str(request.form.get('finding_col'))
            train_ratio = float(request.form.get('ratio'))
            train_data = csv_data
            return redirect(url_for('ai_gen'))
    return render_template('index.html', val_found=val_found)




@app.route('/generate-ai',methods=['GET','POST'])
def ai_gen():
    global train_data
    global train_ratio
    global n_estimator
    global finding_col
    global mpae


    data='enter data'
    mode = model(train_data,n_estimator,finding_col,train_ratio)
    
    if mpae == None:
        mpae = mode.get_mpae()
    if request.method == "POST":
        val = request.form.get('val')
        data = mode.find(val)
    return render_template('generate-ai.html',data=data,mpae=mpae)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, processes=1)