data modify storage bazaar:live Items set from entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items
scoreboard players set #dirty bazaar.tmp 0
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
scoreboard players set #slot bazaar.tmp 0
function bazaar:gui/scan_loop
execute if score #dirty bazaar.tmp matches 1.. run function bazaar:gui/render
function bazaar:gui/dispatch
