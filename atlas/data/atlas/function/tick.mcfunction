execute as @a[tag=!atlas.welcomed] run function atlas:welcome
scoreboard players enable @a atlas
execute as @a[scores={atlas=1..}] at @s run function atlas:gui/open
scoreboard players set @a atlas 0
execute as @a[scores={atlas.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"atlas"}] run function atlas:gui/open
execute as @a[scores={atlas.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"atlas"}] run function atlas:gui/open
scoreboard players set @a atlas.use 0
execute as @a[scores={atlas.dead=1..},tag=atlas.open] run function atlas:gui/close
scoreboard players set @a atlas.dead 0
execute as @a[tag=atlas.open] at @s run function atlas:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"atlas"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"atlas"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"atlas"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"atlas"}}}]
execute as @e[type=minecraft:chest_minecart,tag=atlas.cart] at @s unless entity @a[tag=atlas.open,distance=..8] run function atlas:gui/orphan

scoreboard players add @a atlas.timer 1
execute as @a[scores={atlas.timer=100..}] at @s run function atlas:safe/try
scoreboard players set @a[scores={atlas.timer=100..}] atlas.timer 0
