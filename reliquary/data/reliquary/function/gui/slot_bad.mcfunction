$execute if data storage reliquary:live Items[{Slot:$(slot)b}] run function reliquary:gui/return_item with storage reliquary:macro
function reliquary:gui/queue_slot with storage reliquary:macro
scoreboard players set #dirty reliquary.tmp 1
