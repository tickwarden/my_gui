execute if entity @s[gamemode=spectator] run return run title @s actionbar {"text":"İzleyici modunda açılamaz.","color":"red"}
execute if entity @s[tag=mailbox.open] run return run title @s actionbar {"text":"Menü zaten açık. Sağ tıkla.","color":"yellow"}
execute unless score @s mailbox.id matches 1.. run function mailbox:assign_id
function mailbox:gui/summon
execute unless entity @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] run return run title @s actionbar {"text":"Menü oluşturulamadı.","color":"red"}
scoreboard players set @s mailbox.page 0
scoreboard players set @s mailbox.grace 25
tag @s add mailbox.open
function mailbox:gui/render
playsound minecraft:block.chest.open player @s ~ ~ ~ 0.7 1.1
title @s actionbar {"text":"Sandığa sağ tıkla  •  eğilerek kapat","color":"white"}
tag @e[type=minecraft:chest_minecart,tag=mailbox.this] remove mailbox.this
