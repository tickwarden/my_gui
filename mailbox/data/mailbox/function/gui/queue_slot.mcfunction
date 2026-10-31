$execute unless data storage mailbox:rt p$(pid).actions.s$(slot) run return 0
$data modify storage mailbox:tmp act set from storage mailbox:rt p$(pid).actions.s$(slot)
execute if data storage mailbox:tmp {act:"none"} run return 0
$execute if data storage mailbox:rt p$(pid).queue run return 0
$data modify storage mailbox:rt p$(pid).queue set from storage mailbox:tmp act
