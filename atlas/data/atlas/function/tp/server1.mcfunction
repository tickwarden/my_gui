execute unless data storage atlas:dest s1{set:1b} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest s1.x
execute store result score #y atlas.tmp run data get storage atlas:dest s1.y
execute store result score #z atlas.tmp run data get storage atlas:dest s1.z
execute store result score #dim atlas.tmp run data get storage atlas:dest s1.dim
function atlas:tp/go
