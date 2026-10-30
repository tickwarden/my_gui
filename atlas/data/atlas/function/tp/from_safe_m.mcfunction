$execute unless data storage atlas:rt p$(pid).safe{set:1b} run return run function atlas:act/fail_unset
$execute store result score #x atlas.tmp run data get storage atlas:rt p$(pid).safe.x
$execute store result score #y atlas.tmp run data get storage atlas:rt p$(pid).safe.y
$execute store result score #z atlas.tmp run data get storage atlas:rt p$(pid).safe.z
$execute store result score #dim atlas.tmp run data get storage atlas:rt p$(pid).safe.dim
function atlas:tp/go
