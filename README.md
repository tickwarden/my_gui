# my_gui

Minecraft **Java 1.21.3** için dört bağımsız chest GUI datapack'i. `pack_format` **57**. Diyalog komutu yok; menü, oyuncunun önüne çağrılan görünmez hitbox'lı sandık vagonudur ve başlığı sandık arayüzünde görünür.

Kurulum: bir klasörü dünyanın `datapacks/` dizinine kopyala, `/reload`. Dört paket birlikte durabilir; anahtarlar `custom_data.pack` ile ayrılır.

| Paket | Klasör | Açılış | Ne işe yarar |
|---|---|---|---|
| Zümrüt Çarşı | `bazaar` | `/trigger bazaar` veya Çarşı Asası | Çok sayfalı alış, satış, banka, günlük ödül, sınırlı stok |
| Yol Atlası | `atlas` | `/trigger atlas` veya Atlas Değneği | Ev, sunucu işareti, son güvenli yer, merkez / nether / end |
| Sınıf Emaneti | `reliquary` | `/trigger reliquary` veya Emanet Asası | Kilitli sınıflar, 10 dk kit, ustalık, takım öneki |
| Kutsal Kasa | `vault` | `/trigger vault` veya Kasa Anahtarı | Kişiye özel 3×18 gerçek eşya deposu |
| Posta Kutusu | `mailbox` | `/trigger mailbox` veya Posta Defteri | Gelen kutusu, mesaj yaz, ek |
| Büyü Atölyesi | `atelier` | `/trigger atelier` veya Atölye Kitabı | Büyü seçimi, XP maliyeti (demo) |
| Görev Tahtası | `questboard` | `/trigger questboard` veya Görev Haritası | Günlük/haftalık görev, ödül |

## Ortak kullanım

- Sandık görünen vagona **sağ tık**.
- Kapatmak için **eğil** ya da bariyer. Açılıştan sonra kısa bir süre eğilme yok sayılır.
- Menü eşyası envantere geçerse aynı tick içinde silinir. Yanlışlıkla konan eşya yere iade edilir.
- Huni ve huni vagonu GUI eşyasını çekemez; kasa gerçek eşyada huni altına açılırsa bir tick içinde depoya yazılır, yine de huninin üstünde açmayın.
- İzleyici modu açamaz. Uzaklaşınca veya ölünce kapanır.

## Zümrüt Çarşı

Para, envanterdeki zümrüt değil **banka bakiyesi** (`bazaar.bank`). Banka sayfasından yatırılır ve çekilir. Günlük ödül Minecraft günü başına bir kez, varsayılan 8.

Fiyat ve stok `storage bazaar:shop items.<anahtar>` içindedir. Onay ekranı burayı okur. `stock` değeri `-1` sınırsızdır. Yönetici:

```
/tag @s add bazaar.admin
/function bazaar:admin/grant
```

Yönetici düğmesi stokları `bazaar:defaults` kopyasına döndürür, bakiyeye dokunmaz.

## Yol Atlası

- End adası ilk yüklemede `100 49 0` olarak hazırdır. Dünya merkezi ve nether boştur.
- Kişisel ev (3) herkese açıktır. Merkez, nether, end üstüne yazma ve 6 sunucu işareti için:

```
/tag @s add atlas.admin
```

- Son güvenli yer, yerdeyken ve lavda değilken yaklaşık 5 saniyede bir yazılır.
- Işınlanma varsayılan 8 saniye bekletir (`storage atlas:config cooldown`, tick). Hedefte zemin aranır; Direnç IV (5 sn) ve Yavaş Düşüş verilir.
- Yalnız `overworld`, `the_nether`, `the_end`.

## Sınıf Emaneti

| Sınıf | Kilit |
|---|---|
| Şövalye | yok |
| Nişancı | `adventure/shoot_arrow` |
| Çiftçi | `husbandry/plant_seed` |
| Madenci | `story/smelt_iron` |
| Simyacı | `nether/brew_potion` |
| Kaşif | `adventure/sleep_in_bed` |

Bekleme varsayılan 12000 tick (10 dk): `storage reliquary:config cooldown`. Aynı sınıfın üçüncü verilişinde bir altın elma düşer. Takım yalnız prefix değiştirir; `friendlyFire true` ve `collisionRule always` olduğu için PvP kapanmaz.

```
/function reliquary:admin/teams_off
/function reliquary:admin/teams_on
/function reliquary:admin/clear_teams
```

## Kutsal Kasa

Üst 18 göz gerçek depodur (sayfa A/B/C, toplam 54). Alt şerit düğmedir. Eşya sandığa konunca depoya yazılır, alınca depodan düşer. Kapanırken, oyuncu uzaklaşınca veya sandık vagonu sahipsiz kalınca tekrar yazılır, sonra vagon silinir. Sıkıştır boş gözleri sola toplar.

`/function vault:uninstall` **kasadaki eşyaların veri kopyasını da siler.**

Yaratıcı modda orta tık ile kopyalamak kasayı yanıltabilir. Hayatta kalma için tasarlandı.

## Kaldırma

```
/function bazaar:uninstall
/function atlas:uninstall
/function reliquary:uninstall
/function vault:uninstall
```

Sonra klasörü `datapacks` içinden silip `/reload`.

## Güvenlik

- Tıklama eylemi sandıktaki NBT'den değil, sunucunun sayfa tablosundan seçilir.
- `give` yalnız çarşı deposundaki `minecraft:` kimliğine gider. Sohbet girdisi komut üretmez.
- Menü eşyasında `custom_data.gui` vardır; envanter, yer eşyası ve huni vagonundan temizlenir.
- Op, komut bloğu veya `execute run op` yok. Yönetici yetkisi düz etikettir.
- `team` PvP'yi kapatmaz.

## Sürüm

Yalnızca **1.21.2–1.21.3**, veri paketi formatı **57**. 1.21.4 `custom_model_data`, 1.21.5 metin bileşeni ve 1.21.6 `/dialog` bu paketlerde kullanılmaz. Kaynak dosyalar UTF-8 `mcfunction`dır. `tools/generate.py` paketleri yeniden üretir; elle düzeltme yaptıysan betiği çalıştırma.

Lisans: MIT.
