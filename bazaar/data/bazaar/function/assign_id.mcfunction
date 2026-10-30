scoreboard players add #next bazaar.id 1
scoreboard players operation @s bazaar.id = #next bazaar.id
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:assign_store with storage bazaar:macro
