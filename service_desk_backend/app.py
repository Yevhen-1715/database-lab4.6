from flask import Flask
# Імпортуємо наш Blueprint
from app.my_project.controller.employee_controller import employee_bp

def create_app():
    app = Flask(__name__)
    
    # Реєстрація Blueprint для API
    app.register_blueprint(employee_bp)
    
    @app.route('/')
    def home():
        return "IT Service Desk Backend is running! Access API at /api/employees"

    return app

if __name__ == '__main__':
    # Встановлюємо debug=True, щоб бачити помилки та автоматично перезавантажувати сервер
    app = create_app()
    app.run(debug=True)
    
    
    