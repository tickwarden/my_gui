execute if entity @s[gamemode=spectator] run return run title @s actionbar {"text":"İzleyici modunda açılamaz.","color":"red"}
execute if entity @s[tag=vault.open] run return run title @s actionbar {"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}
execute unless score @s vault.id matches 1.. run function vault:assign_id
function vault:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run return run title @s actionbar {"text":"Menü oluşturulamadı.","color":"red"}
scoreboard players set @s vault.page 0
scoreboard players set @s vault.grace 25
tag @s add vault.open
function vault:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"dark_aqua"}
tag @e[type=minecraft:chest_minecart,tag=vault.this] remove vault.this
