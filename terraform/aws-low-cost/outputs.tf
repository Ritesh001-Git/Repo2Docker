output "instance_id" {
  value = aws_instance.repo2docker.id
}

output "public_ip" {
  value = var.create_elastic_ip ? aws_eip.repo2docker[0].public_ip : aws_instance.repo2docker.public_ip
}

output "ssh_command" {
  value = "ssh ubuntu@${var.create_elastic_ip ? aws_eip.repo2docker[0].public_ip : aws_instance.repo2docker.public_ip}"
}

output "jenkins_url" {
  value = "http://${var.create_elastic_ip ? aws_eip.repo2docker[0].public_ip : aws_instance.repo2docker.public_ip}:8080"
}

output "repo2docker_url" {
  value = "http://${var.create_elastic_ip ? aws_eip.repo2docker[0].public_ip : aws_instance.repo2docker.public_ip}"
}
