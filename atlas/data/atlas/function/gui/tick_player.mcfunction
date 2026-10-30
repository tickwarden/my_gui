tag @e[type=minecraft:chest_minecart,tag=atlas.this] remove atlas.this
scoreboard players operation #id atlas.tmp = @s atlas.id
execute as @e[type=minecraft:chest_minecart,tag=atlas.cart] if score @s atlas.id = #id atlas.tmp run tag @s add atlas.this
execute unless entity @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] run return run function atlas:gui/lost
execute if score @s atlas.grace matches 1.. run scoreboard players remove @s atlas.grace 1
execute if score @s atlas.grace matches 0 if predicate atlas:sneaking run return run function atlas:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=atlas.this,distance=..7,limit=1] run return run function atlas:gui/close
execute at @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function atlas:gui/close
execute at @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function atlas:gui/anti_hopper
function atlas:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=atlas.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=atlas.this] remove atlas.this
