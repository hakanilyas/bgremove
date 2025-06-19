import logging
from rembg import new_session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_session = None

def _init_session():
    global _session
    if _session is None:
        logger.info("Initializing rembg session (U²-Net)...")
        _session = new_session("u2net")
    return _session

def remove_background(image_bytes: bytes) -> bytes:
    """
    Gelen ham görüntü byte’ını alır, arka planı kaldırır ve PNG olarak döner.
    """
    sess = _init_session()
    logger.info("Input size: %d bytes", len(image_bytes))
    output = sess.remove(image_bytes)
    logger.info("Output size: %d bytes", len(output))
    return output
