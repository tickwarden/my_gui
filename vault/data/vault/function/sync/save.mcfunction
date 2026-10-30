data remove storage vault:tmp one
$data modify storage vault:tmp one set from entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] Items[{Slot:$(slot)b}]
data remove storage vault:tmp one.Slot
$data modify storage vault:rt p$(pid).$(page).s$(slot) set from storage vault:tmp one
scoreboard players add #used vault.tmp 1
