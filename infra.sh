#!/usr/bin/env bash
set -euo pipefail

if [ -z ${SSH_AUTH_SOCK+x} ]; then
    echo "SSH_AUTH_SOCK is undefined" >&2
    echo "you need a ssh-agent to deploy via $0" >&2
    exit 1
fi

env="$1"; shift
stack="$1"; shift

export PASSWORD_STORE_DIR=~/.pass/alt
export PASSWORD_STORE_GIT=~/.pass/alt

(umask 0077 && pass ansible/vault-pass/$env > ./.pass-$env)
mkdir -p .tmp
# extract robot_key
rm -f .tmp/robot_key; pass infra/robot_key > .tmp/robot_key
chmod 400 .tmp/robot_key
# add robot_key to the ssh agent
ssh-add .tmp/robot_key

touch .tmp/ssh_config
ANSIBLE_FORCE_COLOR=1 \
 ansible-playbook -e env_name=$env -e stack_name=$stack --vault-id $env@.pass-$env $@ provision.yml | tee $env-$stack-provision.log
if [[ -f ${env}-${stack}-apps.yml ]]; then
 ANSIBLE_FORCE_COLOR=1 \
  ansible-playbook -i .tmp/ansible_hosts -e env_name=$env -e stack_name=$stack --vault-id $env@.pass-$env $@ ${env}-${stack}-apps.yml | tee $env-$stack-apps.log
else
 echo "playbook ${env}-${stack}-apps.yml was not found" >2
 exit 1
fi
