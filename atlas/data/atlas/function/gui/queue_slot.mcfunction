$execute unless data storage atlas:rt p$(pid).actions.s$(slot) run return 0
$data modify storage atlas:tmp act set from storage atlas:rt p$(pid).actions.s$(slot)
execute if data storage atlas:tmp {act:"none"} run return 0
$execute if data storage atlas:rt p$(pid).queue run return 0
$data modify storage atlas:rt p$(pid).queue set from storage atlas:tmp act
