$execute if data storage vault:live Items[{Slot:$(slot)b}] run function vault:gui/return_item with storage vault:macro
function vault:gui/queue_slot with storage vault:macro
scoreboard players set #dirty vault.tmp 1
