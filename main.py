import uvicorn


if __name__ == "__main__":
    uvicorn.run("hello_world_service_consumer:app", host="0.0.0.0", port=8083, reload=False, proxy_headers=True,
                forwarded_allow_ips="*")