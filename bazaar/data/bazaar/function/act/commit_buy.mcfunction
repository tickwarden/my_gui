execute if score #stock bazaar.tmp matches 0 run return run function bazaar:act/fail_stock
execute unless score @s bazaar.bank >= #price bazaar.tmp run return run function bazaar:act/fail_money
scoreboard players operation @s bazaar.bank -= #price bazaar.tmp
function bazaar:act/give_offer with storage bazaar:tmp
execute if score #stock bazaar.tmp matches 1.. run function bazaar:act/dec_stock
playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.5 1.4
tellraw @s [{"text":"Satın alındı. ","color":"green"},{"text":"Kalan bakiye: ","color":"gray"},{"score":{"name":"@s","objective":"bazaar.bank"},"color":"yellow"}]
function bazaar:act/buy_no
