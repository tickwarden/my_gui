execute store result storage atlas:dest nether.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest nether.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest nether.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest nether.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest nether.set set value 1b
data modify storage atlas:dest nether.name set value "Nether kapısı"
