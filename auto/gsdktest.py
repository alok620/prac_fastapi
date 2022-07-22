from google.oauth2 import service_account
from google.cloud import aiplatform
from google.cloud import artifactregistry_v1

my_credentials = service_account.Credentials.from_service_account_file(
    './keys/total-thinker-356217-b007156315ed.json')

scoped_credentials = my_credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

print(my_credentials)

aiplatform.init(
    project='total-thinker-356217',
    location='us-west2',
    credentials=my_credentials
)

client=artifactregistry_v1.ArtifactRegistryClient(credentials=my_credentials)
print(client)

docker_path=client.docker_image_path(project='total-thinker-356217', location='us-west2', repository='images', docker_image='dalle-nano:latest')

print(docker_path)

model=aiplatform.Model.upload(
    display_name='beta',
    serving_container_image_uri='us-west2-docker.pkg.dev/total-thinker-356217/images/dalle-nano:latest',
    serving_container_predict_route='/prediction',
    serving_container_health_route='/health'
)


