from flask import Flask,render_template, request, url_for
from durable.lang import *
import string

#app aconfiguration
app = Flask(__name__)
app.debug  = True
app.static_folder = 'static' #static folder enabled
cardstatus = "" #global variable to hold  the card status
card_number = ""

#function to alter the global variale data
def get_response(val):
    global cardstatus
    cardstatus = val


#durable rules built to detect the card
with ruleset('CardDetect'):
    @when_all(m.subject.matches('3[47][0-9]{13}'))
    def amex(c):
        get_response("Amex Card")

    @when_all(m.subject.matches('4[0-9]{12}([0-9]{3})?'))
    def visa(c):
        get_response("Visa Card")

    @when_all(m.subject.matches('(5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|2720)[0-9]{12}'))
    def mastercard(c):
        get_response("Master Card")


@app.route('/', methods = ['GET','POST'])
@app.route('/Home',methods = ['GET','POST'])
def index():
    return render_template('index.html',response = "Find Card Type")

@app.route('/inform', methods = ['GET','POST'])
def inform():
    if request.method == 'POST':
        card_number = request.form['u-no']
        card_number.replace(" ", "")
        try:
            post('CardDetect',{'subject': card_number })
            return render_template('index.html', response = cardstatus)
        except:
            return render_template('index.html', response = 'Invalid Card Number')


if __name__ == '__main__':
    app.run()