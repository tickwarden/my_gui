$item replace entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] container.13 with $(id) $(count)
data modify entity @e[type=minecraft:chest_minecart,tag=bazaar.this,limit=1] Items[{Slot:13b}].components."minecraft:custom_data" set value {gui:1b,pack:"bazaar"}
function bazaar:page/confirm_icon_name with storage bazaar:tmp offer
