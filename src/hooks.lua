local Backapply_to_runRef = Back.apply_to_run
function Back.apply_to_run(arg_56_0)
    Backapply_to_runRef(arg_56_0)

    if arg_56_0.effect.config.guc_deck and Utils.decks[arg_56_0.effect.config.guc_deck] then
        G.E_MANAGER:add_event(Event({
            func = function()
                Utils.decks[arg_56_0.effect.config.guc_deck]()
                return true
            end
        }))
    end
end
--[[
local evaluate_playref = G.FUNCS.evaluate_play
function G.FUNCS.evaluate_play(self, e)
    evaluate_playref(self, e)

    for i = 1, #G.jokers.cards do
        G.guc_scored_chips = hand_chips * mult
        G.guc_mult = mult
    end
end]]