$execute unless data storage bazaar:rt p$(pid).actions.s$(slot) run return 0
$data modify storage bazaar:tmp act set from storage bazaar:rt p$(pid).actions.s$(slot)
execute if data storage bazaar:tmp {act:"none"} run return 0
$execute if data storage bazaar:rt p$(pid).queue run return 0
$data modify storage bazaar:rt p$(pid).queue set from storage bazaar:tmp act
