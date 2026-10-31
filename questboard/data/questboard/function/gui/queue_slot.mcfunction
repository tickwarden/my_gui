$execute unless data storage questboard:rt p$(pid).actions.s$(slot) run return 0
$data modify storage questboard:tmp act set from storage questboard:rt p$(pid).actions.s$(slot)
execute if data storage questboard:tmp {act:"none"} run return 0
$execute if data storage questboard:rt p$(pid).queue run return 0
$data modify storage questboard:rt p$(pid).queue set from storage questboard:tmp act
