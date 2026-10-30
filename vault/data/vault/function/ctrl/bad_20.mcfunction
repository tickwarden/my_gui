execute if data storage vault:live Items[{Slot:20b}] run function vault:ctrl/return_20
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
function vault:ctrl/queue_compact with storage vault:macro
scoreboard players set #dirty vault.tmp 1
