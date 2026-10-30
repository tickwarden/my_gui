execute unless data storage atlas:dest nether{set:1b} run return run function atlas:act/fail_unset
execute store result score #x atlas.tmp run data get storage atlas:dest nether.x
execute store result score #y atlas.tmp run data get storage atlas:dest nether.y
execute store result score #z atlas.tmp run data get storage atlas:dest nether.z
execute store result score #dim atlas.tmp run data get storage atlas:dest nether.dim
function atlas:tp/go
