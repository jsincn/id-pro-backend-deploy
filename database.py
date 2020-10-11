import sqlite3
import hashlib
from flask import g


DATABASE = 'data/id.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



def _hash(string):
    m = hashlib.sha256(string.upper().encode('utf-8'))
    return str(m.digest())
    # return string


def verify_id_not_present(id):
    c = get_db().cursor()
    c.execute('SELECT * FROM ids WHERE id=?', [int(id)])
    return len(c.fetchall()) == 0


def verify_email_not_present(email):
    c = get_db().cursor()
    c.execute('SELECT * FROM ids WHERE email_hash=?', [_hash(email)])
    return len(c.fetchall()) == 0


def verify_phone_not_present(phone):
    c = get_db().cursor()
    c.execute('SELECT * FROM ids WHERE phone_hash=?', [_hash(phone)])
    return len(c.fetchall()) == 0


def insert_id(id, email, phone):
    c = get_db().cursor()
    c.execute('INSERT INTO ids VALUES (?, ?, ?)', [id, _hash(email), _hash(phone)])
    get_db().commit()


def get_id_by_phone(phone):
    c = get_db().cursor()
    c.execute('SELECT id FROM ids WHERE phone_hash=?', [_hash(phone)])
    return (c.fetchone()[0])


def get_id_by_email(email):
    c = get_db().cursor()
    c.execute('SELECT id FROM ids WHERE email_hash=?', [_hash(email)])
    return (c.fetchone()[0])
