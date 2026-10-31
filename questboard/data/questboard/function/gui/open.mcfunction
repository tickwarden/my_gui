execute if entity @s[gamemode=spectator] run return run title @s actionbar {"text":"İzleyici modunda açılamaz.","color":"red"}
execute if entity @s[tag=questboard.open] run return run title @s actionbar {"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}
execute unless score @s questboard.id matches 1.. run function questboard:assign_id
function questboard:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] run return run title @s actionbar {"text":"Menü oluşturulamadı.","color":"red"}
scoreboard players set @s questboard.page 0
scoreboard players set @s questboard.grace 25
tag @s add questboard.open
function questboard:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"gold"}
tag @e[type=minecraft:chest_minecart,tag=questboard.this] remove questboard.this
