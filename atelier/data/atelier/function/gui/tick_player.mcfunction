tag @e[type=minecraft:chest_minecart,tag=atelier.this] remove atelier.this
scoreboard players operation #id atelier.tmp = @s atelier.id
execute as @e[type=minecraft:chest_minecart,tag=atelier.cart] if score @s atelier.id = #id atelier.tmp run tag @s add atelier.this
execute unless entity @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] run return run function atelier:gui/lost
execute if score @s atelier.grace matches 1.. run scoreboard players remove @s atelier.grace 1
execute if score @s atelier.grace matches 0 if predicate atelier:sneaking run return run function atelier:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=atelier.this,distance=..7,limit=1] run return run function atelier:gui/close
execute at @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function atelier:gui/close
execute at @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function atelier:gui/anti_hopper
function atelier:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=atelier.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=atelier.this] remove atelier.this
