import asyncio
import uvloop

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


from src.application.ocr_1_1 import OCR
from src.application.finalizer_1_1 import Finalizer



async def run():
    while True:
        ocr = OCR("ocr")
        finalizer = Finalizer("finalizer")

        await ocr.run()
        await finalizer.run()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(run())
