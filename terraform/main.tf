provider "kubernetes" {
  # This tells the provider to use the specified kubeconfig file.
  # Ensure the path is correct for your user in the VM.
  config_path = "~/.kube/config"

  # Optional: You can also explicitly specify context if needed, but not usually for k3s default.
  # config_context = "default"
}

resource "kubernetes_namespace" "data_namespace" {
  metadata {
    name = "data-processing"
    labels = {
      purpose = "data-lab"
    }
  }
}

output "data_namespace_name" {
  value = kubernetes_namespace.data_namespace.metadata[0].name
  description = "The name of the created Kubernetes namespace."
}