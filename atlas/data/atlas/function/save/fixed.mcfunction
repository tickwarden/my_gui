$execute store result storage atlas:dest $(key).x int 1 run scoreboard players get #x atlas.tmp
$execute store result storage atlas:dest $(key).y int 1 run scoreboard players get #y atlas.tmp
$execute store result storage atlas:dest $(key).z int 1 run scoreboard players get #z atlas.tmp
$execute store result storage atlas:dest $(key).dim int 1 run scoreboard players get #dim atlas.tmp
$data modify storage atlas:dest $(key).set set value 1b
