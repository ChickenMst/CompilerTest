Helpers.Logger = {
    Logs = {},
    LogLevel = "critical"
}

function Helpers.Logger:Log(type,message)
    if type ~= "critical" or "error" or "warning" or "info" then
        return
    end
    table.insert(self.Logs, {type = type, message = message})
end

function Helpers.Logger:SetLogLevel(level)
    self.LogLevel = level
end