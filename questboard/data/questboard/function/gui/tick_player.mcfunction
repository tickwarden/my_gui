tag @e[type=minecraft:chest_minecart,tag=questboard.this] remove questboard.this
scoreboard players operation #id questboard.tmp = @s questboard.id
execute as @e[type=minecraft:chest_minecart,tag=questboard.cart] if score @s questboard.id = #id questboard.tmp run tag @s add questboard.this
execute unless entity @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] run return run function questboard:gui/lost
execute if score @s questboard.grace matches 1.. run scoreboard players remove @s questboard.grace 1
execute if score @s questboard.grace matches 0 if predicate questboard:sneaking run return run function questboard:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=questboard.this,distance=..7,limit=1] run return run function questboard:gui/close
execute at @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function questboard:gui/close
execute at @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function questboard:gui/anti_hopper
function questboard:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=questboard.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=questboard.this] remove questboard.this
