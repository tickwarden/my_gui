$execute if data storage mailbox:live Items[{Slot:$(slot)b}] run function mailbox:gui/return_item with storage mailbox:macro
function mailbox:gui/queue_slot with storage mailbox:macro
scoreboard players set #dirty mailbox.tmp 1
