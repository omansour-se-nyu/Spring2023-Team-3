import pytest
from src.postgres_connect import PostgresHandler

def test_PostgresHandler_connect_false():
    db = PostgresHandler('', 5432, '', '', '')
    with pytest.raises(Exception):
        db.connect()

def test_PostgresHandler_connect_True():
    db = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    db.connect()

    assert db.cur

def test_PostgresHandler_getQuery_true():
    db = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    #db.connect()
    df = db.getQuery('select * from "Security".login')
    assert df.items()

def test_PostgresHandler_getQuery_false():
    db = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    #db.connect()
    with pytest.raises(Exception):
        df = db.getQuery('')

def test_PostgresHandler_getData_true():
    db = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    #db.connect()
    df = db.getData('"Security".login')
    assert df.items()

def test_PostgresHandler_getData_false():
    db = PostgresHandler('mentcare.cfteod2es6ye.us-east-1.rds.amazonaws.com', 5432, 'postgres', '(mfgaH3)', 'MentCare')
    #db.connect()
    with pytest.raises(Exception):
        df = db.getData('')