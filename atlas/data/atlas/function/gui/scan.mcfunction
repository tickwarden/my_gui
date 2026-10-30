data modify storage atlas:live Items set from entity @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] Items
scoreboard players set #dirty atlas.tmp 0
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
scoreboard players set #slot atlas.tmp 0
function atlas:gui/scan_loop
execute if score #dirty atlas.tmp matches 1.. run function atlas:gui/render
function atlas:gui/dispatch
