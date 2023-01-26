def serverIdList():
    # takes in every line of serverids.txt
    with open ('keys/serverids.txt') as serverId_in:
        serverIdList = serverId_in.readlines()
        
    # converts all the strings to ints
    for i in range(0, len(serverIdList)):
        if serverIdList[i].isdigit():
            serverIdList[i] = int(serverIdList[i])
    
    return serverIdList

def discordApiKey():
    # takes in the bot api from the first line of discord.txt
    with open ('keys/discord.txt') as discord_api_key:
        discord_api = discord_api_key.readlines()
    bottoken = discord_api[0]

    return bottoken