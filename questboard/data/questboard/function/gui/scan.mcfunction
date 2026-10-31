data modify storage questboard:live Items set from entity @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] Items
scoreboard players set #dirty questboard.tmp 0
execute store result storage questboard:macro pid int 1 run scoreboard players get @s questboard.id
scoreboard players set #slot questboard.tmp 0
function questboard:gui/scan_loop
execute if score #dirty questboard.tmp matches 1.. run function questboard:gui/render
function questboard:gui/dispatch
