from sqlalchemy import func, desc

from models import Student, Group, Subject, Teacher, Grade
from db import DBSession


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_01(session):
    return session.query(
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).join(Grade).group_by(Student.id).order_by(desc("avg_grade")).limit(5).all()


# Знайти студента із найвищим середнім балом з певного предмета.
def select_02(session, subject_id: int):
    return session.query(
        Student.full_name,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).join(Grade).filter(Grade.subject_id == subject_id
    ).group_by(Student.id).order_by(desc("avg_grade")).first()


# Знайти середній бал у групах з певного предмета.
def select_03(session, subject_id: int):
    from models import Grade, Student, Group

    return session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).select_from(Grade
    ).join(Student, Grade.student_id == Student.id
    ).join(Group, Student.group_id == Group.id
    ).filter(Grade.subject_id == subject_id
    ).group_by(Group.id).all()


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_04(session):
    return session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade")).scalar()


# Знайти які курси читає певний викладач.
def select_05(session, teacher_id: int):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


# Знайти список студентів у певній групі.
def select_06(session, group_id: int):
    return session.query(Student.full_name).filter(Student.group_id == group_id).all()


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_07(session, group_id: int, subject_id: int):
    return session.query(
        Student.full_name,
        Grade.grade,
        Grade.grade_date
    ).join(Grade).filter(
        Student.group_id == group_id,
        Grade.subject_id == subject_id
    ).all()


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_08(session, teacher_id: int):
    return session.query(
        func.round(func.avg(Grade.grade), 2).label("avg_grade")
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()


# Знайти список курсів, які відвідує певний студент.
def select_09(session, student_id: int):
    return session.query(Subject.name).join(Student.subjects).filter(Student.id == student_id).all()


# Список курсів, які певному студенту читає певний викладач.
def select_10(session, student_id: int, teacher_id: int):
    return session.query(Subject.name).join(Subject.students).filter(
        Student.id == student_id,
        Subject.teacher_id == teacher_id
    ).all()


if __name__ == "__main__":

    with DBSession() as session:
        
        results = select_01(session)
        print(f"* * *\n1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.\n{results}\n")

        results = select_02(session, 3)
        print(f"* * *\n2. Знайти студента із найвищим середнім балом з певного предмета.\n{results}\n")

        results = select_03(session, 1)
        print(f"* * *\n3. Знайти середній бал у групах з певного предмета.\n{results}\n")

        results = select_04(session)
        print(f"* * *\n4. Знайти середній бал на потоці (по всій таблиці оцінок).\n{results}\n")

        results = select_05(session, 2)
        print(f"* * *\n5. Знайти які курси читає певний викладач.\n{results}\n")

        results = select_06(session, 3)
        print(f"* * *\n6. Знайти список студентів у певній групі.\n{results}\n")

        results = select_07(session, 1, 2)
        print(f"* * *\n7. Знайти оцінки студентів у окремій групі з певного предмета.\n{results}\n")

        results = select_08(session, 2)
        print(f"* * *\n8. Знайти середній бал, який ставить певний викладач зі своїх предметів.\n{results}\n")

        results = select_09(session, 3)
        print(f"* * *\n9. Знайти список курсів, які відвідує певний студент.\n{results}\n")

        results = select_10(session, 40, 2)
        print(f"* * *\n10. Список курсів, які певному студенту читає певний викладач.\n{results}\n")