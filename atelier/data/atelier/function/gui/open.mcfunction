execute if entity @s[gamemode=spectator] run return run title @s actionbar {"text":"İzleyici modunda açılamaz.","color":"red"}
execute if entity @s[tag=atelier.open] run return run title @s actionbar {"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}
execute unless score @s atelier.id matches 1.. run function atelier:assign_id
function atelier:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] run return run title @s actionbar {"text":"Menü oluşturulamadı.","color":"red"}
scoreboard players set @s atelier.page 0
scoreboard players set @s atelier.grace 25
tag @s add atelier.open
function atelier:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"light_purple"}
tag @e[type=minecraft:chest_minecart,tag=atelier.this] remove atelier.this
