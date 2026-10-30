execute unless data storage atlas:dest end{set:1b} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest end.x
execute store result score #y atlas.tmp run data get storage atlas:dest end.y
execute store result score #z atlas.tmp run data get storage atlas:dest end.z
execute store result score #dim atlas.tmp run data get storage atlas:dest end.dim
function atlas:tp/go
