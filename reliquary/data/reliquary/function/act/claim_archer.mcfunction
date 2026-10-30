execute unless entity @s[advancements={minecraft:adventure/shoot_arrow=true}] run return run function reliquary:act/fail_lock
execute store result storage reliquary:macro pid int 1 run scoreboard players get @s reliquary.id
function reliquary:kit/begin_archer with storage reliquary:macro
