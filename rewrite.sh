#!/bin/bash
git filter-branch -f --env-filter '
    export GIT_AUTHOR_NAME="Somyasharmatech"
    export GIT_AUTHOR_EMAIL="114328620+Somyasharmatech@users.noreply.github.com"
    export GIT_COMMITTER_NAME="Somyasharmatech"
    export GIT_COMMITTER_EMAIL="114328620+Somyasharmatech@users.noreply.github.com"
' HEAD
git push -f origin feature/initial-implementation
