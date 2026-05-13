import asyncio

import pytest

from macsetup.core.sudo import SudoKeepalive


@pytest.mark.asyncio
async def test_keepalive_start_stop_cleanly() -> None:
    keepalive = SudoKeepalive(interval=3600)
    keepalive.start()
    assert keepalive._task is not None
    assert not keepalive._task.done()
    keepalive.stop()
    # Give the cancellation a tick to propagate.
    await asyncio.sleep(0)
    assert keepalive._task is None


@pytest.mark.asyncio
async def test_keepalive_start_twice_is_idempotent() -> None:
    keepalive = SudoKeepalive(interval=3600)
    keepalive.start()
    first_task = keepalive._task
    keepalive.start()
    assert keepalive._task is first_task
    keepalive.stop()
    await asyncio.sleep(0)
