resource "digitalocean_database_cluster" "postgres-service" {
  name       = "${var.project}-postgres"
  engine     = "pg"
  version    = var.postgres_version
  size       = var.postgres_plan
  region     = var.region
  node_count = 1
  tags       = ["${var.project}"]
}

resource "digitalocean_database_db" "postgres-service-database" {
  for_each = toset(var.postgres_databases)

  cluster_id = digitalocean_database_cluster.postgres-service.id
  name       = each.value
}

output postgres_uuid {
  value = digitalocean_database_cluster.postgres-service.id
}