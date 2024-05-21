from flask import Flask, render_template, request
import json
from date_converter import DateConverter  # Importar a classe

app = Flask(__name__)
converter = DateConverter()  # Criar uma instância da classe
converter.register_routes(app)  # Registrar as rotas no Flask

if __name__ == '__main__':
		app.run(debug=True)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
		result = None
		if request.method == 'POST':
				if 'gregorian_date' in request.form:
						gregorian_date_str = request.form['gregorian_date']
						try:
								year, month, day = map(int, gregorian_date_str.split('-'))
								result = convert_gregorian_to_hebrew(year, month, day)
						except ValueError:
								result = {'error': 'Data gregoriana inválida'}
				elif 'hebrew_year' in request.form:
						try:
								hebrew_year = int(request.form['hebrew_year'])
								hebrew_month = request.form['hebrew_month']
								hebrew_day = int(request.form['hebrew_day'])
								result = convert_hebrew_to_gregorian(hebrew_year, hebrew_month, hebrew_day)
						except ValueError:
								result = {'error': 'Data hebraica inválida'}

		return render_template('index.html', result=result)

if __name__ == '__main__':
		app.run(debug=True)
