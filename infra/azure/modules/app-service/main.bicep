@description('Name of the Linux App Service plan.')
param appServicePlanName string

@description('Globally unique name of the web application.')
param webAppName string

@description('Azure region for the application.')
param location string

@description('Governance tags applied to the resources.')
param resourceTags object

@description('Resource ID of the user-assigned managed identity.')
param managedIdentityResourceId string

@description('Client ID of the user-assigned managed identity.')
param managedIdentityClientId string

@description('Azure Blob Storage account URL.')
param storageAccountUrl string

@description('Private container containing governed documents.')
param storageContainerName string = 'knowledge-documents'

resource appServicePlan 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: appServicePlanName
  location: location
  tags: resourceTags
  sku: {
    name: 'F1'
    tier: 'Free'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2024-11-01' = {
  name: webAppName
  location: location
  tags: resourceTags
  kind: 'app,linux'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${managedIdentityResourceId}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    clientAffinityEnabled: false
    publicNetworkAccess: 'Enabled'
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.14'
      alwaysOn: false
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
      http20Enabled: true
      appCommandLine: 'python -m uvicorn src.api:app --host 0.0.0.0 --port 8000'
      appSettings: [
        {
          name: 'APP_ENVIRONMENT'
          value: 'production'
        }
        {
          name: 'IDENTITY_MODE'
          value: 'entra'
        }
        {
          name: 'DOCUMENT_REPOSITORY'
          value: 'azure'
        }
        {
          name: 'AZURE_STORAGE_ACCOUNT_URL'
          value: storageAccountUrl
        }
        {
          name: 'AZURE_STORAGE_CONTAINER'
          value: storageContainerName
        }
        {
          name: 'AZURE_MANAGED_IDENTITY_CLIENT_ID'
          value: managedIdentityClientId
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'ENABLE_ORYX_BUILD'
          value: 'true'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
  }
}

output appServicePlanName string = appServicePlan.name
output webAppName string = webApp.name
output defaultHostName string = webApp.properties.defaultHostName
