data modify storage vault:live Items set from entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items
scoreboard players set #dirty vault.tmp 0
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
scoreboard players set #slot vault.tmp 0
function vault:gui/scan_loop
execute if score #dirty vault.tmp matches 1.. run function vault:gui/render
function vault:gui/dispatch
