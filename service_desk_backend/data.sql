-- =====================================
-- IT SERVICE DESK DATABASE – FULL BUILD
-- =====================================


DROP DATABASE IF EXISTS it_service_desk;
CREATE DATABASE it_service_desk CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE it_service_desk;

-- === STRUCTURE ===
CREATE TABLE departments (
 department_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(100) NOT NULL
);

CREATE TABLE offices (
 office_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(100) NOT NULL,
 city VARCHAR(80) NOT NULL,
 address VARCHAR(200) NOT NULL
);

CREATE TABLE rooms (
 room_id INT PRIMARY KEY AUTO_INCREMENT,
 office_id INT NOT NULL,
 room_number VARCHAR(20) NOT NULL,
 FOREIGN KEY (office_id) REFERENCES offices(office_id)
);

CREATE TABLE workstations (
 workstation_id INT PRIMARY KEY AUTO_INCREMENT,
 room_id INT NOT NULL,
 desk_number VARCHAR(20) NOT NULL,
 FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

CREATE TABLE employees (
 employee_id INT PRIMARY KEY AUTO_INCREMENT,
 first_name VARCHAR(60) NOT NULL,
 last_name VARCHAR(60) NOT NULL,
 email VARCHAR(120) NOT NULL,
 department_id INT NOT NULL,
 is_it_staff BOOLEAN NOT NULL DEFAULT FALSE,
 FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE equipment_types (
 equipment_type_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(60) NOT NULL
);

CREATE TABLE equipment (
 equipment_id INT PRIMARY KEY AUTO_INCREMENT,
 equipment_type_id INT NOT NULL,
 model VARCHAR(120) NOT NULL,
 serial_number VARCHAR(120) NOT NULL,
 status ENUM('in_use','in_stock','repair','retired') DEFAULT 'in_use',
 workstation_id INT,
 assigned_employee_id INT,
 FOREIGN KEY (equipment_type_id) REFERENCES equipment_types(equipment_type_id),
 FOREIGN KEY (workstation_id) REFERENCES workstations(workstation_id),
 FOREIGN KEY (assigned_employee_id) REFERENCES employees(employee_id)
);

CREATE TABLE ticket_types (
 ticket_type_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(80) NOT NULL
);

CREATE TABLE ticket_statuses (
 status_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(40) NOT NULL,
 is_final BOOLEAN DEFAULT FALSE
);

CREATE TABLE ticket_priorities (
 priority_id INT PRIMARY KEY AUTO_INCREMENT,
 name VARCHAR(40) NOT NULL
);

CREATE TABLE tickets (
 ticket_id BIGINT PRIMARY KEY AUTO_INCREMENT,
 title VARCHAR(200),
 description TEXT NOT NULL,
 ticket_type_id INT NOT NULL,
 status_id INT NOT NULL,
 priority_id INT NOT NULL,
 requester_id INT NOT NULL,
 workstation_id INT,
 equipment_id INT,
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (ticket_type_id) REFERENCES ticket_types(ticket_type_id),
 FOREIGN KEY (status_id) REFERENCES ticket_statuses(status_id),
 FOREIGN KEY (priority_id) REFERENCES ticket_priorities(priority_id),
 FOREIGN KEY (requester_id) REFERENCES employees(employee_id),
 FOREIGN KEY (workstation_id) REFERENCES workstations(workstation_id),
 FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
);

CREATE TABLE ticket_assignments (
  assignment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
  ticket_id BIGINT NOT NULL,
  assignee_id INT NOT NULL,
  role ENUM('owner','resolver','watcher') DEFAULT 'resolver',
  assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- <--- ЦЕЙ СТОВПЕЦЬ
  FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
  FOREIGN KEY (assignee_id) REFERENCES employees(employee_id)
);

-- === SAMPLE DATA ===
INSERT INTO departments (name) VALUES ('IT'),('Finance'),('HR');
INSERT INTO offices (name,city,address) VALUES ('HQ','Lviv','Orlyka 4A'),('Branch','Kyiv','Volodymyrska 15');
INSERT INTO rooms (office_id,room_number) VALUES (1,'101'),(1,'102'),(2,'201');
INSERT INTO workstations (room_id,desk_number) VALUES (1,'D1'),(1,'D2'),(2,'D3');

INSERT INTO employees (first_name,last_name,email,department_id,is_it_staff) VALUES
('Ihor','Melnyk','ihor@it.com',1,TRUE),
('Olena','Koval','olena@it.com',1,TRUE),
('Danylo','Shevchenko','dan@it.com',2,FALSE),
('Valeriia','Romanchuk','val@it.com',3,FALSE);

INSERT INTO equipment_types (name) VALUES ('Laptop'),('Printer'),('Monitor');
INSERT INTO equipment (equipment_type_id,model,serial_number,status,workstation_id,assigned_employee_id) VALUES
(1,'Dell 5440','SN001','in_use',1,3),
(2,'HP LaserJet','SN002','repair',1,3),
(3,'Samsung 27','SN003','in_use',2,4);

INSERT INTO ticket_types (name) VALUES
('Hardware Issue'),('New Device'),('Replacement'),('Software Update'),('Software Problem');
INSERT INTO ticket_statuses (name,is_final) VALUES
('New',FALSE),('In Progress',FALSE),('Resolved',TRUE),('Closed',TRUE);
INSERT INTO ticket_priorities (name) VALUES ('Low'),('Medium'),('High'),('Critical');

-- === ТЕСТОВІ ЗАЯВКИ ===
INSERT INTO tickets (title,description,ticket_type_id,status_id,priority_id,requester_id,workstation_id,equipment_id,created_at)
VALUES
('Принтер не друкує','Помилка Paper Jam','1','2','3','3','1','2',NOW()-INTERVAL 3 DAY),
('Оновити Office 365','Потрібне оновлення пакету Office','4','2','1','4','2','1',NOW()-INTERVAL 2 DAY),
('Заміна монітора','На екрані артефакти','3','1','2','3','1','3',NOW()-INTERVAL 1 DAY),
('ПК не вмикається','ПК у HQ, кімната 101','1','1','2','3','1','1',NOW()-INTERVAL 10 DAY),
('Монітор не показує','Монітор у кімнаті 102','1','2','3','4','2','3',NOW()-INTERVAL 5 DAY),
('Помилка драйвера','Помилка при друці HQ 101','5','2','2','3','1','2',NOW()-INTERVAL 3 DAY),
('Повільна робота','Lenovo працює повільно','1','2','3','4','1','1',NOW()-INTERVAL 2 DAY),
('Проблеми з Office','Word зависає','5','2','3','3','2','1',NOW()-INTERVAL 1 DAY),
('Не працює Wi-Fi','Відсутній інтернет Branch','1','2','3','4','3','1',NOW()-INTERVAL 4 DAY),
('Новий монітор','Потрібен монітор для аналітика','2','1','1','4','3','3',NOW()-INTERVAL 3 DAY);

-- === ПРИЗНАЧЕННЯ ===
INSERT INTO ticket_assignments (ticket_id,assignee_id,role,assigned_at) VALUES
(1,1,'resolver',NOW()-INTERVAL 3 DAY),
(2,2,'resolver',NOW()-INTERVAL 1 DAY),
(3,1,'resolver',NOW()-INTERVAL 12 HOUR),
(4,2,'resolver',NOW()-INTERVAL 5 DAY),
(5,1,'resolver',NOW()-INTERVAL 1 DAY),
(6,2,'resolver',NOW()-INTERVAL 2 DAY),
(7,1,'resolver',NOW()-INTERVAL 8 HOUR),
(8,2,'resolver',NOW()-INTERVAL 1 HOUR),
(9,1,'resolver',NOW()-INTERVAL 2 DAY),
(10,2,'resolver',NOW()-INTERVAL 4 HOUR);

-- ===============================
-- === ЗАПИТИ ===
-- ===============================

-- 1️⃣ Відкриті заявки “In Progress” або “High” за 7 днів
SELECT t.ticket_id, t.title, ts.name AS status, tp.name AS priority, t.created_at
FROM tickets t
JOIN ticket_statuses ts ON t.status_id = ts.status_id
JOIN ticket_priorities tp ON t.priority_id = tp.priority_id
WHERE (ts.name = 'In Progress' OR tp.name = 'High')
 AND t.created_at >= NOW() - INTERVAL 7 DAY;

-- 2️⃣ Середня кількість заявок за місяць на працівника
SELECT e.first_name, e.last_name,
    COUNT(t.ticket_id) / (DATEDIFF(CURDATE(), MIN(t.created_at)) / 30) AS avg_tickets_per_month
FROM employees e
LEFT JOIN tickets t ON t.requester_id = e.employee_id
GROUP BY e.employee_id;

-- 3️⃣ Кількість заявок по офісах (>5)
SELECT o.name AS office_name, COUNT(t.ticket_id) AS ticket_count
FROM tickets t
JOIN workstations ws ON t.workstation_id = ws.workstation_id
JOIN rooms r ON ws.room_id = r.room_id
JOIN offices o ON r.office_id = o.office_id
GROUP BY o.office_id
HAVING COUNT(t.ticket_id) > 5;

-- 4️⃣ Повна інформація про заявки
SELECT e.first_name, e.last_name, t.description, etype.name AS equipment_type,
    o.name AS office_name, r.room_number, ws.desk_number, ts.name AS status,
    es.first_name AS assignee_first_name, es.last_name AS assignee_last_name
FROM tickets t
JOIN employees e ON t.requester_id = e.employee_id
JOIN equipment eq ON t.equipment_id = eq.equipment_id
JOIN equipment_types etype ON eq.equipment_type_id = etype.equipment_type_id
JOIN workstations ws ON t.workstation_id = ws.workstation_id
JOIN rooms r ON ws.room_id = r.room_id
JOIN offices o ON r.office_id = o.office_id
JOIN ticket_statuses ts ON t.status_id = ts.status_id
JOIN ticket_assignments ta ON t.ticket_id = ta.ticket_id
JOIN employees es ON ta.assignee_id = es.employee_id
WHERE ta.role = 'resolver';

-- 5️⃣ Спеціалісти, що реагували швидше середнього часу
WITH avg_response_time AS (
 SELECT AVG(TIMESTAMPDIFF(SECOND, t.created_at, ta.assigned_at)) AS avg_time
 FROM tickets t
 JOIN ticket_assignments ta ON t.ticket_id = ta.ticket_id
 WHERE ta.role = 'resolver'
)
SELECT e.first_name, e.last_name,
    TIMESTAMPDIFF(SECOND, t.created_at, ta.assigned_at) AS response_time
FROM tickets t
JOIN ticket_assignments ta ON t.ticket_id = ta.ticket_id
JOIN employees e ON ta.assignee_id = e.employee_id
CROSS JOIN avg_response_time art
WHERE ta.role = 'resolver'
 AND TIMESTAMPDIFF(SECOND, t.created_at, ta.assigned_at) < art.avg_time;
