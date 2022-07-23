import os
from google.oauth2 import service_account
from google.cloud import aiplatform
from google.cloud import artifactregistry_v1

#variables
PATH_TO_KEY=os.environ.get('UPLOADER_SERVICE_ACCOUNT')           #path to json key file
PROJECT='total-thinker-356217'                                  #project name
LOCATION='us-west2'                                             #region of your gcp project
GAR_REPO='images'                                               #name of google artifact registry repository
DOCKER_IMAGE='dalle-nano:latest'                                #name of image in gar repository
MODEL_DISPLAY_NAME='beta'                                       #name of model once imported
PREDICT_ROUTE='/prediction'                                     #predict route for docker image
HEALTH_ROUTE='/health'                                          #health route for docker image
PORTS=[80]                                                      #exposed docker image ports
ENDPOINT_MACHINE_TYPE='n1-standard-2'                           #machine type for endpoint

#all other parameters can be edited manually in the code body

my_credentials = service_account.Credentials.from_service_account_file(
    PATH_TO_KEY)

scoped_credentials = my_credentials.with_scopes(
    ['https://www.googleapis.com/auth/cloud-platform'])

print(my_credentials)

aiplatform.init(
    project=PROJECT,
    location=LOCATION,
    credentials=my_credentials
)

client=artifactregistry_v1.ArtifactRegistryClient(credentials=my_credentials)
print(client)

docker_path=client.docker_image_path(project=PROJECT, location=LOCATION, repository=GAR_REPO, docker_image=DOCKER_IMAGE)

print(docker_path)

model=aiplatform.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    serving_container_image_uri= f'{LOCATION}-docker.pkg.dev/{PROJECT}/{GAR_REPO}/{DOCKER_IMAGE}',
    serving_container_predict_route=PREDICT_ROUTE,
    serving_container_health_route=HEALTH_ROUTE,
    serving_container_ports=PORTS
)
print(model.display_name + ' created')

endpoint=model.deploy(machine_type=ENDPOINT_MACHINE_TYPE,
    min_replica_count=1
)
print(endpoint)
