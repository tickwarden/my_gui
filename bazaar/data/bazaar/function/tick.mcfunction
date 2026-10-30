execute as @a[tag=!bazaar.welcomed] run function bazaar:welcome
scoreboard players enable @a bazaar
execute as @a[scores={bazaar=1..}] at @s run function bazaar:gui/open
scoreboard players set @a bazaar 0
execute as @a[scores={bazaar.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"bazaar"}] run function bazaar:gui/open
execute as @a[scores={bazaar.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"bazaar"}] run function bazaar:gui/open
scoreboard players set @a bazaar.use 0
execute as @a[scores={bazaar.dead=1..},tag=bazaar.open] run function bazaar:gui/close
scoreboard players set @a bazaar.dead 0
execute as @a[tag=bazaar.open] at @s run function bazaar:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"bazaar"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"bazaar"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"bazaar"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"bazaar"}}}]
execute as @e[type=minecraft:chest_minecart,tag=bazaar.cart] at @s unless entity @a[tag=bazaar.open,distance=..8] run function bazaar:gui/orphan
