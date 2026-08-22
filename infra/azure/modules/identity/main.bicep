@description('Name of the user-assigned managed identity.')
param identityName string

@description('Azure region for the identity.')
param location string

@description('Governance tags applied to the identity.')
param resourceTags object

resource managedIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  name: identityName
  location: location
  tags: resourceTags
}

output identityId string = managedIdentity.id
output principalId string = managedIdentity.properties.principalId
output clientId string = managedIdentity.properties.clientId
