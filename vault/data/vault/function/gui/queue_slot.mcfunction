$execute unless data storage vault:rt p$(pid).actions.s$(slot) run return 0
$data modify storage vault:tmp act set from storage vault:rt p$(pid).actions.s$(slot)
execute if data storage vault:tmp {act:"none"} run return 0
$execute if data storage vault:rt p$(pid).queue run return 0
$data modify storage vault:rt p$(pid).queue set from storage vault:tmp act
