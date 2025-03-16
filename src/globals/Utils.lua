local Utils = {}

function Utils.what_in_what_chance(id,what_in,what_chance)
    return pseudorandom("guc_"..id) < (what_in+(G.GAME.probabilities.normal-1))/what_chance
end

function Utils.create_deck(id,name,text,func)
    SMODS.Deck:new(name, id, {
        guc_deck = id
    }, {x = 5, y = 2}, {
        name = name,
        text = text
    }):register()

    Utils[id] = func
end

function Utils.atlas(name)
    SMODS.Atlas {
        key = name,
        path = name .. ".png",
        px = 71,
        py = 95
    }
end

return Utils