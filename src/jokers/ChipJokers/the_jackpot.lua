return SMODS.Joker({
	key = 'the_jackpot',
	loc_txt = {
		name = '777',
		text = {
			"{C:green}#1# in #2#{} chance to add {C:chips}#3#{} chips",
		}
	},
	config = {extra = {
        what_in = 1,
        what_chance = 77,
        chips = 777
    }},
	loc_vars = function(self, info_queue, card)
		return {vars = {
            card.ability.extra.what_in,
            card.ability.extra.what_chance,
            card.ability.extra.chips,
        }}
	end,
	rarity = 1,
	atlas = 'ChipJokers',
	cost = 7,
	calculate = function(self, card, context)
        if context.joker_main then
            if Utils.what_in_what_chance("the_jackpot", card.ability.extra.what_in, card.ability.extra.what_chance) then
                return {
                    chips = card.ability.extra.chips
                }
            end
			return {
				message = "Nope!",
			}
		end
	end,
})