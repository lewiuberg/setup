from macsetup.core import shell


async def test_run_captures_stdout():
    result = await shell.run(["echo", "hello"])
    assert result.ok
    assert "hello" in result.stdout


async def test_run_nonzero_returncode():
    result = await shell.run(["false"])
    assert not result.ok
    assert result.returncode != 0


async def test_run_streams_lines():
    lines: list[str] = []
    result = await shell.run(["printf", "a\nb\nc\n"], on_line=lines.append)
    assert result.ok
    assert lines == ["a", "b", "c"]


async def test_run_with_input():
    result = await shell.run(["cat"], input="piped\n")
    assert result.ok
    assert "piped" in result.stdout


async def test_run_captures_stderr():
    # `sh -c` is universally available.
    result = await shell.run(["sh", "-c", "echo oops >&2; exit 3"])
    assert result.returncode == 3
    assert "oops" in result.stderr
