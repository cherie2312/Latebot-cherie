import sqlite3


class DBHelper:
    def __init__(self, dbname="latebot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS points (amt text, owner text)"
        #ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON owner (owner ASC)"
        self.conn.execute(tblstmt)
        #self.conn.execute(ownidx)
        self.conn.commit()

    def add_point(self, point_text, owner):
        stmt = "INSERT INTO points (amt,owner) VALUES (?,?)"
        args = (point_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_owner(self,owner):
        try:
            stmt = "DELETE FROM points  WHERE owner = (?)"
            args = (owner,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        except Exception as e:
            print e


    def get_points(self,owner):
        try:
            stmt = "SELECT amt FROM points  WHERE owner = (?)"
            args = (owner,)
            return [x[0] for x in self.conn.execute(stmt, args)]
        
        except Exception as e:
            print e

    def get_total(self,owner):
        try:
            stmt = "SELECT Sum(amt) FROM points WHERE owner = (?)"
            args = (owner,)
            return [x[0] for x in self.conn.execute(stmt,args)]

        except Exception as e:
            print e
    
