$execute unless data storage atelier:rt p$(pid).actions.s$(slot) run return 0
$data modify storage atelier:tmp act set from storage atelier:rt p$(pid).actions.s$(slot)
execute if data storage atelier:tmp {act:"none"} run return 0
$execute if data storage atelier:rt p$(pid).queue run return 0
$data modify storage atelier:rt p$(pid).queue set from storage atelier:tmp act
