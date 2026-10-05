# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import asyncio,json,sys,os,shutil
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../.."))
UVX=os.environ.get("UVX",shutil.which("uvx") or os.path.expanduser("~/.local/bin/uvx"))
async def main():
    env=dict(os.environ,KICAD_MCP_PROFILE="schematic_authoring",KICAD_MCP_OPERATING_MODE="write",KICAD_MCP_WORKSPACE_ROOT=ROOT,KICAD_CLI_PATH=os.environ.get("KICAD_CLI","/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"))
    params=StdioServerParameters(command=UVX,args=["kicad-mcp-pro"],env=env)
    calls=json.load(open(sys.argv[1]))
    async with stdio_client(params) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            for name,args in calls:
                res=await s.call_tool(name,args)
                print("==",name); print("\n".join(getattr(c,'text',str(c)) for c in res.content)[:3000])
asyncio.run(main())
