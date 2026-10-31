$execute if data storage questboard:live Items[{Slot:$(slot)b}] run function questboard:gui/return_item with storage questboard:macro
function questboard:gui/queue_slot with storage questboard:macro
scoreboard players set #dirty questboard.tmp 1
