scoreboard players add #next atlas.id 1
scoreboard players operation @s atlas.id = #next atlas.id
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
function atlas:assign_store with storage atlas:macro
