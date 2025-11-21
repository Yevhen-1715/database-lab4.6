from app.my_project.dao.employee_dao import EmployeeDAO

class EmployeeService:
    def __init__(self):
        self.dao = EmployeeDAO()

    def get_all_employees(self):
        # Бізнес-логіка: тут може бути додаткова фільтрація чи сортування
        return self.dao.get_all()

    def add_new_employee(self, data):
        # Бізнес-логіка: валідація даних
        if not all(k in data for k in ('first_name', 'last_name', 'email', 'department_id')):
            raise ValueError("Неповні дані: потрібні ім'я, прізвище, email та department_id.")
        return self.dao.create(data)

    def get_employees_in_department(self, dept_id):
        # Перевірка: чи існує такий відділ (можна додати)
        return self.dao.get_by_department(dept_id)
    
    
    # Метод для PUT (Update)
    def update_employee(self, employee_id, data):
        # Тут може бути додаткова бізнес-логіка або валідація
        return self.dao.update(employee_id, data)

    # Метод для DELETE
    def delete_employee(self, employee_id):
        # Тут може бути перевірка прав доступу
        return self.dao.delete(employee_id)
    
    
    
from app.my_project.dao.employee_dao import EmployeeDAO
# ... (імпорт інших DAO, якщо потрібен ProjectDAO для валідації)

class EmployeeService:
    def __init__(self):
        self.dao = EmployeeDAO()
        # self.project_dao = ProjectDAO() # Можна додати для перевірки існування Project

    # ... (існуючі методи: get_all_employees, add_new_employee, ...)

    ## 🔗 Методи для зв'язку Many-to-Many (Співробітник <-> Проєкт)
    
    def assign_project(self, employee_id, project_id):
        """
        Бізнес-логіка: Призначає Проєкт Співробітнику. 
        Перевіряє, чи не призначено проєкт вже.
        """
        if not employee_id or not project_id:
            raise ValueError("Потрібні ID співробітника та проєкту.")
            
        # 1. Бізнес-логіка (Приклад: тут можна додати перевірку,
        # чи кількість проєктів співробітника не перевищує ліміт).
        
        # 2. Виклик DAO для встановлення зв'язку
        return self.dao.assign_project(employee_id, project_id)

    def unassign_project(self, employee_id, project_id):
        """
        Бізнес-логіка: Видаляє зв'язок між Співробітником та Проєктом.
        """
        if not employee_id or not project_id:
            raise ValueError("Потрібні ID співробітника та проєкту.")
            
        # 1. Бізнес-логіка (Приклад: тут можна додати перевірку, 
        # чи не є цей проєкт останнім для співробітника, якщо це заборонено)

        # 2. Виклик DAO для видалення зв'язку
        return self.dao.unassign_project(employee_id, project_id)
        
    # ... (існуючі методи: update_employee, delete_employee, ...)