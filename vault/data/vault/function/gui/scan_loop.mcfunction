execute if score #slot vault.tmp matches 27.. run return 0
execute store result storage vault:macro slot int 1 run scoreboard players get #slot vault.tmp
function vault:gui/scan_slot with storage vault:macro
scoreboard players add #slot vault.tmp 1
function vault:gui/scan_loop
