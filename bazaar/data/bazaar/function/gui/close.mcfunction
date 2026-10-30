execute unless entity @s[tag=bazaar.open] run return 0
execute if entity @s
tag @s remove bazaar.open
scoreboard players operation #id bazaar.tmp = @s bazaar.id
execute as @e[type=minecraft:chest_minecart,tag=bazaar.cart] if score @s bazaar.id = #id bazaar.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"bazaar"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s bazaar.grace 0
