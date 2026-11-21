# Provenance and licenses

Verified 2026-11-21 against the official [Pryaxis/TShock v6.2.1 release](https://github.com/Pryaxis/TShock/releases/tag/v6.2.1), its immutable release metadata, Dockerfile, `TShockAPI/TShock.cs`, `TShockAPI/FileTools.cs` and configuration sources at that tag. It supports Terraria 1.4.5.8. The official Dockerfile uses .NET 9, config/log/world/plugin paths and ports 7777/7878; this package downloads the upstream release rather than extending its VOLUME-declaring image.

TShock: Copyright (C) 2011–2019 Pryaxis & TShock Contributors, GNU GPL version 3 or later. The unmodified release is downloaded from upstream during build; corresponding source is available at [the pinned source tag](https://github.com/Pryaxis/TShock/tree/v6.2.1). Full upstream license is included as `COPYING.TShock`. Other bundled upstream components and Terraria content retain their respective upstream licenses and rights. This package grants no rights to Terraria; users need their own legitimate game clients. No automatic EULA acceptance is invented by this launcher.

Launcher, Dockerfile, tests and prose were written for this package. Market designs `terraria-dedicated-server` (XavTo) and `terraria-tshock` (lNamelessl) were inspected through marketplace descriptions by the coordinating agent. No marketplace source files or prose were copied. No local upstream template repository for this new app was supplied. The password, single volume, TCP proxy and disabled REST design were independently implemented using the upstream configuration source.

The marketplace Terraria icon is served from [homarr-labs/dashboard-icons](https://github.com/homarr-labs/dashboard-icons); the Terraria mark belongs to its rights holder and is used to identify the hosted game. The raw PNG URL returned HTTP 200 during verification.

Pinned release: `TShock-6.2.1-for-Terraria-1.4.5.8-linux-x64-Release.zip`, SHA-256 `deb9189acbdbd2ee0f0a06fffe15358033859a4ba842b22f79a84bda68600105`. This matches the official GitHub release asset digest and a local download.

Pinned base: `mcr.microsoft.com/dotnet/runtime:9.0.23-bookworm-slim@sha256:aa21f09894760dc31b207e29256fcf9a74fb14da4384b81ba49b1f038604087f`. Linux amd64 manifest `sha256:e06da7bd10651e3f4b7b8f07e7c97e3bb40ecac8931d75ed5f1cf40e4a942ed7`. Runtime version checked using `dotnet --list-runtimes`.
