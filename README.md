# Geç Gelen CDC ve SCD2 Ambarı

**Depo adı:** `cdc-scd2-warehouse` · Python 3.12+ · bağımsız çalışır · dış paket gerekmez.

Sırasız CDC olaylarından doğru tarihsel müşteri görünümünü atomik olarak oluşturmak.

## Teknik kapsam

Event-time, tombstone, tarihçe yeniden kurma. Bu depo çalıştırılabilir bir mühendislik laboratuvarıdır. Ağ erişimi, özel hesap veya gerçek müşteri verisi gerektirmez. Örneklerde kasıtlı hatalar da bulunur; BLOCK, REVIEW veya false sonucu bazı senaryolarda beklenen davranıştır.

## Hızlı başlangıç

Depo kökünde:

```bash
python -m unittest -v
python app.py demo
python app.py demo --input scenario.json --output custom-report.json
```

`sample-report.json` gerçekten çalıştırılmış örnek çıktıdır. Yeniden çalıştırma sonucu `report.json` olur. Zamanlama ölçümleri hariç sabit seed ve girdiyle tekrarlanabilir. Kurulum için `pip install` gerekmez.

## Mimari ve kararlar

İşlem hattı: raw ingestion → dedup → highest sequence → half-open history → as_of.

Temel varsayım: Aynı zamanda en yüksek source_seq kazanır; valid_from dahil valid_to hariçtir.

Alan motoru ve komut satırı `app.py`, kabul senaryosu `scenario.json`, sınır ve hata testleri `test_core.py` içindedir. Yapılandırma veri sözleşmesi [data-contract.md](data-contract.md), ayrıntılı akış [architecture.md](architecture.md), işletim adımları [runbook.md](runbook.md) içinde açıklanır.

## Doğrulama ve değerlendirme

Testler yalnız örneğin çalışmasını kontrol etmez; projenin davranışına özgü kabul ve ret koşullarını sınar. Örnek senaryoda gözlenen sonuçlar [results.md](results.md) içinde kayıtlıdır. CI Python 3.12/3.13, Ubuntu/Windows için tanımlıdır; yerel doğrulama Python 3.12 üzerinde yapılmıştır. GitHub'da ilk push sonrasında CI ayrıca çalışmalıdır.

## Sınırlar ve üretime geçiş

Etkilenen anahtarın tüm tarihçesi yeniden kurulur; büyük hacimde bölümleme ve artımlı SQL gerekir.

Bu sürümde otomatik canlı entegrasyon, kullanıcı kimlik doğrulama, izleme altyapısı ve gerçek veriyle performans garantisi yoktur. İş kuralları sentetik kabul senaryolarıyla görünür hale getirilmiştir. Üretime geçmeden örnek sözleşmeyi gerçek alanlarla eşleyin, aşağıdaki deneyleri uygulayın ve sonuçları sürümleyin.

## Zorlaştırma deneyleri

1. 100 anahtarda geliş sırasını karıştırıp tarihçe eşitliğini karşılaştırın.
2. Eşzamanlı source_seq kaynakları için deterministik tie-break sözleşmesi ekleyin.
3. Tam tarihçe yeniden kurmayı yalnız etkilenen aralığa daraltın.
4. Silme sonrası yeniden oluşturma ve aynı timestamp düzeltmesini ayrı senaryolarda test edin.

## GitHub'a taşıma

```bash
git init
git add .
git commit -m "Initial working analysis laboratory"
git branch -M main
git remote add origin https://github.com/olcayto-akbudak/cdc-scd2-warehouse.git
git push -u origin main
```

Kendi hesabınıza taşırken `olcayto-akbudak` alanını değiştirin. Hesap bilgisi veya erişim anahtarı kaynak koda koymayın. Çalışan kaynak kod, testler ve teknik belgeler bu depoda yayımlanmıştır.

## Depo yerleşimi

GitHub sürümü dosyaları depo kökünde tutar; `app.py` alan motorunu ve CLI girişini içerir. `test_core.py` doğrudan bu modülü test eder. Belgeler ve örnek veriler aynı kökte yer alır.
