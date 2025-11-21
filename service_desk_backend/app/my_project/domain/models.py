from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String

# ⚠️ ПРИМІТКА: Об'єкт 'db' має бути ініціалізований у вашому головному файлі 
# (наприклад, app/__init__.py) і імпортований тут.
# Змініть імпорт нижче, якщо ваш об'єкт db знаходиться в іншому місці:
# from app import db 

# Приклад ініціалізації db для цілей демонстрації, 
# але ви повинні використовувати свій ініціалізований об'єкт!
db = SQLAlchemy() 

# =====================================================================
# 1. ДОПОМІЖНА ТАБЛИЦЯ (Association Table)
# Встановлює зв'язок "багато до багатьох"
# =====================================================================
employee_project_association = Table(
    'employee_project_association', db.metadata,
    Column('employee_id', Integer, ForeignKey('employee.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('project.id'), primary_key=True)
)

# =====================================================================
# 2. МОДЕЛЬ СПІВРОБІТНИКА (Employee)
# =====================================================================
class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    # Додайте інші поля, які ви використовуєте (наприклад, email, department_id)
    
    # ⭐ Зв'язок M:M: Використовуємо 'secondary' для вказівки допоміжної таблиці
    projects = db.relationship(
        'Project', 
        secondary=employee_project_association, 
        backref=db.backref('employees', lazy='dynamic'),
        lazy='dynamic' 
    )

    def to_dict(self):
        """Серіалізація для виводу: включає повний список проєктів"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # Використовуємо to_dict_simple для запобігання рекурсії
            'projects': [p.to_dict_simple() for p in self.projects.all()]
        }
        
    def to_dict_simple(self):
        """Спрощений dict для використання у вкладених структурах"""
        return {'id': self.id, 'name': f"{self.first_name} {self.last_name}"}


# =====================================================================
# 3. МОДЕЛЬ ПРОЄКТУ (Project)
# =====================================================================
class Project(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    
    # Зворотний зв'язок 'employees' вже доступний завдяки 'backref' у моделі Employee

    def to_dict(self):
        """Серіалізація для виводу: включає повний список співробітників"""
        return {
            'id': self.id,
            'title': self.title,
            'employees': [e.to_dict_simple() for e in self.employees.all()]
        }

    def to_dict_simple(self):
        """Спрощений dict для використання у вкладених структурах"""
        return {'id': self.id, 'title': self.title}