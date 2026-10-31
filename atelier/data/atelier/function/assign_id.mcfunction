scoreboard players add #next atelier.id 1
scoreboard players operation @s atelier.id = #next atelier.id
execute store result storage atelier:macro pid int 1 run scoreboard players get @s atelier.id
function atelier:assign_store with storage atelier:macro
