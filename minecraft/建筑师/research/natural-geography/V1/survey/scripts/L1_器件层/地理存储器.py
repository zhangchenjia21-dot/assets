import json
import sqlite3

def connect(path):
    db=sqlite3.connect(path)
    db.executescript('''
    PRAGMA user_version=1;
    CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS regions(path TEXT PRIMARY KEY,sha256 TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS chunks(cx INTEGER,cz INTEGER,region TEXT,sector INTEGER,sectors INTEGER,timestamp INTEGER,component INTEGER,PRIMARY KEY(cx,cz));
    CREATE TABLE IF NOT EXISTS chunk_status(cx INTEGER,cz INTEGER,status TEXT,data_version INTEGER,region TEXT,PRIMARY KEY(cx,cz));
    CREATE TABLE IF NOT EXISTS status_regions(path TEXT PRIMARY KEY,sha256 TEXT);
    CREATE TABLE IF NOT EXISTS samples(x INTEGER,z INTEGER,cx INTEGER,cz INTEGER,region TEXT,observed TEXT NOT NULL,PRIMARY KEY(x,z));
    CREATE TABLE IF NOT EXISTS cells(gx INTEGER,gz INTEGER,x INTEGER,z INTEGER,elevation REAL,water REAL,biome TEXT,slope REAL,relief REAL,roughness REAL,terrain TEXT,geo_id TEXT,observed TEXT,PRIMARY KEY(gx,gz));
    CREATE TABLE IF NOT EXISTS objects(id TEXT PRIMARY KEY,family TEXT,type TEXT,evidence_level TEXT,confidence REAL,details TEXT,active INTEGER NOT NULL DEFAULT 1);
    CREATE TABLE IF NOT EXISTS members(id TEXT,gx INTEGER,gz INTEGER,PRIMARY KEY(id,gx,gz));
    CREATE TABLE IF NOT EXISTS adjacency(a TEXT,b TEXT,shared_edges INTEGER,PRIMARY KEY(a,b));
    CREATE INDEX IF NOT EXISTS sample_region ON samples(region);
    CREATE INDEX IF NOT EXISTS member_cell ON members(gx,gz);
    CREATE INDEX IF NOT EXISTS terrain_query ON cells(terrain,elevation,water);
    ''')
    return db

def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def put_meta(db,key,value):
    db.execute('INSERT OR REPLACE INTO meta VALUES (?,?)',(key,json.dumps(value,ensure_ascii=False)))
