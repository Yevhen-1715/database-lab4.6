from flask import Blueprint, jsonify, request
from app.my_project.service.employee_service import EmployeeService

# Створюємо Blueprint для маршрутів API
employee_bp = Blueprint('employees', __name__, url_prefix='/api/employees')
employee_service = EmployeeService()

# 1. GET /api/employees - Вивід всіх даних (Read)
@employee_bp.route('/', methods=['GET'])
def list_employees():
    employees = employee_service.get_all_employees()
    return jsonify(employees)

# 2. POST /api/employees - Вставка даних (Create)
@employee_bp.route('/', methods=['POST'])
def create_employee():
    try:
        data = request.json
        new_id = employee_service.add_new_employee(data)
        return jsonify({"message": "Employee created successfully", "id": new_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {e}"}), 500


# 3. GET /api/employees/department/<id> - Зв'язок M:1
@employee_bp.route('/department/<int:dept_id>', methods=['GET'])
def get_employees_by_department(dept_id):
    employees = employee_service.get_employees_in_department(dept_id)
    return jsonify(employees)



# 4. PUT /api/employees/<id> - Оновлення даних (Update)
@employee_bp.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.json
        rows_updated = employee_service.update_employee(employee_id, data)
        
        if rows_updated > 0:
            return jsonify({"message": f"Employee ID {employee_id} updated successfully."}), 200
        else:
            return jsonify({"error": f"Employee ID {employee_id} not found or no changes made."}), 404
    except Exception as e:
        return jsonify({"error": f"Internal server error: {e}"}), 500

# 5. DELETE /api/employees/<id> - Видалення даних (Delete)
@employee_bp.route('/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        rows_deleted = employee_service.delete_employee(employee_id)
        
        if rows_deleted > 0:
            # 204 No Content - стандартний успішний статус для DELETE
            return jsonify({"message": f"Employee ID {employee_id} deleted successfully."}), 204 
        else:
            return jsonify({"error": f"Employee ID {employee_id} not found."}), 404
    except Exception as e:
        return jsonify({"error": f"Internal server error: {e}"}), 500