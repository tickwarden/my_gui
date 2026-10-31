# Demo uygulama: gerçek büyü item modifier / component ile yapılır
execute store result score #cost atelier.tmp run data get storage atelier:catalog unbreaking.cost
title @s actionbar [{"text":"Kırılmazlık ","color":"light_purple"},{"text":"maliyet ~","color":"gray"},{"score":{"name":"#cost","objective":"atelier.tmp"},"color":"blue"},{"text":" XP (demo)","color":"dark_gray"}]
playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.7 1.1
tellraw @s {"text":"[Atölye] Kırılmazlık seçildi. Gerçek uygulama için elindeki eşyaya enchantment component yazılır.","color":"gray"}
