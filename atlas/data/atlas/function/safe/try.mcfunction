execute unless score @s atlas.id matches 1.. run return 0
execute unless data entity @s {OnGround:1b} run return 0
execute if block ~ ~ ~ minecraft:lava run return 0
execute if block ~ ~-1 ~ minecraft:lava run return 0
execute unless block ~ ~-1 ~ #minecraft:solid run return 0
execute unless block ~ ~ ~ #atlas:passable run return 0
execute unless block ~ ~1 ~ #atlas:passable run return 0
function atlas:safe/save
