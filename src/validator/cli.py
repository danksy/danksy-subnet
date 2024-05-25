import typer
from typing import Annotated, Optional

from communex._common import get_node_url  # type: ignore
from communex.client import CommuneClient  # type: ignore
from communex.compat.key import classic_load_key  # type: ignore

from validator._config import ValidatorSettings
from validator.validator import get_subnet_netuid, ContentValidator

app = typer.Typer()

TESTNET_URL="wss://testnet-commune-api-node-0.communeai.net"

@app.command("serve-subnet")
def serve(
        commune_key: Annotated[
            str, typer.Argument(help="Name of the key present in `~/.commune/key`")
        ],
        netuid: Optional[int] = typer.Option(
        default=4, help="netuid of subnet. For danksy mainnet uid is 4 and testnet is 24"
        ),
        testnet: Optional[bool] = typer.Option(
            default=False, help="Use testnet "
        ),
        call_timeout: int = 65,
):
    keypair = classic_load_key(commune_key)  # type: ignore
    settings = ValidatorSettings()  # type: ignore
    url = get_node_url()
    if testnet:
        url = TESTNET_URL
    c_client = CommuneClient(url)
    subnet_uid = netuid
    validator = ContentValidator(
        keypair,
        subnet_uid,
        c_client,
        call_timeout=call_timeout,
    )
    validator.validation_loop(settings)


if __name__ == "__main__":
    typer.run(serve)
