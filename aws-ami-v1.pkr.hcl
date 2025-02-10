# If you have your default VPC available then use it. 

# packer puglin for AWS 
# https://www.packer.io/plugins/builders/amazon 
packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

# which ami to use as the base and where to save it
source "amazon-ebs" "amazon-linux" {
  
  region          = "ap-south-1"
  ami_name        = "ami-version-1.0.1-{{timestamp}}"

 ## for AMI creation u need an ec2 instance , that instance is t2 micro

  instance_type   = "t2.micro"

  source_ami      = "ami-0aee0743bf2e81172"
  
  ssh_username    = "ec2-user"
  
  ami_users       =  ["746669221855","588738612311"]

  ami_regions     = [
                      "ap-south-1",
                      "ap-southeast-1"
                    ]
}

# what to install, configure and file to copy/execute
build {
  name = "hq-packer"
  sources = [
    "source.amazon-ebs.amazon-linux"
  ]

  provisioner "file" {
  source = "provisioner.sh"
  destination = "/tmp/provisioner.sh"
}

  provisioner "shell" {
    inline = ["chmod a+x /tmp/provisioner.sh"]
  }
  
  provisioner "shell" {
    inline = [ "ls -la /tmp"]
  }
  
    provisioner "shell" {
    inline = [ "pwd"]
  }
  
  provisioner "shell" {
    inline = [ "cat /tmp/provisioner.sh"]
  }

  provisioner "shell" {
    inline = ["/bin/bash -x /tmp/provisioner.sh"]
  }
}
