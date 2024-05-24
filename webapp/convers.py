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
def get_hebcal_events(self, start_date, end_date, geonameid="3448439", tzid="America/Sao_Paulo"):
	url = f"https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&c=on&geo=geoname&geonameid={geonameid}&M=on&s=on"
	url += f"&start={start_date}&end={end_date}&tzid={tzid}"
	response = requests.get(url)
	response.raise_for_status()
	data = response.json()
	return data

def register_routes(self, app):
	# ... (suas rotas existentes) ...

	@app.route('/hebcal', methods=['GET', 'POST'])
	def hebcal_events():
			events = None
			if request.method == 'POST':
					start_date = request.form['start_date']
					end_date = request.form['end_date']
					geonameid = request.form.get('geonameid', "3448439") # Default para São Paulo
					tzid = request.form.get('tzid', "America/Sao_Paulo")

					try:
							events = self.get_hebcal_events(start_date, end_date, geonameid, tzid)
					except requests.exceptions.RequestException as e:
							events = {'error': f"Erro na requisição: {e}"}

			return render_template('hebcal.html', events=events)
import requests
import json


class DateConverter:
		# ... (suas funções de conversão e get_hebcal_events existentes) ...

		def get_leyning(self, start_date, end_date, diaspora=True):
				url = f"https://www.hebcal.com/leyning?cfg=json&start={start_date}&end={end_date}"
				if not diaspora:
						url += "&i=on"  # Para Israel, adicione i=on
				response = requests.get(url)
				response.raise_for_status()
				data = response.json()
				return data

		def register_routes(self, app):
				# ... (suas rotas existentes) ...

				@app.route('/leyning', methods=['GET', 'POST'])
				def leyning_readings():
						leyning = None
						if request.method == 'POST':
								start_date = request.form['start_date']
								end_date = request.form['end_date']
								diaspora = 'diaspora' in request.form  # Verifica se a opção "Diáspora" está marcada

								try:
										leyning = self.get_leyning(start_date, end_date, diaspora)
								except requests.exceptions.RequestException as e:
										leyning = {'error': f"Erro na requisição: {e}"}

						return render_template('leyning.html', leyning=leyning)
