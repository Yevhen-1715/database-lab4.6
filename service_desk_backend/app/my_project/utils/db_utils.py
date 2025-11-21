import pymysql.cursors
import yaml

# Функція для завантаження конфігурації
def load_config():
    # Шлях до файлу конфігурації відносно кореня програми (де запускається app.py)
    # Ми використовуємо 'config/app.yml'
    try:
        with open('app/config/app.yml', 'r') as f:
            return yaml.safe_load(f)['DB']
    except FileNotFoundError:
        print("Помилка: Файл конфігурації 'app/config/app.yml' не знайдено.")
        raise

# Функція для отримання з'єднання з БД
def get_db_connection():
    db_config = load_config()
    try:
        connection = pymysql.connect(
            host=db_config['HOST'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            database=db_config['DATABASE'],
            cursorclass=pymysql.cursors.DictCursor # Повертає результати як словники
        )
        return connection
    except Exception as e:
        print(f"Помилка підключення до БД: {e}")
        # Для діагностики, перевірте, чи коректно вказані HOST, USER та PASSWORD
        raise e