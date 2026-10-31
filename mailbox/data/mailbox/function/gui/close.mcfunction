execute unless entity @s[tag=mailbox.open] run return 0
execute if entity @s
tag @s remove mailbox.open
scoreboard players operation #id mailbox.tmp = @s mailbox.id
execute as @e[type=minecraft:chest_minecart,tag=mailbox.cart] if score @s mailbox.id = #id mailbox.tmp run kill @s
clear @s *[minecraft:custom_data={gui:1b,pack:"mailbox"}]
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.55 1
scoreboard players set @s mailbox.grace 0
