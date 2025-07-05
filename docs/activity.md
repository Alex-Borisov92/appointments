# Activity-диаграмма сценария «Пациент записывается на приём»

```mermaid
flowchart TD
    %% ---------- группы ----------
    subgraph Patient
        P_Start([Start])
        P_Open[/Открыть Telegram-бот/]
        P_Input[/Ввести симптомы/]
        P_Confirm[/Подтвердить слот/]
        P_Start --> P_Open --> P_Input --> P_Confirm
    end

    subgraph Bot
        B_Ask[/Спросить симптомы/]
        B_Detect[/ML-модель → специализация/]
        B_Request[/Запросить слоты у API/]
        B_Show[/Показать доступные слоты/]
        B_Send[/Отправить выбранный слот в API/]
        B_Done[/Показать результат/]
    end

    subgraph API
        A_Check[/Проверить свободен ли слот/]
        A_Create[/201 Created/]
        A_Conflict[/409 Conflict/]
    end

    subgraph DB
        D[(appointments<br/>UNIQUE doctor_id + start_time)]
    end
    %% ---------- потоки ----------
    P_Open --> B_Ask
    B_Ask --> P_Input
    P_Input --> B_Detect
    B_Detect --> B_Request
    B_Request --> A_Check
    A_Check -- свободно --> A_Create
    A_Check -- занято --> A_Conflict
    A_Create --> D
    A_Create --> B_Show
    A_Conflict --> B_Show
    B_Show --> P_Confirm
    P_Confirm --> B_Send
    B_Send --> A_Create
    A_Create --> B_Done
