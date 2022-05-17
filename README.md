# async_redmine_telegram_bot
This project aims to create telegram bot, which collects time sheet information (working hours and comments) about users in Redmine groups and send it to telegram chats to control working projects managing in Redmine system.
Each user during working day lives some information about the time spent on the project with comments on his actions. This information may be collected with Redmine REST API, processed and sended by bot to desired telegram chat in async mode. 
To operate with Redmine REST API http_client.py and redmine_client.py created in /source/clients/, to send chat messages telegram_client.py created with python-telegram-bot library. 

Questions:
1. I'm using event_loop from asyncio library to manage with http async requests (aiohttp library) to Redmine REST API in sync python-telegram-bot library. There are two methods (commands) of bot: get_today (source/bot.py), which returns timesheets immediately and run_daily (source/bot.py), which returns timesheet information every day in defined period of time. So, if I run get_today method during run_daily execution it returns an error: RuntimeError: This event loop is already running!. So, I've used introspection method of event loop .isrunning() in "while" cycle to stop adding new tasks to event loop (source/work_flow/workflow.py, set_task method). This approach was helpfull, but I'm not sure if it's correct and "clean" enough.
## Many thanks in advance for the code review and the answer!
