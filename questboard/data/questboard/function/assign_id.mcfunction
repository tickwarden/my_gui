scoreboard players add #next questboard.id 1
scoreboard players operation @s questboard.id = #next questboard.id
execute store result storage questboard:macro pid int 1 run scoreboard players get @s questboard.id
function questboard:assign_store with storage questboard:macro
