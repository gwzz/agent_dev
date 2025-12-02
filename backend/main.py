import sys
import argparse

def run_adk_server():
    """Launch the ADK server as before"""
    print("Hello from agent-dev!")
    # Keep the original functionality if needed
    from city_info_expert.agent import root_agent
    print(f"City Info Expert Agent ready: {root_agent.name}")

def run_fastapi_server():
    """Launch the FastAPI server"""
    import uvicorn
    from api.main import app
    print("Starting FastAPI server for AI Agent Experts...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    parser = argparse.ArgumentParser(description="Agent Development Kit Service")
    parser.add_argument(
        "service",
        nargs="?",
        choices=["adk", "fastapi", "api"],
        default="adk",
        help="Service to run: 'adk' for original ADK server, 'fastapi'/'api' for FastAPI service"
    )

    args = parser.parse_args()

    if args.service in ["fastapi", "api"]:
        run_fastapi_server()
    else:
        run_adk_server()


if __name__ == "__main__":
    main()
