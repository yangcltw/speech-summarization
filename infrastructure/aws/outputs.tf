output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance"
  value       = aws_instance.web.public_ip
}
