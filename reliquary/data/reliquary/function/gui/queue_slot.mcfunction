$execute unless data storage reliquary:rt p$(pid).actions.s$(slot) run return 0
$data modify storage reliquary:tmp act set from storage reliquary:rt p$(pid).actions.s$(slot)
execute if data storage reliquary:tmp {act:"none"} run return 0
$execute if data storage reliquary:rt p$(pid).queue run return 0
$data modify storage reliquary:rt p$(pid).queue set from storage reliquary:tmp act
