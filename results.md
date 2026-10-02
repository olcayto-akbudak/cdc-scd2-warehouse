# Çalıştırılmış kabul sonuçları

Python 3.12.14, sentetik `scenario.json`; yerel test sayısı **8**, tümü başarılı. Ham test günlüğü `test-log.txt`.

3 tarihçe aralığı; as-of sonuçları: [{'key': 'C1', 'at': 19, 'value': {'tier': 'basic'}}, {'key': 'C1', 'at': 20, 'value': {'tier': 'gold'}}, {'key': 'C1', 'at': 30, 'value': None}]

Sonuçlar yalnız bu örneğe aittir; üretim doğruluğu veya performans garantisi olarak yorumlanmamalıdır. Ölçülen iş sonucunu kontrol edin; örnek negatif vaka içeriyorsa ret beklenir. Tam çıktı `sample-report.json`.

## Sınanan davranışlar

| Test | Kontrol |
|---|---|
| `test_late` | late |
| `test_boundary` | boundary |
| `test_dedup` | dedup |
| `test_atomic_conflict` | atomic conflict |
| `test_sequence_winner` | sequence winner |
| `test_bad_time` | bad time |
| `test_ingest_order_invariant` | ingest order invariant |
| `test_before_first` | before first |

## Gelişmiş deney planı

1. 100 anahtarda geliş sırasını karıştırıp tarihçe eşitliğini karşılaştırın.
2. Eşzamanlı source_seq kaynakları için deterministik tie-break sözleşmesi ekleyin.
3. Tam tarihçe yeniden kurmayı yalnız etkilenen aralığa daraltın.
4. Silme sonrası yeniden oluşturma ve aynı timestamp düzeltmesini ayrı senaryolarda test edin.
