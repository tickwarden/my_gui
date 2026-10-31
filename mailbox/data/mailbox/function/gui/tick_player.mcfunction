tag @e[type=minecraft:chest_minecart,tag=mailbox.this] remove mailbox.this
scoreboard players operation #id mailbox.tmp = @s mailbox.id
execute as @e[type=minecraft:chest_minecart,tag=mailbox.cart] if score @s mailbox.id = #id mailbox.tmp run tag @s add mailbox.this
execute unless entity @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] run return run function mailbox:gui/lost
execute if score @s mailbox.grace matches 1.. run scoreboard players remove @s mailbox.grace 1
execute if score @s mailbox.grace matches 0 if predicate mailbox:sneaking run return run function mailbox:gui/close
execute unless entity @e[type=minecraft:chest_minecart,tag=mailbox.this,distance=..7,limit=1] run return run function mailbox:gui/close
execute at @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] if block ~ ~ ~ minecraft:nether_portal run return run function mailbox:gui/close
execute at @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] if block ~ ~-1 ~ minecraft:hopper run return run function mailbox:gui/anti_hopper
function mailbox:gui/scan
execute as @e[type=minecraft:chest_minecart,tag=mailbox.this,limit=1] run data merge entity @s {Motion:[0.0d,0.0d,0.0d]}
tag @e[type=minecraft:chest_minecart,tag=mailbox.this] remove mailbox.this
