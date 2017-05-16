#!/usr/bin/env python3

from flask import g
import datetime
import time
from psycopg2 import ProgrammingError

class Career:
    def __init__(self, db_row, courses):
        if db_row is not None:
            self.careerID = db_row['careerid']
            self.careerName = db_row['name']
            self.authorID = db_row['authorid']
            self.type = None
            self.description = db_row['description']
            self.created = db_row['created_at']
            self.updated = db_row['updated_at']
            self.courses = courses
        else :
            self.careerID = None
            self.careerName = None
            self.authorID = None
            self.type = None
            self.description = None
            self.created = None
            self.updated = None
            self.courses = None

    def edit(self,info):
        if 'careerName' in info:
            self.careerName = info['careerName']
        if 'description' in info:
            self.description = info['description']
        self.updated = time.strftime("%Y-%m-%d %H:%M:%S")
        if 'courses' in info:
            if len(info['courses']) == 0:
                self.courses = None
            else:
                self.courses = info['courses']
        return self

    def save(self):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "CareerPath" SET (name, description, updated_at) = ((%s), (%s), (%s)) WHERE careerID = (%s);',
                    (self.careerName, self.description, self.updated, self.careerID))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        cursor.close()
        if self.courses is not None:
            cursor = g.db.cursor()
            cursor.execute(
                'DELETE FROM "CourseInCareerPath"  WHERE careerID = (%s);',
                (self.careerID,))
            if cursor.rowcount < 0:
                cursor.close()
                return None
            cursor.close()
            for i in range(len(self.courses)):
                cursor = g.db.cursor()
                cursor.execute(
                    'INSERT INTO "CourseInCareerPath" (courseID,ordering,careerID) VALUES (%s,%s,%s) ;',
                    (self.courses[i], i+1 , self.careerID))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                cursor.close()

        g.db.commit()
        return True


    @staticmethod
    def get_by_id(careerid):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "CareerPath" WHERE careerID = (%s) ', (careerid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None
        ret = cursor.fetchone()
        if ret['status'] == 0:
            return None
        cursor.close()
        cursor = g.db.cursor()
        cursor.execute('SELECT courseID FROM "CourseInCareerPath" WHERE careerID = (%s) ORDER BY ordering', (careerid,))
        if cursor.rowcount < 0:
            cursor.close()
            return Career(ret, None)
        else:
            courses = list(cursor.fetchall())
            course_ = list()
            cursor.close()
            for course in courses:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Course" WHERE courseID = (%s) ', (course['courseid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        course_.append(course['courseid'])
            return Career(ret,course_)

    @staticmethod
    def get_all(limit_no=2,scroll_no=0,all=True):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "CareerPath"')
        if cursor.rowcount <= 0:
            cursor.close()
            return None,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_careers = True
            except ProgrammingError:
                has_more_careers = False
        else:
            ret = cursor.fetchall()
            has_more_careers = False
        cursor.close()
        temp = list(ret)
        result = list()
        for career in temp:
            if career['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT courseID FROM "CourseInCareerPath" WHERE careerID = (%s) ORDER BY ordering',
                           (career['careerid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return career(ret, None)
            courses = list(cursor.fetchall())
            course_ = list()
            cursor.close()
            for course in courses:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Course" WHERE courseID = (%s) ', (course['courseid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        course_.append(course['courseid'])
            result.append(Career(career, course_))
        return result,has_more_careers

    @staticmethod
    def get_by_author_id(authorid,limit_no=2,scroll_no=0,all=True):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "CareerPath" WHERE authorID = (%s)', (authorid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None ,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_careers = True
            except ProgrammingError:
                has_more_careers = False
        else:
            ret = cursor.fetchall()
            has_more_careers = False
        cursor.close()
        temp = list(ret)
        result = list()
        for career in temp:
            if career['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT courseID FROM "CourseInCareerPath" WHERE careerID = (%s) ORDER BY ordering', (career['careerid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Career(ret, None)
            courses = list(cursor.fetchall())
            course_ = list()
            cursor.close()
            for course in courses:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Course" WHERE courseID = (%s) ', (course['courseid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None ,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        course_.append(course['courseid'])
            result.append(Career(career,course_))
        return result,has_more_careers

    @staticmethod
    def create(info):
        cursor = g.db.cursor()
        cursor.execute(
            """INSERT INTO "CareerPath" (name,description,created_at,updated_at,authorID,status) VALUES (%s,%s,%s,%s,%s,%s) RETURNING careerID;""",
            (info['careerName'], info['description'],time.strftime("%Y-%m-%d %H:%M:%S"),time.strftime("%Y-%m-%d %H:%M:%S"),info['authorID'], 1))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        ret = cursor.fetchone()['careerid']
        cursor.close()
        if "courses" in info:
            temp = info['courses']
            for i in range(len(info['courses'])):
                cursor = g.db.cursor()
                cursor.execute(
                    """INSERT INTO "CourseInCareerPath" (courseID,careerID,ordering)  VALUES (%s,%s,%s);""",
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
        cursor.execute('SELECT * FROM "CareerPath" WHERE name ~* (%s) OR description ~* (%s)', (query, query))
        if cursor.rowcount <= 0:
            cursor.close()
            return None,None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_careers = True
            except ProgrammingError:
                has_more_careers = False
        else:
            ret = cursor.fetchall()
            has_more_careers = False
        cursor.close()
        temp = list(ret)
        result = list()
        for career in temp:
            if career['status'] == 0:
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT courseID FROM "CourseInCareerPath" WHERE careerID = (%s) ORDER BY ordering', (career['careerid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Career(ret, None),None
            courses = list(cursor.fetchall())
            course_ = list()
            cursor.close()
            for course in courses:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Course" WHERE courseID = (%s) ', (course['courseid'],))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None,None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if ch['status'] == 1:
                        course_.append(course['courseid'])
            result.append(Career(career, course_))
        return result,has_more_careers


    @staticmethod
    def delete_by_id(careerid):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "CareerPath" SET (status) = (%s) WHERE careerID = (%s)', (0, careerid))
        if cursor.rowcount < 0:
            cursor.close()
            return None
        cursor.close()
        g.db.commit()
        return True

