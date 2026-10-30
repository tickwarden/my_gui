execute if data storage vault:live Items[{Slot:26b}] run function vault:ctrl/return_26
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
function vault:ctrl/queue_page_next with storage vault:macro
scoreboard players set #dirty vault.tmp 1
