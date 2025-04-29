Helpers.Addons = {}

function Helpers.Addons:Add(name, func)
    self[name] = func
end

function Helpers.Addons:Remove(name)
    self[name] = nil
end

function Helpers.Addons:Edit(name, func)
    if self[name] then
        self[name] = func
    end
end