targetScope = 'subscription'

@description('Azure region for the development environment.')
param location string = 'australiaeast'

@description('Name of the development resource group.')
param resourceGroupName string = 'rg-aika-dev-aue-001'

@description('Required governance tags.')
param resourceTags object = {
  application: 'ai-knowledge-assistant'
  environment: 'development'
  'data-classification': 'synthetic-only'
  'managed-by': 'bicep'
  purpose: 'portfolio-learning'
  'cost-control': 'monthly-budget-alerts'
}

resource developmentResourceGroup 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: location
  tags: resourceTags
}

output deployedResourceGroupName string = developmentResourceGroup.name

var uniqueSuffix = uniqueString(subscription().id, resourceGroupName)
var identityName = 'id-aika-dev-aue-001'
var storageAccountName = 'staika${uniqueSuffix}'
var keyVaultName = 'kv-aika-${uniqueSuffix}'

module managedIdentityModule './modules/identity/main.bicep' = {
  name: 'managed-identity-deployment'
  scope: developmentResourceGroup
  params: {
    identityName: identityName
    location: location
    resourceTags: resourceTags
  }
}

module storageModule './modules/storage/main.bicep' = {
  name: 'storage-deployment'
  scope: developmentResourceGroup
  params: {
    storageAccountName: storageAccountName
    location: location
    resourceTags: resourceTags
    principalId: managedIdentityModule.outputs.principalId
  }
}

module keyVaultModule './modules/key-vault/main.bicep' = {
  name: 'key-vault-deployment'
  scope: developmentResourceGroup
  params: {
    keyVaultName: keyVaultName
    location: location
    tenantId: tenant().tenantId
    resourceTags: resourceTags
  }
}

output managedIdentityName string = identityName
output storageName string = storageModule.outputs.storageAccountName
output vaultName string = keyVaultModule.outputs.keyVaultName
