return Utils.create_deck("dev_deck", "Developer Deck", {
    "The {C:money,E:2}Gust's Unfree Cards{}",
    "developer deck. Usually",
    "used for testing, this deck",
    "gives you all additions",
    "immediately."
},function()
    add_joker("j_guc_accident", nil, true, false)
    add_joker("j_guc_empty_hand", nil, true, false)
    add_joker("j_guc_the_jackpot", nil, true, false)
    add_joker("j_guc_overloaded", nil, true, false)
end)