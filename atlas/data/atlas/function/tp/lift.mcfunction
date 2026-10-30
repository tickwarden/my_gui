execute if score #lift atlas.tmp matches 20.. run return 0
execute if block ~ ~ ~ #atlas:passable if block ~ ~1 ~ #atlas:passable run return 0
tp @s ~ ~1 ~
scoreboard players add #lift atlas.tmp 1
function atlas:tp/lift
