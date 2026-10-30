execute if data storage vault:live Items[{Slot:25b}] run function vault:ctrl/return_25
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
function vault:ctrl/queue_close with storage vault:macro
scoreboard players set #dirty vault.tmp 1
