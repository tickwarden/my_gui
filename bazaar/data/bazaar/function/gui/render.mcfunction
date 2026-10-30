execute if score @s bazaar.page matches 0 run function bazaar:page/main
execute if score @s bazaar.page matches 1 run function bazaar:page/blocks
execute if score @s bazaar.page matches 2 run function bazaar:page/food
execute if score @s bazaar.page matches 3 run function bazaar:page/combat
execute if score @s bazaar.page matches 4 run function bazaar:page/redstone
execute if score @s bazaar.page matches 5 run function bazaar:page/rare
execute if score @s bazaar.page matches 6 run function bazaar:page/sell
execute if score @s bazaar.page matches 7 run function bazaar:page/bank
execute if score @s bazaar.page matches 8 run function bazaar:page/help
execute if score @s bazaar.page matches 9 run function bazaar:page/confirm
execute if score @s bazaar.page matches 10 run function bazaar:page/admin
title @s actionbar [{"text":"Bakiye ","color":"gray"},{"score":{"name":"@s","objective":"bazaar.bank"},"color":"green"},{"text":" zümrüt","color":"dark_gray"}]
