#!/usr/bin/env bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y ca-certificates curl gnupg git unzip apt-transport-https software-properties-common

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list

curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" \
  > /etc/apt/sources.list.d/jenkins.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin openjdk-17-jre jenkins

usermod -aG docker ubuntu
usermod -aG docker jenkins
systemctl enable --now docker
systemctl enable --now jenkins

curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--write-kubeconfig-mode=644" sh -

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

mkdir -p /home/ubuntu/.kube
cp /etc/rancher/k3s/k3s.yaml /home/ubuntu/.kube/config
chown -R ubuntu:ubuntu /home/ubuntu/.kube

kubectl create namespace monitoring || true
kubectl create namespace repo2docker || true

cat >/home/ubuntu/README-FIRST.txt <<'EOF'
Repo2Docker host is ready.

Useful commands:
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  kubectl get nodes
  helm version
  docker version

Install monitoring:
  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
  helm repo update
EOF

chown ubuntu:ubuntu /home/ubuntu/README-FIRST.txt
