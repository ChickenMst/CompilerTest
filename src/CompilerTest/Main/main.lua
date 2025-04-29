require('Helpers/test')
function onTick()
    server.announce("test","$$test")
    Helpers.test:test()
end