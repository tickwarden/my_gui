execute as @a[tag=!reliquary.welcomed] run function reliquary:welcome
scoreboard players enable @a reliquary
execute as @a[scores={reliquary=1..}] at @s run function reliquary:gui/open
scoreboard players set @a reliquary 0
execute as @a[scores={reliquary.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"reliquary"}] run function reliquary:gui/open
execute as @a[scores={reliquary.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"reliquary"}] run function reliquary:gui/open
scoreboard players set @a reliquary.use 0
execute as @a[scores={reliquary.dead=1..},tag=reliquary.open] run function reliquary:gui/close
scoreboard players set @a reliquary.dead 0
execute as @a[tag=reliquary.open] at @s run function reliquary:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"reliquary"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"reliquary"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"reliquary"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"reliquary"}}}]
execute as @e[type=minecraft:chest_minecart,tag=reliquary.cart] at @s unless entity @a[tag=reliquary.open,distance=..8] run function reliquary:gui/orphan
