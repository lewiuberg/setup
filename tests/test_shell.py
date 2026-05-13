import asyncio
import sys

import pytest

from macsetup.core.shell import CommandResult, Shell


@pytest.mark.asyncio
async def test_run_captures_output() -> None:
    shell = Shell()
    result = await shell.run([sys.executable, "-c", "print('hello world')"])
    assert isinstance(result, CommandResult)
    assert result.ok
    assert "hello world" in result.output


@pytest.mark.asyncio
async def test_run_captures_nonzero_exit() -> None:
    shell = Shell()
    result = await shell.run([sys.executable, "-c", "import sys; sys.exit(3)"])
    assert not result.ok
    assert result.exit_code == 3


@pytest.mark.asyncio
async def test_stream_lines_in_order() -> None:
    shell = Shell()
    seen: list[str] = []

    code = "for i in range(3):\n    print(f'line {i}', flush=True)"
    exit_code = await shell.stream([sys.executable, "-c", code], seen.append)
    assert exit_code == 0
    assert seen == ["line 0", "line 1", "line 2"]


@pytest.mark.asyncio
async def test_stream_supports_async_callback() -> None:
    shell = Shell()
    seen: list[str] = []

    async def on_line(line: str) -> None:
        await asyncio.sleep(0)
        seen.append(line)

    exit_code = await shell.stream([sys.executable, "-c", "print('only')"], on_line)
    assert exit_code == 0
    assert seen == ["only"]


def test_which_returns_path_or_none() -> None:
    shell = Shell()
    # `sh` is guaranteed on macOS; some fictional binary is not.
    assert shell.which("sh") is not None
    assert shell.which("definitely-not-a-real-binary-xyz") is None
    assert shell.has("sh")
    assert not shell.has("definitely-not-a-real-binary-xyz")
