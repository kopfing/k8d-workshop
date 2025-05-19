# Kubernetes Workshop Environment

This is an environment for our Kubernetes and containerization workshops and also serves as a pre-workshop check. It is designed to help you prepare and ensure that everything is in place on your laptop to participate easily. Or if you just want to play around with kubernetes and containerization, this is a good starting point. 



## Prerequisites

### General

- **Laptop**: Make sure you have a laptop with at least 8GB of RAM and 4 CPU cores.
-  **Operating System**: Ensure you are using a supported operating system (Linux, macOS, or Windows).
-  **Internet Connection**: A stable internet connection is required for downloading tools and accessing online resources. Internet access without a proxy is recommended.
    - The local ports 80, 443 and 5000 should be available on your machine and not occupied by other services.

### Software ####
-  **Docker Desktop** (https://www.docker.com/get-started/): Install Docker Desktop. Make sure it is running and you can access it from the command line.
-  **Visual Studio Code** (https://code.visualstudio.com/) :  Install Visual Studio Code because we will use devcontainers for the workshop. If you are familiar with Devcontainers and your IDE supports them, you can use that instead.




## Installation Steps

Open Visual Studio Code and open the folder where you cloned this repository. You should see a pop-up asking if you want to reopen the folder in a container. Click "Reopen in Container". This will set up the development environment for the workshop.
This will take a few minutes as it downloads the necessary images and sets up the environment. Once it's done, you should see a terminal window open in Visual Studio Code.

All the necessary tools like k3d, kubectl, docker, etc are already installed in the devcontainer. 

### Create a k3d kubernetes cluster

```bash
# inside the devcontainer
# Create a k3d cluster with the configuration file
k3d cluster create --config k3d-config.yaml
```

### Build, push, and deploy the demo application

```bash
# inside the devcontainer

# Change to the demo directory
cd demo

# Build the demo application
docker build -t localhost:5000/helloapp:latest .

# Push the demo application to the local registry
docker push localhost:5000/helloapp:latest

# deploy the sample application
kubectl apply -f hello-world.yaml
```

## Check if everything is working

On your **local machine (laptop)** open a browser and go to the following URL:

```
http://hello.localhost
```

You should see a page with the text **"Hello World! Everything is working!"**

🎉 Congratulations! 👍 You have successfully set up the workshop environment and built, pushed and deployed a demo application to the k3d kubernetes cluster.

## Troubleshooting

* It might take a couple of seconds until the application is available on localhost. If you see a 404 error, wait a few seconds and try again.
* If waiting doesn't help check if you have **http**://localhost NOT http**s**. We are using an unsecured http 80 port for the demo application for simplicity.

## Cleanup

To delete the k3d cluster with the sample application, run the following command:

```bash
# inside the devcontainer
k3d cluster delete workshop
```

After that you would need to recreate it by following the steps above to run the demo application again.

After you closed visual studio code, you can also delete the docker container and that were created during the workshop, the name will start with vsc-k8s-workshop-*. This will free up space on your machine.


## Structure of the workshop environment

This workshop environment is designed to be easy to set up and use. It uses Docker and k3d to create a local kubernetes cluster and a local registry. The devcontainer is configured to use these tools and provides a consistent environment for the workshop.

### Objectives for this environment

- Easy to set up and use
- Behaves the same on Windows, Linux and MacOS
- As little as possible to install on your local machine

### Technology stack

The technology stack used in this workshop is
- **Docker**: The containerization platform used to create and run the devcontainer and the k3d cluster. 
- **K3d** (https://k3d.io/):  kubernetes in docker for local development and to provide a local registry
- **Mise** (https://mise.jdx.dev/): for dev tool management see mise.toml what tools are installed in the devcontainer
- **Visual Studio Code** (https://code.visualstudio.com/): for easy use with devcontainers (https://containers.dev/) to provide a consistent environment for the workshop.


### Docker/Kubernetes Registry

The k3d registry is provided as a docker container and therefore accessible **from the host machine AND from the devcontainer at localhost:5000**. This is important because docker only allows localhost to serve a registry that is unsecured (http). And because we want to have it easy for local development our registry created by k3d is unsecured. 

The reason why it is also accessible from the devcontainer via localhost is that the devcontainer forwards the port 5000 to the host machine, because it is defined in the devcontainer.json file. This is done by the following line in the devcontainer.json file:

```json
"forwardPorts": [5000]
```

The registry is also accessible **from the k3d cluster** but there it is called **myregistry:5000**. This is because k3d creates a docker network for the cluster and the registry is accessible from the cluster using the name myregistry.


### Kubernetes

The kubernetes cluster is created using k3d from within the devcontainer but uses the docker daemon of the host machine. So the devcontainer, the kubernetes cluster and the docker registry are all running on the same docker daemon on the host machine (=your development laptop) as siblings.

kubectl - the command line tool to interact with kubernetes cluster is already installed in the devcontainer. It is also configured to point to the k3d cluster that was created by the k3d command. This is done by the environment variable KUBECONFIG which is set to the location of the kubeconfig file that was created by k3d. This is done in the devcontainer.json file by the following line:

```json
  "containerEnv": {
    "KUBECONFIG": "${containerWorkspaceFolder}/kubeconfig_workshop"
  },
```

K3d uses this to create the `kubeconfig_workshop` file in the workspace folder of the devcontainer. This file is used by kubectl to connect to the k3d cluster it also acts as authentication. So for real clusters this should usually be treated as a secret and should not be shared. 

As soon as you create the k3d cluster with the command `k3d cluster create --config k3d-config.yaml` the kubeconfig file is created and kubectl is configured to use it. You can check this by running the following command in the devcontainer:

```bash
# inside the devcontainer
kubectl cluster-info
```

that should show something like this:

```bash
Kubernetes control plane is running at https://host.docker.internal:43207
CoreDNS is running at https://host.docker.internal:43207/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://host.docker.internal:43207/api/v1/namespaces/kube-system/services/https:metrics-server:https/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

The Cluster is configured in the `k3d-config.yaml` file. It is created with 1 server node (control plane) and 3 worker nodes. This is often overkill for local development but for the workshop this way we can simulate a real cluster behaviour with multiple nodes, node failures, and advanced node scheduling. The registry is also defined in the `k3d-config.yaml`.


# Contact
If you have any questions or issues, please contact us at [hello@cnc.io](mailto:hello@cnc.io) or open an issue on the GitHub repository. We are happy to help you and improve the workshop environment.