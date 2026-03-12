# Runbook Destino (Laptop B / WSL)

Guia de instalacion para preparar el nodo destino que recibira tareas remotas por SSH.

## Objetivo

Dejar WSL de Laptop B listo para que `agent-A` (Laptop A) ejecute comandos remotos de forma segura y auditada.

## Prerrequisitos

- WSL2 operativo en Laptop B.
- Usuario Linux con permisos `sudo`.
- Conectividad de red entre Laptop A y Laptop B.
- (Opcional) Docker instalado si se ejecutaran playbooks de servicios.

## Paso 1: clonar repo en WSL destino

```bash
git clone <URL_DEL_REPO> wsl-ssh-agents
cd wsl-ssh-agents
```

## Paso 2: instalar y configurar SSH server

```bash
bash scripts/ssh/bootstrap_destino.sh
```

Este script:

- instala `openssh-server`
- crea drop-in `/etc/ssh/sshd_config.d/opencode.conf`
- reinicia servicio `ssh`
- muestra pistas de red (hostname + IP)

## Paso 3: validar que SSH escucha en destino

```bash
sudo ss -tlnp | grep ':22'
```

Resultado esperado: puerto `22` en estado `LISTEN` con proceso `sshd`.

## Paso 4: permitir autenticacion por llave desde Laptop A

Desde Laptop A, correr:

```bash
bash scripts/ssh/bootstrap_busqueda.sh laptop-b user@IP_DESTINO
```

Este paso copia la llave publica al destino y prueba acceso por alias.

## Paso 5: prueba de acceso remoto end-to-end

Desde Laptop A:

```bash
ssh laptop-b "hostname && uname -a"
```

Resultado esperado: nombre de host y kernel remoto sin pedir password.

## Paso 6: consideraciones WSL (IP dinamica)

En WSL2, la IP del entorno Linux puede cambiar al reiniciar. Si ocurre:

- usar modo red mirrored en WSL (si disponible), o
- configurar forwarding desde Windows host hacia WSL (portproxy)

## Hardening minimo recomendado

- `PermitRootLogin no`
- `PubkeyAuthentication yes`
- `PasswordAuthentication yes` (temporal), luego migrar a `no`
- `MaxAuthTries 3`

## Troubleshooting rapido

- `ssh: connection refused`: servicio `sshd` no levantado o IP/puerto incorrecto.
- `Permission denied (publickey)`: revisar `~/.ssh/authorized_keys` en destino.
- timeout: revisar firewall/reglas de red entre laptops.

## Criterio de salida (done)

- Laptop A conecta a Laptop B por alias SSH.
- Login por llave funciona.
- `agent-A` puede ejecutar tareas remotas contra `laptop-b`.
