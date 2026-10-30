scoreboard players add #next vault.id 1
scoreboard players operation @s vault.id = #next vault.id
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
function vault:assign_store with storage vault:macro
