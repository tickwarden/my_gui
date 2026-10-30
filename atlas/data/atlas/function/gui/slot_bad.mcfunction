$execute if data storage atlas:live Items[{Slot:$(slot)b}] run function atlas:gui/return_item with storage atlas:macro
function atlas:gui/queue_slot with storage atlas:macro
scoreboard players set #dirty atlas.tmp 1
