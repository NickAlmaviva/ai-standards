# Usare ai-standards in CI / agenti automatici

Nelle pipeline dei microservizi non serve installare nulla nei repository: basta clonare ai-standards nel job e impostare le variabili.

```yaml
# .gitlab-ci.yml di un microservizio (esempio)
ai-review:
  image: node:22
  variables:
    AI_STD_REF: "v1.0.0"
  before_script:
    - git clone --depth 1 --branch "$AI_STD_REF" https://gitlab-ci-token:${CI_JOB_TOKEN}@git.tuaazienda.it/platform/ai-standards.git /opt/ai-standards
    - sed "s|__AI_STANDARDS_HOME__|/opt/ai-standards|g" /opt/ai-standards/config/kilo.template.jsonc > /tmp/kilo.jsonc
    - export KILO_CONFIG=/tmp/kilo.jsonc KILO_CONFIG_DIR=/opt/ai-standards
    - npm i -g @kilocode/cli
  script:
    - kilo run "/review"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Per centralizzare anche questo job, pubblicalo come template in ai-standards (es. `ci/templates/ai-review.yml`) e includilo nei progetti con `include: project:`.
