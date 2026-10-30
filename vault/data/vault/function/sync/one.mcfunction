$execute unless entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] run return 0
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b,components:{"minecraft:custom_data":{gui:1b}}}] run data remove entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}]
$execute if data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/save {pid:$(pid),slot:$(slot),page:"$(page)"}
$execute unless data entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}] run function vault:sync/clear {pid:$(pid),slot:$(slot),page:"$(page)"}
