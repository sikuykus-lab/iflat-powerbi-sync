# Все операции API CRM из OpenAPI (снимок)

Источник: `iflat_openapi_1.4.0.json` — **API CRM** версия спецификации **1.4.0**.

Это **инвентаризация контракта**: сами HTTP-запросы к продакшену здесь **не выполнялись** (есть DELETE/POST и побочные эффекты).

- Уникальных путей: **261**
- Всего операций (метод × путь): **500**
- По методам: GET 222, POST 113, PUT 88, PATCH 0, DELETE 77

## Сводка по тегам (количество операций)

| Тег | Операций |
|-----|----------|
| Планирование работ | 50 |
| Производство работ | 34 |
| Дома | 31 |
| Пользователи | 29 |
| Приемка | 24 |
| Замечания | 23 |
| Помещения | 20 |
| Справочники | 20 |
| Согласование | 19 |
| Ипотека | 18 |
| Сделки | 17 |
| Объекты | 16 |
| Документы | 15 |
| Технические заявки | 13 |
| Ревизии | 12 |
| Задачи | 11 |
| Инфоблоки | 10 |
| Чек-листы | 10 |
| Комментарии | 9 |
| Планы | 9 |
| ЭЦП | 7 |
| Организации | 6 |
| Регистрация сделок в Росреестре | 6 |
| Шаблоны | 6 |
| Электронные документы | 6 |
| Авторизация | 5 |
| Договоры | 5 |
| ЖК | 5 |
| Записи журнала работ | 5 |
| Конфигурация форм | 5 |
| Пользовательские настройки | 5 |
| Сметы | 5 |
| Смс шаблоны | 5 |
| Сотрудники | 5 |
| Теги | 5 |
| Цены | 5 |
| BIM | 4 |
| Сделки: покупатели | 4 |
| Файлы | 4 |
| История изменений | 3 |
| Сущности | 3 |
| Импорт | 2 |
| Лиды | 2 |
| Телеграм | 1 |
| Экспорт | 1 |

## Полный список (сортировка: путь, затем метод)

