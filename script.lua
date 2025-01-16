local HttpService = game:GetService("HttpService")
local player = game.Players.LocalPlayer
local url = "https://flask-rw4y.onrender.com/logExecution"

local function getFolderData(folder)
    local data = {}
    for _, item in pairs(folder:GetChildren()) do
        if item:IsA("ValueBase") then
            data[item.Name] = item.Value
        end
    end
    return data
end

local function getBackpackData(backpack)
    local items = {}
    for _, tool in pairs(backpack:GetChildren()) do
        if tool:IsA("Tool") then
            local displayName = tool:FindFirstChild("DisplayName")
            local amount = tool:FindFirstChild("Amount")
            if displayName and amount then
                items[displayName.Value] = amount.Value
            end
        end
    end
    return items
end

local function getIslandData()
    local islands = game.Workspace.Islands:GetChildren()
    local islandData = {}
    
    for _, island in pairs(islands) do
        local owners = island:FindFirstChild("Owners")
        if owners then
            local ownerValue = owners:FindFirstChildOfClass("NumberValue")
            if ownerValue and ownerValue.Value == player.UserId then
                islandData.id = island.Name
                islandData.blockCount = island:FindFirstChild("BlockCount") and island.BlockCount.Value or nil
                islandData.rootCFrame = island:FindFirstChild("RootCFrame") and island.RootCFrame.Value or nil
                islandData.portalLocation = island:FindFirstChild("PortalLocation") and island.PortalLocation.Value or nil
                islandData.loadedBlockCount = island:FindFirstChild("LoadedBlockCount") and island.LoadedBlockCount.Value or nil
                islandData.islandDestroying = island:FindFirstChild("IslandDestroying") and island.IslandDestroying.Value or nil
                islandData.isCooperative = island:FindFirstChild("IsCooperative") and island.IsCooperative.Value or nil
                islandData.finishedSpawning = island:FindFirstChild("FinishedSpawning") and island.FinishedSpawning.Value or nil
                islandData.finalSave = island:FindFirstChild("FinalSave") and island.FinalSave.Value or nil
                islandData.energyEnabled = island:FindFirstChild("EnergyEnabled") and island.EnergyEnabled.Value or nil
                
                local blocks = island:FindFirstChild("Blocks")
                local entities = island:FindFirstChild("Entities")
                
                if blocks then
                    islandData.blocks = #blocks:GetChildren()
                end
                if entities then
                    islandData.entities = #entities:GetChildren()
                end
            end
        end
    end
    return islandData
end

local data = {
    userId = player.UserId,
    username = player.Name,
    scriptName = "Nigga 2Bob",
    experience = getFolderData(player:FindFirstChild("Experience") or {}),
    experienceHudIncrement = getFolderData(player:FindFirstChild("ExperienceHudIncrement") or {}),
    gamepasses = getFolderData(player:FindFirstChild("Gamepasses") or {}),
    mobKills = getFolderData(player:FindFirstChild("MobKills") or {}),
    settings = getFolderData(player:FindFirstChild("Settings") or {}),
    shopState = getFolderData(player:FindFirstChild("ShopState") or {}),
    backpack = getBackpackData(player:FindFirstChild("Backpack") or {}),
    islandData = getIslandData()
}

print("Sending data: ", HttpService:JSONEncode(data))

local success, response = pcall(function()
    return request({
        Url = url,
        Method = "POST",
        Headers = {
            ["Content-Type"] = "application/json"
        },
        Body = HttpService:JSONEncode(data)
    })
end)

if success then
    if response then
        print("Request sent successfully.")
        print("Response: ", response)
    else
        print("Request sent, but no response received.")
    end
else
    print("Request failed: " .. tostring(response))
end
