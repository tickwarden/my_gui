execute as @a[tag=!questboard.welcomed] run function questboard:welcome
scoreboard players enable @a questboard
execute as @a[scores={questboard=1..}] at @s run function questboard:gui/open
scoreboard players set @a questboard 0
execute as @a[scores={questboard.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"questboard"}] run function questboard:gui/open
execute as @a[scores={questboard.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"questboard"}] run function questboard:gui/open
scoreboard players set @a questboard.use 0
execute as @a[scores={questboard.dead=1..},tag=questboard.open] run function questboard:gui/close
scoreboard players set @a questboard.dead 0
execute as @a[tag=questboard.open] at @s run function questboard:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"questboard"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"questboard"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"questboard"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"questboard"}}}]
execute as @e[type=minecraft:chest_minecart,tag=questboard.cart] at @s unless entity @a[tag=questboard.open,distance=..8] run function questboard:gui/orphan
