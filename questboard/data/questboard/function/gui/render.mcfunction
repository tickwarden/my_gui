execute if score @s questboard.page matches 0 run function questboard:page/main
execute if score @s questboard.page matches 1 run function questboard:page/daily
execute if score @s questboard.page matches 2 run function questboard:page/weekly
execute if score @s questboard.page matches 3 run function questboard:page/progress
execute if score @s questboard.page matches 4 run function questboard:page/rewards
execute if score @s questboard.page matches 5 run function questboard:page/help
title @s actionbar {"text":"Görev Tahtası  •  kabul et, ilerle, ödül al","color":"gold"}
