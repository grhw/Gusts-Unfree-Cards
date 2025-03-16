return SMODS.Joker({
	key = 'empty_hand',
	loc_txt = {
		name = 'Empty Hand',
		text = {
			"Adds {X:negative,C:white}+1{} joker slot if all",
            "discards are used on the first round.",
            "{C:inactive}(Currently {C:negative}+#1#{C:inactive} joker slot)"
		}
	},
	config = {extra = {
        add_jokers = 0,
        already_triggered_this_round = false
    }},
	loc_vars = function(self, info_queue, card)
		return {vars = {
            card.ability.extra.add_jokers,
        }}
	end,
	rarity = 2,
	atlas = 'UtilJokers',
	cost = 12,
	calculate = function(self, card, context)
        if context.pre_discard and not card.ability.extra.already_triggered_this_round then
            if G.GAME.current_round.discards_used >= G.GAME.round_resets.discards - 1 and G.GAME.current_round.hands_played == 0 then
                card.ability.extra.add_jokers = card.ability.extra.add_jokers + 1
                card.ability.extra.already_triggered_this_round = true
                G.jokers.config.card_limit = G.jokers.config.card_limit + 1

                return {
                    message = "+1 Joker Slot"
                }
            end
            --[[return {
                message = table.concat({G.GAME.current_round.discards_used, G.GAME.round_resets.discards, G.GAME.current_round.hands_played}, ","),
            }]]
        end
        if context.end_of_round and context.cardarea == G.jokers then
            card.ability.extra.already_triggered_this_round = false
        end
	end,
	remove_from_deck = function(self, card, from_debuff)
        G.jokers.config.card_limit = G.jokers.config.card_limit - card.ability.extra.add_jokers
	end
})