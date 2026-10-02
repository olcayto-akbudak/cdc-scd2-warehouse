import unittest, tempfile, json, sqlite3, copy
from pathlib import Path
import app as c

class CoreTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'test.sqlite'
        self.config = json.loads((Path(__file__).resolve().parent / 'scenario.json').read_text(encoding='utf-8'))

    def warehouse(self):
        return c.Warehouse(self.path)

    def test_late(self):
        w = self.warehouse()
        for b in self.config['batches']:
            w.ingest(b)
        self.assertEqual(w.as_of('C1', 20), {'tier': 'gold'})
        self.assertEqual(len(w.history()), 3)

    def test_boundary(self):
        w = self.warehouse()
        w.ingest(self.config['batches'][0])
        self.assertIsNone(w.as_of('C1', 30))

    def test_dedup(self):
        w = self.warehouse()
        e = self.config['batches'][0][0]
        w.ingest([e])
        self.assertEqual(w.ingest([e])['duplicate_events'], 1)

    def test_atomic_conflict(self):
        w = self.warehouse()
        e = self.config['batches'][0][0]
        w.ingest([e])
        bad = copy.deepcopy(e)
        bad['payload'] = {}
        with self.assertRaises(ValueError):
            w.ingest([self.config['batches'][1][0], bad])
        self.assertEqual(len(w.history()), 1)

    def test_sequence_winner(self):
        w = self.warehouse()
        a = self.config['batches'][0][0]
        b = copy.deepcopy(a)
        b.update(id='new', seq=5, payload={'tier': 'new'})
        w.ingest([b, a])
        self.assertEqual(w.as_of('C1', 10), {'tier': 'new'})

    def test_bad_time(self):
        e = copy.deepcopy(self.config['batches'][0][0])
        e['at'] = 'yesterday'
        with self.assertRaises(ValueError):
            self.warehouse().ingest([e])

    def test_ingest_order_invariant(self):
        w = self.warehouse()
        events = sum(self.config['batches'], [])
        w.ingest(events)
        expected = w.history()
        other = c.Warehouse(Path(self.temp.name) / 'other.db')
        for e in reversed(events):
            other.ingest([e])
        self.assertEqual(other.history(), expected)

    def test_before_first(self):
        w = self.warehouse()
        w.ingest(self.config['batches'][0])
        self.assertIsNone(w.as_of('C1', 9))
if __name__ == '__main__':
    unittest.main()
