execute store result score #now atlas.tmp run time query gametime
scoreboard players operation #left atlas.tmp = @s atlas.cd
scoreboard players operation #left atlas.tmp -= #now atlas.tmp
scoreboard players set #20 atlas.tmp 20
scoreboard players operation #left atlas.tmp /= #20 atlas.tmp
playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.7
title @s actionbar [{"text":"Bekleme: ","color":"red"},{"score":{"name":"#left","objective":"atlas.tmp"},"color":"yellow"},{"text":" sn","color":"gray"}]
