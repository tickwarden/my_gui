data modify storage atelier:live Items set from entity @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] Items
scoreboard players set #dirty atelier.tmp 0
execute store result storage atelier:macro pid int 1 run scoreboard players get @s atelier.id
scoreboard players set #slot atelier.tmp 0
function atelier:gui/scan_loop
execute if score #dirty atelier.tmp matches 1.. run function atelier:gui/render
function atelier:gui/dispatch
