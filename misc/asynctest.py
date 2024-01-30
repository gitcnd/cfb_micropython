import uasyncio as asyncio

async def delayed_goodbye():
    import asyncio
    await asyncio.sleep(5)  # Wait for 5 seconds
    print("goodbye")

# Print "hello world" and start the asynchronous task
print("hello world")
asyncio.run(delayed_goodbye())