| Путь | Метод | operationId | Краткое описание | Теги |
|------|-------|-------------|------------------|------|
| `/agentDocuments` | GET | `getAgentDocuments` | Получить список доверенностей | Пользователи |
| `/agentDocuments` | POST | `addAgentDocument` | Создать доверенность | Пользователи |
| `/agentDocuments/{agentDocumentId}` | DELETE | `deleteAgentDocument` | Удалить доверенность | Пользователи |
| `/agentDocuments/{agentDocumentId}` | GET | `getAgentDocumentId` | Получить доверенность | Пользователи |
| `/agentDocuments/{agentDocumentId}` | PUT | `updateAgentDocument` | Обновить доверенность | Пользователи |
| `/approvalActions` | GET | `getApprovalActions` | Получить список действий согласования | Согласование |
| `/approvalActions` | POST | `addApprovalAction` | Создать действие согласования | Согласование |
| `/approvalActions/{approvalActionId}` | GET | `getApprovalAction` | Получить действие согласования | Согласование |
| `/approvalActions/{approvalActionId}` | PUT | `updateApprovalAction` | Обновить действие согласования | Согласование |
| `/approvalChains` | GET | `getApprovalChains` | Получить список цепочек согласования | Согласование |
| `/approvalChains` | POST | `addApprovalChain` | Создать цепочку согласования | Согласование |
| `/approvalChains/{approvalChainId}` | DELETE | `deleteApprovalChain` | Удалить цепочку согласования | Согласование |
| `/approvalChains/{approvalChainId}` | GET | `getApprovalChain` | Получить цепочку согласования | Согласование |
| `/approvalChains/{approvalChainId}` | PUT | `updateApprovalChain` | Обновить цепочку согласования | Согласование |
| `/approvalRequests` | GET | `getApprovalRequests` | Получить список запросов на согласование | Согласование |
| `/approvalRequests` | POST | `addApprovalRequest` | Создать запрос на согласование | Согласование |
| `/approvalRequests/{approvalRequestId}` | DELETE | `deleteApprovalRequest` | Удалить запрос на согласование | Согласование |
| `/approvalRequests/{approvalRequestId}` | GET | `getApprovalRequest` | Получить запрос на согласование | Согласование |
| `/approvalRequests/{approvalRequestId}` | PUT | `updateApprovalRequest` | Обновить запрос на согласование | Согласование |
| `/approvalSteps` | GET | `getApprovalSteps` | Получить список шагов согласования | Согласование |
| `/approvalSteps` | POST | `addApprovalStep` | Создать шаг согласования | Согласование |
| `/approvalSteps/{approvalStepId}` | DELETE | `deleteApprovalStep` | Удалить шаг согласования | Согласование |
| `/approvalSteps/{approvalStepId}` | GET | `getApprovalStep` | Получить шаг согласования | Согласование |
| `/approvalSteps/{approvalStepId}` | PUT | `updateApprovalStep` | Обновить шаг согласования | Согласование |
| `/audits` | GET | `getAudits` | Получить список изменений | История изменений |
| `/auth/checkUsers` | POST | `checkUsers` | Найти пользователей по номеру телефона | Авторизация |
| `/auth/passwordReset` | POST | `passwordResetApiUser` | Сохранить новый пароль пользователя | Авторизация |
| `/auth/register` | POST | `registerUser` | Регистрация пользователя | Авторизация |
| `/auth/smsCode` | POST | `smsCodeApiUser` | Отправить код подтверждения на телефон пользователя | Авторизация |
| `/auth/smsCodeCheck` | POST | `smsCodeCheck` | Проверить код подтверждения | Авторизация |
| `/banks` | GET | `getBanks` | Получить список банков | Ипотека |
| `/banks` | POST | `addBank` | Создать банк | Ипотека |
| `/banks/{bankId}` | DELETE | `deleteBank` | Удалить банк | Ипотека |
| `/banks/{bankId}` | GET | `getBank` | Просмотреть банк | Ипотека |
| `/banks/{bankId}` | PUT | `updateBank` | Обновить банк | Ипотека |
| `/buildingObjectStatuses` | GET | `getBuildingObjectStatuses` | Получить список возможных статусов * | Объекты |
| `/buildingObjectTypes` | GET | `getBuildingObjectTypes` | Получить список типов объектов | Объекты |
| `/buildingObjectTypes` | POST | `addBuildingObjectType` | Добавить тип объекта | Объекты |
| `/buildingObjectTypes/{buildingObjectTypeId}` | DELETE | `deleteBuildingObjectType` | Удалить тип объекта | Объекты |
| `/buildingObjectTypes/{buildingObjectTypeId}` | GET | `getBuildingObjectType` | Получить тип объекта | Объекты |
| `/buildingObjectTypes/{buildingObjectTypeId}` | PUT | `updateBuildingObjectType` | Обновить информацию о типе объекта | Объекты |
| `/buildingObjects` | GET | `getBuildingObjects` | Получить список объектов | Объекты |
| `/buildingObjects` | POST | `addBuildingObjects` | Создать объект | Объекты |
| `/buildingObjects/{buildingObjectId}` | DELETE | `deleteBuildingObjects` | Удалить объект | Объекты |
| `/buildingObjects/{buildingObjectId}` | GET | `getbuildingObject` | Получить объект | Объекты |
| `/buildingObjects/{buildingObjectId}` | PUT | `updateBuildingObjects` | Обновить информацию об объекте | Объекты |
| `/checkListSteps` | GET | `getSteps` | Получить список всех доступных шагов чек листа | Чек-листы |
| `/checkListSteps` | POST | `addStep` | Создать шаг | Чек-листы |
| `/checkListSteps/{stepId}` | DELETE | `deleteStep` | Удалить шаг | Чек-листы |
| `/checkListSteps/{stepId}` | GET | `getStep` | Просмотреть шаг | Чек-листы |
| `/checkListSteps/{stepId}` | PUT | `updateStep` | Обновить шаг | Чек-листы |
| `/checkLists` | GET | `getCheckLists` | Получить список всех доступных чек-листов | Чек-листы |
| `/checkLists` | POST | `createCheckLists` | Создать чек-лист | Чек-листы |
| `/checkLists/{checkListId}` | DELETE | `deleteCheckLists` | Удалить чек-лист | Чек-листы |
| `/checkLists/{checkListId}` | GET | `getCheckList` | Получить чек-лист | Чек-листы |
| `/checkLists/{checkListId}` | PUT | `updateCheckLists` | Обновить чек-лист | Чек-листы |
| `/claimCategories` | GET | `getClaimCategories` | Получить список возможных категорий техзаявок | Технические заявки |
| `/claimCategories` | POST | `addClaimCategory` | Создать категорию техзаявок | Технические заявки |
| `/claimCategories/{claimCategoryId}` | DELETE | `deleteClaimCategory` | Удалить категорию техзаявок | Технические заявки |
| `/claimCategories/{claimCategoryId}` | GET | `getClaimCategory` | Получить категорию техзаявок | Технические заявки |
| `/claimCategories/{claimCategoryId}` | PUT | `updateClaimCategory` | Обновить категорию техзаявок | Технические заявки |
| `/claimPriorities` | GET | `getPriorities` | Получить список видов срочности | Технические заявки |
| `/claimTypes` | GET | `getClaimTypes` | Получить список возможных типов * | Технические заявки |
| `/claims` | GET | `getClaims` | Получить список технических заявок * | Технические заявки |
| `/claims` | POST | `addClaim` | Создать техническую заявку * | Технические заявки |
| `/claims/statuses` | GET | `getClaimsStatuses` | Получить список возможных статусов * | Технические заявки |
| `/claims/{claimId}` | GET | `getClaim` | Получить техническую заяку * | Технические заявки |
| `/claims/{claimId}` | PUT | `updateClaim` | Обновить техническую заявку | Технические заявки |
| `/claims/{claimId}/remarks` | GET | `getClaimRemarks` | Замечания по технической заявке | Технические заявки |
| `/comments` | GET | `getComments` | Получить комментарии | Комментарии |
| `/comments` | POST | `addComment` | Отправить комментарий | Комментарии |
| `/comments/{commentId}` | DELETE | `deleteComment` | Удалить комментарий | Комментарии |
| `/comments/{commentId}` | PUT | `updateComment` | Обновить комментарий | Комментарии |
| `/confirmationDocumentTypes` | GET | `getConfirmationDocumentTypes` | Получить список типов удостоверения личности | Пользователи |
| `/contracts` | GET | `getContracts` | Просмотреть договоры | Договоры |
| `/contracts` | POST | `addContract` | Создать договор | Договоры |
| `/contracts/{contractId}` | DELETE | `deleteContract` | Удалить договор | Договоры |
| `/contracts/{contractId}` | GET | `getContract` | Получить договор | Договоры |
| `/contracts/{contractId}` | PUT | `updateContract` | Обновить договор | Договоры |
| `/dealRegistrationStatuses` | GET | `getDealRegistrationStatuses` | Получить список возможных статусов заявлений в Росреестр | Регистрация сделок в Росреестре |
| `/dealRegistrations` | GET | `getDealRegistrations` | Получить список заявлений в Росреестр | Регистрация сделок в Росреестре |
| `/dealRegistrations` | POST | `addDealRegistration` | Создать заявление в Росреестре | Регистрация сделок в Росреестре |
| `/dealRegistrations/{dealRegistrationId}` | GET | `getDealRegistration` | Получить заявление в Росреестре | Регистрация сделок в Росреестре |
| `/dealRegistrations/{dealRegistrationId}/actions` | POST | `actionDealRegistration` | Действия с регистрацией сделки | Регистрация сделок в Росреестре |
| `/dealRegistrations/{dealRegistrationId}/externalDocumentTypes` | GET | `getExternalDocumentTypes` | Типы документов из внешнего интеграционного сервиса | Регистрация сделок в Росреестре |
| `/dealStages` | GET | `getDealStages` | Получить список возможных стадий | Сделки |
| `/dealStatuses` | GET | `getDealStatuses` | Получить список возможных статусов * | Сделки |
| `/deals` | GET | `getDeals` | Получить список сделок | Сделки |
| `/deals` | POST | `addDeal` | Создать сделку | Сделки |
| `/deals/contractTypes` | GET | `getContractTypes` | Получить список возможных типов договоров * | Сделки |
| `/deals/{dealId}` | GET | `getDeal` | Получить сделку | Сделки |
| `/deals/{dealId}` | PUT | `updateDeal` | Обновить информацию о сделке | Сделки |
| `/deals/{dealId}/clients` | GET | `getDealClients` | Получить список покупателей помещения | Сделки: покупатели |
| `/deals/{dealId}/clients` | POST | `addDealClient` | Добавить пользователя в список покупателей | Сделки: покупатели |
| `/deals/{dealId}/clients/{userId}` | DELETE | `deleteDealClient` | Удалить пользователя из списка покупателей | Сделки: покупатели |
| `/deals/{dealId}/clients/{userId}` | PUT | `updateDealClient` | Обновить долю и подпись покупателя | Сделки: покупатели |
| `/deals/{dealId}/providers/{providerId}/statuses` | GET | `providerDealStatuses` | Получить все статусы сделки по провайдеру | Сделки |
| `/deals/{dealId}/providers/{providerId}/statuses` | POST | `providerDealStatusesStore` | Создать статус сделки по провайдеру | Сделки |
| `/deals/{dealId}/reservationPayments` | POST | `getDealReservationPayment` | Создать платеж за бронирование помещения | Сделки |
| `/digitalDocumentStatuses` | GET | `getDigitalDocumentStatuses` | Получить список возможных статусов * | Электронные документы |
| `/digitalDocuments` | GET | `getDigitalDocuments` | Получить список документов | Электронные документы |
| `/digitalDocuments` | POST | `addDigitalDocument` | Добавить документ | Электронные документы |
| `/digitalDocuments/{documentId}` | DELETE | `deleteDigitalDocument` | Удалить документ | Электронные документы |
| `/digitalDocuments/{documentId}` | GET | `getDigitalDocument` | Посмотреть документ | Электронные документы |
| `/digitalDocuments/{documentId}` | PUT | `updateDigitalDocument` | Обновить документ | Электронные документы |
| `/districts` | GET | `getDistricts` | Получить список жилых комплексов | ЖК |
| `/districts` | POST | `addDistrict` | Создать жилой комплекс | ЖК |
| `/districts/{districtId}` | DELETE | `deleteDistrict` | Удалить жилой комплекс | ЖК |
| `/districts/{districtId}` | GET | `getDistrict` | Получить жилой комплекс | ЖК |
| `/districts/{districtId}` | PUT | `updateDistrict` | Обновить жилой комплекс | ЖК |
| `/divisions` | GET | `getDivisions` | Список подразделений | Пользователи |
| `/divisions` | POST | `createDivision` | Создать подразделение | Пользователи |
| `/divisions/{divisionId}` | DELETE | `deleteDivision` | Удалить подразделение | Пользователи |
| `/divisions/{divisionId}` | GET | `getDivision` | Получить подразделение | Пользователи |
| `/divisions/{divisionId}` | PUT | `updateDivision` | Обновить информацию подразделения | Пользователи |
| `/documentPages` | GET | `getDocumentPages` | Получить страницы документа | Документы |
| `/documentPages` | POST | `createDocumentPage` | Создать страницу документа | Документы |
| `/documentPages/{pageId}` | DELETE | `deleteDocumentPage` | Удалить страницу документа | Документы |
| `/documentPages/{pageId}` | GET | `getDocumentPage` | Получить страницу документа | Документы |
| `/documentPages/{pageId}` | PUT | `updateDocumentPage` | Обновить страницу документа | Документы |
| `/documentTypes` | GET | `getDocumentTypes` | Получить список возможных документов | Документы |
| `/documentTypes` | POST | `addDocumentType` | Добавить тип документа | Документы |
| `/documentTypes/{typeId}` | DELETE | `deleteDocumentType` | Удалить тип документа | Документы |
| `/documentTypes/{typeId}` | GET | `getDocumentType` | Получить тип документа | Документы |
| `/documentTypes/{typeId}` | PUT | `updateDocumentType` | Изменить тип документа | Документы |
| `/documents` | GET | `getDocuments` | Получить список документов | Документы |
| `/documents` | POST | `createDocument` | Создать документ | Документы |
| `/documents/{documentId}` | DELETE | `deleteDocument` | Удалить документ | Документы |
| `/documents/{documentId}` | GET | `getDocument` | Получить документ | Документы |
| `/documents/{documentId}` | PUT | `updateDocument` | Обновить документ | Документы |
| `/entityAttributes` | GET | `getEntityAttributes` | Получить список атрибутов сущности | Справочники |
| `/entityAttributes` | POST | `addEntityAttribute` | Создать атрибут сущности | Справочники |
| `/entityAttributes/{entityAttributeId}` | DELETE | `deleteEntityAttribute` | Удалить атрибут сущности | Справочники |
| `/entityAttributes/{entityAttributeId}` | GET | `getEntityAttribute` | Получить атрибут сущности | Справочники |
| `/entityAttributes/{entityAttributeId}` | PUT | `updateEntityAttribute` | Изменить атрибут сущности | Справочники |
| `/entityConfigs` | GET | `getEntityConfigs` | Получить конфиг нескольких сущностей | Сущности |
| `/entityConfigs/{entity}` | GET | `getEntityConfig` | Получить конфиг сущности | Сущности |
| `/entityVersions` | GET | `getEntityVersions` | Получить версии таблиц сущностей | Сущности |
| `/estimates` | GET | `getEstimates` | Просмотреть сметы | Сметы |
| `/estimates` | POST | `addEstimate` | Создать смету | Сметы |
| `/estimates/{estimateId}` | DELETE | `deleteEstimate` | Удалить смету | Сметы |
| `/estimates/{estimateId}` | GET | `getEstimate` | Получить смету | Сметы |
| `/estimates/{estimateId}` | PUT | `updateEstimate` | Обновить смету | Сметы |
| `/export/entities/{entity}/{entityId}/templates/{templateName}` | GET | `exportEntity` | Экспорт сущности в заданом формате | Экспорт |
| `/export/pdf/rooms/{roomId}` | GET | `savePdf` | Экспорт помещения в PDF презентацию | Помещения |
| `/externalObjects/{type}` | POST | `getExternalObjects` | Получить карты объектов. Необходимо указать либо внешние, либо внутренние ID объектов | Объекты |
| `/externalObjects/{type}/maps` | GET | `getExternalObjectMaps` | Получить карты объектов. Необходимо указать либо внешние, либо внутренние ID объектов | Объекты |
| `/externalObjects/{type}/maps` | POST | `createExternalObjects` | Создать карту объекта | Объекты |
| `/externalObjects/{type}/maps/{id}` | PUT | `updateExternalObjects` | Обновить карту объекта | Объекты |
| `/externalObjects/{type}/syncMaps` | POST | `syncExternalObjectMaps` | Синхронизировать карты объекта | Объекты |
| `/floors` | GET | `getFloors` | Получить список этажей | Дома |
| `/floors` | POST | `addFloor` | Добавить этаж | Дома |
| `/floors/{floorId}` | DELETE | `deleteFloor` | Удалить этаж | Дома |
| `/floors/{floorId}` | PUT | `updateFloor` | Обновить этаж | Дома |
| `/formSchemas` | GET | `getFormSchemas` | Получить список конфигурации форм | Конфигурация форм |
| `/formSchemas` | POST | `addFormSchema` | Создать конфигурацию формы | Конфигурация форм |
| `/formSchemas/{formSchemaId}` | DELETE | `deleteFormSchema` | Удалить конфигурацию формы | Конфигурация форм |
| `/formSchemas/{formSchemaId}` | GET | `getFormSchema` | Просмотреть конфигурацию формы | Конфигурация форм |
| `/formSchemas/{formSchemaId}` | PUT | `updateFormSchema` | Изменить конфигурацию формы | Конфигурация форм |
| `/freeTimes` | GET | `getFreeTimes` | Получить список доступного времени в день задачи | Задачи |
| `/grades` | GET | `getGrades` | Просмотреть список должностей | Пользователи |
| `/grades` | POST | `addGrade` | Создать должность | Пользователи |
| `/grades/{gradeId}` | DELETE | `deleteGrade` | Удалить должность | Пользователи |
| `/grades/{gradeId}` | GET | `getGrade` | Получить должность | Пользователи |
| `/grades/{gradeId}` | PUT | `updateGrade` | Обновить должность | Пользователи |
| `/histories` | GET | `getHistories` | Получить список записей из истории изменения статусов | История изменений |
| `/houseMeters` | GET | `getHouseMeters` | Получить список приборов учета дома | Дома |
| `/houseMeters` | POST | `addHouseMeter` | Добавить прибор учета в дом | Дома |
| `/houseMeters/{houseMeterId}` | DELETE | `deleteHouseMeter` | Удалить прибор учета | Дома |
| `/houseMeters/{houseMeterId}` | GET | `getHouseMeter` | Получить прибор учета | Дома |
| `/houseMeters/{houseMeterId}` | PUT | `updateHouseMeter` | Обновить прибор учета | Дома |
| `/houses` | GET | `getHouses` | Получить список домов | Дома |
| `/houses` | POST | `addHouse` | Создать дом | Дома |
| `/houses/{houseId}` | DELETE | `deleteHouse` | Удалить дом | Дома |
| `/houses/{houseId}` | GET | `getHouse` | Получить дом | Дома |
| `/houses/{houseId}` | PUT | `updateHouse` | Обновить информацию о доме | Дома |
| `/houses/{houseId}/bimElementsByRemarks` | GET | `getBimElementsByRemarks` | Получить элементы BIM-модели, содержащие замечания | BIM |
| `/houses/{houseId}/bimElementsByWork` | GET | `getBimElementsByWork` | Получить элементы BIM-модели, связанные с работами | BIM |
| `/houses/{houseId}/bimElementsByWorkPercentage` | GET | `getbimElementsByWorkPercentage` | Получить элементы BIM-модели, содержащие процент выполнения работ | BIM |
| `/houses/{houseId}/bimModel` | GET | `getHouseBimModel` | Получить BIM-модель дома | BIM |
| `/houses/{houseId}/inspectionsDays/{date}/times` | GET | `getInspectionDayTimes` | Получить список доступного времени в день приемки * | Приемка |
| `/houses/{houseId}/inspectionsPeriods` | GET | `getInspectionPeriods` | Получить список доступных периодов приемки для дома * | Приемка |
| `/houses/{houseId}/metro` | GET | `getHouseMetro` | Получить список ближайших станций метро для дома | Дома |
| `/houses/{houseId}/roomBadges` | GET | `getHouseRoomBadges` | Получить список доступных тегов помещений | Дома |
| `/import` | POST | `import` | Импорт | Импорт |
| `/import/feeds` | POST | `importFeed` | Импорт из фида | Импорт |
| `/inspectionExperts` | GET | `getInspectionExperts` | Получить список экспертов | Приемка |
| `/inspectionExperts` | POST | `addInspectionExpert` | Добавить эксперта к приемке | Приемка |
| `/inspectionExperts/{expertId}` | DELETE | `deleteInspectionExpert` | Удалить эксперта из приемки | Приемка |
| `/inspectionExperts/{expertId}` | GET | `getInspectionExpert` | Получить запись об эксперте | Приемка |
| `/inspectionFreeDays` | GET | `getInspectionFreeDays` | Получить список доступных дней приемки * | Приемка |
| `/inspectionMeters` | GET | `getInspectionMeters` | Получить список счетчиков | Приемка |
| `/inspectionRoomPeriods` | POST | `addInspectionRoomPeriods` | Открыть запись на приемку для помещений | Приемка |
| `/inspectionRoomPeriods` | PUT | `updateInspectionRoomPeriods` | Изменить период для записи на приемку | Приемка |
| `/inspectionSteps` | GET | `getInspectionSteps` | Получить список шагов | Приемка |
| `/inspectionSteps` | POST | `addInspectionStep` | Добавить шаг приемки | Приемка |
| `/inspectionSteps/{inspectionStepId}` | DELETE | `deleteInspectionStep` | Удалить шаг приемки | Приемка |
| `/inspectionSteps/{inspectionStepId}` | PUT | `updateInspectionSteps` | Обновить шаг | Приемка |
| `/inspectionUsers` | GET | `getInspectionUsers` | Получить список участников приемки | Приемка |
| `/inspectionUsers` | POST | `addInspectionUser` | Создать участника приемки | Приемка |
| `/inspectionUsers/{inspectionId}` | PUT | `updateInspectionUser` | Обновить информацию о участнике участника приемки | Приемка |
| `/inspections` | GET | `getInspections` | Получить список приемок | Приемка |
| `/inspections` | POST | `addInspection` | Создать приемку * | Приемка |
| `/inspections/batch` | POST | `addInspections` | Создать несколько приемок * | Приемка |
| `/inspections/statuses` | GET | `getInspectionsStatuses` | Получить список возможных статусов * | Приемка |
| `/inspections/{inspectionId}` | GET | `getInspection` | Получить приемку * | Приемка |
| `/inspections/{inspectionId}` | PUT | `updateInspection` | Обновить информацию о приемке * | Приемка |
| `/inspections/{inspectionId}/steps` | POST | `addInspectionStepByInspection` | Добавить шаг приемки | Приемка |
| `/leads` | GET | `getLeads` | Получить список лидов | Лиды |
| `/leads` | POST | `addLead` | Создать лид | Лиды |
| `/materialRegisters` | GET | `getMaterialRegisters` | Получить список отчетов о расходе материалов | Производство работ |
| `/materialRegisters` | POST | `addMaterialRegisters` | Создать отчет о расходе материалов | Производство работ |
| `/materialRegisters/{registerId}` | DELETE | `deleteMaterialRegister` | Удалить отчет о расходе материалов | Производство работ |
| `/materialRegisters/{registerId}` | GET | `getMaterialRegister` | Получить отчет о расходе материалов | Производство работ |
| `/materialRegisters/{registerId}` | PUT | `updateMaterialRegister` | Изменить отчет о расходе материалов | Производство работ |
| `/materials` | GET | `getMaterials` | Просмотреть список материалов | Планирование работ |
| `/materials` | POST | `addMaterial` | Создать материал | Планирование работ |
| `/materials/{materialId}` | DELETE | `deleteMaterial` | Удалить материал | Планирование работ |
| `/materials/{materialId}` | GET | `getMaterial` | Получить материал | Планирование работ |
| `/materials/{materialId}` | PUT | `updateMaterial` | Обновить материал | Планирование работ |
| `/messageTemplates` | GET | `getMessageTemplates` | Получить список Смс шаблонов | Смс шаблоны |
| `/messageTemplates` | POST | `addMessageTemplate` | Создать Смс шаблон | Смс шаблоны |
| `/messageTemplates/{messageTemplateId}` | DELETE | `deleteMessageTemplate` | Удалить Смс шаблон | Смс шаблоны |
| `/messageTemplates/{messageTemplateId}` | GET | `getmessageTemplate` | Получить Смс шаблон | Смс шаблоны |
| `/messageTemplates/{messageTemplateId}` | PUT | `updateMessageTemplate` | Обновить информацию о Смс шаблоне | Смс шаблоны |
| `/mortgagePrograms` | GET | `getMortgagePrograms` | Получить список банковских программ * | Ипотека |
| `/mortgageResponseStatuses` | GET | `getMortgageResponseStatuses` | Получить список возможных статусов по ипотеке | Ипотека |
| `/mortgageResponses` | GET | `getMortgageResponses` | Получить список ответов банка на заявку по ипотеке | Ипотека |
| `/mortgageResponses` | POST | `addMortgageResponse` | Добавить ответ банка на заявку по ипотеке | Ипотека |
| `/mortgageResponses/{responseId}` | DELETE | `deleteMortgageResponse` | Удалить ответ банка на заявку по ипотеке | Ипотека |
| `/mortgageResponses/{responseId}` | GET | `getMortgageResponse` | Посмотреть ответ банка по заявке на ипотеку | Ипотека |
| `/mortgageResponses/{responseId}` | PUT | `updateMortgageResponse` | Обновить ответ банка на заявку по ипотеке | Ипотека |
| `/mortgages` | GET | `getMortgages` | Получить список заявок на ипотеку | Ипотека |
| `/mortgages` | POST | `addMortgage` | Добавить заявку на ипотеку | Ипотека |
| `/mortgages/{mortgageId}` | DELETE | `deleteMortgage` | Удалить заявку | Ипотека |
| `/mortgages/{mortgageId}` | GET | `getMortgage` | Посмотреть заявку на ипотеку | Ипотека |
| `/mortgages/{mortgageId}` | PUT | `updateMortgage` | Обновить заявку на ипотеку | Ипотека |
| `/mortgages/{mortgageId}/externalForm` | GET | `getExternalForm` | Посмотреть ссылку на ипотечную анкету | Ипотека |
| `/objectOrganizations` | GET | `getObjectOrganizations` | Получить список записей об организациях дома | Дома |
| `/objectOrganizations` | POST | `addObjectOrganization` | Добавить запись об организации дома | Дома |
| `/objectOrganizations/{objectOrganizationId}` | DELETE | `deleteObjectOrganization` | Удалить запись об организации дома | Дома |
| `/objectOrganizations/{objectOrganizationId}` | GET | `getObjectOrganization` | Получить запись об организации дома | Дома |
| `/objectOrganizations/{objectOrganizationId}` | PUT | `updateObjectOrganization` | Обновить запись об организации дома | Дома |
| `/objectRepresentativeTypes` | GET | `getObjectRepresentativeTypes` | Получить список типов представителей по дому | Пользователи |
| `/objectRepresentatives` | GET | `getObjectRepresentatives` | Получить список представителей по дому | Дома |
| `/objectRepresentatives` | POST | `addObjectRepresentative` | Добавить представителя по дому | Дома |
| `/objectRepresentatives/{objectRepresentativeId}` | DELETE | `deleteObjectRepresentative` | Удалить представителя по дому | Дома |
| `/objectRepresentatives/{objectRepresentativeId}` | GET | `getObjectRepresentative` | Получить представителя по дому | Дома |
| `/objectRepresentatives/{objectRepresentativeId}` | PUT | `updateObjectRepresentative` | Обновить представителя по дому | Дома |
| `/organizationTypes` | GET | `getOrganizationTypes` | Получить список типов организаций | Организации |
| `/organizations` | GET | `getOrganizations` | Получить список организаций | Организации |
| `/organizations` | POST | `addOrganization` | Добавить организацию | Организации |
| `/organizations/{organizationId}` | DELETE | `deleteOrganization` | Удалить организацию | Организации |
| `/organizations/{organizationId}` | GET | `getOrganization` | Посмотреть организацию | Организации |
| `/organizations/{organizationId}` | PUT | `updateOrganization` | Редактировать организацию | Организации |
| `/owners/{ownerType}/{ownerId}/attachments` | GET | `getAttachments` | Получить прикрепленные к объекту файлы | Файлы |
| `/owners/{ownerType}/{ownerId}/attachments` | POST | `addAttachment` | Добавить файл к объекту | Файлы |
| `/owners/{ownerType}/{ownerId}/attachments/{fileId}` | DELETE | `deleteAttachment` | Удалить файл объекта | Файлы |
| `/owners/{ownerType}/{ownerId}/attachments/{fileId}` | PUT | `updateAttachment` | Обновить файл у объекта | Файлы |
| `/owners/{ownerType}/{ownerId}/comments` | GET | `getEntityComments` | Получить комментарии * | Комментарии |
| `/owners/{ownerType}/{ownerId}/comments` | POST | `addEntityComment` | Отправить комментарий * | Комментарии |
| `/owners/{ownerType}/{ownerId}/comments/{commentId}` | DELETE | `deleteEntityComment` | Удалить комментарий | Комментарии |
| `/owners/{ownerType}/{ownerId}/comments/{commentId}` | GET | `getEntityComment` | Получить комментарий | Комментарии |
| `/owners/{ownerType}/{ownerId}/comments/{commentId}` | PUT | `updateEntityComment` | Обновить комментарий | Комментарии |
| `/owners/{ownerType}/{ownerId}/infoBlocks` | GET | `getInfoBlocks` | Получить список инфоблоков | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks` | POST | `addInfoBlock` | Добавить инфоблок | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}` | DELETE | `deleteInfoBlock` | Удалить инфоблок | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}` | GET | `getInfoBlock` | Получить инфоблок | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}` | PUT | `updateInfoBlock` | Обновить инфоблок | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items` | GET | `getInfoBlockItems` | Получить список элементов инфоблока | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items` | POST | `addInfoBlockItem` | Добавить элемент в инфоблок | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items/{infoBlockItemId}` | DELETE | `deleteInfoBlockItem` | Удалить элемент инфоблока | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items/{infoBlockItemId}` | GET | `getInfoBlockItem` | Получить элемент инфоблока | Инфоблоки |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items/{infoBlockItemId}` | PUT | `updateInfoBlockItem` | Обновить элемент инфоблока | Инфоблоки |
| `/paymentSchemes` | GET | `getPaymentSchemes` | Получить список типов оплаты | Сделки |
| `/personalDocumentTypes` | GET | `getPersonalDocumentTypes` | Получить список типов удостоверения личности | Пользователи |
| `/plans` | GET | `getPlans` | Получить список доступных планов по дому | Планы |
| `/plans` | POST | `addPlan` | Создать план | Планы |
| `/plans/{planId}` | DELETE | `deletePlan` | Удалить план | Планы |
| `/plans/{planId}` | GET | `getPlan` | Получить план | Планы |
| `/plans/{planId}` | PUT | `updatePlan` | Обновление плана | Планы |
| `/polygons/` | GET | `getPolygons` | Получть области разметки на плане | Планы |
| `/polygons/` | POST | `addPolygon` | Создать области разметки на плане | Планы |
| `/polygons/{polygonId}` | DELETE | `deletePolygon` | Удалить область разметки | Планы |
| `/polygons/{polygonId}` | PUT | `updatePolygon` | Обновление области разметки | Планы |
| `/portfolios` | GET | `getPortfolios` | Просмотреть список портфелей | Планирование работ |
| `/portfolios` | POST | `createPortfolio` | Создать портфель | Планирование работ |
| `/portfolios/{id}` | DELETE | `deletePortfolio` | Удалить портфель | Планирование работ |
| `/portfolios/{id}` | GET | `getPortfolio` | Просмотреть портфель | Планирование работ |
| `/portfolios/{id}` | PUT | `updatePortfolio` | Обновить портфель | Планирование работ |
| `/prices` | GET | `getPrices` | Получить список видов цен | Цены |
| `/prices` | POST | `addPrice` | Создать вид цены | Цены |
| `/prices/{priceId}` | DELETE | `deletePrice` | Удалить вид цены | Цены |
| `/prices/{priceId}` | GET | `getPrice` | Просмотреть вид цены | Цены |
| `/prices/{priceId}` | PUT | `updatePrice` | Изменить вид цены | Цены |
| `/projectSections` | GET | `getProjectSections` | Просмотреть список разделов проектной документации | Производство работ |
| `/projectSections/{projectSectionId}` | GET | `getProjectSection` | Получить раздел проектной документации | Производство работ |
| `/projects` | GET | `getProjects` | Просмотреть список проектов | Планирование работ |
| `/projects` | POST | `addProject` | Создать проект | Планирование работ |
| `/projects/{projectId}` | DELETE | `deleteProject` | Удалить проект | Планирование работ |
| `/projects/{projectId}` | GET | `getProject` | Получить проект | Планирование работ |
| `/projects/{projectId}` | PUT | `updateProject` | Обновить проект | Планирование работ |
| `/providers/{providerId}/deals` | POST | `addOrUpdateDealByProvider` | Обновить/создать сделку по провайдеру | Сделки |
| `/references` | GET | `getReferences` | Получить список справочников | Справочники |
| `/references` | POST | `addReference` | Создать справочник | Справочники |
| `/references/{code}/items` | GET | `getReferenceItems` | Получить список элементов справочника | Справочники |
| `/references/{code}/items` | POST | `addReferenceItem` | Создать элемент справочника | Справочники |
| `/references/{code}/items/{itemId}` | DELETE | `deleteReferenceItem` | Удалить элемент справочника | Справочники |
| `/references/{code}/items/{itemId}` | GET | `getReferenceItem` | Получить элемент справочника | Справочники |
| `/references/{code}/items/{itemId}` | PUT | `updateReferenceItem` | Обновить элемент справочника | Справочники |
| `/references/{referenceId}` | DELETE | `deleteReference` | Удалить справочник | Справочники |
| `/references/{referenceId}` | GET | `getReference` | Получить справочник | Справочники |
| `/references/{referenceId}` | PUT | `updateReference` | Изменить справочник | Справочники |
| `/remarkCategories` | GET | `getRemarkCategories` | Получить список категорий замечаний | Замечания |
| `/remarkCategories` | POST | `addRemarkCategory` | Добавить категорию замечания | Замечания |
| `/remarkCategories/{categoryId}` | DELETE | `deleteRemarkCategory` | Удалить категорию замечания | Замечания |
| `/remarkCategories/{categoryId}` | GET | `getRemarkCategory` | Просмотреть категорию замечания | Замечания |
| `/remarkCategories/{categoryId}` | PUT | `updateRemarkCategory` | Обновить категорию замечания | Замечания |
| `/remarkCategorySettings` | POST | `addRemarkCategorySetting` | Создать настройку | Замечания |
| `/remarkCategorySettings/` | GET | `getRemarkCategorySettings` | Получить список настроек категорий замечаний | Замечания |
| `/remarkCategorySettings/{settingId}` | DELETE | `deleteRemarkCategorySetting` | Удалить настройку | Замечания |
| `/remarkCategorySettings/{settingId}` | GET | `getRemarkCategorySetting` | Просмотреть настройку | Замечания |
| `/remarkCategorySettings/{settingId}` | PUT | `updatetRemarkCategorySetting` | Изменить настройку | Замечания |
| `/remarkDefectTypes` | GET | `getDefectTypes` | Получить список возможных типов дефектов | Замечания |
| `/remarkStatuses` | GET | `getRemarkStatuses` | Получить список возможных статусов | Замечания |
| `/remarkTemplates` | GET | `getRemarkTemplates` | Получить список шаблонов замечаний | Замечания |
| `/remarkTemplates` | POST | `addRemarkTemplate` | Добавить шаблон замечаний | Замечания |
| `/remarkTemplates/{remarkTemplateId}` | DELETE | `deleteRemarkTemplate` | Удалить шаблон замечаний | Замечания |
| `/remarkTemplates/{remarkTemplateId}` | GET | `getRemarkTemplate` | Получить шаблон замечаний | Замечания |
| `/remarkTemplates/{remarkTemplateId}` | PUT | `updateRemarkTemplate` | Изменить шаблон замечаний | Замечания |
| `/remarkWorkTypes` | GET | `getRemarkWorkTypes` | Получить список возможных видов работ | Замечания |
| `/remarks` | GET | `getRemarks` | Получить список замечаний | Замечания |
| `/remarks` | POST | `addRemark` | Создать замечание | Замечания |
| `/remarks/{remarkId}` | DELETE | `deleteRemark` | Удалить замечание | Замечания |
| `/remarks/{remarkId}` | GET | `getRemark` | Просмотреть замечание | Замечания |
| `/remarks/{remarkId}` | PUT | `updateRemark` | Изменить замечание | Замечания |
| `/reservationTypes` | GET | `getReservationTypes` | Получить список типов бронирования | Сделки |
| `/reservationTypes` | POST | `addReservationType` | Добавить тип бронирования | Сделки |
| `/reservationTypes/{typeId}` | DELETE | `deleteReservationType` | Удалить тип бронирования | Сделки |
| `/reservationTypes/{typeId}` | GET | `getReservationType` | Получить тип бронирования | Сделки |
| `/reservationTypes/{typeId}` | PUT | `updateReservationType` | Изменить тип бронирования | Сделки |
| `/revisionStatuses` | GET | `getRevisionStatuses` | Получить список возможных статусов | Ревизии |
| `/revisionTypes` | GET | `getRevisionTypes` | Получить список типов ревизий | Ревизии |
| `/revisionTypes` | POST | `addRevisionTypes` | Создать тип ревизии | Ревизии |
| `/revisionTypes/{typeId}` | DELETE | `deleteRevisionTypes` | Удалить тип ревизии | Ревизии |
| `/revisionTypes/{typeId}` | GET | `getRevisionType` | Получить тип ревизии | Ревизии |
| `/revisionTypes/{typeId}` | PUT | `updateRevisionTypes` | Изменить тип ревизии | Ревизии |
| `/revisions` | GET | `getRevisions` | Получить список ревизий | Ревизии |
| `/revisions` | POST | `addRevision` | Создать ревизию | Ревизии |
| `/revisions/{revisionId}` | DELETE | `deleteRevision` | Удалить ревизию | Ревизии |
| `/revisions/{revisionId}` | GET | `getRevision` | Получить ревизию | Ревизии |
| `/revisions/{revisionId}` | PUT | `updateRevision` | Изменить ревизию | Ревизии |
| `/revisions/{revisionId}/actions` | POST | `actionRevision` | Действия с ревизией | Ревизии |
| `/roles` | GET | `getRoles` | Получить список ролей | Пользователи |
| `/roles` | POST | `addRole` | Создать роль | Пользователи |
| `/roles/{roleId}` | DELETE | `deleteRole` | Удалить роль | Пользователи |
| `/roles/{roleId}` | PUT | `updateRole` | Обновить роль | Пользователи |
| `/roomBadges` | GET | `getRoomBadges` | Получить список доступных тегов помещений | Дома |
| `/roomMeters` | GET | `getRoomMeters` | Получить список приборов учета по помещениям | Помещения |
| `/roomMeters` | POST | `addRoomMeter` | Добавить прибор учета в помещение | Помещения |
| `/roomMeters/{roomMeterId}` | DELETE | `deleteRoomMeter` | Удалить прибор учета из помещения | Помещения |
| `/roomMeters/{roomMeterId}` | GET | `getRoomMeter` | Получить прибор учета | Помещения |
| `/roomMeters/{roomMeterId}` | PUT | `updateRoomMeter` | Обновить прибор учета в помещении | Помещения |
| `/roomTypes` | GET | `getRoomTypes` | Получить список типов помещений | Помещения |
| `/roomTypes` | POST | `addRoomType` | Создать тип помещения | Помещения |
| `/roomTypes/{roomTypeId}` | DELETE | `deleteRoomType` | Удалить тип помещения | Помещения |
| `/roomTypes/{roomTypeId}` | GET | `getRoomType` | Получить тип помещения | Помещения |
| `/roomTypes/{roomTypeId}` | PUT | `updateRoomType` | Изменить тип помещения | Помещения |
| `/rooms` | GET | `getRooms` | Получить список помещений | Помещения |
| `/rooms` | POST | `addRoom` | Добавить помещение | Помещения |
| `/rooms/actions` | POST | `roomActions` | Массовые действия с помещениями | Помещения |
| `/rooms/statuses` | GET | `getRoomStatuses` | Получить список возможных статусов * | Помещения |
| `/rooms/types` | GET | `getRoomTypesCollection` | Получить список типов помещений | Помещения |
| `/rooms/{roomId}` | DELETE | `deleteRoom` | Удалить помещение | Помещения |
| `/rooms/{roomId}` | GET | `getRoom` | Получить помещение | Помещения |
| `/rooms/{roomId}` | PUT | `updateRoom` | Обновить информацию о помещении | Помещения |
| `/rooms/{roomId}/recommended` | GET | `getRecommendedRooms` | Получить список рекомендуемых помещений к данному помещению | Помещения |
| `/scheduleWorks` | GET | `getScheduleWorks` | Просмотреть список работ в графике | Планирование работ |
| `/scheduleWorks` | POST | `addScheduleWork` | Создать работу в графике | Планирование работ |
| `/scheduleWorks/{scheduleWorkId}` | DELETE | `deleteScheduleWork` | Удалить работу в графике | Планирование работ |
| `/scheduleWorks/{scheduleWorkId}` | GET | `getScheduleWork` | Получить работу в графике | Планирование работ |
| `/scheduleWorks/{scheduleWorkId}` | PUT | `updateScheduleWork` | Обновить работу в графике | Планирование работ |
| `/schedules` | GET | `getSchedules` | Просмотреть список графиков | Планирование работ |
| `/schedules` | POST | `addSchedule` | Создать график | Планирование работ |
| `/schedules/{scheduleId}` | DELETE | `deleteSchedule` | Удалить график | Планирование работ |
| `/schedules/{scheduleId}` | GET | `getSchedule` | Получить график | Планирование работ |
| `/schedules/{scheduleId}` | PUT | `updateSchedule` | Обновить график | Планирование работ |
| `/sections` | GET | `getSections` | Получить список секций дома | Дома |
| `/sections` | POST | `addSection` | Добавить секцию дома | Дома |
| `/sections/{sectionId}` | DELETE | `deleteSection` | Удалить секцию дома | Дома |
| `/sections/{sectionId}` | PUT | `updateSection` | Обновить секцию дома | Дома |
| `/signatureStatuses` | GET | `getSignatureStatuses` | Получить список возможных статусов эцп | ЭЦП |
| `/signatures` | GET | `getSignatures` | Получить список цифровых подписей | ЭЦП |
| `/signatures` | POST | `addSignature` | Создать ЭЦП | ЭЦП |
| `/signatures/{signatureId}` | GET | `getSignature` | Получить цифровую подпись | ЭЦП |
| `/signatures/{signatureId}` | PUT | `updateSignature` | Обновить ЭЦП | ЭЦП |
| `/signatures/{signatureId}/actions` | POST | `actionSignature` | Действия с ЭЦП | ЭЦП |
| `/signs` | GET | `getSigns` | Получить подписи | ЭЦП |
| `/staffUsers` | GET | `getStaffUsers` | Получить список сотрудников | Сотрудники |
| `/staffUsers` | POST | `addStaffUser` | Добавить сотрудника | Сотрудники |
| `/staffUsers/{staffUserId}` | DELETE | `deleteStaffUser` | Удалить сотрудника | Сотрудники |
| `/staffUsers/{staffUserId}` | GET | `getStaffUser` | Получить сотрудника * | Сотрудники |
| `/staffUsers/{staffUserId}` | PUT | `updateStaffUser` | Обновить информацию сотрудника * | Сотрудники |
| `/standards` | GET | `getStandards` | Получить список нормативов | Справочники |
| `/standards` | POST | `addStandard` | Создать норматив | Справочники |
| `/standards/{itemId}` | DELETE | `deleteStandard` | Удалить норматив | Справочники |
| `/standards/{itemId}` | GET | `getStandard` | Просмотреть норматив | Справочники |
| `/standards/{itemId}` | PUT | `updateStandard` | Обновить норматив | Справочники |
| `/tags` | GET | `getTags` | Получить список тегов | Теги |
| `/tags` | POST | `addTag` | Создать тег | Теги |
| `/tags/{tagId}` | DELETE | `deleteTag` | Удалить тег | Теги |
| `/tags/{tagId}` | GET | `getTag` | Просмотреть тег | Теги |
| `/tags/{tagId}` | PUT | `updateTag` | Изменить тег | Теги |
| `/taskCategories` | GET | `getTasksCatrgories` | Просмотреть список категорий задач | Задачи |
| `/taskCategories` | POST | `addTaskCategory` | Создать категорию задачи | Задачи |
| `/taskCategories/{categoryId}` | DELETE | `deleteTaskCategory` | Удалить категорию задачи | Задачи |
| `/taskCategories/{categoryId}` | GET | `getTaskCategory` | Получить категорию задачи | Задачи |
| `/taskCategories/{categoryId}` | PUT | `updateTaskCategory` | Обновить категорию задачи | Задачи |
| `/tasks` | GET | `getTasks` | Просмотреть список задач | Задачи |
| `/tasks` | POST | `addTask` | Создать задачу | Задачи |
| `/tasks/{taskId}` | DELETE | `deleteTask` | Удалить задачу | Задачи |
| `/tasks/{taskId}` | GET | `getTask` | Получить задачу | Задачи |
| `/tasks/{taskId}` | PUT | `updateTask` | Обновить задачу | Задачи |
| `/telegram/setWebhook` | POST | `setWebhook` | Установить вебхук для бота | Телеграм |
| `/templates` | GET | `getTemplates` | Получить список шаблонов | Шаблоны |
| `/templates` | POST | `addTemplate` | Создать шаблон | Шаблоны |
| `/templates/{templateId}` | DELETE | `deleteTemplate` | Удалить шаблон | Шаблоны |
| `/templates/{templateId}` | GET | `getTemplate` | Получить шаблон | Шаблоны |
| `/templates/{templateId}` | PUT | `updateTemplate` | Обновить шаблон | Шаблоны |
| `/templates/{templateId}/actions` | POST | `actionTemplates` | Действия с шаблонами | Шаблоны |
| `/units` | GET | `getUnits` | Просмотреть список единиц измерения | Планирование работ |
| `/units` | POST | `addUnit` | Создать единицу измерения | Планирование работ |
| `/units/{unitId}` | DELETE | `deleteUnit` | Удалить единицу измерения | Планирование работ |
| `/units/{unitId}` | GET | `getUnit` | Получить единицу измерения | Планирование работ |
| `/units/{unitId}` | PUT | `updateUnit` | Обновить единицу измерения | Планирование работ |
| `/userSettings` | GET | `getUserSettings` | Получить список пользовательских настроек | Пользовательские настройки |
| `/userSettings` | POST | `createUserSetting` | Создать пользовательскую настройку | Пользовательские настройки |
| `/userSettings/{id}` | DELETE | `deleteUserSetting` | Удалить пользовательскую настройку | Пользовательские настройки |
| `/userSettings/{id}` | GET | `getUserSetting` | Просмотреть пользовательскую настройку | Пользовательские настройки |
| `/userSettings/{id}` | PUT | `updateUserSetting` | Обновить пользовательскую настройку | Пользовательские настройки |
| `/userStatuses` | GET | `getUserStatuses` | Получить список статусов пользователей | Пользователи |
| `/users` | GET | `getUsers` | Получить список пользователей | Пользователи |
| `/users` | POST | `addUser` | Создать пользователя | Пользователи |
| `/users/{userId}` | DELETE | `deleteUser` | Удалить пользователя | Пользователи |
| `/users/{userId}` | GET | `getUser` | Получить пользователя * | Пользователи |
| `/users/{userId}` | PUT | `updateUser` | Обновить информацию пользователя * | Пользователи |
| `/users/{userId}/personalData` | PUT | `updateOrCreatePersonalData` | Обновить персональную информацию о пользователе | Пользователи |
| `/viewHistories` | GET | `getViewHistories` | Получить историю просмотра | История изменений |
| `/workAccumulationRegisters` | GET | `getWorkAccumulationRegisters` | Получить список записей регистра накопления работ | Производство работ |
| `/workActRows` | POST | `addWorkActRow` | Добавить строку акта о приемке работ | Производство работ |
| `/workActRows/{workActRowId}` | DELETE | `deleteWorkActRow` | Удалить строку акта о приемке работ | Производство работ |
| `/workActRows/{workActRowId}` | PUT | `updateWorkActRow` | Изменить строку акта о приемке работ | Производство работ |
| `/workActStatuses` | GET | `getWorkActStatuses` | Получить список статусов акта о выполненной работе | Производство работ |
| `/workActStatuses/{statusId}` | GET | `getWorkActStatus` | Получить статус акта о выполненной работе | Производство работ |
| `/workActs` | GET | `getWorkActs` | Получить список актов выполненной работе | Производство работ |
| `/workActs` | POST | `addWorkAct` | Создать акт о выполненной работе | Производство работ |
| `/workActs/{actId}` | GET | `getWorkAct` | Получить Акт о приемке выполненных работ | Производство работ |
| `/workActs/{actId}` | PUT | `updateWorkAct` | Изменить акт о выполненной работе | Производство работ |
| `/workActs/{actId}/actions` | POST | `actionWorkAct` | Действия с актом выполненых работ | Производство работ |
| `/workJournalRows` | POST | `addWorkJournalRow` | Добавить строку журнала выполненных работ | Производство работ |
| `/workJournalRows/{workJournalRowId}` | DELETE | `deleteWorkJournalRow` | Удалить строку журнала выполненных работ | Производство работ |
| `/workJournalRows/{workJournalRowId}` | PUT | `updateWorkJournalRow` | Изменить строку журнала выполненных работ | Производство работ |
| `/workJournalStatuses` | GET | `getWorkJournalStatuses` | Получить список статусов журналов выполненных работ | Производство работ |
| `/workJournals` | GET | `getWorkJournals` | Получить список журналов выполненных работ | Производство работ |
| `/workJournals` | POST | `addWorkJournal` | Создать журнал выполненных работ | Производство работ |
| `/workJournals/{workJournalId}` | GET | `getWorkJournal` | Получить журнал выполненных работ | Производство работ |
| `/workJournals/{workJournalId}` | PUT | `updateWorkJournal` | Изменить журнал выполненных работ | Производство работ |
| `/workLogs` | GET | `getWorkLogs` | Просмотреть список записей журнала работ | Записи журнала работ |
| `/workLogs` | POST | `addWorkLog` | Создать запись журнала работ | Записи журнала работ |
| `/workLogs/{workLogId}` | DELETE | `deleteWorkLog` | Удалить запись журнала работ | Записи журнала работ |
| `/workLogs/{workLogId}` | GET | `getWorkLog` | Получить запись журнала работ | Записи журнала работ |
| `/workLogs/{workLogId}` | PUT | `updateWorkLog` | Обновить запись журнала работ | Записи журнала работ |
| `/workMaterials` | GET | `getWorkMaterials` | Просмотреть список материалов внутри работы | Планирование работ |
| `/workMaterials` | POST | `addWorkMaterial` | Создать материал внутри работы | Планирование работ |
| `/workMaterials/{workMaterialId}` | DELETE | `deleteWorkMaterial` | Удалить материал в работе | Планирование работ |
| `/workMaterials/{workMaterialId}` | GET | `getWorkMaterial` | Получить материал в работе | Планирование работ |
| `/workMaterials/{workMaterialId}` | PUT | `updateWorkMaterial` | Обновить материал в работе | Планирование работ |
| `/workRegisterStatuses` | GET | `getWorkRegisterStatuses` | Получить список статусов отчета о выполненной работе | Производство работ |
| `/workRegisterStatuses/{statusId}` | GET | `getWorkRegisterStatus` | Получить статус отчета о выполненной работе | Производство работ |
| `/workRegisters` | GET | `getWorkRegisters` | Получить список отчетов о выполненной работе | Производство работ |
| `/workRegisters` | POST | `addWorkRegister` | Создать отчет о выполненной работе | Производство работ |
| `/workRegisters/{registerId}` | GET | `getWorkRegister` | Получить отчет о выполненной работе | Производство работ |
| `/workRegisters/{registerId}` | PUT | `updateWorkRegister` | Изменить отчет о выполненной работе | Производство работ |
| `/workRegisters/{workRegisterId}/actions` | POST | `actionWorkRegisterId` | Действия с отчетами о выполненной работе | Производство работ |
| `/workStages` | GET | `getWorkStages` | Список этапов работ | Планирование работ |
| `/workStages` | POST | `addWorkStage` | Создать этап работ | Планирование работ |
| `/workStages/{workStageId}` | DELETE | `deleteWorkStage` | Удалить этап работ | Планирование работ |
| `/workStages/{workStageId}` | GET | `getWorkStage` | Получить этап работ | Планирование работ |
| `/workStages/{workStageId}` | PUT | `updateWorkStage` | Обновить этап работ | Планирование работ |
| `/workTypes` | GET | `getWorkTypes` | Просмотреть список видов работ | Планирование работ |
| `/workTypes` | POST | `addWorkType` | Создать вид работы | Планирование работ |
| `/workTypes/{workTypeId}` | DELETE | `deleteWorkType` | Удалить вид работы | Планирование работ |
| `/workTypes/{workTypeId}` | GET | `getWorkType` | Получить вид работы | Планирование работ |
| `/workTypes/{workTypeId}` | PUT | `updateWorkType` | Обновить вид работы | Планирование работ |
| `/works` | GET | `getWorks` | Просмотреть список работ в план-графике | Планирование работ |
| `/works` | POST | `addWork` | Создать работу | Планирование работ |
| `/works/{workId}` | DELETE | `deleteWork` | Удалить работу | Планирование работ |
| `/works/{workId}` | GET | `getWork` | Получить работу | Планирование работ |
| `/works/{workId}` | PUT | `updateWork` | Обновить работу | Планирование работ |
| `/works/{workId}/actions` | POST | `actionWorks` | Действия с работами | Производство работ |
