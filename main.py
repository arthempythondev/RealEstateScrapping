import aiohttp
import asyncio
import pandas as pd

from scrapper import get_properties


async def main(postcodes, output_file):
    async with aiohttp.ClientSession(headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.214.93.255 Safari/537.36'
    }) as session:
        tasks = [get_properties(session, postcode) for postcode in postcodes]
        results = await asyncio.gather(*tasks)

        data = [item for sublist in results for item in sublist]
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        return f"Data saved to {output_file}"


postcodes = ['10308']
output_file = 'properties.csv'

if __name__ == '__main__':
    df = asyncio.run(main(postcodes, output_file))
