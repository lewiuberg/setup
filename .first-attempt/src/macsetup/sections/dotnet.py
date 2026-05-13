""".NET SDK + Azure Artifact Credential Provider.

The legacy script downloaded a pinned cask formula file from a historical
GitHub commit — fragile. Modern approach: install the standard cask, then
the credential provider via the Microsoft installer script.
"""

from __future__ import annotations

from pathlib import Path

from macsetup.core.config import Item
from macsetup.core.detect import command_exists, installed_casks
from macsetup.core.shell import run
from macsetup.sections.base import Emit, Section, SectionStatus, Status


CRED_PROVIDER_PATH = (
    Path.home() / ".nuget" / "plugins" / "netcore" / "CredentialProvider.Microsoft"
)
CRED_PROVIDER_INSTALL_URL = "https://aka.ms/install-artifacts-credprovider.sh"


class DotnetSection(Section):
    name = ".NET"
    description = ".NET SDK + Azure Artifact Credential Provider"

    async def detect(self) -> SectionStatus:
        sdk_ok = "dotnet-sdk" in await installed_casks() or command_exists("dotnet")
        cred_ok = CRED_PROVIDER_PATH.exists()
        count = int(sdk_ok) + int(cred_ok)
        if count == 0:
            return SectionStatus(Status.PENDING, 0, 2)
        if count == 2:
            return SectionStatus(Status.DONE, 2, 2)
        return SectionStatus(Status.PARTIAL, count, 2)

    async def install(self, items: list[Item], emit: Emit) -> None:
        if "dotnet-sdk" not in await installed_casks() and not command_exists("dotnet"):
            await emit("Installing .NET SDK cask…")
            result = await run(["brew", "install", "--cask", "dotnet-sdk"], on_line=emit)
            if not result.ok:
                await emit(f".NET SDK install failed: {result.stderr.strip()}")
                return
        else:
            await emit(".NET SDK already installed")

        if CRED_PROVIDER_PATH.exists():
            await emit("Azure Artifact Credential Provider already installed")
            return
        await emit("Installing Azure Artifact Credential Provider…")
        result = await run(
            ["bash", "-c", f'sh -c "$(curl -fsSL {CRED_PROVIDER_INSTALL_URL})"'],
            on_line=emit,
        )
        if result.ok:
            await emit(
                "Credential Provider installed. First time you open a "
                ".NET project: dotnet restore --interactive"
            )
        else:
            await emit(f"Credential Provider install failed: {result.stderr.strip()}")
