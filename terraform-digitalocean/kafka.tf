resource "digitalocean_database_cluster" "kafka-service" {
  name       = "${var.project}-kafka"
  engine     = "kafka"
  version    = var.kafka_version
  size       = var.kafka_plan
  region     = var.region
  node_count = 3
  tags       = ["${var.project}"]
}

resource "digitalocean_database_kafka_topic" "kafka-service-topic" {
  for_each = toset(var.kafka_topics)

  cluster_id         = digitalocean_database_cluster.kafka-service.id
  name               = each.value
  partition_count    = 3
  replication_factor = 2
  config {
    cleanup_policy   = "delete"
  }
}

output kafka_uuid {
  value = digitalocean_database_cluster.kafka-service.id
}