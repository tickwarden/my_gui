data modify storage reliquary:live Items set from entity @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] Items
scoreboard players set #dirty reliquary.tmp 0
execute store result storage reliquary:macro pid int 1 run scoreboard players get @s reliquary.id
scoreboard players set #slot reliquary.tmp 0
function reliquary:gui/scan_loop
execute if score #dirty reliquary.tmp matches 1.. run function reliquary:gui/render
function reliquary:gui/dispatch
