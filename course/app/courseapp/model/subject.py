#!/usr/bin/env python3
from psycopg2 import ProgrammingError
from flask import g
import datetime
import time
import psycopg2
import psycopg2.extras

class Subject:
    def __init__(self, db_row, chunks):
        if db_row is not None:
            self.subjectID = db_row['subjectid']
            self.subjectName = db_row['name']
            self.authorID = db_row['authorid']
            self.type = None
            self.description = db_row['description']
            self.created = db_row['created_at']
            self.updated = db_row['updated_at']
            self.chunks = chunks
        else :
            self.subjectID = None
            self.subjectName = None
            self.authorID = None
            self.type = None
            self.description = None
            self.created = None
            self.updated = None
            self.chunks = None

    def edit(self,info):
        if 'subjectName' in info:
            self.subjectName = info['subjectName']
        if 'description' in info:
            self.description = info['description']
        self.updated = time.strftime("%Y-%m-%d %H:%M:%S")
        if 'chunks' in info:
            if len(info['chunks']) == 0:
                self.chunks = None
            else:
                self.chunks = info['chunks']
        return self

    def save(self):
        cursor = g.db.cursor()
        cursor.execute('UPDATE "Subject" SET (name, description, updated_at) = ((%s), (%s), (%s)) WHERE subjectID = (%s);',
                    (self.subjectName, self.description, self.updated, self.subjectID))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        cursor.close()
        if self.chunks is not None:
            cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute(
                'DELETE FROM "ChunkInSubject"  WHERE subjectID = (%s);',
                (self.subjectID,))
            if cursor.rowcount < 0:
                cursor.close()
                return None
            cursor.close()
            for i in range(len(self.chunks)):
                cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(
                    'INSERT INTO "ChunkInSubject" (chunkID,ordering,subjectID) VALUES (%s,%s,%s) ;',
                    (self.chunks[i], i+1 , self.subjectID))
                if cursor.rowcount == 0:
                    cursor.close()
                    return None
                cursor.close()

        g.db.commit()
        return True


    @staticmethod
    def get_by_id(subjectid):
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM "Subject" WHERE subjectID = (%s) ', (subjectid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None
        ret = cursor.fetchone()
        if not bool(ret['status']):
            return None
        cursor.close()
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('SELECT chunkID FROM "ChunkInSubject" WHERE subjectID = (%s) ORDER BY ordering', (subjectid,))
        if cursor.rowcount < 0:
            cursor.close()
            return Course(ret, None)
        else:
            chunks = list(cursor.fetchall())
            cursor.close()
            return Subject(ret,chunks)

    @staticmethod
    def get_all(limit_no=2, scroll_no=0, all=True):
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM "Subject"')
        if cursor.rowcount <= 0:
            cursor.close()
            return None , None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_subjects = True
            except ProgrammingError:
                has_more_subjects = False
        else:
            ret = cursor.fetchall()
            has_more_subjects = False
        cursor.close()
        temp = list(ret)
        result = list()
        for subject in temp:
            if not bool(subject['status']):
                continue
            cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute('SELECT chunkID FROM "ChunkInSubject" WHERE subjectID = (%s) ORDER BY ordering',
                           (subject['subjectid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Subject(ret, None) , None
            chunks = list(cursor.fetchall())
            cursor.close()
            result.append(Subject(subject, chunks))
        return result,has_more_subjects

    @staticmethod
    def get_by_author_id(authorid,limit_no=2, scroll_no=0, all=True):
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM "Subject" WHERE authorID = (%s)', (authorid,))
        if cursor.rowcount <= 0:
            cursor.close()
            return None , None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_subjects = True
            except ProgrammingError:
                has_more_subjects = False
        else:
            ret = cursor.fetchall()
            has_more_subjects = False
        cursor.close()
        temp = list(ret)
        result = list()
        for subject in temp:
            if not bool(subject['status']):
                continue
            cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute('SELECT chunkID FROM "ChunkInSubject" WHERE subjectID = (%s) ORDER BY ordering', (subject['subjectid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Subject(ret, None) , None
            chunks = list(cursor.fetchall())
            cursor.close()
            result.append(Subject(subject,chunks))
        return result,has_more_subjects

    @staticmethod
    def create(info):
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute(
            """INSERT INTO "Subject" (name,description,created_at,updated_at,authorID,status)  VALUES (%s,%s,%s,%s,%s,%s) RETURNING subjectID ;""",
            (info['subjectName'], info['description'],time.strftime("%Y-%m-%d %H:%M:%S"),time.strftime("%Y-%m-%d %H:%M:%S"),info['authorID'],True ))
        if cursor.rowcount == 0:
            cursor.close()
            return None
        ret = cursor.fetchone()['subjectid']
        cursor.close()
        if "chunks" in info:
            temp = info['chunks']
            for i in range(len(info['chunks'])):
                cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
                cursor.execute(
                    """INSERT INTO "ChunkInSubject" (chunkID,subjectID,ordering)  VALUES (%s,%s,%s) ;""",
                    (temp[i], ret, i+1))
                if cursor.rowcount == 0:
                    cursor.close()
                    return None
                cursor.close()
        g.db.commit()

        return True

    @staticmethod
    def search(query,limit_no=2, scroll_no=0, all=True):
        query = query.strip()
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM "Subject" WHERE name ~* (%s) OR description ~* (%s)', (query, query))
        if cursor.rowcount <= 0:
            cursor.close()
            return None , None
        if not all:
            cursor.scroll(scroll_no)
            ret = cursor.fetchmany(limit_no)
            try:
                cursor.scroll(0)
                has_more_subjects = True
            except ProgrammingError:
                has_more_subjects = False
        else:
            ret = cursor.fetchall()
            has_more_subjects = False
        cursor.close()
        temp = list(ret)
        result = list()
        for subject in temp:
            if not bool(subject['status']):
                continue
            cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
            cursor.execute('SELECT chunkID FROM "ChunkInSubject" WHERE subjectID = (%s) ORDER BY ordering', (subject['subjectid'],))
            if cursor.rowcount < 0:
                cursor.close()
                return Subject(ret, None) , None
            chunks = list(cursor.fetchall())
            cursor.close()
            result.append(Subject(subject, chunks))
        return result,has_more_subjects


    @staticmethod
    def delete_by_id(subjectid):
        cursor = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
        cursor.execute('UPDATE "Subject" SET (status) = (%s) WHERE subjectID = (%s)', (False,subjectid))
        if cursor.rowcount < 0:
            cursor.close()
            return None
        cursor.close()
        g.db.commit()
        return True

