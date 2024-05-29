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
import requests
import json


class DateConverter:
		# ... (suas funções de conversão, get_hebcal_events e get_leyning existentes) ...

		def get_shabbat_times(self, geonameid="3448439", m="on"):
				url = f"https://www.hebcal.com/shabbat?cfg=json&geonameid={geonameid}&M={m}"
				response = requests.get(url)
				response.raise_for_status()
				data = response.json()
				return data

		def register_routes(self, app):
				# ... (suas rotas existentes) ...

				@app.route('/shabbat', methods=['GET', 'POST'])
				def shabbat_times():
						shabbat_info = None
						if request.method == 'POST':
								geonameid = request.form.get('geonameid', "3448439")  # Default para São Paulo
								m = request.form.get('havdalah_type', "on")  # Tipo de Havdalah (padrão: M=on)

								try:
										shabbat_info = self.get_shabbat_times(geonameid, m)
								except requests.exceptions.RequestException as e:
										shabbat_info = {'error': f"Erro na requisição: {e}"}

						return render_template('shabbat.html', shabbat_info=shabbat_info)
import requests
import json

class DateConverter:
		# ... (suas funções existentes) ...

		def get_yahrzeits(self, events_data):
				url = "https://www.hebcal.com/yahrzeit"
				headers = {'Content-Type': 'application/x-www-form-urlencoded'}
				data = {
						'cfg': 'json',
						'v': 'yahrzeit',
						'years': '3',  # Número de anos a serem retornados (pode ser ajustado)
						'hebdate': 'on',  # Incluir data hebraica
				}

				# Adicionar os dados dos eventos ao dicionário `data`
				for i, event in enumerate(events_data, start=1):
						data[f'y{i}'] = event['year']
						data[f'm{i}'] = event['month']
						data[f'd{i}'] = event['day']
						data[f't{i}'] = event['type']
						if 'name' in event:
								data[f'n{i}'] = event['name']

				response = requests.post(url, headers=headers, data=data)
				response.raise_for_status()
				return response.json()

		def register_routes(self, app):
				# ... (suas rotas existentes) ...

				@app.route('/yahrzeit', methods=['GET', 'POST'])
				def yahrzeit_dates():
						yahrzeits = None
						if request.method == 'POST':
								events_data = [
										{'year': int(request.form['y1']), 'month': int(request.form['m1']), 'day': int(request.form['d1']), 'type': request.form['t1'], 'name': request.form.get('n1', '')},
										# Adicione mais eventos aqui se necessário
								]
								try:
										yahrzeits = self.get_yahrzeits(events_data)
								except requests.exceptions.RequestException as e:
										yahrzeits = {'error': f"Erro na requisição: {e}"}

						return render_template('yahrzeit.html', yahrzeits=yahrzeits)
import requests
import json


class DateConverter:
		# ... (your existing conversion and API methods) ...

		def get_zmanim(self, date, geonameid="3448439"):
				url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={geonameid}&date={date}"
				response = requests.get(url)
				response.raise_for_status()
				data = response.json()
				return data

		def register_routes(self, app):
				# ... (your existing routes) ...

				@app.route('/zmanim', methods=['GET', 'POST'])
				def zmanim_times():
						zmanim_info = None
						if request.method == 'POST':
								date = request.form['date']
								geonameid = request.form.get('geonameid', "3448439")  # Default for São Paulo

								try:
										zmanim_info = self.get_zmanim(date, geonameid)
								except requests.exceptions.RequestException as e:
										zmanim_info = {'error': f"Erro na requisição: {e}"}

						return render_template('zmanim.html', zmanim_info=zmanim_info)
