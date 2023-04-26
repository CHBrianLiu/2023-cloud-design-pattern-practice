param rgLocation = resourceGroup().location

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-12-01' = {
  name: 'briancloudpatternpractice'
  location: rgLocation
  sku: {
    name: 'basic'
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: 'brianasyncreqreply'
  location: rgLocation
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'

  resource blobService 'blobServices' = {
    name: 'default'

    resource blobContainer 'containers' = {
      name: 'picturegeneration'
    }
  }

  resource queueService 'queueServices' = {
    name: 'default'

    resource queue 'queues' = {
      name: 'picturegeneration'
    }
  }
}