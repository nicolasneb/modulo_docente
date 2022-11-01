from importsAndConfigs import app
from schemas.student_courseSchema import StudentCourseSchema
from entities.student_courseEntity import StudentCourseEntity
from intermediary.userIntermediary import IntermediaryUser
from flask import request, jsonify
import pandas as pd

db = StudentCourseEntity.prepare_table_student_course_and_get_db()
# with app.app_context():
#     db.create_all() #creo todas las tablas (en este caso 1)

student_course_schema = StudentCourseSchema() #Instanciamos para poder iteractuar con bd para ABM de uno
student_course_schemas = StudentCourseSchema(many=True) #Para varios/muchos

class IntermediaryStudentCourse():

    def get_student_courses():
        student_courses = StudentCourseEntity.query.all()
        courses = []
        for student_course in student_courses:
            courses.append(student_course)
        result = student_course_schemas.dump(courses)
        return jsonify(result)

    def get_course_by_ID():
        id = request.json['course_id']
        student_course = StudentCourseEntity.query.filter(StudentCourseEntity.course_id == id).all()
        result = student_course_schemas.dump(student_course)
        return jsonify(result)

    def get_course_by_ID(id):
        student_course = StudentCourseEntity.query.filter(StudentCourseEntity.course_id == id).all()
        result = student_course_schemas.dump(student_course)
        return result

    def get_student_course_by_ID():
        id = request.json['student_course_id']
        student_course = StudentCourseEntity.query.filter(StudentCourseEntity.id == id).first()
        result = student_course_schema.dump(student_course)
        return jsonify(result)

    def get_student_course_by_ID(id):
        student_course = StudentCourseEntity.query.filter(StudentCourseEntity.id == id).first()
        return student_course

    def upload_grades_by_excel():
        df = pd.read_excel('./files/grades.xlsx')
        courses = []
        for index, row in df.iterrows():
            id = IntermediaryUser.get_ID_by_dni(row['dni'])
            student_course = StudentCourseEntity.query.filter(StudentCourseEntity.student_id == id).first()
            student_course.note_first = row['note_first']
            student_course.note_second = row['note_second']
            db.session.commit()
            courses.append(student_course)
        result = student_course_schemas.dump(courses)
        return jsonify(result)

    def get_final_course_note_students():
        id = request.json['course_id']
        course = IntermediaryStudentCourse.get_course_by_ID(id)
        courseGrades = []
        for student in course:
            user = IntermediaryUser.get_user_by_ID(student['student_id'])
            student_grade = {}
            student_grade['name'] = user.name
            student_grade['lastname'] = user.lastname
            student_grade['dni'] = user.dni
            student_grade['nota_final_cursada'] = (int(student['note_first'])+int(student['note_second']))/2
            courseGrades.append(student_grade)
        return jsonify(student_grade)

    def get_course_students():
        course_id = request.json['course_id']
        course = IntermediaryStudentCourse.get_course_by_ID(course_id)
        course_students = []
        for student in course:
            user = IntermediaryUser.get_user_by_ID(student['student_id'])
            students = {}
            students['name'] = user.name
            students['lastname'] = user.lastname
            students['dni'] = user.dni
            course_students.append(students)
        return jsonify(course_students)

    # def get_course_students(course_id):
    #     course = IntermediaryStudentCourse.get_course_by_ID(course_id)
    #     course_students = []
    #     for student in course:
    #         user = IntermediaryUser.get_user_by_ID(student['student_id'])
    #         students = {}
    #         students['name'] = user.name
    #         students['lastname'] = user.lastname
    #         students['dni'] = user.dni
    #         course_students.append(students)
    #     return jsonify(course_students)

    # def course_students_to_excel():
    #     course_id = request.json['course_id']
    #     course_students = IntermediaryStudentCourse.get_course_students(course_id)
    #     df = pd.DataFrame(course_students)
    #     df.to_excel('./files/students/students.xlsx')
    #     return 'ok'
