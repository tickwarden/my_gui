$execute unless data storage vault:rt p$(pid).$(page).s$(slot) run return 0
data remove storage vault:tmp one
$data modify storage vault:tmp one set from storage vault:rt p$(pid).$(page).s$(slot)
$data modify storage vault:tmp one.Slot set value $(slot)b
data modify entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items append from storage vault:tmp one
