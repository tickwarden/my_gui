$execute unless data storage atlas:rt p$(pid).h$(sel){set:1b} run return run function atlas:act/fail_unset
$execute store result score #x atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).x
$execute store result score #y atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).y
$execute store result score #z atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).z
$execute store result score #dim atlas.tmp run data get storage atlas:rt p$(pid).h$(sel).dim
function atlas:tp/go
