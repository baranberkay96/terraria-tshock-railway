# Local verification — 2026-11-21

- Official GitHub `releases/latest` returned `v6.2.1`, TShock 6.2.1 for Terraria 1.4.5.8. Downloaded release SHA-256 matches both the Dockerfile and GitHub's asset digest.
- `docker build --platform linux/amd64` passed. The base tag and digest resolve to .NET 9.0.23. Image size reported by local Docker: approximately 132 MB. Build log: sibling `_research/docker-build.log` in the delivery workspace.
- Five bootstrap unit tests passed: health/game-port collision fallback, invalid input fallbacks with locked password, stored password/custom configuration retention and password rotation, corrupt configuration preservation, and rejection of control characters/invalid password length.
- `to_serialized.py` successfully converted `template.json` to Railway serialized configuration.
- Local Docker runtime used `--init --platform linux/amd64 --memory 1g --cpus 2`, a fresh named volume at `/data`, and game/health ports bound only to host loopback.
- Fresh small classic world generation completed successfully under the 1 GiB memory cap. Observed usage: 429 MiB during generation, 505 MiB after boot, about 455 MiB after reloading. No OOM was observed. Generation and plugin use can vary; this does not claim Free-plan compatibility.
- Runtime logs identify TShock 6.2.1.0, Terraria 1.4.5.8, OTAPI 3.3.14 and protocol 326. The integration probe uses the observed protocol and the packet layout checked in upstream `GetDataHandlers.cs`.
- Real game handshake passed after sending protocol, player information and client UUID: empty and wrong passwords received disconnect packet 2; the correct password received world-information packet 7. This checks authentication, not full gameplay. Reproduce with `GAME_TEST_PASSWORD={test-password} python3 services/tshock/tests/smoke_game.py` against local port 17777 (override `GAME_TEST_PORT` if needed).
- Private `/health` returned HTTP 200 after startup. TCP 7878 returned connection refused. Persisted config has `RestApiEnabled=false`, `DisableUUIDLogin=true`, `DisableLoginBeforeJoin=true` and the default eight slots.
- Launcher and TShock processes both ran with UID/GID 10001 (Docker init stayed PID 1). Final graceful stop exited 0 with `OOMKilled=false`.
- Graceful Docker stop requested `exit`, saved the world and shut down. A new container used the same volume while receiving a short invalid password and invalid optional form inputs. It loaded the existing world, returned healthy, kept the previously valid password and passed the game authentication test again.
- World SHA-256 before and after container recreation was identical: `b16ad5399b34077e516f4b70487a98ddd5a109e61e67060dd3bca62af8248de0` (2,997,374 bytes). A custom `ServerName` configuration marker survived. `tshock.sqlite` exists on the volume.
- The PNG marketplace icon URL returned HTTP 200. The jsDelivr SVG candidate did not and was replaced with the verified raw PNG.

The isolated local test container and volume were removed after testing. No Railway project, cloud deployment, source repository, or marketplace listing was created by these checks. In-game administrator setup and complete client gameplay remain first-cloud-deploy checks; local tests exercised protocol authentication and persistent state.

Review follow-up: PORT=7777 regression failed before the guard and passed after falling back to health port8080. All five unit tests and the final linux/amd64 Docker rebuild passed.
