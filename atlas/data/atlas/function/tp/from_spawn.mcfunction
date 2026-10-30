execute unless data storage atlas:dest spawn{set:1b} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest spawn.x
execute store result score #y atlas.tmp run data get storage atlas:dest spawn.y
execute store result score #z atlas.tmp run data get storage atlas:dest spawn.z
execute store result score #dim atlas.tmp run data get storage atlas:dest spawn.dim
function atlas:tp/go
