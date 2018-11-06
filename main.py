from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route('/')
def homepage():
   return render_template('index.html')

@app.route('/answer',methods = ['POST', 'GET'])
def answer():
   if request.method == 'POST':
	symbol = request.form['symbol']
	print(symbol)
	symbol = symbol.upper()
	print(symbol)
	r = requests.get(
		   'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=O0VYSACAKHVTFZ1P')
	data = r.json()
	metaData = data['Meta Data']
	lastRefreshed = metaData['3. Last Refreshed']
	timeZone = metaData['5. Time Zone']
	dateTime = lastRefreshed + " " + timeZone
	stockInfo = data['Time Series (Daily)']
	lastDataSet = stockInfo['2018-11-05']
	openingStockPrice = lastDataSet['1. open']
	currentStockPrice = lastDataSet['4. close']
	stockDelta = float(currentStockPrice) - float(openingStockPrice)
	url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
	result = requests.get(url).json()
	for x in result['ResultSet']['Result']:
		if x['symbol'] == symbol:
			company = x['name']
	companyName = company
	print('STOCK REPORT')
	print(dateTime + "\n")
	print("{} ({})\n".format(companyName, symbol))
	percentChange = stockDelta / float(openingStockPrice) * float(100)
	if stockDelta < 0:
		printThis = "{} {} ({}%)\n".format(currentStockPrice, round(stockDelta, 2), round(percentChange, 2))
	else:
		printThis = "{} +{} (+{}%)\n".format(currentStockPrice, round(stockDelta, 2), round(percentChange, 2))
   	return render_template("answer.html",companyName = companyName, symbol = symbol, printThis = printThis)

if __name__ == '__main__':
   app.run(debug = True)