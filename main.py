from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def homepage():
   return render_template('index.html')

@app.route('/answer',methods = ['POST', 'GET'])
def answer():
   if request.method == 'POST':
   	buy_commission = int((request.form['buy_commission']))
   	initial_share_price = int((request.form['initial_share_price']))
   	allotment = int((request.form['allotment']))
   	final_share_price = int((request.form['final_share_price']))
   	sell_commission = int((request.form['sell_commission']))
   	tax_rate = int((request.form['capital_gain_tax_rate']))
   	proceeds = allotment*final_share_price
   	total_purchase_price = allotment*initial_share_price
   	initial_investment = (total_purchase_price + buy_commission + sell_commission)
   	taxable_gain = proceeds - initial_investment
   	tax =(float) (tax_rate*taxable_gain)/100
   	cost = initial_investment + tax
   	net_profit = taxable_gain - tax
   	roi = '{0:.2f}%'.format((net_profit)*100/(initial_investment+tax))
   	break_even_share_price = (float)(initial_share_price + (float)(sell_commission + buy_commission)/allotment)

   	return render_template("answer.html",p = proceeds, c = cost, tpp = total_purchase_price, bc = buy_commission, sc = sell_commission, t = tax, np = net_profit, ri = roi, brk = break_even_share_price)

if __name__ == '__main__':
   app.run(debug = True)

