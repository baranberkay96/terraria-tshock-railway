# Terraria TShock Server — Railway composer specification

Verified against official stable TShock **6.2.1** for **Terraria 1.4.5.8** on **2026-11-21**. Service repository: `baranberkay96/terraria-tshock-railway`, root `/services/tshock`. The deployable repository is the contents of this `template/` directory.

## Services and networking

Create one `Terraria` service from the repository root above, build its Dockerfile for linux/amd64, and mount one Railway volume at `/data`. Add a TCP proxy targeting **7777**. Do not create a public HTTP domain or proxy port 7878. Set the healthcheck to `/health`, timeout 1200 seconds, `PORT=8080`, restart policy `ALWAYS`, one replica. Set deployment draining to 180 seconds and overlap to zero. This application does not require UDP.

Apply all variables and descriptions from `template.json`. `SERVER_PASSWORD` is `${{secret(32)}}`; no user inputs or external API keys are needed for the default deployment. Read the generated password from Railway Variables, then connect a matching Terraria client to the assigned TCP proxy hostname and external port. TShock's setup code is shown in private logs for first administrator setup. The game password protects access before that setup is complete. REST, UUID login and login-before-join password bypass are disabled on every boot.

## Pinned artifacts

- TShock release ZIP: `https://github.com/Pryaxis/TShock/releases/download/v6.2.1/TShock-6.2.1-for-Terraria-1.4.5.8-linux-x64-Release.zip`.
- SHA-256: `deb9189acbdbd2ee0f0a06fffe15358033859a4ba842b22f79a84bda68600105`, matching GitHub's asset digest and downloaded bytes.
- Base image: `mcr.microsoft.com/dotnet/runtime:9.0.23-bookworm-slim@sha256:aa21f09894760dc31b207e29256fcf9a74fb14da4384b81ba49b1f038604087f`.
- Upstream source and licensing references are recorded in `NOTICE.md`. No `VOLUME` instruction is present.

## Persistence and recovery

World `/data/worlds/world.wld`; TShock settings, SQLite accounts/permissions, backups and logs `/data/tshock`; additional plugins `/data/plugins`. The launcher's security-managed settings are enforced on boot; other configuration persists. Stop the service and back up the whole volume before changing versions, adding plugins or restoring a world. Small worlds are the default; size and difficulty changes do not overwrite an existing world. SIGTERM requests the console `exit` command to save the world, waits up to 150 seconds, then terminates only if necessary.

Malformed numeric values and world names fall back to defaults. An invalid password retains the previous valid stored password; a fresh volume receives an undisclosed random password and a log instruction to set `SERVER_PASSWORD` and redeploy. This avoids public unauthenticated joining and avoids a crash loop. A malformed config is retained as `config.invalid-*.json` before restoring safe defaults.

## Improvements over market templates

Marketplace descriptions for XavTo's `terraria-dedicated-server` and lNamelessl's `terraria-tshock` were inspected by the coordinating agent. No source or listing text was copied. This independent package keeps the practical single-service TCP world design and adds checksum-pinned TShock artifacts, a digest-pinned compatible runtime, a mandatory generated game password, disabled REST, disabled password-bypassing UUID/prejoin logins, consistent volume paths, graceful save on termination, and safe form-input fallbacks. No nonexistent Terraria EULA environment variable or acceptance flow is introduced.

## Resource estimate

| Service | Estimated idle RAM / CPU | Estimated typical RAM / CPU | Storage |
| --- | --- | --- | --- |
| Terraria | 0.4–0.7 GiB / 0.03–0.10 vCPU | 0.7–1.5 GiB / 0.1–0.5 vCPU | 1–5 GiB volume; world size, backups and plugins affect use |

At RAM $10/GiB-month, CPU $20/vCPU-month and volume $0.15/GiB-month: idle estimate **$4.75–$9.75/month** with a 1–5 GiB volume; typical estimate **$9.15–$25.75/month**, plus network egress and any plan minimum. These are estimates, not fixed bills. Recommend Hobby and 1–2 GiB available RAM for small worlds. Free's 0.5 GiB cap is unsupported. Trial is capped at 1 GiB/service and may be tight during generation or active play. Hobby volumes are limited to 5 GiB/service by default. Larger worlds, players and plugins require higher resources. Local measured results are recorded in `TEST-RESULTS.md`.

## Verification checklist

- Build the Dockerfile using `docker build --platform linux/amd64 services/tshock`.
- Run bootstrap unit tests: `python3 -m unittest discover -s services/tshock/tests -v`.
- Wait for world generation and private `/health` HTTP 200; no public HTTP domain should exist.
- Join through the external TCP proxy using Terraria 1.4.5.8 and the generated password. Confirm a wrong or empty password is rejected.
- Complete administrator setup from private logs, create an account and verify in-game login.
- Verify REST port 7878 refuses connections.
- Save, restart and verify that the existing world, accounts, config and plugins remain on `/data`.
- Set invalid numeric/world values and a short password; verify safe defaults and retention of the valid stored password.
- Back up `/data` and test restoration before an upgrade.

## Open questions

- Railway public TCP authentication and volume persistence passed pre-publication and published-template checks on 2026-11-21. Full graphical-client gameplay and in-game administrator setup were not exercised.
- Mobile/console interoperability, plugins and full gameplay are not claimed by the package's protocol authentication test.
