execute if score #slot bazaar.tmp matches 27.. run return 0
execute store result storage bazaar:macro slot int 1 run scoreboard players get #slot bazaar.tmp
function bazaar:gui/scan_slot with storage bazaar:macro
scoreboard players add #slot bazaar.tmp 1
function bazaar:gui/scan_loop
