from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from db.users import get_user, create_user
from db.tasks import create_task, get_task, get_all_tasks, update_task_is_done, get_stats

class Tasks(StatesGroup):
    waiting_taks_name = State()
    waiting_taks_id = State()

router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    tg_id = message.from_user.id
    create_user(tg_id)
    await message.answer(f"Привет, {message.from_user.full_name}!\n\n"
                         f"Вот список команд:\n"
                         f"/start - Главное меню\n"
                         f"/add - Создать задачу\n"
                         f"/tasks - Посмотреть все задачи\n"
                         f"/done - Выполнить задачу\n"
                         f"/stats - Статистика по задачам")

@router.message(Command("add"))
async def cmd_add_task(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(Tasks.waiting_taks_name)

@router.message(Tasks.waiting_taks_name)
async def state_create_task(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    create_task(user_id=user["id"],
                task_name=message.text,
                is_done=False)
    await message.answer(f"Добавлена задача: {message.text}")
    await state.clear()

@router.message(Command("tasks"))
async def cmd_view_tasks(message: Message):
    tasks = get_all_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас нету задач")
        return

    text = ("Ваши задачи: \n\n"
            "№. ID | Название | Статус\n")
    for i, task in enumerate(tasks, start=1):
        done = "✅ Выполнена"
        if not task["is_done"]:
            done = "⬜ Не выполнена"
        text += f"{i}. {task["id"]} | {task["task_name"]} | {done}\n"

    await message.answer(text)

@router.message(Command('done'))
async def cmd_done(message: Message, state: FSMContext):
    await state.set_state(Tasks.waiting_taks_id)
    await message.answer("Введите айди задачи, чтобы ее выполнить:")

@router.message(Tasks.waiting_taks_id)
async def state_done_task(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Пожалуйста, введите айди задачи")
    done = update_task_is_done(True, int(message.text), message.from_user.id)
    if not done:
        await message.answer("У вас нету задачи с таким айди")
        await state.clear()
        return

    await message.answer(f"Задача: {done["task_name"]} - Выполнена, введите /tasks")
    await state.clear()

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    stats = get_stats(message.from_user.id)
    done = 0
    not_done = 0
    for row in stats:
        if row["is_done"]:
            done = row["count"]
        else:
            not_done = row["count"]

    
    text = (f"Ваша статистика по задачам:\n\n"
            f"Всего задач: {done+not_done}\n"
            f"Выполнено задач: {done}\n"
            f"Еще не выполнено: {not_done}")
    await message.answer(text)