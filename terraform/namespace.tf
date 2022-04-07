locals {
  namespace_list = toset(["qa", "staging"])
}
provider "kubernetes" {
  config_context = var.kubectl_config_context_name
  config_path    = var.kubectl_config_path
}
module "create_namespace" {
  for_each    = local.namespace_list
  source      = "./modules/aws-k8s-ns"
  name        = "${each.key}"
  labels      = var.labels
  annotations = var.annotations
}


