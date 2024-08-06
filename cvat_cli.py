from cvat_sdk import make_client

with make_client('http://43.204.240.199', port='8080', credentials=('cylian', 'draConian1')) as client:
    client.organization_slug = "treex"
    print(client.jobs)
