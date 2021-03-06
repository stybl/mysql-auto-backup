import mysql.connector as sql

class AutoBackupMySQLIndex:
    def __init__(self, config):
        self.config = config
        self.conn = sql.connect(user=self.config["user"], password=self.config["pass"], host=self.config["host"], database=self.config["database"])
        self.db = self.conn.cursor()
        self.db.execute("USE " + self.config["database"])

    def createTable(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS {}.{} ( `id` INT NOT NULL AUTO_INCREMENT , `filename` TEXT NOT NULL , `timestamp` DATETIME NOT NULL , PRIMARY KEY (`id`));".format(self.config["database"], self.config["indexTable"]))
        self.conn.commit()

    def insert(self, filename, time):
        self.db.execute("INSERT INTO {}.{} (`filename`, `timestamp`) VALUES (%s, %s);".format(self.config["database"], self.config["indexTable"]), (str(filename), str(time)))
        self.conn.commit()

    def getData(self):
        self.db.execute("SELECT `filename`,`timestamp` FROM {}.{}".format(self.config["database"], self.config["indexTable"]))
        return self.db.fetchall()

    def loadTable(self, data):
        self.db.executemany("INSERT INTO {}.{} (`filename`, `timestamp`) VALUES (%s, %s);".format(self.config["database"], self.config["indexTable"]), data)

    def close(self):
        self.conn.close()