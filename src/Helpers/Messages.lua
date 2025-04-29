Helpers.Messages = {}

function Helpers.Messages:Announce(title, message, target)
    server.announce(title, message, target)
end

function Helpers.Messages:LogMessage(message, target)
    if "$$customchat" then
        return
    end
    server.log(message, target)
end