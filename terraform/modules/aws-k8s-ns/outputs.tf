output "name" {
  description = "The name of the created namespace."
  value       = kubernetes_namespace.namespace.id
}