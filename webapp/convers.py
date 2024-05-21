import requests
import json


class DateConverter:
		def __init__(self):
				pass  # No initialization needed for now

		def convert_gregorian_to_hebrew(self, year, month, day, after_sunset=False):
				url = f"https://www.hebcal.com/converter?cfg=json&gy={year}&gm={month}&gd={day}&g2h=1"
				if after_sunset:
						url += "&gs=on"
				response = requests.get(url)
				response.raise_for_status()
				data = response.json()
				return data

		def convert_hebrew_to_gregorian(self, year, month, day):
				url = f"https://www.hebcal.com/converter?cfg=json&hy={year}&hm={month}&hd={day}&h2g=1"
				response = requests.get(url)
				response.raise_for_status()
				data = response.json()
				return data

		def register_routes(self, app):  # Novo método para registrar rotas no Flask
				@app.route('/', methods=['GET', 'POST'])
				def index():
						result = None
						if request.method == 'POST':
								if 'gregorian_date' in request.form:
										gregorian_date_str = request.form['gregorian_date']
										try:
												year, month, day = map(int, gregorian_date_str.split('-'))
												result = self.convert_gregorian_to_hebrew(year, month, day)
										except ValueError:
												result = {'error': 'Data gregoriana inválida'}
								elif 'hebrew_year' in request.form:
										try:
												hebrew_year = int(request.form['hebrew_year'])
												hebrew_month = request.form['hebrew_month']
												hebrew_day = int(request.form['hebrew_day'])
												result = self.convert_hebrew_to_gregorian(hebrew_year, hebrew_month, hebrew_day)
										except ValueError:
												result = {'error': 'Data hebraica inválida'}

						return render_template('index.html', result=result)
