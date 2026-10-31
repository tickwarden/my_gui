execute unless entity @s[tag=atelier.open] run return 0
execute if entity @s
tag @s remove atelier.open
scoreboard players operation #id atelier.tmp = @s atelier.id
execute as @e[type=minecraft:chest_minecart,tag=atelier.cart] if score @s atelier.id = #id atelier.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"atelier"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s atelier.grace 0
