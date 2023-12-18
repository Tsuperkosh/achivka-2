from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:macho man1@localhost/mydatabase'
db = SQLAlchemy(app)

# Модель для хранения чисел
class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=True, nullable=False)

# Модель для хранения логов
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Создание таблиц
with app.app_context():
    db.create_all()

@app.route('/process', methods=['POST'])
def process_number():
    data = request.get_json()
    number = data.get('number')
    
    if not isinstance(number, int) or number < 0:
        return jsonify({'error': 'Invalid number'}), 400
    
    # Проверка на уникальность числа
    if Number.query.filter_by(value=number).first():
        error_message = f'Number {number} has already been processed.'
        db.session.add(Log(message=error_message))
        db.session.commit()
        return jsonify({'error': error_message}), 400

    # Сохранение числа
    db.session.add(Number(value=number))
    db.session.commit()

    # Увеличение числа
    return jsonify({'result': number + 1})



if __name__ == '__main__':
app.run(debug=True, port=5000)
