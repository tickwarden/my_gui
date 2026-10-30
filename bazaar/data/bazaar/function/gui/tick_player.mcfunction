tag @e[type=minecraft:chest_minecart,tag=bazaar.this] remove bazaar.this
scoreboard players operation #id bazaar.tmp = @s bazaar.id
execute as @e[type=minecraft:chest_minecart,tag=bazaar.cart] if score @s bazaar.id = #id bazaar.tmp run tag @s add bazaar.this
execute unless entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] run return run function bazaar:gui/lost
execute if score @s bazaar.grace matches 1.. run scoreboard players remove @s bazaar.grace 1
execute if score @s bazaar.grace matches 0 if predicate bazaar:sneaking run return run function bazaar:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=bazaar.this,distance=..7,limit=1] run return run function bazaar:gui/close
execute at @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function bazaar:gui/close
execute at @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function bazaar:gui/anti_hopper
function bazaar:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=bazaar.this] remove bazaar.this
