if __name__ == "__main__":
    mode = os.getenv("PHB_API_MODE", "fastapi").lower()

    # Railway uses PORT, so both modes must respect it
    port = int(os.getenv("PORT", "8000"))

    if mode == "flask":
        flask_app.run(host="0.0.0.0", port=port)
    else:
        import uvicorn
        uvicorn.run(
            "phb_api:fastapi_app",
            host="0.0.0.0",
            port=port,
            reload=False,
        )
