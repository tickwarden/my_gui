execute unless entity @s[tag=atlas.open] run return 0
execute if entity @s
tag @s remove atlas.open
scoreboard players operation #id atlas.tmp = @s atlas.id
execute as @e[type=minecraft:chest_minecart,tag=atlas.cart] if score @s atlas.id = #id atlas.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"atlas"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s atlas.grace 0
