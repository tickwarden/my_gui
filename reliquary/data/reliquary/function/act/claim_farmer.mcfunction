execute unless entity @s[advancements={minecraft:husbandry/plant_seed=true}] run return run function reliquary:act/fail_lock
execute store result storage reliquary:macro pid int 1 run scoreboard players get @s reliquary.id
function reliquary:kit/begin_farmer with storage reliquary:macro
