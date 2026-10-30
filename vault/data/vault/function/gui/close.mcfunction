execute unless entity @s[tag=vault.open] run return 0
tag @e[type=minecraft:chest_minecart,tag=vault.this] remove vault.this
scoreboard players operation #id vault.tmp = @s vault.id
execute as @e[type=minecraft:chest_minecart,tag=vault.cart] if score @s vault.id = #id vault.tmp run tag @s add vault.this
execute if entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run function vault:gui/save
tag @s remove vault.open
scoreboard players operation #id vault.tmp = @s vault.id
execute as @e[type=minecraft:chest_minecart,tag=vault.cart] if score @s vault.id = #id vault.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"vault"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s vault.grace 0
