tag @e[type=minecraft:chest_minecart,tag=vault.this] remove vault.this
scoreboard players operation #id vault.tmp = @s vault.id
execute as @e[type=minecraft:chest_minecart,tag=vault.cart] if score @s vault.id = #id vault.tmp run tag @s add vault.this
execute unless entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run return run function vault:gui/lost
execute if score @s vault.grace matches 1.. run scoreboard players remove @s vault.grace 1
execute if score @s vault.grace matches 0 if predicate vault:sneaking run return run function vault:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=vault.this,distance=..7,limit=1] run return run function vault:gui/close
execute at @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function vault:gui/close
execute at @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function vault:gui/anti_hopper
function vault:gui/vault_tick
execute as @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=vault.this] remove vault.this
