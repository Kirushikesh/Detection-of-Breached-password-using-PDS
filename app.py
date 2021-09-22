from flask import Flask, render_template, request
from bitarray import bitarray
from bloom_filter import BloomFilter

app = Flask(__name__)
n = 1000000
p = 0.01
m=9585058
k=6

bfilter=BloomFilter(n,p,m,k)

array=bitarray()
with open('bloom_filter_data.bin','rb') as fh:
    array.fromfile(fh)

bfilter.set_bit_array(array)

@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        item=request.form['Input']
        output=bfilter.check(item)

        if(output==False):
            return render_template('home.html',prediction_text="Hurray! You have a safe password")
        else:
            return render_template('home.html',prediction_text="Sorry you passwords is probably breached ;(")
    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)
