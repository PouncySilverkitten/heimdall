import multiprocessing
import sqlite3


class Forseti:
    def __init__(self, queue):
        self.queue = queue
        self.file = '_heimdall.db'
        self.conn = sqlite3.connect(self.file)
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA journal_mode=WAL;")
        if self.c.fetchall()[0][0] != "wal":
            print("Error enabling write-ahead lookup!")

    def main(self):
        while True:
            incoming = self.queue.get()

            query, values, mode = incoming[0], incoming[1], incoming[2]
            try:
                if mode == 'execute':
                    self.c.execute(query, values)
                elif mode == 'executemany':
                    self.c.executemany(query, values)
            except:
                pass

            self.conn.commit()


def main(queue):
    forseti = Forseti(queue)
    forseti.main()
