tag @e[type=minecraft:chest_minecart,tag=reliquary.this] remove reliquary.this
scoreboard players operation #id reliquary.tmp = @s reliquary.id
execute as @e[type=minecraft:chest_minecart,tag=reliquary.cart] if score @s reliquary.id = #id reliquary.tmp run tag @s add reliquary.this
execute unless entity @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] run return run function reliquary:gui/lost
execute if score @s reliquary.grace matches 1.. run scoreboard players remove @s reliquary.grace 1
execute if score @s reliquary.grace matches 0 if predicate reliquary:sneaking run return run function reliquary:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=reliquary.this,distance=..7,limit=1] run return run function reliquary:gui/close
execute at @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function reliquary:gui/close
execute at @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function reliquary:gui/anti_hopper
function reliquary:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=reliquary.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=reliquary.this] remove reliquary.this
