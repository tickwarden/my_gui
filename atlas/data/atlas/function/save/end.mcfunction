execute store result storage atlas:dest end.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest end.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest end.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest end.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest end.set set value 1b
data modify storage atlas:dest end.name set value "End adası"
