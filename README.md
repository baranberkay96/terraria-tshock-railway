# Deploy and Host Terraria TShock Server with Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/terraria-tshock-server?referralCode=20H68q)

Run a password-protected Terraria 1.4.5.8 world using TShock 6.2.1. This community template exposes the game through Railway's TCP proxy and stores worlds, TShock accounts, configuration, logs and plugins on a persistent volume. The generated server password protects joining; the REST API is disabled.

## About Hosting Terraria TShock Server

TShock adds player accounts, permissions, moderation commands and plugin support to a Terraria dedicated server. This deployment runs one server and one world with eight player slots by default. First boot generates a small classic world, which can take several minutes. A private HTTP readiness endpoint becomes healthy once the game port accepts connections. The launcher runs TShock without root privileges and requests a save before stopping on redeploy. Use a matching Terraria 1.4.5.8 client. This is a TShock server, with no tModLoader modpack or promised console/mobile cross-play compatibility.

## Common Use Cases

- A private Terraria world for friends.
- A cooperative progression server with persistent saves.
- A moderated community using TShock accounts and permissions.
- Testing compatible TShock plugins in a separate environment.

## Dependencies for Terraria TShock Server Hosting

- A Railway account and a volume-capable plan; Hobby is recommended.
- A Terraria 1.4.5.8 desktop client for each player.
- At least 1 GiB available RAM for a small world; allow 1–2 GiB or more for active play.

### Deployment Dependencies

- [TShock release and compatibility notes](https://github.com/Pryaxis/TShock/releases/tag/v6.2.1)
- [TShock documentation](https://tshock.readme.io/docs)
- [Railway TCP proxies](https://docs.railway.com/guides/public-networking#tcp-proxying)
- [Railway volumes](https://docs.railway.com/guides/volumes)

### Implementation Details

| Service | Purpose | Persistence | Public access |
| --- | --- | --- | --- |
| Terraria | TShock 6.2.1 / Terraria 1.4.5.8 | `/data` volume | TCP proxy to game port 7777 |

After deployment, find the TCP proxy hostname and allocated external port in the Terraria service's Networking settings. In Terraria choose Multiplayer → Join via IP, enter that hostname, then the external port, then the `SERVER_PASSWORD` from Railway Variables. The proxy port usually differs from 7777. Do not enter an HTTP URL.

For the first administrator, read TShock's setup code from the private deployment logs, join with the server password, then follow [TShock's first administrator guide](https://tshock.readme.io/docs/becoming-an-admin). Use `/setup {code}`, `/user add {name} {strong-password} superadmin`, then `/login {name} {strong-password}`. Complete setup before sharing access. Keep deployment logs private; they contain the initial setup code. No public REST or web administrator endpoint is created.

`WORLD_SIZE` and `DIFFICULTY` apply only when creating a new world. The existing world remains `/data/worlds/world.wld` across redeploys. Back up the entire volume before replacing worlds or upgrading. Accounts and settings live in `/data/tshock`; optional compatible plugin DLLs belong in `/data/plugins`. Stop the service before restoring files. TShock saves automatically and on graceful shutdown. Railway volume backups are recommended because the volume itself is not an off-site backup.

Invalid numeric or world name values fall back to documented defaults. Invalid passwords preserve a valid stored password; on a fresh volume they lock access with an undisclosed random password. Fix `SERVER_PASSWORD` and redeploy to restore access. Security settings, game port, autosave and REST disabling are enforced on every boot; other TShock configuration survives.

Keep one replica per world. Increase service RAM/CPU and `MAX_PLAYERS` to scale a world, or deploy a separate service and volume for another world. Large worlds and plugins need more memory. Free 0.5 GiB is not supported; Trial's 1 GiB cap may be too tight for generation or active play.

The Dockerfile pins the TShock release ZIP with SHA-256 and the .NET 9.0.23 image with its manifest digest. Upgrade by changing the release URL, checksum and compatible runtime together, rebuilding, and testing a volume backup before upgrading the live world.

### Why Deploy Terraria TShock Server on Railway?

Railway provides a stable TCP endpoint, persistent storage, deployment logs and adjustable resources for an always available Terraria world. Manage one service and keep backups of the world and TShock account database before upgrades.
