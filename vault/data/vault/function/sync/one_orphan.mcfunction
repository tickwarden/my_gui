$execute if data entity @s Items[{Slot:$(slot)b,components:{"minecraft:custom_data":{gui:1b}}}] run data remove entity @s Items[{Slot:$(slot)b}]
$execute if data entity @s Items[{Slot:$(slot)b}] run function vault:sync/save_self {pid:$(pid),slot:$(slot),page:"$(page)"}
$execute unless data entity @s Items[{Slot:$(slot)b}] run function vault:sync/clear {pid:$(pid),slot:$(slot),page:"$(page)"}
