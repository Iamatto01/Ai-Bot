# __main__.py
from OracleDBClient import OracleDBClient
from AI_Agent import AI_Agent
from TelegramGroup import TelegramGroup
from Simulation import Simulation

if __name__ == "__main__":
    dsn = "ORCL"  # TNS alias from tnsnames.ora
    user = "SYSTEM"
    password = "Kentang99"

    gemini_api_key = "AIzaSyA4bGS73qmpGkCbzLhTkvf5rI5PTpO3CfE"
    telegram_api_key = "6768102658:AAG1Sc2BFQs4Hz9MLkJbGpEcAPyyuJMaOII"
  
    # Initialize OracleDBClient
    oracle_client = OracleDBClient(dsn=dsn, user=user, password=password)

    # Initialize AI_Agent
    ai_agent = AI_Agent(oracle_client=oracle_client, gemini_api_key=gemini_api_key)

    # Initialize TelegramGroup instances
    telegram_groups = [
        TelegramGroup(group_id="group_1", group_name="Group 1", created_at="2023-01-01", privacy_settings="public", telegram_api_key=telegram_api_key),
        TelegramGroup(group_id="group_2", group_name="Group 2", created_at="2023-01-02", privacy_settings="private", telegram_api_key=telegram_api_key)
    ]

    # Start the simulation
    simulation = Simulation(ai_agent=ai_agent, telegram_groups=telegram_groups, mongo_client=oracle_client)
    simulation.start()
    simulation.run()

    # Start Telegram polling
    for tg in telegram_groups:
        tg.start_polling()

 