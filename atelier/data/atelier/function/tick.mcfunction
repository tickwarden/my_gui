execute as @a[tag=!atelier.welcomed] run function atelier:welcome
scoreboard players enable @a atelier
execute as @a[scores={atelier=1..}] at @s run function atelier:gui/open
scoreboard players set @a atelier 0
execute as @a[scores={atelier.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"atelier"}] run function atelier:gui/open
execute as @a[scores={atelier.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"atelier"}] run function atelier:gui/open
scoreboard players set @a atelier.use 0
execute as @a[scores={atelier.dead=1..},tag=atelier.open] run function atelier:gui/close
scoreboard players set @a atelier.dead 0
execute as @a[tag=atelier.open] at @s run function atelier:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"atelier"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"atelier"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"atelier"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"atelier"}}}]
execute as @e[type=minecraft:chest_minecart,tag=atelier.cart] at @s unless entity @a[tag=atelier.open,distance=..8] run function atelier:gui/orphan
