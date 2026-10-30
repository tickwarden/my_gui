scoreboard players set #20 reliquary.tmp 20
scoreboard players operation #left reliquary.tmp /= #20 reliquary.tmp
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.8
title @s actionbar [{"text":"Bekleme: ","color":"red"},{"score":{"name":"#left","objective":"reliquary.tmp"},"color":"yellow"},{"text":" sn","color":"gray"}]
