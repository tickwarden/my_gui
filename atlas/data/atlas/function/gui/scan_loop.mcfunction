execute if score #slot atlas.tmp matches 27.. run return 0
execute store result storage atlas:macro slot int 1 run scoreboard players get #slot atlas.tmp
function atlas:gui/scan_slot with storage atlas:macro
scoreboard players add #slot atlas.tmp 1
function atlas:gui/scan_loop
