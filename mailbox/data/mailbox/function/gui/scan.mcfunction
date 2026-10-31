data modify storage mailbox:live Items set from entity @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] Items
scoreboard players set #dirty mailbox.tmp 0
execute store result storage mailbox:macro pid int 1 run scoreboard players get @s mailbox.id
scoreboard players set #slot mailbox.tmp 0
function mailbox:gui/scan_loop
execute if score #dirty mailbox.tmp matches 1.. run function mailbox:gui/render
function mailbox:gui/dispatch
