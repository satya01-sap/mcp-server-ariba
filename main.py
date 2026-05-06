import os
import base64
import requests
import logging
import time
import contextlib

from typing import Optional, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Depends
#from fastapi.responses import JSONResponse
from mcp.server.fastmcp import FastMCP
# XSUAA
from sap.xssec import create_security_context
from mcp.server.transport_security import TransportSecuritySettings

from starlette.applications import Starlette
from starlette.routing import Mount


load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


mcp = FastMCP(
    "ariba-server",
    stateless_http=True,
    json_response=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "ariba-mcp-btp.cfapps.xxxx.hana.ondemand.com"
        ],
        allowed_origins=[
            "https://ariba-mcp-btp.cfapps.xxxx.hana.ondemand.com"
        ],
    )
)
#end

# Create a lifespan context manager to run the session manager
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app())
    ],
    lifespan=lifespan,
)


# ------------------ ARIBA CLIENT ------------------
class AribaClient:
    def __init__(self):
        self.client_id = os.getenv("ARIBA_CLIENT_ID")
        self.client_secret = os.getenv("ARIBA_CLIENT_SECRET")
        self.api_key = os.getenv("ARIBA_API_KEY")

        self.token_url = os.getenv("ARIBA_TOKEN_URL")
        self.api_base_url = os.getenv("ARIBA_API_BASE_URL")

        if not all([self.client_id, self.client_secret, self.api_key]):
            raise ValueError("Missing environment variables")

        self.token: Optional[str] = None

    def get_token(self) -> str:
        if self.token and time.time() < self.token_expiry - 1440:
            return self.token

        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        response = requests.post(
            self.token_url,
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            params={"grant_type": "client_credentials"}
        )

        response.raise_for_status()

        self.token = response.json().get("access_token")
        logger.info(f"the self token ={self.token}")
        self.token_expiry = time.time() + response.json().get("expires_in", 1440)
        return self.token

    def get_event_summary(
        self,
        doc_id: str,
        user: str,
        password_adapter: str,
        realm: str
    ) -> Dict[str, Any]:

        token = self.get_token()

        endpoint = f"{self.api_base_url}/events/{doc_id}/supplierBids"

        response = requests.get(
            endpoint,
            headers={
                "Authorization": f"Bearer {token}",
                "apiKey": self.api_key
            },
            params={
                "user": user,
                "passwordAdapter": password_adapter,
                "realm": realm
            }
        )

        response.raise_for_status()
        logger.info(f"the response ={response.json()}")
        return response.json()


# Singleton client
client = AribaClient()


# ------------------ MCP TOOL ------------------
@mcp.tool()
def get_event_summary(
    doc_id: str,
    user: str,
    password_adapter: str,
    realm: str
) -> Dict[str, Any]:
    """
    Retrieve supplier bids for a sourcing event.

    Args:
        doc_id: Document ID (e.g., 'Doc1213131')
        user: Username (e.g., myuser)
        password_adapter: Password adapter (e.g., 'myadaptor')
        realm: Realm name (e.g., 'myrelm')
    """
    return client.get_event_summary(doc_id, user, password_adapter, realm)


def main():
    # Initialize and run the server
    #mcp.run(transport="stdio")
    mcp.run(transport='streamable-http')
    

if __name__ == "__main__":
    main()

