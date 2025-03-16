return SMODS.Joker({
	key = 'overloaded',
	loc_txt = {
		name = 'Overloaded',
		text = {
			"Card gains {C:chips}+#2#{} hand size every {C:attention}played hand{}",
            "but {C:mult}-#3#{} hand size every {C:attention}discard{}.",
            "{C:inactive}(Currently {C:chips}+#1#{C:inactive} hand size)"
		}
	},
	config = {extra = {
        add_hand_size = 1,
        play_hand_size_change = 1,
        discard_hand_size_change_negative = 2,
    }},
	loc_vars = function(self, info_queue, card)
		return {vars = {
            card.ability.extra.add_hand_size,
            card.ability.extra.play_hand_size_change,
            card.ability.extra.discard_hand_size_change_negative,
        }}
	end,
	rarity = 2,
	atlas = 'UtilJokers',
	cost = 12,
	calculate = function(self, card, context)
        if context.pre_discard then
            card.ability.extra.add_hand_size = card.ability.extra.add_hand_size - card.ability.extra.discard_hand_size_change_negative
            G.hand:change_size(-card.ability.extra.discard_hand_size_change_negative)
            return {
                message = "-" .. card.ability.extra.discard_hand_size_change_negative .. " Hand Size"
            }
        end
        if context.before then
            card.ability.extra.add_hand_size = card.ability.extra.add_hand_size + card.ability.extra.play_hand_size_change
            G.hand:change_size(card.ability.extra.play_hand_size_change)
            return {
                message = "+" .. card.ability.extra.play_hand_size_change .. " Hand Size"
            }
        end
	end,
	remove_from_deck = function(self, card, from_debuff)
        G.hand:change_size(-card.ability.extra.add_hand_size)
	end
})