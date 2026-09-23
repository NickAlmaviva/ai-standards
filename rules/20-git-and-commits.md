# Git e commit

- Messaggi di commit in formato Conventional Commits: `type(scope): descrizione` (feat, fix, refactor, test, docs, chore, ci).
- Lo scope è il nome del microservizio o del SAE, oppure il modulo toccato.
- Un commit = una modifica logica. Non mescolare refactoring e feature.
- Non eseguire `git push`, `git rebase` o `git reset --hard` senza richiesta esplicita.
- Non usare `git stash` per spostare lavoro tra worktree.
