"""Geç Gelen CDC ve SCD2 Ambarı.

Problem: Sırasız CDC olaylarından doğru tarihsel müşteri görünümünü atomik olarak oluşturmak.
Method: Event-time, tombstone, tarihçe yeniden kurma
Invariant: Aynı zamanda en yüksek source_seq kazanır; valid_from dahil valid_to hariçtir.
Boundary: Etkilenen anahtarın tüm tarihçesi yeniden kurulur; büyük hacimde bölümleme ve artımlı SQL gerekir."""
import json, sqlite3, tempfile
from pathlib import Path

class Warehouse:

    def __init__(self, path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.executescript('CREATE TABLE IF NOT EXISTS raw(event_id TEXT PRIMARY KEY,business_key TEXT,event_time INTEGER,source_seq INTEGER,payload TEXT,deleted INTEGER,UNIQUE(business_key,event_time,source_seq));\n        CREATE TABLE IF NOT EXISTS history(business_key TEXT,valid_from INTEGER,valid_to INTEGER,source_seq INTEGER,payload TEXT,deleted INTEGER,PRIMARY KEY(business_key,valid_from));')

    def ingest(self, events):
        affected = set()
        duplicates = 0
        with sqlite3.connect(self.path) as db:
            db.execute('BEGIN IMMEDIATE')
            for e in events:
                if type(e['at']) is not int or type(e['seq']) is not int:
                    raise ValueError('integer event time/sequence required')
                value = (e['id'], e['key'], e['at'], e['seq'], json.dumps(e.get('payload', {}), sort_keys=True), int(e.get('deleted', False)))
                previous = db.execute('SELECT * FROM raw WHERE event_id=?', (e['id'],)).fetchone()
                if previous:
                    if previous != value:
                        raise ValueError('conflicting replay event')
                    duplicates += 1
                    continue
                db.execute('INSERT INTO raw VALUES (?,?,?,?,?,?)', value)
                affected.add(e['key'])
            for key in affected:
                allrows = db.execute('SELECT event_time,source_seq,payload,deleted FROM raw WHERE business_key=? ORDER BY event_time,source_seq', (key,)).fetchall()
                times = {}
                for row in allrows:
                    times[row[0]] = row
                ordered = list(times.values())
                db.execute('DELETE FROM history WHERE business_key=?', (key,))
                for i, (at, seq, payload, deleted) in enumerate(ordered):
                    db.execute('INSERT INTO history VALUES (?,?,?,?,?,?)', (key, at, ordered[i + 1][0] if i + 1 < len(ordered) else None, seq, payload, deleted))
        return {'affected_keys': sorted(affected), 'duplicate_events': duplicates}

    def as_of(self, key, at):
        with sqlite3.connect(self.path) as db:
            row = db.execute('SELECT payload,deleted FROM history WHERE business_key=? AND valid_from<=? AND (valid_to>? OR valid_to IS NULL)', (key, at, at)).fetchone()
            return None if not row or row[1] else json.loads(row[0])

    def history(self):
        with sqlite3.connect(self.path) as db:
            return [{'key': k, 'from': a, 'to': b, 'source_seq': seq, 'payload': json.loads(p), 'deleted': bool(d)} for k, a, b, seq, p, d in db.execute('SELECT * FROM history ORDER BY business_key,valid_from')]

def run(config):
    with tempfile.TemporaryDirectory() as temp:
        warehouse = Warehouse(Path(temp) / 'warehouse.sqlite')
        batches = [warehouse.ingest(batch) for batch in config['batches']]
        return {'batches': batches, 'history': warehouse.history(), 'queries': [{'key': q['key'], 'at': q['at'], 'value': warehouse.as_of(q['key'], q['at'])} for q in config['queries']]}

import argparse, json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Run reproducible synthetic project scenario')
    parser.add_argument('command', choices=['demo'])
    parser.add_argument('--input', default='scenario.json')
    parser.add_argument('--output', default='report.json')
    args = parser.parse_args()
    report = run(json.loads(Path(args.input).read_text(encoding='utf-8')))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    print(f'Report: {target}')
if __name__ == '__main__':
    main()
