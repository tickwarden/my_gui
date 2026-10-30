$tellraw @s [{"text":"$(name)","color":"yellow","bold":true},{"text":"  x$(count)","color":"white"},{"text":"  •  ","color":"dark_gray"},{"text":"$(price) zümrüt","color":"green"},{"text":"  ($(mode))","color":"gray"}]
$scoreboard players set #stock bazaar.tmp $(stock)
execute if score #stock bazaar.tmp matches ..-1 run tellraw @s {"text":"Stok: sınırsız","color":"gray"}
execute if score #stock bazaar.tmp matches 0.. run tellraw @s [{"text":"Kalan stok: ","color":"gray"},{"score":{"name":"#stock","objective":"bazaar.tmp"},"color":"aqua"}]
execute if score #stock bazaar.tmp matches 0 run tellraw @s {"text":"Bu ürün tükendi.","color":"red"}
