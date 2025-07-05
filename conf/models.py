from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Зв'язкова таблиця студент-предмет
student_subjects = Table(
    'student_subjects',
    Base.metadata,
    Column('student_id', ForeignKey('students.id'), primary_key=True),
    Column('subject_id', ForeignKey('subjects.id'), primary_key=True)
)

class Group(Base):

    __tablename__ = 'groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    students = relationship("Student", back_populates="group")


class Teacher(Base):

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    first_name = Column(String(120))
    last_name = Column(String(120))
    phone = Column("cell_phone", String(20))
    address = Column(String(100))
    start_work = Column(Date, nullable=False)
    # full_name = Column(String, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):

    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    students = relationship("Student", secondary=student_subjects, back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Student(Base):

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)

    group = relationship("Group", back_populates="students")
    subjects = relationship("Subject", secondary=student_subjects, back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Grade(Base):
    
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
