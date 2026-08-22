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
