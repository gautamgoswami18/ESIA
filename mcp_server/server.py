from mcp.server.fastmcp import FastMCP

from mcp_server.tools.employee_profile import employee_profile
from mcp_server.tools.search_employee import search_employee
from mcp_server.tools.resume_summary import resume_summary
from mcp_server.tools.compare_candidates import compare_candidates

mcp = FastMCP("ESIA MCP Server")

mcp.tool()(employee_profile)
mcp.tool()(search_employee)
mcp.tool()(resume_summary)
mcp.tool()(compare_candidates)

if __name__ == "__main__":
    mcp.run()