import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_exchange_rate(date_str):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_str}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

async def get_exchange_rates(days):
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(1, days+1)]
    tasks = [fetch_exchange_rate(date) for date in dates]
    results = await asyncio.gather(*tasks)
    return results

def print_exchange_rates(results):
    popular_currencies = {'USD', 'EUR', 'RUB', 'GBP', 'PLN'}  # Тільки 5 популярних валют
    for idx, result in enumerate(results, 1):
        date_str = (datetime.now() - timedelta(days=idx)).strftime('%d.%m.%Y')
        print(f"{date_str}:")
        if result:
            for rate in result['exchangeRate']:
                if rate['currency'] in popular_currencies:
                    print(f"{rate['currency']}: {rate.get('saleRateNB', '-')}, {rate.get('purchaseRateNB', '-')}")
        else:
            print("Failed to fetch exchange rates for this date.")
        print()

async def main(days):
    results = await get_exchange_rates(days)
    print_exchange_rates(results)

if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 10  
    asyncio.run(main(days))

