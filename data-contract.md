# Girdi ve çıktı sözleşmesi

UTF-8 JSON nesnesi; örnek dosya alanların tam iç içe yapısını gösterir. Zamanlar bu laboratuvarda sayısal sanal zaman/gün değeridir; saat dilimi dönüşümü yapılmaz.

| Üst alan | Tür | Örnek |
|---|---|---|
| `batches` | `list` | [[{'id': 'E1', 'key': 'C1', 'at': 10, 'seq': 1, 'payload': {'tier': 'basic'}}, {'id': 'E3', 'key': 'C1', 'at': 30, 'seq': 3, 'deleted': True}], [{'id': 'E2', 'k |
| `queries` | `list` | [{'key': 'C1', 'at': 19}, {'key': 'C1', 'at': 20}, {'key': 'C1', 'at': 30}] |

## Semantik

Aynı zamanda en yüksek source_seq kazanır; valid_from dahil valid_to hariçtir.

Alan motorunun doğrulamaları `app.py` içinde açıkça bulunur. Eksik zorunlu anahtarlar hata verir. Satır bazında karantina/bulgu üreten motorlar rapora yazar; yapısal konfigürasyon hataları işlemi keser. Tam JSON Schema dosyası bu sürümün kapsamında değildir.

## Çıktı

Gerçek çıktı şeması ve örnek değerler `sample-report.json` içinde yer alır. Örnek işleme özgü sonuçlar `results.md` içinde açıklanır. Dış tüketici alan adlarını ve birimleri değiştirmeden sözleşmeyi sürümlemelidir.
