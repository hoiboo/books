#!/bin/bash

# 定义要推送的本地分支
local_branch="dev"

# 定义要推送的远程仓库和分支
remotes=(
    "origin dev"
    "gitlab dev"
)

# 循环推送
for remote in "${remotes[@]}"; do
    IFS=' ' read -r -a remote_info <<< "$remote"
    remote_name="${remote_info[0]}"
    remote_branch="${remote_info[1]}"
    git push "$remote_name" "$local_branch:$remote_branch"
done