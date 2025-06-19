import logging
from fastapi import FastAPI, File, UploadFile, HTTPException, Response
from bg_removal import remove_background

# Konsola hem timestamp hem log seviyesi basacak format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-5s | %(name)s | %(message)s"
)

app = FastAPI(
    title="Background Removal API",
    description="Upload an image and get back a PNG with transparent background",
    version="1.0.0"
)

@app.post("/remove-bg", summary="Remove image background")
async def remove_bg_endpoint(file: UploadFile = File(...)):
    # Sadece jpeg/png uzantılarını kabul et
    if file.content_type not in ("image/png", "image/jpeg", "image/jpg"):
        raise HTTPException(400, "Invalid image type; only JPEG/PNG allowed.")
    img_bytes = await file.read()
    try:
        out_bytes = remove_background(img_bytes)
    except Exception as e:
        logging.exception("Background removal failed")
        raise HTTPException(500, "Background removal error")
    # PNG döndüğümüzü belirt
    return Response(content=out_bytes, media_type="image/png")
