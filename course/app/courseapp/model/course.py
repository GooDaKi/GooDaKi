#!/usr/bin/env python3

from flask import g
import datetime
import time
from psycopg2 import ProgrammingError

class Course:
    def __init__(self, db_row, subjects):
        if db_row is not None:
            self.courseID = db_row['courseid']
            self.courseName = db_row['name']
            self.authorID = db_row['authorid']
            self.type = None
            self.description = db_row['description']
            self.created = db_row['created_at']
            self.updated = db_row['updated_at']
            self.subjects = subjects
        else :
            self.courseID = None
            self.courseName = None
            self.authorID = None
            self.type = None
            self.description = None
            self.created = None
            self.updated = None
            self.subjects = None

    def edit(self,info):
        if 'courseName' in info:
            self.courseName = info['courseName']
        if 'description' in info:
            self.description = info['description']
        self.updated = time.strftime("%Y-%m-%d %H:%M:%S")
        if 'subjects' in info:
            if len(info['subjects']) == 0:
                self.subjects = None
            else:
                self.subjects = info['subjects']
        return self

    def save(self):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "Course" SET (name, description, updated_at) = ((%s), (%s), (%s)) WHERE courseID = (%s);',
                    (self.courseName, self.description, self.updated, self.courseID))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        cursor.close()
        if self.subjects is not None:
            cursor = g.db.cursor()
            cursor.execute(
                'DELETE FROM "SubjectInCourse"  WHERE courseID = (%s);',
                (self.courseID,))
            if cursor.rowcount < 0:
                cursor.close()
                return None
            cursor.close()
            for i in range(len(self.subjects)):
                cursor = g.db.cursor()
                cursor.execute(
                    'INSERT INTO "SubjectInCourse" (subjectID,ordering,courseID) VALUES (%s,%s,%s) ;',
                    (self.subjects[i], i+1 , self.courseID))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                cursor.close()

        g.db.commit()
        return True


    @staticmethod
    def get_by_id(courseid):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course" WHERE courseID = (%s) ', (courseid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None
        ret = cursor.fetchone()
        if ret['status'] == 0:
            return None
        cursor.close()
        cursor = g.db.cursor()
        cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering', (courseid,))
        if cursor.rowcount < 0:
            cursor.close()
            return Course(ret, None)
        else:
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject['subjectid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        subject_.append(subject['subjectid'])
            return Course(ret,subject_)

    @staticmethod
    def get_all(limit_no=2,scroll_no=0,all=True):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course"')
        if cursor.rowcount <= 0:
            cursor.close()
            return None,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_courses = True
            except ProgrammingError:
                has_more_courses = False
        else:
            ret = cursor.fetchall()
            has_more_courses = False
        cursor.close()
        temp = list(ret)
        result = list()
        for course in temp:
            if course['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering',
                           (course['courseid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Course(ret, None)
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject['subjectid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        subject_.append(subject['subjectid'])
            result.append(Course(course, subject_))
        return result,has_more_courses

    @staticmethod
    def get_by_author_id(authorid,limit_no=2,scroll_no=0,all=True):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course" WHERE authorID = (%s)', (authorid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None ,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_courses = True
            except ProgrammingError:
                has_more_courses = False
        else:
            ret = cursor.fetchall()
            has_more_courses = False
        cursor.close()
        temp = list(ret)
        result = list()
        for course in temp:
            if course['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering', (course['courseid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Course(ret, None)
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject['subjectid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None ,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        subject_.append(subject['subjectid'])
            result.append(Course(course,subject_))
        return result,has_more_courses

    @staticmethod
    def create(info):
        cursor = g.db.cursor()
        cursor.execute(
            """INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES (%s,%s,%s,%s,%s,%s) RETURNING courseID;""",
            (info['courseName'], info['description'],time.strftime("%Y-%m-%d %H:%M:%S"),time.strftime("%Y-%m-%d %H:%M:%S"),info['authorID'], 1))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        ret = cursor.fetchone()['courseid']
        cursor.close()
        if "subjects" in info:
            temp = info['subjects']
            for i in range(len(info['subjects'])):
                cursor = g.db.cursor()
                cursor.execute(
                    """INSERT INTO "SubjectInCourse" (subjectID,courseID,ordering)  VALUES (%s,%s,%s);""",
                    (temp[i], ret, i+1))
                if cursor.rowcount == 0:
                    cursor.close()
                    return None
                cursor.close()
        g.db.commit()
        return ret

    @staticmethod
    def search(query,limit_no=2,scroll_no=0,all=True):
        query = query.strip()
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course" WHERE name ~* (%s) OR description ~* (%s)', (query, query))
        if cursor.rowcount <= 0:
            cursor.close()
            return None,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_courses = True
            except ProgrammingError:
                has_more_courses = False
        else:
            ret = cursor.fetchall()
            has_more_courses = False
        cursor.close()
        temp = list(ret)
        result = list()
        for course in temp:
            if course['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering', (course['courseid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Course(ret, None),None
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject['subjectid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        subject_.append(subject['subjectid'])
            result.append(Course(course, subject_))
        return result,has_more_courses


    @staticmethod
    def delete_by_id(courseid):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "Course" SET (status) = (%s) WHERE courseID = (%s)', (0, courseid))
        if cursor.rowcount < 0:
            cursor.close()
            return None
        cursor.close()
        g.db.commit()
        return True

