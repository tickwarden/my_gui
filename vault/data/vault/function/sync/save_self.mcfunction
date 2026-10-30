data remove storage vault:tmp one
$data modify storage vault:tmp one set from entity @s Items[{Slot:$(slot)b}]
data remove storage vault:tmp one.Slot
$data modify storage vault:rt p$(pid).$(page).s$(slot) set from storage vault:tmp one
