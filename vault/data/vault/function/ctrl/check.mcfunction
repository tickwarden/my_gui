scoreboard players set #dirty vault.tmp 0
data modify storage vault:live Items set from entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute unless data storage vault:live Items[{Slot:18b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_18
execute unless data storage vault:live Items[{Slot:20b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_20
execute unless data storage vault:live Items[{Slot:25b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_25
execute unless data storage vault:live Items[{Slot:26b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_26
execute unless data storage vault:live Items[{Slot:19b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_fill_19
execute unless data storage vault:live Items[{Slot:21b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_fill_21
execute unless data storage vault:live Items[{Slot:22b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_fill_22
execute unless data storage vault:live Items[{Slot:23b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_fill_23
execute unless data storage vault:live Items[{Slot:24b,components:{"minecraft:custom_data":{gui:1b,pack:"vault"}}}] run function vault:ctrl/bad_fill_24
