function bazaar:act/count_item with storage bazaar:tmp
execute if score #have bazaar.tmp < #count bazaar.tmp run return run function bazaar:act/fail_items
function bazaar:act/clear_item with storage bazaar:tmp
scoreboard players operation @s bazaar.bank += #price bazaar.tmp
execute if score #stock bazaar.tmp matches 0.. run function bazaar:act/inc_stock
playsound minecraft:entity.villager.trade player @s ~ ~ ~ 0.8 1
tellraw @s [{"text":"Satıldı. Banka +","color":"green"},{"score":{"name":"#price","objective":"bazaar.tmp"},"color":"yellow"}]
function bazaar:act/buy_no
