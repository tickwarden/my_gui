execute as @a[tag=!mailbox.welcomed] run function mailbox:welcome
scoreboard players enable @a mailbox
execute as @a[scores={mailbox=1..}] at @s run function mailbox:gui/open
scoreboard players set @a mailbox 0
execute as @a[scores={mailbox.use=1..}] at @s if items entity @s weapon.mainhand *[minecraft:custom_data={key:1b,pack:"mailbox"}] run function mailbox:gui/open
execute as @a[scores={mailbox.use=1..}] at @s if items entity @s weapon.offhand *[minecraft:custom_data={key:1b,pack:"mailbox"}] run function mailbox:gui/open
scoreboard players set @a mailbox.use 0
execute as @a[scores={mailbox.dead=1..},tag=mailbox.open] run function mailbox:gui/close
scoreboard players set @a mailbox.dead 0
execute as @a[tag=mailbox.open] at @s run function mailbox:gui/tick_player
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{gui:1b,pack:"mailbox"}}}}]
clear @a *[minecraft:custom_data={gui:1b,pack:"mailbox"}]
execute as @e[type=minecraft:hopper_minecart] if data entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"mailbox"}}}] run data remove entity @s Items[{components:{"minecraft:custom_data":{gui:1b,pack:"mailbox"}}}]
execute as @e[type=minecraft:chest_minecart,tag=mailbox.cart] at @s unless entity @a[tag=mailbox.open,distance=..8] run function mailbox:gui/orphan
