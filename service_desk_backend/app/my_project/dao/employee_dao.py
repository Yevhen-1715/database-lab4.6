from ..domain.models import Employee, Project, db # Припускаємо, що моделі та db тут імпортовані
from sqlalchemy.exc import IntegrityError

class EmployeeDAO:
    # ... (існуючі методи: get_all, create, get_by_department, ...)

    ## 🔗 Методи для зв'язку Many-to-Many (Співробітник <-> Проєкт)

    def assign_project(self, employee_id, project_id):
        """
        Встановлює зв'язок між Employee та Project у базі даних.
        """
        employee = Employee.query.get(employee_id)
        project = Project.query.get(project_id)

        if not employee:
            raise ValueError(f"Співробітник з ID {employee_id} не знайдений.")
        if not project:
            raise ValueError(f"Проєкт з ID {project_id} не знайдений.")

        # Перевірка: чи вже існує зв'язок
        if project in employee.projects.all():
            return True # Успіх: зв'язок вже існує
            
        try:
            # SQLAlchemy: додаємо об'єкт Project до колекції projects Employee
            employee.projects.append(project)
            db.session.commit()
            return True
        except IntegrityError:
            # Виникає, якщо зв'язок вже існує, але ми його вже перевірили вище. 
            # Відкат сесії на всяк випадок.
            db.session.rollback()
            return False 

    def unassign_project(self, employee_id, project_id):
        """
        Видаляє зв'язок між Employee та Project із бази даних.
        """
        employee = Employee.query.get(employee_id)
        project = Project.query.get(project_id)
        
        if not employee or not project:
            return 0 # Зв'язок не знайдено, або об'єктів не існує

        # Перевіряємо, чи існує зв'язок
        if project in employee.projects.all():
            # SQLAlchemy: видаляємо об'єкт Project з колекції projects Employee
            employee.projects.remove(project)
            db.session.commit()
            return 1 # Успіх: видалено 1 запис
        
        return 0 # Зв'язок не знайдено







from app.my_project.utils.db_utils import get_db_connection

class EmployeeDAO:
    def get_all(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT employee_id, first_name, last_name, email, department_id, is_it_staff FROM employees"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()

    def create(self, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO employees (first_name, last_name, email, department_id, is_it_staff) 
                             VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (data['first_name'], data['last_name'], data['email'], 
                                     data['department_id'], data.get('is_it_staff', False)))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()
    
    def get_by_department(self, department_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """SELECT e.*, d.name AS department_name FROM employees e 
                             JOIN departments d ON e.department_id = d.department_id
                             WHERE d.department_id = %s"""
                cursor.execute(sql, (department_id,))
                return cursor.fetchall()
        finally:
            conn.close()

    def update(self, employee_id, data):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                set_clauses = []
                values = []
                for key, value in data.items():
                    set_clauses.append(f"{key} = %s")
                    values.append(value)
                
                if not set_clauses:
                    return 0 

                sql = f"UPDATE employees SET {', '.join(set_clauses)} WHERE employee_id = %s"
                values.append(employee_id)
                
                cursor.execute(sql, tuple(values))
                conn.commit()
                return cursor.rowcount 
        finally:
            conn.close()

    def delete(self, employee_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM employees WHERE employee_id = %s"
                cursor.execute(sql, (employee_id,))
                conn.commit()
                return cursor.rowcount 
        finally:
            conn.close()

    def delete(self, employee_id):
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ticket_assignments WHERE assignee_id = %s", (employee_id,))

                cursor.execute("UPDATE equipment SET assigned_employee_id = NULL WHERE assigned_employee_id = %s", (employee_id,))
                cursor.execute("DELETE FROM tickets WHERE requester_id = %s", (employee_id,))
                sql = "DELETE FROM employees WHERE employee_id = %s"
                cursor.execute(sql, (employee_id,))
                
                conn.commit()
                return cursor.rowcount 
        finally:
            conn.close()
            
            
            