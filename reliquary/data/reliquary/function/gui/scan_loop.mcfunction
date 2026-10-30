execute if score #slot reliquary.tmp matches 27.. run return 0
execute store result storage reliquary:macro slot int 1 run scoreboard players get #slot reliquary.tmp
function reliquary:gui/scan_slot with storage reliquary:macro
scoreboard players add #slot reliquary.tmp 1
function reliquary:gui/scan_loop
