return SMODS.Joker({
	key = 'accident',
	loc_txt = {
		name = 'Accident',
		text = {
			"{X:mult,C:white}??x{} Mult",
            "{C:green}#1# in #2#{} chance to",
            "get {X:mult,C:white}#5#x{} Mult",
            "otherwise get a random mult",
            "from {X:mult,C:white}#3#x{} to {X:mult,C:white}#4#x{}."
		}
	},
	config = {extra = {
        lowest_mult = 1,
        highest_mult = 10,
        what_in = 1,
        what_chance = 10,
        or_else_mult = -11,
    }},
	loc_vars = function(self, info_queue, card)
		return {vars = {
            card.ability.extra.what_in,
            card.ability.extra.what_chance,
            card.ability.extra.lowest_mult,
            card.ability.extra.highest_mult,
            card.ability.extra.or_else_mult,
        }}
	end,
	rarity = 3,
	atlas = 'MultJokers',
	cost = 9,
	calculate = function(self, card, context)
		if context.joker_main then
			local xmult = math.random(card.ability.extra.lowest_mult,card.ability.extra.highest_mult)
            if Utils.what_in_what_chance("accident", card.ability.extra.what_in, card.ability.extra.what_chance) then
                xmult = card.ability.extra.or_else_mult
            end
			return {
				xmult = xmult,
				--message = localize { type = 'variable', key = 'x_mult', vars = { xmult } }
			}
		end
	end
})