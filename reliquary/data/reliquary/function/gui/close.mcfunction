execute unless entity @s[tag=reliquary.open] run return 0
execute if entity @s
tag @s remove reliquary.open
scoreboard players operation #id reliquary.tmp = @s reliquary.id
execute as @e[type=minecraft:chest_minecart,tag=reliquary.cart] if score @s reliquary.id = #id reliquary.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"reliquary"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s reliquary.grace 0
