execute if score #slot atelier.tmp matches 27.. run return 0
execute store result storage atelier:macro slot int 1 run scoreboard players get #slot atelier.tmp
function atelier:gui/scan_slot with storage atelier:macro
scoreboard players add #slot atelier.tmp 1
function atelier:gui/scan_loop
