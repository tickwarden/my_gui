scoreboard players add #next reliquary.id 1
scoreboard players operation @s reliquary.id = #next reliquary.id
execute store result storage reliquary:macro pid int 1 run scoreboard players get @s reliquary.id
function reliquary:assign_store with storage reliquary:macro
