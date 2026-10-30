execute store result score #now atlas.tmp run time query gametime
scoreboard players set #left atlas.tmp 0
execute if score @s atlas.cd > #now atlas.tmp run scoreboard players operation #left atlas.tmp = @s atlas.cd
execute if score @s atlas.cd > #now atlas.tmp run scoreboard players operation #left atlas.tmp -= #now atlas.tmp
scoreboard players set #20 atlas.tmp 20
execute if score #left atlas.tmp matches 1.. run scoreboard players operation #left atlas.tmp /= #20 atlas.tmp
title @s actionbar [{"text":"Atlas","color":"aqua"},{"text":"  •  bekleme ","color":"gray"},{"score":{"name":"#left","objective":"atlas.tmp"},"color":"yellow"},{"text":" sn","color":"dark_gray"}]
