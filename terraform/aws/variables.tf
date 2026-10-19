variable "project_name" {
  type    = string
  default = "repo2docker"
}

variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "key_name" {
  type        = string
  description = "Existing AWS EC2 key pair name."
}

variable "allowed_ssh_cidr" {
  type        = string
  description = "CIDR allowed to SSH into the instance. Use your public IP /32."
}

variable "allowed_jenkins_cidr" {
  type        = string
  description = "CIDR allowed to access Jenkins. Use your public IP /32 for lowest exposure."
}

variable "create_elastic_ip" {
  type        = bool
  default     = false
  description = "Set true only when you need a stable public IP. Public IPv4 addresses may cost money."
}

variable "root_volume_size" {
  type    = number
  default = 30
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.20.1.0/24"
}
