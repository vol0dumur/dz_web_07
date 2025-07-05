from faker import Faker
from random import choice, randint, sample
# from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Group, Student, Teacher, Subject, Grade
from db import URI

engine = create_engine(URI)
Session = sessionmaker(bind=engine)
session = Session()

# Кількість студентів
N_STUDENTS = 50
# Кількість груп
N_GROUPS = 3
# Кількість предметів
N_SUBJECTS = 8
# Предмети для випадкового обирання
SUBJECTS = ["Вища математика", "Фізика", "Хімія", "Інформатика та програмування", "Іноземна мова", "Філософія",\
            "Історія України", "Економічна теорія", "Правознавство", "Українська мова", "Психологія", "Екологія"\
            "Механіка та опір матеріалів", "Промисловий дизайн", "Накреслювальна геометрія", "Бухгалтерський облік"]
# Кількість викладачів
N_TEACHERS = 5
# Кількість оцінок у кожного студента з усіх предметів
N_GRADES = 20

fake = Faker("uk-UA")

try:
    # Створити таблиці (якщо ще не створені)
    Base.metadata.create_all(engine)

    # Додаємо групи
    groups = []
    for i in range(N_GROUPS):
        group = Group(name=f"GR-2025-{i+1}")
        session.add(group)
        groups.append(group)

    # Додаємо викладачів
    teachers = []
    for _ in range(N_TEACHERS):
        # teacher = Teacher(full_name=fake.name())
        teacher = Teacher(first_name=fake.first_name())
        teacher = Teacher(last_name=fake.last_name())
        teacher = Teacher(phone=fake.phone_number())
        teacher = Teacher(address=fake.address())
        teacher = Teacher(start_work=fake.date_between(start_date="-10y", end_date="-1y"))
        session.add(teacher)
        teachers.append(teacher)

    session.flush()  # Щоб були доступні ID

    # Додаємо предмети
    subjects = []
    used_subject_names = set()
    while len(subjects) < N_SUBJECTS:
        name = choice(SUBJECTS)
        if name in used_subject_names:
            continue
        used_subject_names.add(name)
        subject = Subject(name=name, teacher=choice(teachers))
        session.add(subject)
        subjects.append(subject)

    # Додаємо студентів
    students = []
    for _ in range(N_STUDENTS):
        student = Student(
            full_name=fake.name(),
            group=choice(groups)
        )
        # Призначаємо від 3 до 5 предметів
        student.subjects = sample(subjects, k=randint(3, 5))
        session.add(student)
        students.append(student)

    session.flush()

    # Додаємо оцінки
    for student in students:
        for _ in range(N_GRADES):
            subject = choice(student.subjects)
            grade = Grade(
                student=student,
                subject=subject,
                grade=randint(60, 100),
                grade_date=fake.date_between(start_date="-1y", end_date="today")
            )
            session.add(grade)

    # Зберігаємо всі зміни
    session.commit()
    print("Базу успішно заповнено випадковими даними!")

except Exception as e:
    session.rollback()
    print(f"Помилка при заповненні: {e}")
finally:
    session.close()
