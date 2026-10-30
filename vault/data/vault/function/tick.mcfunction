execute as @a[tag=!vault.welcomed] run function vault:welcome
scoreboard players enable @a vault
execute as @a[scores={vault=1..}] at @s run function vault:gui/open
scoreboard players set @a vault 0
execute as @a[scores={vault.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"vault"}] run function vault:gui/open
execute as @a[scores={vault.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"vault"}] run function vault:gui/open
scoreboard players set @a vault.use 0
execute as @a[scores={vault.dead=1..},tag=vault.open] run function vault:gui/close
scoreboard players set @a vault.dead 0
execute as @a[tag=vault.open] at @s run function vault:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"vault"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}]
execute as @e[type=minecraft:chest_minecart,tag=vault.cart] at @s unless entity @a[tag=vault.open,distance=..8] run function vault:gui/orphan
