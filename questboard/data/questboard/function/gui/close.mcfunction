execute unless entity @s[tag=questboard.open] run return 0
execute if entity @s
tag @s remove questboard.open
scoreboard players operation #id questboard.tmp = @s questboard.id
execute as @e[type=minecraft:chest_minecart,tag=questboard.cart] if score @s questboard.id = #id questboard.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"questboard"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s questboard.grace 0
