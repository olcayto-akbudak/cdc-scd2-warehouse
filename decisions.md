# Tasarım kararları

## Alan motorunu CLI'dan ayırmak

`run(config)` orkestrasyonu kaynak kodun doğrudan test edilebilmesini sağlar. JSON arayüz taşınabilirliği artırır; bu sürüm kullanıcı arayüzü barındırmaz.

## Seçilen yöntem

Event-time, tombstone, tarihçe yeniden kurma. Aynı zamanda en yüksek source_seq kazanır; valid_from dahil valid_to hariçtir.

## Bilinçli sınır

Etkilenen anahtarın tüm tarihçesi yeniden kurulur; büyük hacimde bölümleme ve artımlı SQL gerekir.

## Önerilen sonraki doğrulama

Gerçek kullanım hacmiyle testten önce mevcut kabul ve ret örneklerinin alan uzmanı tarafından onaylanması gerekir. Sonraki sürüm performans ölçümleri, dış adaptör sözleşmesi ve üretim gözlemlenebilirliğini ayrı karar kayıtlarında ele almalıdır.
