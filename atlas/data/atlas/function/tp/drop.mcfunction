execute if score #drop atlas.tmp matches 32.. run return 0
execute store result score #py atlas.tmp run data get entity @s Pos[1]
execute if score #py atlas.tmp matches ..-60 run return 0
execute unless block ~ ~-1 ~ #atlas:passable run return 0
execute if block ~ ~-1 ~ minecraft:lava run return 0
tp @s ~ ~-1 ~
scoreboard players add #drop atlas.tmp 1
function atlas:tp/drop
