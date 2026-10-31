execute if score #slot questboard.tmp matches 27.. run return 0
execute store result storage questboard:macro slot int 1 run scoreboard players get #slot questboard.tmp
function questboard:gui/scan_slot with storage questboard:macro
scoreboard players add #slot questboard.tmp 1
function questboard:gui/scan_loop
