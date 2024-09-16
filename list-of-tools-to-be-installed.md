=========================================================================================================================================
# List of Tools to be Installed
=========================================================================================================================================
1. For Editor - Visual Studio Code 
   https://code.visualstudio.com/

2. Get a GitHub 
   https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home

3. Get a Docker Hub Account 
   https://hub.docker.com/

4. For Java JDK
   https://www.oracle.com/java/technologies/downloads/#jdk17-windows

5. For Python
   https://www.python.org/

6. Jupyter Lab
   $ pip install jupyterlab
   $ pip install notebook

7. Docker Desktop for Windows
   https://www.docker.com/

8. Install Pandas
   $ pip install pandas

9. Install Sckit Learn
   $ pip install scikit-learn

10. Install Joblib
   $ pip install joblib

11. AWS CLI
    https://awscli.amazonaws.com/AWSCLIV2.msi

   Note: 
   - Using IAM , create 'mlapp' user and associate AWS S3FullAccess Policy to user(mlapp)
   - Create IAM credentials for same mlapp user (AccessKeyID,SecretAccessKeyID)
   - Permissions/Policy: AmazonEC2ContainerRegistryFullAccess,AmazonS3FullAccess

    $ aws --version   # Verify AWS CLI Installation
    $ aws configure   # Configure AWS CLI to Allow programatic access to AWS account
       - AccessKeyID
       - SecretAccessKeyID
       - region: us-east-2
       - output: json

13. Install Kubernetes 
    https://kind.sigs.k8s.io/
    https://kind.sigs.k8s.io/docs/user/quick-start#installation

    $ curl.exe -Lo kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.24.0/kind-windows-amd64
    $ Move-Item .\kind-windows-amd64.exe c:\some-dir-in-your-PATH\kind.exe

    Note: SET PATH =$PATH: C:\kind\kind.exe

    To Create Kubernetes Cluster 
    $ kind create cluster --name main-k8s-kind-cluster


14. Install Kubectl (CLI method and Clinet to connect with Kubernetes)
    URL: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
     $ curl.exe -LO "https://dl.k8s.io/release/v1.31.0/bin/windows/amd64/kubectl.exe"

    - Note: SET PATH =$PATH: C:\kubectl\kubectl.exe

15. Install PySpark
    $ pip install pyspark
   
16. Install MLFLow
    $ pip install mlflow

17. To Start MLFlow
    $ mlflow ui --port 5000    # Open http://localhost:5000

    In another cmd, run
    $ py app.py
   
###################################
# List of Docker Commands
###################################

$ docker images
$ docker ps -a
$ docker build -t <name-of-the-docker-image> .
$ docker run --name <name-of-the-docker-image>

# List containers running:
$ docker ps -a

# Stop container:
$ docker stop <container id>

$ docker images
$ docker login
$ docker rmi <<image-id>>
$ docker rm $(docker ps -a)
$ docker rmi $(docker images -a -q)
$ docker push <<image-id>>
$ docker push ssadcloud/mlapp:latest

###################################
# CI/CD Using Jenkins
###################################
Name of the S3 Bucket: mlapp-models-storage-artifacts
URI of the S3 Bucket:  s3://mlapp-models-storage-artifacts
AWS S3 CLI Command for File Upload:
      $ aws s3 cp <<artifact-object-name>> <<Name of the S3 Bucket/Name of the object>>

Job1: 01_mlapp_build_docker_image
      This Jenkins job is designated to pull the ML mode from GitHub , and build Source Code and generate (.joblib) and upload to AWS S3 buckets, and build Docker Images for MLApp
         $ cd mlops-predict-rental-price\
         $ aws s3 cp rental_price_model.joblib s3://mlapp-models-storage-artifacts/mlapp.joblib
         $ docker build . -t ssadcloud/mlapp
         $ docker push ssadcloud/mlapp

Job2: 02_mlapp_push_docker_image_registry
      This job to push image built from 01_mlapp_build_docker_image into Container Registry

        $ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 932589472370.dkr.ecr.us-east-2.amazonaws.com
        $ docker build -t mlapp-ecr .
        $ docker tag mlapp-ecr:latest 932589472370.dkr.ecr.us-east-2.amazonaws.com/mlapp-ecr:latest
        $ docker push 932589472370.dkr.ecr.us-east-2.amazonaws.com/mlapp-ecr:latest


Job3: 03_mlapp_deploy_to_k8s
         #Task1
         $ cd mlops-predict-rental-price/k8s-config-files
         $ kubectl delete -f mlapp-service.yaml
         $ kubectl delete -f mlapp-deployment.yaml

         # Task2
         $ cd mlops-predict-rental-price/k8s-config-files
         $ kubectl apply -f mlapp-deployment.yaml
         $ kubectl apply -f mlapp-service.yaml

========================================================================================================================================
# What is Kubeflow Pipelines?
========================================================================================================================================
- Links : https://www.kubeflow.org/docs/components/pipelines/overview/

- Kubeflow Pipelines (KFP) is a platform for building and deploying portable and scalable machine learning (ML) workflows using Docker containers.

 - Kubeflow Pipelines - Compnents and Pipelines

 - Component: 
   - A component is a remote function definition
   - It specifies inputs, has user-defined logic in its body, and can create outputs
   - When the component template is instantiated with input parameters, we call it a task


