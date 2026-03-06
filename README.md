Реалізуйте серверну частину аплікації, котра складається з трьох рівнів:
-	Рівень доступу до даних
-	Рівень бізнес логіки
-	Презентаційний рівень
Зв'язок між рівнями слід реалізувати із застосуванням інтерфейсів (класи рівня бізнес-логіки мають використовувати інтерфейси рівня доступу до даних, а не імплементацію) та шаблонів інверсія управління та впровадження залежностей
Презентаційний рівень на даний момент не виконує жодної логіки і представлений лише інтерфейсами
Рівень доступу до даних слід реалізувати з використанням ORM фреймворку для заповнення бази даних, створеної в лабораторній 1.б (діаграма класів). Також на рівні доступу до даних слід реалізувати зчитування даних з .csv файлу.
Рівень бізнес-логіки здійснює виклик рівня доступу до даних для вичитування даних з файлу, виконує створення необхідних моделей для заповнення бази даних та викликає рівень доступу до даних для збереження інформації в базі даних.

Важливо: всі дані мають міститись в одному файлі. При завантаженні даних в базу даних слід реалізувати необхідну логіку для коректного збереження даних в таблиці.
Файл має містити мінімально 1000 рядків.
Для створення файлу слід створити окремий модуль/клас, який запускається з командного рядка.

Варіант-19 Dental Software – Eaglesoft – Dental Practice Managemen

## Project Overview

This project implements a **Three-Tier Architecture** for a dental clinic management system. It focuses on the transition from a conceptual UML model to a functional database using **SQLAlchemy ORM**. The system handles data generation, business logic processing, and persistent storage while adhering to SOLID principles, specifically **Dependency Inversion**.

## Features & Requirements Fulfilled

* **ORM Implementation**: Used **SQLAlchemy** to map the UML class diagram (including Inheritance and Composition) to a SQLite database.
* **Dependency Injection (DI)**: The Business Logic Layer (BLL) receives its dependencies via interfaces, ensuring loose coupling.
* **Inversion of Control (IoC)**: Object lifecycle and dependencies are managed in the `main.py` entry point.
* **Data Generation**: A separate module generates a `clinic_data.csv` file with over 1000 rows of randomized data.
* **UML Consistency**: The database schema strictly follows the provided UML diagram:
* **Generalization**: `Patient` and `Dentist` inherit from `User`.
* **Aggregation**: `Dentist` manages multiple `Appointments`.
* **Composition**: `XRayImage` is strictly bound to an `Appointment` (Cascade delete).


## Project Structure

```text
.
├── bll/                  # Business Logic Layer
│   └── services.py       # Data processing & model creation
├── dal/                  # Data Access Layer
│   ├── interfaces.py     # Repository interfaces
│   ├── models.py         # SQLAlchemy ORM models
│   └── repository.py     # Concrete repository implementation
├── presentation/         # Presentation Layer
│   └── interfaces.py     # View interfaces (abstract)
├── generator.py          # CSV data generator (1000+ rows)
├── main.py               # Application entry point (IoC/DI container)
└── .gitignore            # Excluded files (venv, db, cache)

```

## Setup and Installation

1. **Generate Data**:
Run the generator to create the source CSV file:
```bash
python generator.py

```


2. **Initialize Database**:
Run the main application to create the schema and populate the database:
```bash
python main.py

```



## Technologies Used

* **Python 3.11+**
* **SQLAlchemy** (ORM Framework)
* **SQLite** (Database Engine)
* **CSV** (Data Source)
