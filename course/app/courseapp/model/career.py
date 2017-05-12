#!/usr/bin/env python3

from flask import g
import datetime
import time


class Course:
    def __init__(self, db_row, subjects):
        if db_row is not None:
            self.courseID = db_row[0]
            self.courseName = db_row[1]
            self.authorID = db_row[5]
            self.type = None
            self.description = db_row[2]
            self.created = db_row[3]
            self.updated = db_row[4]
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
        temp = self.subjects
        if 'subjects' in info:
            if len(info['subjects']) == 0:
                self.subjects = None
            else:
                self.subjects = info['subjects']
        option = True
        if temp == self.subjects:
            option = False
        return self.save(option)

    def save(self,option):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "Course" SET (name, description, updated_at) = ((%s), (%s), (%s)) WHERE courseID = (%s);',
                    (self.courseName, self.description, self.updated, self.courseID))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        cursor.close()
        if option:
            cursor = g.db.cursor()
            cursor.execute(
                'DELETE FROM "SubjectInCourse"  WHERE courseID = (%s);',
                (self.courseID,))
            if cursor.rowcount < 0:
                cursor.close()
                return None
            cursor.close()

            if not self.subjects is None:
                for i in range(len(self.subjects)):
                    cursor = g.db.cursor()
                    cursor.execute(
                        'INSERT INTO "SubjectInCourse" (subjectID,ordering,courseID) VALUES (%s,%s,%s) ;',
                        (self.subjects[i], i+1 , self.courseID))
                    if cursor.rowcount == 0:
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
        if not bool(ret[6]):
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
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject,))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if bool(ch):
                        subject_.append(subject[0])
            return Course(ret,subject_)


    @staticmethod
    def get_by_author_id(authorid):
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course" WHERE authorID = (%s)', (authorid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None
        ret = cursor.fetchall()
        cursor.close()
        temp = list(ret)
        result = list()
        for course in temp:
            if not bool(course[6]):
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering', (course[0],))
            if cursor.rowcount < 0:
                cursor.close()
                return Course(ret, None)
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject,))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if bool(ch):
                        subject_.append(subject[0])
            result.append(Course(course,subject_))
        return result

    @staticmethod
    def create(info):
        cursor = g.db.cursor()
        cursor.execute(
            """INSERT INTO "Course" (name,description,created_at,updated_at,authorID,status) VALUES (%s,%s,%s,%s,%s,%s) ;""",
            (info['courseName'], info['description'],time.strftime("%Y-%m-%d %H:%M:%S"),time.strftime("%Y-%m-%d %H:%M:%S"),info['authorID'],True ))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        cursor.close()
        g.db.commit()
        return True

    @staticmethod
    def search(query):
        query = query.strip()
        cursor = g.db.cursor()
        cursor.execute('SELECT * FROM "Course" WHERE name ~* (%s) OR description ~* (%s)', (query, query))
        if cursor.rowcount <= 0:
            cursor.close()
            return None
        ret = cursor.fetchall()
        cursor.close()
        temp = list(ret)
        result = list()
        for course in temp:
            if not bool(course[6]):
                continue
            cursor = g.db.cursor()
            cursor.execute('SELECT subjectID FROM "SubjectInCourse" WHERE courseID = (%s) ORDER BY ordering', (course[0],))
            if cursor.rowcount < 0:
                cursor.close()
                return Course(ret, None)
            subjects = list(cursor.fetchall())
            subject_ = list()
            cursor.close()
            for subject in subjects:
                cursor = g.db.cursor()
                cursor.execute('SELECT status FROM "Subject" WHERE subjectID = (%s) ', (subject,))
                if cursor.rowcount <= 0:
                    cursor.close()
                    return None
                else:
                    ch = cursor.fetchone()
                    cursor.close()
                    if bool(ch):
                        subject_.append(subject[0])
            result.append(Course(course, subject_))
        return result


    @staticmethod
    def delete_by_id(courseid):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "Course" SET (status) = (%s) WHERE courseID = (%s)', (False,courseid))
        if cursor.rowcount < 0:
            cursor.close()
            return None
        cursor.close()
        g.db.commit()
        return True