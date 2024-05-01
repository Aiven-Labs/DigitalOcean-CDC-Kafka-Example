variable "project" {
    description = "A name for identifying grouped services"
    default = "demo"
}

variable "region" {
    description = "The cloud where service will be created"
    default = "nyc1"
}

variable "api_token" {
    description = "The api token for the environment prod or dev"
}

variable "kafka_version" {
    description = "Kafka service machine types"
    default = "3.5"
}

variable "kafka_plan" {
    description = "Kafka service machine types"
    default = "db-s-2vcpu-2gb"
}

variable "kafka_topics" {
  description = "Kafka topics"  
  type    = set(string)
  default = ["weather", "postgres"]
}

variable "postgres_plan" {
    description = "Postgres service machine types"
    default = "db-s-1vcpu-1gb"
}

variable "postgres_version" {
    description = "Postgres service version"
    default = "15"
}

variable "postgres_databases" {
  description = "Postgres databases names"  
  type    = set(string)
  default = ["pipeline"]
}