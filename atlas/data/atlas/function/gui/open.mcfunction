execute if entity @s[gamemode=spectator] run return run title @s actionbar {"text":"İzleyici modunda açılamaz.","color":"red"}
execute if entity @s[tag=atlas.open] run return run title @s actionbar {"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}
execute unless score @s atlas.id matches 1.. run function atlas:assign_id
function atlas:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] run return run title @s actionbar {"text":"Menü oluşturulamadı.","color":"red"}
scoreboard players set @s atlas.page 0
scoreboard players set @s atlas.grace 25
tag @s add atlas.open
function atlas:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"aqua"}
tag @e[type=minecraft:chest_minecart,tag=atlas.this] remove atlas.this