###################################
# Kind Commands
###################################

$ curl.exe -Lo kind-windows-amd64.exe https://kind.sigs.k8s.io/dl/v0.8.1/kind-windows-amd64
$ Move-Item .\kind-windows-amd64.exe c:\kind\kind.exe

$ kind
$ kind create cluster --name main-kind-k8s-cluster
$ kind get clusters
$ kind delete cluster main-kind-k8s-cluster

###################################
# List of Kuberenetes Commands
###################################
 - kubectl get nodes
 - kubectl get pods
 - kubectl get pods -A
 - kubectl get svc -A
 - kubectl apply -f mlapp-deployment.yaml
 - kubectl apply -f mlapp-service.yaml
 - kubectl delete -f mlapp-deployment
 - kubectl port-forward svc/rental-price-predictor-service 5000:5000

###################################
# Deploying Kubeflow Pipelines 
###################################
$ export PIPELINE_VERSION=2.2.0
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
$ kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
$ kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION"


$ kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
Open your browser and resolve http://localhost:8080


# curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"rooms_count": 2, "area_in_sqft": 1000}'



========================================================================================================================================
# DEPLOYMENT ON CLOUD
========================================================================================================================================
=================================================================================================
# STEPS TO BE FOLLOWED - TO Implement AWS EKS
=================================================================================================
#  AWS Key and Security Groups
    - Create an KeyPair, and store in Vault/S3
    - Create an Security Group
    - Recommonded ports with Inbound Security - SSH(22),HTTP(80),HTTPS(443) and Custom ports - 8080 & 8888

# Create Ubuntu environment
    To get started with automated deployment, you must have a Ubuntu environment using one of the following methods:
    - Launch a Ubuntu-based Amazon EC2 instance with t2.large(Recommended)
    - Recommend to use a Ubuntu AWS Deep Learning AMI (DLAMI)
    - AWS Deep Learning Base AMI (Ubuntu 20.04) for your EC2 instance
        Note: Ubuntu 18.04 Support is discontinued

# Tools Installation:
  
  # Install git:
    $ sudo apt-get update -y
    $ sudo apt-get install git -y
  
  # Install Juypter:
    $ pip install jupyter 
    $ jupyter notebook --generate-config
    $ nano .jupyter/jupyter_notebook_config.py

    # The IP address the notebook server will listen on. 
        c.NotebookApp.ip = '0.0.0.0' # default value is 'localhost'
        c.NotebookApp.open_browser = False # default value is True
    
    $ jupyter --version
    $ jupyter lab --allow-root

    Note: 
    - Check Security Groups for Inbount Port - Allowed port for 8888
    - You can also run in venv
       $ virtualenv venv
       $ source venv/bin/activate
       $ jupyter lab --allow-root

# Helm Installation:
https://helm.sh/docs/intro/install/

For Linux: 
    $ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    $ chmod 700 get_helm.sh
    $ ./get_helm.sh

For Windows: 
    $ winget install Helm.Helm
    
# Download Kubeflow Manifests
    $ export KUBEFLOW_RELEASE_VERSION=v1.7.0
    $ export AWS_RELEASE_VERSION=v1.7.0-aws-b1.0.3
    $ git clone https://github.com/awslabs/kubeflow-manifests.git && cd kubeflow-manifests
    $ git checkout ${AWS_RELEASE_VERSION}
    $ git clone --branch ${KUBEFLOW_RELEASE_VERSION} https://github.com/kubeflow/manifests.git upstream
    $ make install-tools
    $ apt-get install python -y
    $ alias python=python3.11

# Configure AWS Account
    $ aws configure
        # AWS Access Key ID [None]: <enter access key id>
        # AWS Secret Access Key [None]: <enter secret access key>
        # Default region name [None]: <AWS region>
        # Default output format [None]: json

# KServe Installation:
    $ curl -s "https://raw.githubusercontent.com/kserve/kserve/release-0.12/hack/quick_install.sh" | bash
    $ kubectl create namespace kserve-test

# KUBECTL INSTALLATION
   $ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# EKSCTL INSTALLATION
   $ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
   $ sudo mv /tmp/eksctl /usr/local/bin
   $ eksctl version
   $ eksctl create cluster --name sigmaEKS-Cluster --region us-east-2 --nodegroup-name sigmaEKS-Cluster-NG --node-type t2.micro --nodes 2 --nodes-min 2 --nodes-max 5 --ssh-access --ssh-public-key kp --managed


########################################################################
CI/CD Using Jenkins
########################################################################

Task-1:
# Run Python script and save output
python train_model.py > output.txt


Task-2:
# Extract run_id and remove any extra carriage return characters
RUN_ID=$(grep 'MLflow run completed with ID:' output.txt | awk '{print $NF}' | tr -d '\r')

# Print RUN_ID to verify
echo "Extracted RUN_ID: $RUN_ID"

# Build Docker image using the extracted run_id
mlflow models build-docker -m runs:/${RUN_ID}/model -n ssadcloud/mlapp --enable-mlserver
docker push ssadcloud/mlapp:latest
    

Task-3:
Deploy ML Model Using mlapp-deployment.yaml


# To Delete Cluster
	eksctl delete cluster --name <<cluster-name>>
   eksctl delete cluster --name sigmaEKS-Cluster --region us-east-2