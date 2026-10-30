execute store result storage atlas:dest spawn.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest spawn.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest spawn.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest spawn.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest spawn.set set value 1b
data modify storage atlas:dest spawn.name set value "Dünya merkezi"
