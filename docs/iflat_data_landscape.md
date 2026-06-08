# Карта данных CRM (чтение API + OpenAPI 1.4.0)

Сгенерировано: **2026-05-10 20:24 UTC**.

## Политика доступа

- К бизнес-сущностям обращались **только методом GET**.
- Единственный **POST** — `POST /api/v1/oauth/token` для получения Bearer-токена (не изменяет объекты в системе).
- Мутации (`POST`/`PUT`/`PATCH`/`DELETE` к ресурсам) **не выполнялись**.

## Сводка прогона GET

- Операций GET в спецификации: **222**.
- Запросов выполнено (уникальных шаблонов пути): **170**.
- Шаблонов без ни одного выполненного GET (не удалось подставить все path-параметры из цепочки списков): **52** — см. параметры и ответы в `iflat_openapi_1.4.0.json`.
- Ответ **200**: **143**, иначе / исключение: **27**.
- Итераций подстановки path-параметров из списков: **3** (накопленные id: agentDocumentId=1, buildingObjectTypeId=1, categoryId=1, checkListId=1, claimId=1, commentId=1, dealId=1, districtId=1, divisionId=1, documentId=1, entityAttributeId=1, expertId=1, floorId=1, houseId=1, houseMeterId=1, inspectionId=2, inspectionStepId=1, itemId=1, messageTemplateId=1, objectOrganizationId=1, objectRepresentativeId=1, organizationId=1, planId=1, projectSectionId=1, referenceId=1, remarkId=1, remarkTemplateId=1, roleId=1, roomId=1, roomMeterId=1, roomTypeId=1, sectionId=1, signatureId=1, staffUserId=1, stepId=1, tagId=1, taskId=1, typeId=2, unitId=1, userId=1).

### Как интерпретировать ошибки

- **404** на отдельном ресурсе — возможно, неверный или чужой id из «черновика» банка.
- **422** — часто не хватает обязательных query-параметров (спецификация не помечает их required).
- Пустой банк для вложенных путей — шаблон так и остался непробитым.

## Откуда брать данные (обзор)

| Задача BI / учёт | Основные GET (спецификация) | Заметки |
|------------------|----------------------------|---------|
| Тип ОН (квартира, ММ, кладовая…) | `/rooms`, `/rooms/types`, embed `room_type` | Фильтр `roomType`, в теле — связь `room_type`. |
| Статус помещения | `/rooms`, `/rooms/statuses`, embed `status` | `statusId`, объект `status` с цветами. |
| Сделки, ДДУ/ДКП | `/deals`, embed из описания deal | Поля договора / `contract_type_id` — сверять с живым ответом и справочниками. |
| Приёмки, ответственные | `/inspections`, связь по `roomId` | Пагинация `page`/`perPage`; состав полей — в ответе и схеме Inspection. |
| ЭЦП / бумага по АПП | `/deals` с embed (см. параметр в Swagger к вашей версии), документы | Часто в связанных документах/сделке; точные embed — в OpenAPI для `/deals/{id}`. |
| ЖК / фаза / корпус | `/districts`, `/houses`, `/sections`, `/rooms` (`districtId`, `houseId`) | Иерархию уточнять по полям House/Section в ответах. |
| Отделка / white box | `/rooms` + embed `decoration` | Коды отделки — справочник и поля в Room. |

## Таблица всех GET из OpenAPI + результат пробы


| Путь | operationId | Теги | GET статус | Примечание |
|------|-------------|------|------------|------------|
| `/agentDocuments` | `getAgentDocuments` | Пользователи | 200 |  |
| `/agentDocuments/{agentDocumentId}` | `getAgentDocumentId` | Пользователи | 200 |  |
| `/approvalActions` | `getApprovalActions` | Согласование | 200 |  |
| `/approvalActions/{approvalActionId}` | `getApprovalAction` | Согласование | — |  |
| `/approvalChains` | `getApprovalChains` | Согласование | 200 |  |
| `/approvalChains/{approvalChainId}` | `getApprovalChain` | Согласование | — |  |
| `/approvalRequests` | `getApprovalRequests` | Согласование | 200 |  |
| `/approvalRequests/{approvalRequestId}` | `getApprovalRequest` | Согласование | — |  |
| `/approvalSteps` | `getApprovalSteps` | Согласование | 200 |  |
| `/approvalSteps/{approvalStepId}` | `getApprovalStep` | Согласование | — |  |
| `/audits` | `getAudits` | История изменений | 200 |  |
| `/banks` | `getBanks` | Ипотека | 200 |  |
| `/banks/{bankId}` | `getBank` | Ипотека | — |  |
| `/buildingObjectStatuses` | `getBuildingObjectStatuses` | Объекты | 200 |  |
| `/buildingObjectTypes` | `getBuildingObjectTypes` | Объекты | 200 |  |
| `/buildingObjectTypes/{buildingObjectTypeId}` | `getBuildingObjectType` | Объекты | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/buildingObjects` | `getBuildingObjects` | Объекты | 200 |  |
| `/buildingObjects/{buildingObjectId}` | `getbuildingObject` | Объекты | — |  |
| `/checkListSteps` | `getSteps` | Чек-листы | 200 |  |
| `/checkListSteps/{stepId}` | `getStep` | Чек-листы | 200 |  |
| `/checkLists` | `getCheckLists` | Чек-листы | 200 |  |
| `/checkLists/{checkListId}` | `getCheckList` | Чек-листы | 200 |  |
| `/claimCategories` | `getClaimCategories` | Технические заявки | 200 |  |
| `/claimCategories/{claimCategoryId}` | `getClaimCategory` | Технические заявки | — |  |
| `/claimPriorities` | `getPriorities` | Технические заявки | 200 |  |
| `/claimTypes` | `getClaimTypes` | Технические заявки | 200 |  |
| `/claims` | `getClaims` | Технические заявки | 200 |  |
| `/claims/statuses` | `getClaimsStatuses` | Технические заявки | 200 |  |
| `/claims/{claimId}` | `getClaim` | Технические заявки | 200 |  |
| `/claims/{claimId}/remarks` | `getClaimRemarks` | Технические заявки | 200 |  |
| `/comments` | `getComments` | Комментарии | 200 |  |
| `/confirmationDocumentTypes` | `getConfirmationDocumentTypes` | Пользователи | 200 |  |
| `/contracts` | `getContracts` | Договоры | 200 |  |
| `/contracts/{contractId}` | `getContract` | Договоры | — |  |
| `/dealRegistrationStatuses` | `getDealRegistrationStatuses` | Регистрация сделок в Росреестре | 200 |  |
| `/dealRegistrations` | `getDealRegistrations` | Регистрация сделок в Росреестре | 200 |  |
| `/dealRegistrations/{dealRegistrationId}` | `getDealRegistration` | Регистрация сделок в Росреестре | — |  |
| `/dealRegistrations/{dealRegistrationId}/externalDocumentTypes` | `getExternalDocumentTypes` | Регистрация сделок в Росреестре | — |  |
| `/dealStages` | `getDealStages` | Сделки | 200 |  |
| `/dealStatuses` | `getDealStatuses` | Сделки | 200 |  |
| `/deals` | `getDeals` | Сделки | 200 |  |
| `/deals/contractTypes` | `getContractTypes` | Сделки | 200 |  |
| `/deals/{dealId}` | `getDeal` | Сделки | 200 |  |
| `/deals/{dealId}/clients` | `getDealClients` | Сделки: покупатели | 200 |  |
| `/deals/{dealId}/providers/{providerId}/statuses` | `providerDealStatuses` | Сделки | — |  |
| `/digitalDocumentStatuses` | `getDigitalDocumentStatuses` | Электронные документы | 200 |  |
| `/digitalDocuments` | `getDigitalDocuments` | Электронные документы | 200 |  |
| `/digitalDocuments/{documentId}` | `getDigitalDocument` | Электронные документы | 200 |  |
| `/districts` | `getDistricts` | ЖК | 200 |  |
| `/districts/{districtId}` | `getDistrict` | ЖК | 200 |  |
| `/divisions` | `getDivisions` | Пользователи | 200 |  |
| `/divisions/{divisionId}` | `getDivision` | Пользователи | 200 |  |
| `/documentPages` | `getDocumentPages` | Документы | 200 |  |
| `/documentPages/{pageId}` | `getDocumentPage` | Документы | — |  |
| `/documentTypes` | `getDocumentTypes` | Документы | 200 |  |
| `/documentTypes/{typeId}` | `getDocumentType` | Документы | 200 |  |
| `/documents` | `getDocuments` | Документы | 200 |  |
| `/documents/{documentId}` | `getDocument` | Документы | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/entityAttributes` | `getEntityAttributes` | Справочники | 200 |  |
| `/entityAttributes/{entityAttributeId}` | `getEntityAttribute` | Справочники | 200 |  |
| `/entityConfigs` | `getEntityConfigs` | Сущности | 200 |  |
| `/entityConfigs/{entity}` | `getEntityConfig` | Сущности | — |  |
| `/entityVersions` | `getEntityVersions` | Сущности | 200 |  |
| `/estimates` | `getEstimates` | Сметы | 200 |  |
| `/estimates/{estimateId}` | `getEstimate` | Сметы | — |  |
| `/export/entities/{entity}/{entityId}/templates/{templateName}` | `exportEntity` | Экспорт | — |  |
| `/export/pdf/rooms/{roomId}` | `savePdf` | Помещения | 200 |  |
| `/externalObjects/{type}/maps` | `getExternalObjectMaps` | Объекты | — |  |
| `/floors` | `getFloors` | Дома | 200 |  |
| `/formSchemas` | `getFormSchemas` | Конфигурация форм | 200 |  |
| `/formSchemas/{formSchemaId}` | `getFormSchema` | Конфигурация форм | — |  |
| `/freeTimes` | `getFreeTimes` | Задачи | 400 | {<br>"message": "Не передан часовой пояс",<br>"success": false<br>} |
| `/grades` | `getGrades` | Пользователи | 200 |  |
| `/grades/{gradeId}` | `getGrade` | Пользователи | — |  |
| `/histories` | `getHistories` | История изменений | 200 |  |
| `/houseMeters` | `getHouseMeters` | Дома | 200 |  |
| `/houseMeters/{houseMeterId}` | `getHouseMeter` | Дома | 200 |  |
| `/houses` | `getHouses` | Дома | 200 |  |
| `/houses/{houseId}` | `getHouse` | Дома | 200 |  |
| `/houses/{houseId}/bimElementsByRemarks` | `getBimElementsByRemarks` | BIM | 200 |  |
| `/houses/{houseId}/bimElementsByWork` | `getBimElementsByWork` | BIM | 500 | {<br>"success": false,<br>"message": "Произошла ошибка, перезагрузите страницу и по…"<br>} |
| `/houses/{houseId}/bimElementsByWorkPercentage` | `getbimElementsByWorkPercentage` | BIM | 200 |  |
| `/houses/{houseId}/bimModel` | `getHouseBimModel` | BIM | 500 | {<br>"success": false,<br>"message": "Произошла ошибка, перезагрузите страницу и по…"<br>} |
| `/houses/{houseId}/inspectionsDays/{date}/times` | `getInspectionDayTimes` | Приемка | — |  |
| `/houses/{houseId}/inspectionsPeriods` | `getInspectionPeriods` | Приемка | 200 |  |
| `/houses/{houseId}/metro` | `getHouseMetro` | Дома | 200 |  |
| `/houses/{houseId}/roomBadges` | `getHouseRoomBadges` | Дома | 200 |  |
| `/inspectionExperts` | `getInspectionExperts` | Приемка | 200 |  |
| `/inspectionExperts/{expertId}` | `getInspectionExpert` | Приемка | 200 |  |
| `/inspectionFreeDays` | `getInspectionFreeDays` | Приемка | 400 | {<br>"message": "Не указано помещение для поиска доступных дне…",<br>"success": false<br>} |
| `/inspectionMeters` | `getInspectionMeters` | Приемка | 200 |  |
| `/inspectionSteps` | `getInspectionSteps` | Приемка | 200 |  |
| `/inspectionUsers` | `getInspectionUsers` | Приемка | 200 |  |
| `/inspections` | `getInspections` | Приемка | 200 |  |
| `/inspections/statuses` | `getInspectionsStatuses` | Приемка | 200 |  |
| `/inspections/{inspectionId}` | `getInspection` | Приемка | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/leads` | `getLeads` | Лиды | 200 |  |
| `/materialRegisters` | `getMaterialRegisters` | Производство работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/materialRegisters/{registerId}` | `getMaterialRegister` | Производство работ | — |  |
| `/materials` | `getMaterials` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/materials/{materialId}` | `getMaterial` | Планирование работ | — |  |
| `/messageTemplates` | `getMessageTemplates` | Смс шаблоны | 200 |  |
| `/messageTemplates/{messageTemplateId}` | `getmessageTemplate` | Смс шаблоны | 200 |  |
| `/mortgagePrograms` | `getMortgagePrograms` | Ипотека | 200 |  |
| `/mortgageResponseStatuses` | `getMortgageResponseStatuses` | Ипотека | 200 |  |
| `/mortgageResponses` | `getMortgageResponses` | Ипотека | 200 |  |
| `/mortgageResponses/{responseId}` | `getMortgageResponse` | Ипотека | — |  |
| `/mortgages` | `getMortgages` | Ипотека | 200 |  |
| `/mortgages/{mortgageId}` | `getMortgage` | Ипотека | — |  |
| `/mortgages/{mortgageId}/externalForm` | `getExternalForm` | Ипотека | — |  |
| `/objectOrganizations` | `getObjectOrganizations` | Дома | 200 |  |
| `/objectOrganizations/{objectOrganizationId}` | `getObjectOrganization` | Дома | 200 |  |
| `/objectRepresentativeTypes` | `getObjectRepresentativeTypes` | Пользователи | 200 |  |
| `/objectRepresentatives` | `getObjectRepresentatives` | Дома | 200 |  |
| `/objectRepresentatives/{objectRepresentativeId}` | `getObjectRepresentative` | Дома | 200 |  |
| `/organizationTypes` | `getOrganizationTypes` | Организации | 200 |  |
| `/organizations` | `getOrganizations` | Организации | 200 |  |
| `/organizations/{organizationId}` | `getOrganization` | Организации | 200 |  |
| `/owners/{ownerType}/{ownerId}/attachments` | `getAttachments` | Файлы | — |  |
| `/owners/{ownerType}/{ownerId}/comments` | `getEntityComments` | Комментарии | — |  |
| `/owners/{ownerType}/{ownerId}/comments/{commentId}` | `getEntityComment` | Комментарии | — |  |
| `/owners/{ownerType}/{ownerId}/infoBlocks` | `getInfoBlocks` | Инфоблоки | — |  |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}` | `getInfoBlock` | Инфоблоки | — |  |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items` | `getInfoBlockItems` | Инфоблоки | — |  |
| `/owners/{ownerType}/{ownerId}/infoBlocks/{infoBlockId}/items/{infoBlockItemId}` | `getInfoBlockItem` | Инфоблоки | — |  |
| `/paymentSchemes` | `getPaymentSchemes` | Сделки | 200 |  |
| `/personalDocumentTypes` | `getPersonalDocumentTypes` | Пользователи | 200 |  |
| `/plans` | `getPlans` | Планы | 200 |  |
| `/plans/{planId}` | `getPlan` | Планы | 200 |  |
| `/polygons/` | `getPolygons` | Планы | 200 |  |
| `/portfolios` | `getPortfolios` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/portfolios/{id}` | `getPortfolio` | Планирование работ | — |  |
| `/prices` | `getPrices` | Цены | 200 |  |
| `/prices/{priceId}` | `getPrice` | Цены | — |  |
| `/projectSections` | `getProjectSections` | Производство работ | 200 |  |
| `/projectSections/{projectSectionId}` | `getProjectSection` | Производство работ | 200 |  |
| `/projects` | `getProjects` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/projects/{projectId}` | `getProject` | Планирование работ | — |  |
| `/references` | `getReferences` | Справочники | 200 |  |
| `/references/{code}/items` | `getReferenceItems` | Справочники | — |  |
| `/references/{code}/items/{itemId}` | `getReferenceItem` | Справочники | — |  |
| `/references/{referenceId}` | `getReference` | Справочники | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/remarkCategories` | `getRemarkCategories` | Замечания | 200 |  |
| `/remarkCategories/{categoryId}` | `getRemarkCategory` | Замечания | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/remarkCategorySettings/` | `getRemarkCategorySettings` | Замечания | 200 |  |
| `/remarkCategorySettings/{settingId}` | `getRemarkCategorySetting` | Замечания | — |  |
| `/remarkDefectTypes` | `getDefectTypes` | Замечания | 200 |  |
| `/remarkStatuses` | `getRemarkStatuses` | Замечания | 200 |  |
| `/remarkTemplates` | `getRemarkTemplates` | Замечания | 200 |  |
| `/remarkTemplates/{remarkTemplateId}` | `getRemarkTemplate` | Замечания | 200 |  |
| `/remarkWorkTypes` | `getRemarkWorkTypes` | Замечания | 200 |  |
| `/remarks` | `getRemarks` | Замечания | 200 |  |
| `/remarks/{remarkId}` | `getRemark` | Замечания | 200 |  |
| `/reservationTypes` | `getReservationTypes` | Сделки | 200 |  |
| `/reservationTypes/{typeId}` | `getReservationType` | Сделки | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/revisionStatuses` | `getRevisionStatuses` | Ревизии | 200 |  |
| `/revisionTypes` | `getRevisionTypes` | Ревизии | 200 |  |
| `/revisionTypes/{typeId}` | `getRevisionType` | Ревизии | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/revisions` | `getRevisions` | Ревизии | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/revisions/{revisionId}` | `getRevision` | Ревизии | — |  |
| `/roles` | `getRoles` | Пользователи | 200 |  |
| `/roomBadges` | `getRoomBadges` | Дома | 200 |  |
| `/roomMeters` | `getRoomMeters` | Помещения | 200 |  |
| `/roomMeters/{roomMeterId}` | `getRoomMeter` | Помещения | 200 |  |
| `/roomTypes` | `getRoomTypes` | Помещения | 200 |  |
| `/roomTypes/{roomTypeId}` | `getRoomType` | Помещения | 404 | {<br>"message": "Объект не найден",<br>"success": false<br>} |
| `/rooms` | `getRooms` | Помещения | 200 |  |
| `/rooms/statuses` | `getRoomStatuses` | Помещения | 200 |  |
| `/rooms/types` | `getRoomTypesCollection` | Помещения | 200 |  |
| `/rooms/{roomId}` | `getRoom` | Помещения | 200 |  |
| `/rooms/{roomId}/recommended` | `getRecommendedRooms` | Помещения | 404 | {<br>"message": "The route api/v1/rooms/783448/recommended cou…"<br>} |
| `/scheduleWorks` | `getScheduleWorks` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/scheduleWorks/{scheduleWorkId}` | `getScheduleWork` | Планирование работ | — |  |
| `/schedules` | `getSchedules` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/schedules/{scheduleId}` | `getSchedule` | Планирование работ | — |  |
| `/sections` | `getSections` | Дома | 200 |  |
| `/signatureStatuses` | `getSignatureStatuses` | ЭЦП | 200 |  |
| `/signatures` | `getSignatures` | ЭЦП | 200 |  |
| `/signatures/{signatureId}` | `getSignature` | ЭЦП | 200 |  |
| `/signs` | `getSigns` | ЭЦП | 200 |  |
| `/staffUsers` | `getStaffUsers` | Сотрудники | 200 |  |
| `/staffUsers/{staffUserId}` | `getStaffUser` | Сотрудники | 200 |  |
| `/standards` | `getStandards` | Справочники | 200 |  |
| `/standards/{itemId}` | `getStandard` | Справочники | 200 |  |
| `/tags` | `getTags` | Теги | 200 |  |
| `/tags/{tagId}` | `getTag` | Теги | 200 |  |
| `/taskCategories` | `getTasksCatrgories` | Задачи | 200 |  |
| `/taskCategories/{categoryId}` | `getTaskCategory` | Задачи | 200 |  |
| `/tasks` | `getTasks` | Задачи | 200 |  |
| `/tasks/{taskId}` | `getTask` | Задачи | 200 |  |
| `/templates` | `getTemplates` | Шаблоны | 200 |  |
| `/templates/{templateId}` | `getTemplate` | Шаблоны | — |  |
| `/units` | `getUnits` | Планирование работ | 200 |  |
| `/units/{unitId}` | `getUnit` | Планирование работ | 200 |  |
| `/userSettings` | `getUserSettings` | Пользовательские настройки | 200 |  |
| `/userSettings/{id}` | `getUserSetting` | Пользовательские настройки | — |  |
| `/userStatuses` | `getUserStatuses` | Пользователи | 200 |  |
| `/users` | `getUsers` | Пользователи | 200 |  |
| `/users/{userId}` | `getUser` | Пользователи | 200 |  |
| `/viewHistories` | `getViewHistories` | История изменений | 200 |  |
| `/workAccumulationRegisters` | `getWorkAccumulationRegisters` | Производство работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workActStatuses` | `getWorkActStatuses` | Производство работ | 200 |  |
| `/workActStatuses/{statusId}` | `getWorkActStatus` | Производство работ | — |  |
| `/workActs` | `getWorkActs` | Производство работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workActs/{actId}` | `getWorkAct` | Производство работ | — |  |
| `/workJournalStatuses` | `getWorkJournalStatuses` | Производство работ | 200 |  |
| `/workJournals` | `getWorkJournals` | Производство работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workJournals/{workJournalId}` | `getWorkJournal` | Производство работ | — |  |
| `/workLogs` | `getWorkLogs` | Записи журнала работ | 200 |  |
| `/workLogs/{workLogId}` | `getWorkLog` | Записи журнала работ | — |  |
| `/workMaterials` | `getWorkMaterials` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workMaterials/{workMaterialId}` | `getWorkMaterial` | Планирование работ | — |  |
| `/workRegisterStatuses` | `getWorkRegisterStatuses` | Производство работ | 200 |  |
| `/workRegisterStatuses/{statusId}` | `getWorkRegisterStatus` | Производство работ | — |  |
| `/workRegisters` | `getWorkRegisters` | Производство работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workRegisters/{registerId}` | `getWorkRegister` | Производство работ | — |  |
| `/workStages` | `getWorkStages` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/workStages/{workStageId}` | `getWorkStage` | Планирование работ | — |  |
| `/workTypes` | `getWorkTypes` | Планирование работ | 200 |  |
| `/workTypes/{workTypeId}` | `getWorkType` | Планирование работ | — |  |
| `/works` | `getWorks` | Планирование работ | 403 | {<br>"message": "У вас недостаточно прав для совершения этого …",<br>"success": false<br>} |
| `/works/{workId}` | `getWork` | Планирование работ | — |  |

## Детали успешных ответов (форма JSON)

Ниже развернуты первые **75** успешных GET; полный набор значений `body_shape` лежит в `iflat_get_probe_results.json`.

### `/agentDocuments` — `getAgentDocuments`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/agentDocuments` params `{'page': 1, 'perPage': 2}`

- Время: 188 ms


```json
{
"data": [
{
"id": "…",
"user_id": "…",
"agent_id": "…",
"deal_id": "…",
"issue_date": "…",
"issuer_name": "…",
"registration_number": "…",
"has_signature_permit": "…",
"approved": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/agentDocuments?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/agentDocuments?page=157",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/agentDocuments?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 157,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/agentDocuments",
"per_page": 2,
"to": 2,
"total": 313
}
}
```

### `/agentDocuments/{agentDocumentId}` — `getAgentDocumentId`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/agentDocuments/708` params `{}`

- Время: 184 ms


```json
{
"id": 708,
"user_id": 228549,
"agent_id": 317819,
"deal_id": 259925,
"issue_date": null,
"issuer_name": null,
"registration_number": null,
"has_signature_permit": 0,
"approved": 0
}
```

### `/approvalActions` — `getApprovalActions`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/approvalActions` params `{'page': 1, 'perPage': 2}`

- Время: 5083 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/approvalActions?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/approvalActions?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/approvalActions",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/approvalChains` — `getApprovalChains`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/approvalChains` params `{'page': 1, 'perPage': 2}`

- Время: 181 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/approvalChains?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/approvalChains?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/approvalChains",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/approvalRequests` — `getApprovalRequests`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/approvalRequests` params `{'page': 1, 'perPage': 2}`

- Время: 183 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/approvalRequests?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/approvalRequests?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/approvalRequests",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/approvalSteps` — `getApprovalSteps`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/approvalSteps` params `{'page': 1, 'perPage': 2}`

- Время: 189 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/approvalSteps?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/approvalSteps?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/approvalSteps",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/audits` — `getAudits`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/audits` params `{'page': 1, 'perPage': 2}`

- Время: 604 ms


```json
{
"data": [
{
"id": "…",
"user_id": "…",
"event": "…",
"owner_type": "…",
"owner_id": "…",
"fields": "…",
"created_at": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/audits?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/audits?page=373077",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/audits?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 373077,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/audits",
"per_page": 2,
"to": 2,
"total": 746153
}
}
```

### `/banks` — `getBanks`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/banks` params `{}`

- Время: 184 ms


```json
[
{
"id": 44,
"name": "ВСК Страхование",
"position": 0
},
"…"
]
```

### `/buildingObjectStatuses` — `getBuildingObjectStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/buildingObjectStatuses` params `{}`

- Время: 208 ms


```json
[
{
"id": 1,
"name": "Строится",
"bg_color": "#eaf3fd",
"text_color": "#212529",
"position": 0,
"routes": [
"…",
"…"
]
},
"…"
]
```

### `/buildingObjectTypes` — `getBuildingObjectTypes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/buildingObjectTypes` params `{'page': 1, 'perPage': 2}`

- Время: 197 ms


```json
{
"data": [
{
"id": "…",
"name": "…",
"is_final": "…",
"is_default": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/buildingObjectTypes?p…",
"last": "https://YOUR_CRM_API_HOST/api/v1/buildingObjectTypes?p…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/buildingObjectTypes?p…"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 10,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/buildingObjectTypes",
"per_page": 2,
"to": 2,
"total": 20
}
}
```

### `/buildingObjects` — `getBuildingObjects`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/buildingObjects` params `{'page': 1, 'perPage': 2}`

- Время: 185 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/buildingObjects?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/buildingObjects?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/buildingObjects",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/checkListSteps` — `getSteps`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/checkListSteps` params `{}`

- Время: 286 ms


```json
{
"data": [
{
"id": "…",
"check_list_id": "…",
"name": "…",
"description": "…",
"position": "…",
"photo_required": "…",
"no_empty_print": "…",
"remark_category_id": "…",
"parent_id": "…",
"path": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/checkListSteps?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/checkListSteps?page=6",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/checkListSteps?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 6,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/checkListSteps",
"per_page": 24,
"to": 24,
"total": 134
}
}
```

### `/checkListSteps/{stepId}` — `getStep`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/checkListSteps/5379` params `{}`

- Время: 184 ms


```json
{
"id": 5379,
"check_list_id": 4761,
"name": "1. Входная дверь",
"description": null,
"position": 1,
"photo_required": 2,
"no_empty_print": true,
"remark_category_id": 196,
"parent_id": null,
"path": "/5379/"
}
```

### `/checkLists` — `getCheckLists`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/checkLists` params `{}`

- Время: 184 ms


```json
{
"data": [
{
"id": "…",
"name": "…",
"description": "…",
"entities": "…",
"inspection_allowed": "…",
"self_inspection_allowed": "…",
"parent_id": "…",
"path": "…",
"is_folder": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/checkLists?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/checkLists?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/checkLists",
"per_page": 96,
"to": 16,
"total": 16
}
}
```

### `/checkLists/{checkListId}` — `getCheckList`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/checkLists/4879` params `{}`

- Время: 184 ms


```json
{
"id": 4879,
"name": "Гарантия (Без отделки)",
"description": null,
"entities": null,
"inspection_allowed": 1,
"self_inspection_allowed": 0,
"parent_id": null,
"path": "/4879/",
"is_folder": false
}
```

### `/claimCategories` — `getClaimCategories`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claimCategories` params `{}`

- Время: 185 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/claimCategories?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/claimCategories?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/claimCategories",
"per_page": 24,
"to": null,
"total": 0
}
}
```

### `/claimPriorities` — `getPriorities`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claimPriorities` params `{}`

- Время: 183 ms


```json
[
{
"id": 1,
"name": "Низкая"
},
"…"
]
```

### `/claimTypes` — `getClaimTypes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claimTypes` params `{}`

- Время: 184 ms


```json
[
{
"id": 1,
"name": "Внутренняя",
"position": 10
},
"…"
]
```

### `/claims` — `getClaims`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claims` params `{'page': 1, 'perPage': 2}`

- Время: 271 ms


```json
{
"data": [
{
"id": "…",
"owner_id": "…",
"owner_type": "…",
"type_id": "…",
"category_id": "…",
"house_id": "…",
"user_id": "…",
"author_id": "…",
"status_id": "…",
"responsible_id": "…",
"subject": "…",
"description": "…",
"date_planned": "…",
"date_planned_left": "…",
"date_complete": "…",
"created_at": "…",
"priority_id": "…",
"reviewer_id": "…",
"date_review": "…",
"room_id": "…",
"status_updated_at": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/claims?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/claims?page=10475",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/claims?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 10475,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/claims",
"per_page": 2,
"to": 2,
"total": 20950
}
}
```

### `/claims/statuses` — `getClaimsStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claims/statuses` params `{}`

- Время: 182 ms


```json
[
{
"id": 1,
"name": "Новая",
"bg_color": "#E5F0FF",
"text_color": "#4F4F4F",
"position": 0,
"routes": [
"…",
"…"
]
},
"…"
]
```

### `/claims/{claimId}` — `getClaim`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claims/248712` params `{}`

- Время: 212 ms


```json
{
"id": 248712,
"owner_id": null,
"owner_type": null,
"type_id": 2,
"category_id": null,
"house_id": 4662,
"user_id": 227992,
"author_id": 227992,
"status_id": 1,
"responsible_id": null,
"subject": "Гарантийное обращение",
"description": null,
"date_planned": null,
"date_planned_left": false,
"date_complete": null,
"created_at": "2026-05-10T19:52:19.000000Z",
"priority_id": null,
"reviewer_id": null,
"date_review": null,
"room_id": 580688,
"status_updated_at": null
}
```

### `/claims/{claimId}/remarks` — `getClaimRemarks`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/claims/248712/remarks` params `{'page': 1, 'perPage': 2}`

- Время: 209 ms


```json
{
"data": [
{
"id": "…",
"owner_id": "…",
"owner_type": "…",
"inspection_step_id": "…",
"comment": "…",
"instruction": "…",
"plan_point_type": "…",
"plan_points": "…",
"status_id": "…",
"house_id": "…",
"section_id": "…",
"floor_id": "…",
"room_id": "…",
"plan_id": "…",
"category_id": "…",
"defect_type_id": "…",
"work_type_id": "…",
"defect_count": "…",
"created_at": "…",
"date_planned": "…",
"date_start": "…",
"date_complete": "…",
"date_deadline": "…",
"date_deadline_expired": "…",
"price": "…",
"standard_id": "…",
"status_updated_at": "…",
"work_id": "…",
"author_id": "…"
}
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/claims/248712/remarks…",
"last": "https://YOUR_CRM_API_HOST/api/v1/claims/248712/remarks…",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/claims/248712/remarks",
"per_page": 2,
"to": 1,
"total": 1
}
}
```

### `/comments` — `getComments`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/comments` params `{'perPage': 2}`

- Время: 192 ms


```json
{
"data": [
{
"id": "…",
"owner_id": "…",
"owner_type": "…",
"author_id": "…",
"text": "…",
"is_public": "…",
"created_at": "…",
"parent_id": "…",
"path": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/comments?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/comments?page=14938",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/comments?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 14938,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/comments",
"per_page": 2,
"to": 2,
"total": 29875
}
}
```

### `/confirmationDocumentTypes` — `getConfirmationDocumentTypes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/confirmationDocumentTypes` params `{}`

- Время: 185 ms


```json
[
{
"id": 1,
"name": "Устав"
},
"…"
]
```

### `/contracts` — `getContracts`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/contracts` params `{'page': 1, 'perPage': 2}`

- Время: 204 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/contracts?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/contracts?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/contracts",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/dealRegistrationStatuses` — `getDealRegistrationStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/dealRegistrationStatuses` params `{}`

- Время: 185 ms


```json
[
{
"id": 1,
"name": "Новая",
"bg_color": "#e5f0ff",
"text_color": "#4f4f4f",
"position": 0
},
"…"
]
```

### `/dealRegistrations` — `getDealRegistrations`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/dealRegistrations` params `{'page': 1, 'perPage': 2}`

- Время: 186 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/dealRegistrations?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/dealRegistrations?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/dealRegistrations",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/dealStages` — `getDealStages`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/dealStages` params `{}`

- Время: 183 ms


```json
{
"data": [
{
"code": "…",
"name": "…",
"position": "…"
},
"…"
]
}
```

### `/dealStatuses` — `getDealStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/dealStatuses` params `{}`

- Время: 284 ms


```json
[
{
"id": 6,
"name": "Новая заявка",
"stage": "NEW",
"stage_name": "Выбор объекта",
"bg_color": "#cbe8f9",
"text_color": "#000000",
"position": 5
},
"…"
]
```

### `/deals` — `getDeals`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/deals` params `{'page': 1}`

- Время: 382 ms


```json
{
"data": [
{
"id": "…",
"price": "…",
"payments": "…",
"sign_type": "…",
"ownership_type_id": "…",
"payment_term_id": "…",
"buyers_married": "…",
"object_purchased_in_marriage": "…",
"surcharge_amount": "…",
"room_id": "…",
"status_id": "…",
"created_at": "…",
"created_at_formatted": "…",
"contract_type_id": "…",
"contract_number": "…",
"contract_date": "…",
"registration_date": "…",
"registration_number": "…",
"act_date": "…",
"act_number": "…",
"one_sided_act_date": "…",
"resign_one_sided_act": "…",
"readiness_message_date": "…",
"readiness_message_sending_date": "…",
"readiness_message_sending_number": "…",
"payment_scheme_id": "…",
"keys_given": "…",
"responsible_id": "…",
"reservation_date_start": "…",
"reservation_date_end": "…",
"reservation_date": "…",
"reservation_price": "…",
"reservation_confirm": "…",
"reservation_confirm_hours": "…",
"inspection_sign_type": "…",
"inspection_prepare_stage": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/deals?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/deals?page=818",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/deals?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 818,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/deals",
"per_page": 24,
"to": 24,
"total": 19609
}
}
```

### `/deals/contractTypes` — `getContractTypes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/deals/contractTypes` params `{}`

- Время: 188 ms


```json
[
{
"id": 1,
"name": "ДДУ"
},
"…"
]
```

### `/deals/{dealId}` — `getDeal`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/deals/365116` params `{}`

- Время: 199 ms


```json
{
"id": 365116,
"price": "0.00",
"payments": "1063.30",
"sign_type": "online",
"ownership_type_id": null,
"payment_term_id": null,
"buyers_married": null,
"object_purchased_in_marriage": null,
"surcharge_amount": null,
"room_id": 516189,
"status_id": 6,
"created_at": "2026-05-08T09:01:15.000000Z",
"created_at_formatted": "08.05.2026",
"contract_type_id": 2,
"contract_number": "ДКП/Рас/НП/17Ф/1-24",
"contract_date": "2026-05-08T00:00:00.000000Z",
"registration_date": null,
"registration_number": null,
"act_date": null,
"act_number": null,
"one_sided_act_date": null,
"resign_one_sided_act": null,
"readiness_message_date": null,
"readiness_message_sending_date": null,
"readiness_message_sending_number": null,
"payment_scheme_id": null,
"keys_given": 0,
"responsible_id": null,
"reservation_date_start": null,
"reservation_date_end": null,
"reservation_date": null,
"reservation_price": null,
"reservation_confirm": null,
"reservation_confirm_hours": null,
"inspection_sign_type": null,
"inspection_prepare_stage": null
}
```

### `/deals/{dealId}/clients` — `getDealClients`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/deals/365116/clients` params `{}`

- Время: 204 ms


```json
[
{
"id": 222884,
"user_group_id": 10,
"last_name": "Ульянцева",
"first_name": "Ирина",
"middle_name": "Витальевна",
"full_name": "Ульянцева Ирина Витальевна",
"phone": "79264140460",
"email": "ulyantseva.ira@mail.ru",
"created_at": "2025-02-05T14:52:36.000000Z",
"last_visit_at": "2025-07-01T08:26:37.000000Z",
"staff_fired_at": null,
"house_permissions": null,
"email_unavailable": 0,
"grade_id": null,
"organization_id": null,
"part": null,
"extra_fullname_string": null,
"extra_signature": null,
"personal_data": {
"id": "…",
"user_id": "…",
"date_of_birth": "…",
"place_of_birth": "…",
"passport_series": "…",
"passport_number": "…",
"passport_issue_date": "…",
"passport_department_code": "…",
"passport_issued_by": "…",
"address_match": "…",
"registration_address": "…",
"registration_city": "…",
"registration_district": "…",
"registration_street": "…",
"registration_house": "…",
"registration_building": "…",
"registration_apartment": "…",
"registration_postal_code": "…",
"residential_address": "…",
"residential_city": "…",
"residential_district": "…",
"residential_street": "…",
"residential_house": "…",
"residential_building": "…",
"residential_apartment": "…",
"residential_postal_code": "…",
"inn": "…",
"snils": "…",
"company_name": "…",
"company_inn": "…",
"company_ogrn": "…",
"company_address": "…",
"company_bank_details": "…",
"company_legal_document": "…",
"is_changed": "…",
"gender": "…",
"personal_document_type_id": "…"
},
"signature": {
"id": "…",
"user_id": "…",
"external_id": "…",
"provider_id": "…",
"status_id": "…",
"registration_stage": "…",
"created_at": "…",
"expires_at": "…",
"error_description": "…",
"status": "…"
},
"status_id": 4
}
]
```

### `/digitalDocumentStatuses` — `getDigitalDocumentStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/digitalDocumentStatuses` params `{}`

- Время: 185 ms


```json
[
{
"id": 1,
"name": "Черновик",
"bg_color": "#bfbfbf",
"text_color": "#ffffff",
"position": 0
},
"…"
]
```

### `/digitalDocuments` — `getDigitalDocuments`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/digitalDocuments` params `{'page': 1, 'perPage': 2}`

- Время: 214 ms


```json
{
"data": [
{
"id": "…",
"owner_id": "…",
"owner_type": "…",
"document_type_id": "…",
"user_id": "…",
"name": "…",
"created_at": "…",
"status_id": "…",
"current_signature_provider_id": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/digitalDocuments?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/digitalDocuments?page…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/digitalDocuments?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 2138,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/digitalDocuments",
"per_page": 24,
"to": 24,
"total": 51298
}
}
```

### `/digitalDocuments/{documentId}` — `getDigitalDocument`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/digitalDocuments/71140` params `{}`

- Время: 186 ms


```json
{
"id": 71140,
"owner_id": 376832,
"owner_type": "Inspection",
"document_type_id": 348,
"user_id": 234925,
"name": "ЭЦП_АПП ключей застройщику_квартира (#376832,…",
"created_at": "2026-05-10T14:38:04.000000Z",
"status_id": 1,
"current_signature_provider_id": null
}
```

### `/districts` — `getDistricts`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/districts` params `{'page': 1}`

- Время: 187 ms


```json
{
"data": [
{
"id": "…",
"name": "…",
"type_id": "…",
"is_village": "…",
"description": "…",
"city": "…",
"area": "…",
"region": "…",
"direction": "…",
"distance": "…",
"coordinates": "…",
"video_url": "…",
"main_url": "…",
"timezone": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/districts?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/districts?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/districts",
"per_page": 24,
"to": 3,
"total": 3
}
}
```

### `/districts/{districtId}` — `getDistrict`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/districts/862` params `{}`

- Время: 187 ms


```json
{
"id": 862,
"name": "Сколково",
"type_id": 1,
"is_village": 0,
"description": null,
"city": null,
"area": null,
"region": null,
"direction": null,
"distance": null,
"coordinates": null,
"video_url": null,
"main_url": "https://novosel.absgroup.ru",
"timezone": null
}
```

### `/divisions` — `getDivisions`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/divisions` params `{}`

- Время: 188 ms


```json
{
"data": [
{
"id": "…",
"name": "…",
"parent_id": "…",
"path": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/divisions?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/divisions?page=3",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/divisions?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 3,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/divisions",
"per_page": 24,
"to": 24,
"total": 50
}
}
```

### `/divisions/{divisionId}` — `getDivision`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/divisions/1047` params `{}`

- Время: 186 ms


```json
{
"id": 1047,
"name": "\"ВИВ\" ООО",
"parent_id": null,
"path": "/1047/"
}
```

### `/documentPages` — `getDocumentPages`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/documentPages` params `{}`

- Время: 203 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/documentPages?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/documentPages?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/documentPages",
"per_page": 24,
"to": null,
"total": 0
}
}
```

### `/documentTypes` — `getDocumentTypes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/documentTypes` params `{'page': 1, 'perPage': 2}`

- Время: 185 ms


```json
{
"data": [
{
"id": "…",
"name": "…",
"is_system": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/documentTypes?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/documentTypes?page=21",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/documentTypes?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 21,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/documentTypes",
"per_page": 2,
"to": 2,
"total": 42
}
}
```

### `/documentTypes/{typeId}` — `getDocumentType`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/documentTypes/234` params `{}`

- Время: 183 ms


```json
{
"id": 234,
"name": "7_Акт комиссионного обследования",
"is_system": false
}
```

### `/documents` — `getDocuments`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/documents` params `{'page': 1, 'perPage': 2}`

- Время: 201 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/documents?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/documents?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/documents",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/entityAttributes` — `getEntityAttributes`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/entityAttributes` params `{}`

- Время: 232 ms


```json
{
"data": [
{
"id": "…",
"object_type": "…",
"object_subtype": "…",
"entity": "…",
"entity_type_id": "…",
"code": "…",
"name": "…",
"type": "…",
"options": "…",
"position": "…",
"enabled": "…",
"is_filterable": "…",
"is_default": "…",
"is_public": "…",
"is_required": "…",
"created_at": "…",
"updated_at": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/entityAttributes?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/entityAttributes?page=21",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/entityAttributes?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 21,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/entityAttributes",
"per_page": 64,
"to": 64,
"total": 1339
}
}
```

### `/entityAttributes/{entityAttributeId}` — `getEntityAttribute`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/entityAttributes/536` params `{}`

- Время: 230 ms


```json
{
"id": 536,
"object_type": "Claim",
"object_subtype": null,
"entity": "Claim",
"entity_type_id": null,
"code": "nomer_esed",
"name": "Номер ЕСЭД",
"type": "string",
"options": [],
"position": 1,
"enabled": 1,
"is_filterable": 1,
"is_default": false,
"is_public": 1,
"is_required": 0,
"created_at": "2023-12-13T11:16:23.000000Z",
"updated_at": "2023-12-13T11:16:23.000000Z"
}
```

### `/entityConfigs` — `getEntityConfigs`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/entityConfigs` params `{}`

- Время: 234 ms


```json
{
"data": [
{
"entity_name": "…",
"entity_title": "…",
"show_url": "…",
"fields": "…",
"relations": "…"
},
"…"
]
}
```

### `/entityVersions` — `getEntityVersions`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/entityVersions` params `{}`

- Время: 212 ms


```json
{
"data": {
"districts": "8805398e2bb15c4769a147777997f298",
"houses": "a83c74a169a30a6a67849633a9cc5b95",
"sections": "ac923b4bb1c95bdfad42888f5a7c6cd0",
"floors": "46a48e74175e0ebf6a16c4fbc11f8e59",
"meters": "e0d106b71ebd30edca77c14c792e9625",
"house_meters": "7027d6cd14025931709570096724d920",
"room_meters": "334c4a4c42fdb79d7ebc3e73b517e6f8",
"room_statuses": "a69c4ac24456bbe50ba42ef6fcd3700e",
"check_lists": "5025fd20885fa571625a9153ab9650a5",
"steps": "5d1653c3763b47127ef2f3845e9d1ac3",
"remark_categories": "57b9a52b15cb6807806e2e3d65ea3382",
"remark_templates": "76c33b4e3bdc26988cc1609b8c844c19",
"remark_statuses": "8ccbef17f3bf0e440b1ebc305abda581",
"inspection_statuses": "24f93a6b1b747e21f15e9bf8e46575bd",
"inspection_types": "d983c1d3e4675c4bf66d0720aafe4b8a",
"inspection_experts": "d7e62b3fdec1552ffb0e370523c3f6f9",
"revision_statuses": "d524e29115216374ba105a3728284758",
"revision_types": "a3c550b5efc7112518274e2ac26c79f5",
"plans": "1600aa2afce707e4ac2f42af8dcfe292",
"task_categories": "334c4a4c42fdb79d7ebc3e73b517e6f8",
"units": "b00ea159efbfb17c1f7b09dce860c030",
"standards": "5c9a2db1867787241a98db01c59b762f",
"work_stages": "334c4a4c42fdb79d7ebc3e73b517e6f8",
"works": "59267388ded3d0cef0b80e3cfeedd9c6",
"work_register_statuses": "ca95c58734e914a7956c6ce25a3e8994",
"developer_settings": "68a54ff1aabb4fd57c766bb558083d5b",
"billing_features": "ed8e292ddff88ef50b59934b4b7e072b",
"tags": "6249ba14c09a6a4aedfd109d04bacce0"
}
}
```

### `/estimates` — `getEstimates`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/estimates` params `{'page': 1, 'perPage': 2}`

- Время: 202 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/estimates?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/estimates?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/estimates",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/export/pdf/rooms/{roomId}` — `savePdf`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/export/pdf/rooms/783448` params `{}`

- Время: 433 ms


```json
%PDF-1.7
1 0 obj
<< /Type /Catalog
/Outlines 2 0 R
/Pages 3 0 R >>
endobj
2 0 obj
<< /Type /Outlines /Count 0 >>
endobj
3 0 obj
<< /Type /Pages
/Kids [6 0 R
19 0 R
]
/Count 2
/Resources <<
/ProcSet 4 0 R
/Font << 
/F1 8 0 R
/F2 13 0 R
>>
/XObject << 
/I1 18 0 R
/I2 21 0 R
>>
>>
/MediaBox [0.000 0.000 595.280 841.890]
 >>
endobj
4 0 obj
[/PDF /Text /ImageC ]
endobj
5 0 obj
<<
/Producer (�� d o m p 
```

### `/floors` — `getFloors`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/floors` params `{}`

- Время: 196 ms


```json
{
"data": [
{
"id": "…",
"house_id": "…",
"number": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/floors?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/floors?page=15",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/floors?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 15,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/floors",
"per_page": 48,
"to": 48,
"total": 683
}
}
```

### `/formSchemas` — `getFormSchemas`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/formSchemas` params `{'page': 1, 'perPage': 2}`

- Время: 186 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/formSchemas?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/formSchemas?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/formSchemas",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/grades` — `getGrades`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/grades` params `{'page': 1, 'perPage': 2}`

- Время: 180 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/grades?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/grades?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/grades",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/histories` — `getHistories`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/histories` params `{'page': 1, 'perPage': 2}`

- Время: 495 ms


```json
{
"data": [
{
"id": "…",
"owner_type": "…",
"owner_id": "…",
"user_id": "…",
"type": "…",
"status_from": "…",
"status_to": "…",
"status": "…",
"text": "…",
"created_at": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/histories?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/histories?page=608113",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/histories?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 608113,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/histories",
"per_page": 2,
"to": 2,
"total": 1216226
}
}
```

### `/houseMeters` — `getHouseMeters`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houseMeters` params `{'page': 1}`

- Время: 189 ms


```json
{
"data": [
{
"id": "…",
"house_id": "…",
"meter_id": "…",
"photo_enabled": "…",
"room_type_id": "…",
"tariff_count": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/houseMeters?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/houseMeters?page=132",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/houseMeters?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 132,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/houseMeters",
"per_page": 24,
"to": 24,
"total": 3154
}
}
```

### `/houseMeters/{houseMeterId}` — `getHouseMeter`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houseMeters/3301` params `{}`

- Время: 184 ms


```json
{
"id": 3301,
"house_id": 4855,
"meter_id": 1,
"photo_enabled": 0,
"room_type_id": 1,
"tariff_count": 3
}
```

### `/houses` — `getHouses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses` params `{'page': 1, 'perPage': 2}`

- Время: 201 ms


```json
{
"data": [
{
"id": "…",
"district_id": "…",
"name": "…",
"city": "…",
"street": "…",
"area": "…",
"house": "…",
"fias": "…",
"address": "…",
"address_mail": "…",
"address_construction": "…",
"position": "…",
"self_inspection": "…",
"development_start": "…",
"development_end": "…",
"development_start_quarter": "…",
"development_start_year": "…",
"development_end_quarter": "…",
"development_end_year": "…",
"house_state_id": "…",
"coordinates": "…",
"elevator": "…",
"floors_count": "…",
"inspection_register_interval": "…",
"transfer_date": "…",
"commissioning_permit_date": "…",
"commissioning_permit_number": "…",
"timezone": "…",
"shared_calendar_house_id": "…",
"warranty_start": "…",
"warranty_end": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/houses?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/houses?page=20",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/houses?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 20,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/houses",
"per_page": 2,
"to": 2,
"total": 39
}
}
```

### `/houses/{houseId}` — `getHouse`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363` params `{}`

- Время: 197 ms


```json
{
"id": 6363,
"district_id": 741,
"name": "09_фаза_2_корпус",
"city": null,
"street": null,
"area": null,
"house": null,
"fias": null,
"address": "",
"address_mail": null,
"address_construction": null,
"position": 0,
"self_inspection": null,
"development_start": "",
"development_end": "",
"development_start_quarter": 0,
"development_start_year": 0,
"development_end_quarter": 0,
"development_end_year": 0,
"house_state_id": 1,
"coordinates": null,
"elevator": null,
"floors_count": null,
"inspection_register_interval": 1,
"transfer_date": null,
"commissioning_permit_date": null,
"commissioning_permit_number": null,
"timezone": "Europe/Moscow",
"shared_calendar_house_id": null,
"warranty_start": null,
"warranty_end": null
}
```

### `/houses/{houseId}/bimElementsByRemarks` — `getBimElementsByRemarks`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363/bimElementsByRemarks` params `{}`

- Время: 221 ms


```json
[]
```

### `/houses/{houseId}/bimElementsByWorkPercentage` — `getbimElementsByWorkPercentage`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363/bimElementsByWorkPercentage` params `{}`

- Время: 202 ms


```json
[]
```

### `/houses/{houseId}/inspectionsPeriods` — `getInspectionPeriods`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363/inspectionsPeriods` params `{}`

- Время: 186 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/inspectio…",
"last": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/inspectio…",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/inspectio…",
"per_page": 300,
"to": null,
"total": 0
}
}
```

### `/houses/{houseId}/metro` — `getHouseMetro`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363/metro` params `{}`

- Время: 185 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/metro?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/metro?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/houses/6363/metro",
"per_page": 24,
"to": null,
"total": 0
}
}
```

### `/houses/{houseId}/roomBadges` — `getHouseRoomBadges`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/houses/6363/roomBadges` params `{}`

- Время: 185 ms


```json
[
{
"id": 838,
"reference_id": 2,
"type": "room_badges",
"name": "Сделка оплачена",
"position": 0,
"created_at": "2025-09-19 06:02:08",
"updated_at": "2025-09-19 06:02:08",
"parent_id": null,
"path": "/838/",
"is_folder": 0
}
]
```

### `/inspectionExperts` — `getInspectionExperts`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspectionExperts` params `{'page': 1, 'perPage': 2}`

- Время: 205 ms


```json
{
"data": [
{
"id": "…",
"inspection_id": "…",
"name": "…",
"organization_name": "…",
"organization_inn": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/inspectionExperts?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/inspectionExperts?pag…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/inspectionExperts?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 902,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/inspectionExperts",
"per_page": 2,
"to": 2,
"total": 1803
}
}
```

### `/inspectionExperts/{expertId}` — `getInspectionExpert`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspectionExperts/2373` params `{}`

- Время: 201 ms


```json
{
"id": 2373,
"inspection_id": 383305,
"name": "Удоденко Александр Юрьевич",
"organization_name": "Профприемка",
"organization_inn": "502715255251"
}
```

### `/inspectionMeters` — `getInspectionMeters`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspectionMeters` params `{}`

- Время: 201 ms


```json
{
"data": [
{
"id": "…",
"inspection_id": "…",
"meter_id": "…",
"photo_enabled": "…",
"number": "…",
"tariff_count": "…",
"value": "…",
"values": "…",
"room_meter_id": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/inspectionMeters?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/inspectionMeters?page…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/inspectionMeters?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 2949,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/inspectionMeters",
"per_page": 24,
"to": 24,
"total": 70761
}
}
```

### `/inspectionSteps` — `getInspectionSteps`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspectionSteps` params `{}`

- Время: 4697 ms


```json
{
"data": [
{
"id": "…",
"owner_id": "…",
"owner_type": "…",
"name": "…",
"position": "…",
"photo_required": "…",
"no_empty_print": "…",
"wrong": "…",
"step_id": "…",
"parent_id": "…",
"path": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/inspectionSteps?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/inspectionSteps?page=…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/inspectionSteps?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 46887,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/inspectionSteps",
"per_page": 24,
"to": 24,
"total": 1125282
}
}
```

### `/inspectionUsers` — `getInspectionUsers`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspectionUsers` params `{'page': 1}`

- Время: 200 ms


```json
{
"data": [
{
"id": "…",
"user_id": "…",
"deal_id": "…",
"inspection_id": "…",
"agent_document_id": "…",
"has_agent": "…",
"sign_type": "…",
"approved": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/inspectionUsers?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/inspectionUsers?page=341",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/inspectionUsers?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 341,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/inspectionUsers",
"per_page": 24,
"to": 24,
"total": 8174
}
}
```

### `/inspections` — `getInspections`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspections` params `{'page': 1}`

- Время: 244 ms


```json
{
"data": [
{
"id": "…",
"type_id": "…",
"room_id": "…",
"take_date": "…",
"take_date_start": "…",
"take_date_end": "…",
"status_id": "…",
"is_agent": "…",
"has_external_expert": "…",
"responsible_id": "…",
"author_id": "…",
"created_at": "…",
"updated_at": "…",
"additional": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/inspections?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/inspections?page=1083",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/inspections?page=2"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 1083,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/inspections",
"per_page": 24,
"to": 24,
"total": 25973
}
}
```

### `/inspections/statuses` — `getInspectionsStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/inspections/statuses` params `{}`

- Время: 187 ms


```json
[
{
"id": 1,
"name": "Новая",
"bg_color": "#E5F0FF",
"text_color": "#4F4F4F",
"class": "light",
"position": 5,
"routes": [
"…",
"…"
]
},
"…"
]
```

### `/leads` — `getLeads`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/leads` params `{'page': 1, 'perPage': 2}`

- Время: 184 ms


```json
{
"data": [],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/leads?page=1",
"last": "https://YOUR_CRM_API_HOST/api/v1/leads?page=1",
"prev": null,
"next": null
},
"meta": {
"current_page": 1,
"from": null,
"last_page": 1,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/leads",
"per_page": 2,
"to": null,
"total": 0
}
}
```

### `/messageTemplates` — `getMessageTemplates`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/messageTemplates` params `{'page': 1, 'perPage': 2}`

- Время: 186 ms


```json
{
"data": [
{
"id": "…",
"object_type": "…",
"object_id": "…",
"type": "…",
"template": "…"
},
"…"
],
"links": {
"first": "https://YOUR_CRM_API_HOST/api/v1/messageTemplates?mess…",
"last": "https://YOUR_CRM_API_HOST/api/v1/messageTemplates?mess…",
"prev": null,
"next": "https://YOUR_CRM_API_HOST/api/v1/messageTemplates?mess…"
},
"meta": {
"current_page": 1,
"from": 1,
"last_page": 19,
"links": [
"…",
"…"
],
"path": "https://YOUR_CRM_API_HOST/api/v1/messageTemplates",
"per_page": 2,
"to": 2,
"total": 38
}
}
```

### `/messageTemplates/{messageTemplateId}` — `getmessageTemplate`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/messageTemplates/127` params `{}`

- Время: 183 ms


```json
{
"id": 127,
"object_type": "House",
"object_id": 2126,
"type": "inspection_invite",
"template": "Здравствуйте! Ваш объект готов, запишитесь на…"
}
```

### `/mortgagePrograms` — `getMortgagePrograms`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/mortgagePrograms` params `{'page': 1}`

- Время: 222 ms


```json
[
{
"id": 408,
"name": "Новые метры",
"bank_id": 81,
"bank": {
"name": "…",
"logo": "…"
},
"object_kind_id": 1,
"user_types": "1,2,5",
"refinans": 1,
"sum_min": 300000,
"sum_max": 25000000,
"years_min": 3,
"years_max": 25,
"pv_min": 20,
"pv_max": 80,
"mc": 1,
"pv_mc": 5,
"state_support": 0,
"income_docs": "1,2",
"payment": 21540,
"rate": 8.25
},
"…"
]
```

### `/mortgageResponseStatuses` — `getMortgageResponseStatuses`

- Запрос: `https://YOUR_CRM_API_HOST/api/v1/mortgageResponseStatuses` params `{}`

- Время: 180 ms


```json
[
{
"id": 1,
"name": "Новая",
"bg_color": "#e5f0ff",
"text_color": "#4f4f4f",
"position": 0
},
"…"
]
```


## Query-параметры (выдержка из OpenAPI): ключевые ресурсы

### Помещения `/rooms`

| Имя | Где | Обяз. | Описание |
|-----|-----|-------|----------|
| `page` | query | False | Номер страницы |
| `orderBy` | query | False | Порядок сортировки. Варианты: price, -price, area, -area, number. |
| `houseId` | query | False | ID дома для фильтрации. Может быть указано несколько через запятую. |
| `sectionId` | query | False | ID секции дома для фильтрации. |
| `districtId` | query | False | ID ЖК для фильтрации. |
| `roomType` | query | False | Список ID типов помещений для фильтрации. Может быть указано несколько через запятую. |
| `isStudio` | query | False | Признак студии для фильтрации. |
| `floorId` | query | False | ID этажа для фильтрации |
| `statusId` | query | False | ID статуса для фильтрации |
| `roomCount` | query | False | Количество комнат для фильтрации |
| `priceFrom` | query | False | Цена продажи От для фильтрации |
| `priceTo` | query | False | Цена продажи До для фильтрации |
| `areaFrom` | query | False | Площадь От для фильтрации |
| `areaTo` | query | False | Площадь До для фильтрации |
| `floorFrom` | query | False | Этаж От для фильтрации |
| `floorTo` | query | False | Этаж До для фильтрации |
| `developmentEndYear` | query | False | Год сдачи дома для фильтрации |
| `developmentEndQuarter` | query | False | Квартал сдачи дома для фильтрации. Указывается только вместе с годом сдачи. |
| `badges` | query | False | Список ID тегов помещений для фильтрации. Например: 12,32,41 |
| `id` | query | False | Список ID помещений для фильтрации. Например: 175,247 |
| `number` | query | False | Номер помещения, поиск по вхождению строки. Например: 18 |
| `numberExact` | query | False | Номер помещения, поиск точного совпадения. Например: 180 |
| `saleStatuses` | query | False | Статус продажи помещений для фильтрации. Возможные варианты: FREE, RESERVATION, SOLD |
| `tags` | query | False | ID тегов для фильтрации |
| `projectSectionId` | query | False | ID раздела проектной документации для фильтрации |
| `embed` | query | False | Перечень связанных объектов, которые нужно вернуть в одном запросе. Подключайте только то, что действительно нужно, это сократит объем данных и ускорит ответ. Возможные варианты: room_type, status, floor, section, badges, plan, plans, custom_fields, prices, decoration, tasks, tags, project_section, provider_maps |
| `customField` | query | False | Фильтр по пользовательским полям. В первой квадратной скобке указывается код поля. Во второй операция.<br>- значение от: customField[square][from]=1000<br>- значение до: customField[square][to]=1500<br>- список значений: customField[number][in]=10,20,30<br>- точное совпадение: customField[is_multi_floor_apartment][eq]=1<br>- частичное совпадение: customField[room_decoration][like]=отделк |

### Одно помещение `/rooms/{roomId}`

| Имя | Где | Обяз. | Описание |
|-----|-----|-------|----------|
| `roomId` | path | True | ID помещения |
| `embed` | query | False | Перечень связанных объектов, которые нужно вернуть в одном запросе. Подключайте только то, что действительно нужно, это сократит объем данных и ускорит ответ. Возможные варианты: room_type, status, sale_status, floor, section, house, house.district, badges, plan, plans, custom_fields, prices, tasks, tags |

### Приёмки `/inspections`

| Имя | Где | Обяз. | Описание |
|-----|-----|-------|----------|
| `page` | query | False | Номер страницы |
| `roomId` | query | False | ID помещения для фильтрации |
| `typeId` | query | False | ID типа приемки. Возможные значения: 1 - Клиентская приемка, 2 - Внутренняя,3 - Передача упр-щей компании |
| `houseId` | query | False | ID дома |
| `inSchedule` | query | False | Выбрать только предстоящие приемки по графику |
| `statusId` | query | False | ID статуса приемки |
| `dateFrom` | query | False | Дата создания приемки начальная (формат 10.04.2021) |
| `dateTo` | query | False | Дата создания приемки конечная |
| `takeDateFrom` | query | False | Дата проведения приемки начальная для фильтрации |
| `takeDateTo` | query | False | Дата проведения приемки конечная для фильтрации |
| `updatedDateFrom` | query | False | Дата обновления приемки начальная (формат 10.04.2021) |
| `updatedDateTo` | query | False | Дата обновления приемки конечная |
| `embed` | query | False | Перечень связанных объектов, которые нужно вернуть в одном запросе. Возможные варианты: responsible, users, status, room, room.house, room.deal.users, steps, steps.remarks, steps.remarks.attachments, wrong_steps.remarks, claims, claims.status, claims.type, tasks, meeting, meetings, meetings.users, meetings.category, meetings.responsible, expert, expert.attachments, room.tags |
| `orderBy` | query | False | Порядок сортировки. Варианты: id, -id, take_date_start, -take_date_start. |

### Сделки `/deals`

| Имя | Где | Обяз. | Описание |
|-----|-----|-------|----------|
| `page` | query | False | Номер страницы |
| `orderBy` | query | False | Порядок сортировки. Варианты: id, -id, statusId, -statusId. |
| `roomId` | query | False | ID помещения для фильтрации |
| `statusId` | query | False | ID статуса для фильтрации |
| `userId` | query | False | ID собственника для фильтрации |
| `stage` | query | False | Стадия сделки для фильтрации. Возможные варианты: RESERVATION, INSPECTION |
| `signType` | query | False | Способ подписания. Возможные варианты: offline, online |
| `embed` | query | False | Перечень связанных объектов, которые нужно вернуть в одном запросе. Возможные варианты: status, contract_type, documents, room, room.custom_fields, room.room_type, room.plan, room.floor, room.section, room.house, room.house.documents, room.status, room.inspection, room.inspection.status, room.inspection.wrong_steps, provider_statuses, last_provider_statuses, custom_fields, mortgage, tasks, deal_registration, digital_documents |

### Дома `/houses`

| Имя | Где | Обяз. | Описание |
|-----|-----|-------|----------|
| `page` | query | False | Номер страницы |
| `perPage` | query | False | Количество на страницу |
| `embed` | query | False | Перечень связанных объектов, которые нужно вернуть в одном запросе. Возможные варианты: district, sections, cover, logo, house_state, badges, metro, prices, room_types, floor_range, floors, reservation_types, info_blocks, info_blocks.items, info_blocks.items.image, info_blocks.attachments |


## Схемы объектов (фрагмент из OpenAPI, упрощённо)

### Schema `Room`


```json
{
  "type": "object",
  "properties": {
    "area": {
      "type": "number",
      "description": "Общая площадь",
      "format": "float"
    },
    "area_additional": {
      "type": "number",
      "description": "Площадь дополнительная",
      "format": "float"
    },
    "area_additional_fact": {
      "type": "number",
      "description": "Площадь дополнительная (факт)",
      "format": "float"
    },
    "area_balcony": {
      "type": "number",
      "description": "Площадь балкона",
      "format": "float"
    },
    "area_balcony_fact": {
      "type": "number",
      "description": "Площадь балкона (факт)",
      "format": "float"
    },
    "area_balcony_w_ratio": {
      "type": "number",
      "description": "Площадь лоджии с понижающим коэфф-ом",
      "format": "float"
    },
    "area_balcony_w_ratio_fact": {
      "type": "number",
      "description": "Площадь лоджии с понижающим коэфф-ом (факт)",
      "format": "float"
    },
    "area_fact": {
      "type": "number",
      "description": "Общая площадь (факт)",
      "format": "float"
    },
    "area_kitchen": {
      "type": "number",
      "description": "Площадь кухни",
      "format": "float"
    },
    "area_kitchen_fact": {
      "type": "number",
      "description": "Площадь кухни (факт)",
      "format": "float"
    },
    "area_living": {
      "type": "number",
      "description": "Площадь жилая",
      "format": "float"
    },
    "area_living_fact": {
      "type": "number",
      "description": "Площадь жилая (факт)",
      "format": "float"
    },
    "area_overall": {
      "type": "number",
      "description": "Общая площадь с коэфф-том",
      "format": "float"
    },
    "area_overall_fact": {
      "type": "number",
      "description": "Общая площадь с коэфф-том (факт)",
      "format": "float"
    },
    "area_rooms": {
      "type": "number",
      "description": "Площадь комнат",
      "format": "float"
    },
    "area_rooms_fact": {
      "type": "number",
      "description": "Площадь комнат (факт)",
      "format": "float"
    },
    "badges": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "created_at": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "is_folder": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "parent_id": {
            "…": "max_depth"
          },
          "path": {
            "…": "max_depth"
          },
          "position": {
            "…": "max_depth"
          },
          "reference_id": {
            "…": "max_depth"
          },
          "updated_at": {
            "…": "max_depth"
          }
        }
      }
    },
    "balcony": {
      "type": "string",
      "description": "Тип балкона",
      "example": "Лоджия"
    },
    "balcony_id": {
      "type": "integer",
      "description": "ID типа балкона"
    },
    "bathroom": {
      "type": "string",
      "description": "Тип санузла"
    },
    "bathroom_id": {
      "type": "integer",
      "description": "ID типа санузал"
    },
    "cadastral_number": {
      "type": "string",
      "description": "Кадастровый номер помещения",
      "example": "77-77-09/020/2008-082"
    },
    "deal": {
      "type": "object",
      "properties": {
        "act_date": {
          "type": "string",
          "description": "Дата акта приема-передачи",
          "format": "date-time",
          "example": "2021-05-18 10:04:41"
        },
        "act_number": {
          "type": "string",
          "description": "Номер акта приема-передачи",
          "example": "АПП-123/2021"
        },
        "attachments": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "buyers_married": {
          "type": "boolean",
          "description": "Покупатель (и) в браке",
          "example": true
        },
        "contract_date": {
          "type": "string",
          "description": "Дата договора",
          "example": "20.07.2020"
        },
        "contract_number": {
          "type": "string",
          "description": "Номер договора",
          "example": "Д010/20"
        },
        "contract_type": {
          "…": "max_depth"
        },
        "contract_type_id": {
          "type": "integer",
          "description": "Тип договора",
          "example": 1
        },
        "created_at": {
          "type": "string",
          "description": "Дата создания сделки",
          "format": "date-time",
          "example": "2020-08-16 18:34:04"
        },
        "deal_registrations": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "digital_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "id": {
          "type": "integer",
          "description": "ID Сделки",
          "example": 408
        },
        "inspection_prepare_stage": {
          "type": "string",
          "description": "Шаг подготовки к приемке",
          "example": "user_data"
        },
        "inspection_sign_type": {
          "type": "string",
          "description": "Способ подписания на приемке (offline, online)",
          "example": "online"
        },
        "inspection_users": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "keys_given": {
          "type": "integer",
          "description": "Ключи получены (0/1)",
          "example": 1
        },
        "mortgage": {
          "…": "max_depth"
        },
        "object_purchased_in_marriage": {
          "type": "boolean",
          "description": "Объект приобретен в браке",
          "example": false
        },
        "one_sided_act_date": {
          "type": "string",
          "description": "Дата одностороннего акта приема-передачи",
          "format": "date-time",
          "example": "2021-05-18 10:04:41"
        },
        "ownership_type_id": {
          "type": "integer",
          "description": "Тип собственности",
          "example": 1
        },
        "payment_scheme": {
          "…": "max_depth"
        },
        "payments": {
          "type": "number",
          "description": "Сумма платежей, руб",
          "format": "float",
          "example": 623201
        },
        "price": {
          "type": "number",
          "description": "Сумма сделки, руб",
          "format": "float",
          "example": 3256000
        },
        "provider_maps": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "provider_statuses": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "readiness_message_date": {
          "type": "string",
          "description": "Дата сообщения о готовности объекта",
          "format": "date-time",
          "example": "2021-05-10 10:04:41"
        },
        "readiness_message_sending_date": {
          "type": "string",
          "description": "Дата отправки сообщения о готовности объекта",
          "format": "date-time",
          "example": "2021-05-11 10:04:41"
        },
        "readiness_message_sending_number": {
          "type": "string",
          "description": "Трек-номер отправки сообщения о готовности",
          "example": "AGC1129121124"
        },
        "registration_date": {
          "type": "string",
          "description": "Дата регистрации сделки",
          "format": "date-time",
          "example": "2021-05-12 10:04:41"
        },
        "registration_number": {
          "type": "string",
          "description": "Номер регистрации",
          "example": "109675/20"
        },
        "reservation_confirm": {
          "type": "integer",
          "description": "Подтверждение бронирования сделки (1 - подтверждена)",
          "example": 0
        },
        "reservation_confirm_hours": {
          "type": "integer",
          "description": "Кол-во часов, через которое неподтвержденная бронь будет отменена",
          "example": 3
        },
        "reservation_date_end": {
          "type": "string",
          "description": "Дата, до которой забронирована сделка",
          "format": "date-time",
          "example": "2020-10-12 10:04:41"
        },
        "reservation_date_start": {
          "type": "string",
          "description": "Дата, с которой забронирована сделка",
          "format": "date-time",
          "example": "2020-10-07 11:04:41"
        },
        "reservation_price": {
          "type": "integer",
          "description": "Стоимость бронирования сделки",
          "example": 3000
        },
        "resign_one_sided_act": {
          "type": "integer",
          "description": "Односторонний акт перепеодписан на двусторонний (0/1)",
          "example": 1
        },
        "responsible": {
          "…": "max_depth"
        },
        "room": {
          "$ref": "#/components/schemas/Room",
          "note": "cycle"
        },
        "room_id": {
          "type": "integer",
          "description": "Id Помещения",
          "example": 1081
        },
        "sign_type": {
          "type": "string",
          "description": "Способ подписания (offline, online)",
          "example": "online"
        },
        "stage": {
          "type": "string",
          "description": "Стадия сделки. Передается вместо статуса, берется первый статус в стадии.",
          "example": "CANCEL"
        },
        "status": {
          "…": "max_depth"
        },
        "status_id": {
          "type": "integer",
          "description": "Статус сделки",
          "example": 1
        },
        "surcharge_amount": {
          "type": "number",
          "description": "Сумма доплаты по факту пересчета площадей БТИ, руб",
          "format": "float",
          "example": 64000
        },
        "tasks": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "users": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        }
      }
    },
    "decoration": {
      "type": "object",
      "properties": {
        "created_at": {
          "type": "string",
          "description": "Дата и время создания записи",
          "format": "date-time",
          "example": "2025-08-14 11:24:14"
        },
        "id": {
          "type": "integer",
          "description": "ID записи",
          "example": 321
        },
        "is_folder": {
          "type": "integer",
          "description": "Является папкой",
          "example": 0
        },
        "name": {
          "type": "string",
          "description": "Наименование варианта справочника",
          "example": "Бассейн в доме"
        },
        "parent_id": {
          "type": "integer",
          "description": "ID родительской записи",
          "example": 1
        },
        "path": {
          "type": "string",
          "description": "Путь в иерархии",
          "example": "/1/2/"
        },
        "position": {
          "type": "integer",
          "description": "Позиция",
          "example": 1
        },
        "reference_id": {
          "type": "integer",
          "description": "ID справочника",
          "example": 4
        },
        "updated_at": {
          "type": "string",
          "description": "Дата и время изменения записи",
          "format": "date-time",
          "example": "2025-09-04 16:33:27"
        }
      }
    },
    "decoration_id": {
      "type": "integer",
      "description": "ID типа отделки"
    },
    "floor": {
      "type": "object",
      "properties": {
        "house_id": {
          "type": "integer",
          "description": "Id Здания",
          "example": 581
        },
        "id": {
          "type": "integer",
          "description": "Id Этажа",
          "example": 1092
        },
        "number": {
          "type": "integer",
          "description": "Номер этажа",
          "example": 3
        },
        "section_id": {
          "type": "integer",
          "description": "Id Секции",
          "example": 581
        }
      }
    },
    "floor_id": {
      "type": "integer",
      "description": "Id этажа",
      "example": 438
    },
    "house": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "Город",
          "example": "г. Москва"
        },
        "commissioning_permit_date": {
          "type": "string",
          "description": "Дата разрешения на ввод в эксплуатацию дома",
          "example": "2023-10-12"
        },
        "commissioning_permit_number": {
          "type": "string",
          "description": "Номер разрешения на ввод в эксплуатацию дома",
          "example": "28475632"
        },
        "coordinates": {
          "type": "string",
          "description": "Координаты дома на карте",
          "example": "37.587874, 55.73367"
        },
        "development_end": {
          "type": "string",
          "description": "Окончание строительства",
          "example": "II квартал 2021"
        },
        "development_start": {
          "type": "string",
          "description": "Начало строительства",
          "example": "I квартал 2018"
        },
        "district_id": {
          "type": "integer",
          "description": "Id ЖК",
          "example": 175
        },
        "fias": {
          "type": "string",
          "description": "Код ФИАС (уникальный идентификатор российского адреса)",
          "example": "01000000-0000-0000-0000-000000000000"
        },
        "house": {
          "type": "string",
          "description": "Номер дома",
          "example": "24а"
        },
        "house_state_id": {
          "type": "integer",
          "description": "Id стадии строительства",
          "example": 1
        },
        "id": {
          "type": "integer",
          "description": "Id дома",
          "example": 327
        },
        "name": {
          "type": "string",
          "description": "Название дома",
          "example": "Очередь 1"
        },
        "position": {
          "type": "integer",
          "description": "Позиция в списке"
        },
        "self_inspection": {
          "type": "integer",
          "description": "Наличие бесконтактной приемки",
          "example": 0
        },
        "street": {
          "type": "string",
          "description": "Улица",
          "example": "ул. Зеленая"
        },
        "transfer_date": {
          "type": "string",
          "description": "Дата передачи дома по ДДУ",
          "example": "2024-10-12"
        },
        "warranty_end": {
          "type": "string",
          "description": "Дата окончания гарантии по дому",
          "example": "2026-12-01"
        },
        "warranty_start": {
          "type": "string",
          "description": "Дата начала гарантии по дому",
          "example": "2023-12-01"
        }
      }
    },
    "house_id": {
      "type": "integer",
      "description": "Id Дома",
      "example": 327
    },
    "id": {
      "type": "integer",
      "description": "Id Квартиры",
      "example": 1081
    },
    "number": {
      "type": "string",
      "description": "Номер помещения",
      "example": "12"
    },
    "payment_schemes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {
            "…": "max_depth"
          },
          "group": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "position": {
            "…": "max_depth"
          }
        }
      }
    },
    "plan": {
      "type": "ob
```

### Schema `Inspection`


```json
{
  "type": "object",
  "properties": {
    "additional": {
      "type": "object",
      "properties": {}
    },
    "attachments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "collection": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "extension": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "size": {
            "…": "max_depth"
          },
          "url": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "author_id": {
      "type": "integer",
      "description": "Id автора (создателя) приемки",
      "example": 4326
    },
    "claims": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "attachments": {
            "…": "max_depth"
          },
          "author": {
            "…": "max_depth"
          },
          "author_id": {
            "…": "max_depth"
          },
          "category": {
            "…": "max_depth"
          },
          "category_id": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "custom_fields": {
            "…": "max_depth"
          },
          "date_complete": {
            "…": "max_depth"
          },
          "date_planned": {
            "…": "max_depth"
          },
          "date_review": {
            "…": "max_depth"
          },
          "description": {
            "…": "max_depth"
          },
          "house": {
            "…": "max_depth"
          },
          "house_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "last_status_history": {
            "…": "max_depth"
          },
          "owner_id": {
            "…": "max_depth"
          },
          "owner_type": {
            "…": "max_depth"
          },
          "priority_id": {
            "…": "max_depth"
          },
          "remarks": {
            "…": "max_depth"
          },
          "responsible": {
            "…": "max_depth"
          },
          "responsible_id": {
            "…": "max_depth"
          },
          "reviewer": {
            "…": "max_depth"
          },
          "reviewer_id": {
            "…": "max_depth"
          },
          "room": {
            "…": "max_depth"
          },
          "room_id": {
            "…": "max_depth"
          },
          "status": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          },
          "subject": {
            "…": "max_depth"
          },
          "tasks": {
            "…": "max_depth"
          },
          "type": {
            "…": "max_depth"
          },
          "type_id": {
            "…": "max_depth"
          },
          "user": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          },
          "watchers": {
            "…": "max_depth"
          }
        }
      }
    },
    "clients": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_documents": {
            "…": "max_depth"
          },
          "avatar": {
            "…": "max_depth"
          },
          "custom_fields": {
            "…": "max_depth"
          },
          "divisions": {
            "…": "max_depth"
          },
          "email": {
            "…": "max_depth"
          },
          "first_name": {
            "…": "max_depth"
          },
          "full_name": {
            "…": "max_depth"
          },
          "grade": {
            "…": "max_depth"
          },
          "house_permissions": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "last_name": {
            "…": "max_depth"
          },
          "middle_name": {
            "…": "max_depth"
          },
          "organization": {
            "…": "max_depth"
          },
          "personal_data": {
            "…": "max_depth"
          },
          "phone": {
            "…": "max_depth"
          },
          "provider_maps": {
            "…": "max_depth"
          },
          "roles": {
            "…": "max_depth"
          },
          "self_agent_documents": {
            "…": "max_depth"
          },
          "signatures": {
            "…": "max_depth"
          },
          "status": {
            "…": "max_depth"
          },
          "user_group_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "created_at": {
      "type": "string",
      "description": "Дата создания приемки",
      "format": "date-time",
      "example": "2020-08-16 18:34:04"
    },
    "digital_documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "attachment": {
            "…": "max_depth"
          },
          "attachment_extension": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "document_type_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "owner_id": {
            "…": "max_depth"
          },
          "owner_type": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "expert": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "Id эксперта",
          "example": 41
        },
        "inspection_id": {
          "type": "integer",
          "description": "Id Приемки",
          "example": 408
        },
        "name": {
          "type": "string",
          "description": "ФИО эксперта",
          "example": "Степанов Евгений Дмитриевич"
        },
        "organization_inn": {
          "type": "string",
          "description": "ИНН организации",
          "example": "5042063717"
        },
        "organization_name": {
          "type": "string",
          "description": "Название организации",
          "example": "ООО СтройЭксперт"
        }
      }
    },
    "history": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "created_at": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "owner_id": {
            "…": "max_depth"
          },
          "owner_type": {
            "…": "max_depth"
          },
          "status_from": {
            "…": "max_depth"
          },
          "status_to": {
            "…": "max_depth"
          },
          "text": {
            "…": "max_depth"
          },
          "type": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "id": {
      "type": "integer",
      "description": "Id Приемки",
      "example": 408
    },
    "inspection_meters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "…": "max_depth"
          },
          "inspection_id": {
            "…": "max_depth"
          },
          "meter_id": {
            "…": "max_depth"
          },
          "number": {
            "…": "max_depth"
          },
          "photo_enabled": {
            "…": "max_depth"
          },
          "room_meter_id": {
            "…": "max_depth"
          },
          "tariff_count": {
            "…": "max_depth"
          },
          "values": {
            "…": "max_depth"
          }
        }
      }
    },
    "inspection_users": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_document_id": {
            "…": "max_depth"
          },
          "approved": {
            "…": "max_depth"
          },
          "deal_id": {
            "…": "max_depth"
          },
          "has_agent": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "inspection_id": {
            "…": "max_depth"
          },
          "sign_type": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "is_agent": {
      "type": "boolean",
      "description": "Приемка доверенным лицом"
    },
    "meeting": {
      "type": "object",
      "properties": {
        "author": {
          "…": "max_depth"
        },
        "author_id": {
          "type": "integer",
          "description": "Id автора",
          "example": 1138
        },
        "category": {
          "…": "max_depth"
        },
        "date_end": {
          "type": "string",
          "description": "Дата окончания",
          "format": "date-time",
          "example": "2020-08-20 11:03:12"
        },
        "date_start": {
          "type": "string",
          "description": "Дата начала",
          "format": "date-time",
          "example": "2020-08-20 11:03:12"
        },
        "description": {
          "type": "string",
          "description": "Описание",
          "example": "Описание"
        },
        "external_organization": {
          "…": "max_depth"
        },
        "external_organization_id": {
          "type": "integer",
          "description": "Id организации внешнего эксперта",
          "example": 1138
        },
        "house": {
          "…": "max_depth"
        },
        "house_id": {
          "type": "integer",
          "description": "Id связанного здания",
          "example": 1303
        },
        "id": {
          "type": "integer",
          "description": "Id задачи",
          "example": 1
        },
        "internal_organization": {
          "…": "max_depth"
        },
        "internal_organization_id": {
          "type": "integer",
          "description": "Id организации внутреннего эксперта",
          "example": 1138
        },
        "owner_id": {
          "type": "integer",
          "description": "Id владельца",
          "example": 12
        },
        "owner_type": {
          "type": "string",
          "description": "Тип владельца",
          "example": "Inspection"
        },
        "responsible": {
          "…": "max_depth"
        },
        "responsible_id": {
          "type": "integer",
          "description": "Id ответственного",
          "example": 1138
        },
        "room": {
          "…": "max_depth"
        },
        "room_id": {
          "type": "integer",
          "description": "Id связанного помещения",
          "example": 1303
        },
        "status_id": {
          "type": "integer",
          "description": "Id статуса задачи",
          "example": 3
        },
        "type_id": {
          "type": "integer",
          "description": "Id типа задачи",
          "example": 2
        },
        "users": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        }
      }
    },
    "meetings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "author": {
            "…": "max_depth"
          },
          "author_id": {
            "…": "max_depth"
          },
          "category": {
            "…": "max_depth"
          },
          "date_end": {
            "…": "max_depth"
          },
          "date_start": {
            "…": "max_depth"
          },
          "description": {
            "…": "max_depth"
          },
          "external_organization": {
            "…": "max_depth"
          },
          "external_organization_id": {
            "…": "max_depth"
          },
          "house": {
            "…": "max_depth"
          },
          "house_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "internal_organization": {
            "…": "max_depth"
          },
          "internal_organization_id": {
            "…": "max_depth"
          },
          "owner_id": {
            "…": "max_depth"
          },
          "owner_type": {
            "…": "max_depth"
          },
          "responsible": {
            "…": "max_depth"
          },
          "responsible_id": {
            "…": "max_depth"
          },
          "room": {
            "…": "max_depth"
          },
          "room_id": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          },
          "type_id": {
            "…": "max_depth"
          },
          "users": {
            "…": "max_depth"
          }
        }
      }
    },
    "responsible": {
      "type": "object",
      "properties": {
        "agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "avatar": {
          "…": "max_depth"
        },
        "custom_fields": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "divisions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": "krylov097@mail.ru"
        },
        "first_name": {
          "type": "string",
          "description": "Имя",
          "example": "Иван"
        },
        "full_name": {
          "type": "string",
          "description": "Полное ФИО",
          "example": "Крылов Иван Николаевич"
        },
        "grade": {
          "…": "max_depth"
        },
        "house_permissions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "id": {
          "type": "integer",
          "description": "Id Пользователя",
          "example": 4326
        },
        "last_name": {
          "type": "string",
          "description": "Фамилия",
          "example": "Крылов"
        },
        "middle_name": {
          "type": "string",
          "description": "Отчество",
          "example": "Николаевич"
        },
        "organization": {
          "…": "max_depth"
        },
        "personal_data": {
          "…": "max_depth"
        },
        "phone": {
          "type": "string",
          "description": "Телефон (обязательное поле, если пользователь должен авторизовываться в кабинете)",
          "example": "79002007300"
        },
        "provider_maps": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "roles": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "self_agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "signatures": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "status": {
          "…": "max_depth"
        },
        "user_group_id": {
          "type": "integer",
          "description": "Id группы пользователя (10 - клиент, 5 - сотрудник, 4 - администратор)",
          "example": 5
        }
      }
    },
    "responsible_id": {
      "type": "integer",
      "description": "Id ответственного пользователя",
      "example": 4326
    },
    "room": {
      "type": "object",
      "properties": {
        "area": {
          "type": "number",
          "desc
```

### Schema `Deal`


```json
{
  "type": "object",
  "properties": {
    "act_date": {
      "type": "string",
      "description": "Дата акта приема-передачи",
      "format": "date-time",
      "example": "2021-05-18 10:04:41"
    },
    "act_number": {
      "type": "string",
      "description": "Номер акта приема-передачи",
      "example": "АПП-123/2021"
    },
    "attachments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "collection": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "extension": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "size": {
            "…": "max_depth"
          },
          "url": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "buyers_married": {
      "type": "boolean",
      "description": "Покупатель (и) в браке",
      "example": true
    },
    "contract_date": {
      "type": "string",
      "description": "Дата договора",
      "example": "20.07.2020"
    },
    "contract_number": {
      "type": "string",
      "description": "Номер договора",
      "example": "Д010/20"
    },
    "contract_type": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "ID типа договора",
          "example": 408
        },
        "name": {
          "type": "string",
          "description": "Название",
          "example": "ДДУ"
        }
      }
    },
    "contract_type_id": {
      "type": "integer",
      "description": "Тип договора",
      "example": 1
    },
    "created_at": {
      "type": "string",
      "description": "Дата создания сделки",
      "format": "date-time",
      "example": "2020-08-16 18:34:04"
    },
    "deal_registrations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "deal_id": {
            "…": "max_depth"
          },
          "external_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "metadata": {
            "…": "max_depth"
          },
          "provider_id": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "digital_documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "collection": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "extension": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "size": {
            "…": "max_depth"
          },
          "url": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "id": {
      "type": "integer",
      "description": "ID Сделки",
      "example": 408
    },
    "inspection_prepare_stage": {
      "type": "string",
      "description": "Шаг подготовки к приемке",
      "example": "user_data"
    },
    "inspection_sign_type": {
      "type": "string",
      "description": "Способ подписания на приемке (offline, online)",
      "example": "online"
    },
    "inspection_users": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_document_id": {
            "…": "max_depth"
          },
          "approved": {
            "…": "max_depth"
          },
          "deal_id": {
            "…": "max_depth"
          },
          "has_agent": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "inspection_id": {
            "…": "max_depth"
          },
          "sign_type": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "keys_given": {
      "type": "integer",
      "description": "Ключи получены (0/1)",
      "example": 1
    },
    "mortgage": {
      "type": "object",
      "properties": {
        "chosen_response_id": {
          "type": "integer",
          "description": "Выбранный ответ банка",
          "example": 240
        },
        "created_at": {
          "type": "string",
          "description": "Дата создания заявки",
          "format": "date-time",
          "example": "2022-08-16 18:34:04"
        },
        "deal_id": {
          "type": "integer",
          "description": "Id сделки",
          "example": 147
        },
        "external_id": {
          "type": "string",
          "description": "Id заявки на ипотеку во внешнем сервисе",
          "example": "5435460"
        },
        "extra": {
          "type": "object",
          "properties": {}
        },
        "id": {
          "type": "integer",
          "description": "Id заявки на ипотеку",
          "example": 25
        },
        "is_own": {
          "type": "integer",
          "description": "Уже есть одобрение ипотеки (1 - да, 0 - нет)",
          "example": 1
        },
        "provider_id": {
          "type": "integer",
          "description": "Id сервис провайдера, через которого оформляется ипотека",
          "example": 12
        },
        "status_id": {
          "type": "integer",
          "description": "Статус заявки на ипотеку",
          "example": 1
        }
      }
    },
    "object_purchased_in_marriage": {
      "type": "boolean",
      "description": "Объект приобретен в браке",
      "example": false
    },
    "one_sided_act_date": {
      "type": "string",
      "description": "Дата одностороннего акта приема-передачи",
      "format": "date-time",
      "example": "2021-05-18 10:04:41"
    },
    "ownership_type_id": {
      "type": "integer",
      "description": "Тип собственности",
      "example": 1
    },
    "payment_scheme": {
      "type": "object",
      "properties": {
        "description": {
          "type": "string",
          "description": "Описание",
          "example": "Оплата с помощью ипотечного кредита"
        },
        "group": {
          "type": "string",
          "description": "Группа",
          "example": "mortgage"
        },
        "id": {
          "type": "integer",
          "description": "ID схемы оплаты",
          "example": 408
        },
        "name": {
          "type": "string",
          "description": "Название",
          "example": "Ипотека"
        },
        "position": {
          "type": "integer",
          "description": "Позиция",
          "example": 2
        }
      }
    },
    "payments": {
      "type": "number",
      "description": "Сумма платежей, руб",
      "format": "float",
      "example": 623201
    },
    "price": {
      "type": "number",
      "description": "Сумма сделки, руб",
      "format": "float",
      "example": 3256000
    },
    "provider_maps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "deal_id": {
            "…": "max_depth"
          },
          "external_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "pipeline_id": {
            "…": "max_depth"
          },
          "provider": {
            "…": "max_depth"
          }
        }
      }
    },
    "provider_statuses": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "deal_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "provider_id": {
            "…": "max_depth"
          },
          "provider_name": {
            "…": "max_depth"
          }
        }
      }
    },
    "readiness_message_date": {
      "type": "string",
      "description": "Дата сообщения о готовности объекта",
      "format": "date-time",
      "example": "2021-05-10 10:04:41"
    },
    "readiness_message_sending_date": {
      "type": "string",
      "description": "Дата отправки сообщения о готовности объекта",
      "format": "date-time",
      "example": "2021-05-11 10:04:41"
    },
    "readiness_message_sending_number": {
      "type": "string",
      "description": "Трек-номер отправки сообщения о готовности",
      "example": "AGC1129121124"
    },
    "registration_date": {
      "type": "string",
      "description": "Дата регистрации сделки",
      "format": "date-time",
      "example": "2021-05-12 10:04:41"
    },
    "registration_number": {
      "type": "string",
      "description": "Номер регистрации",
      "example": "109675/20"
    },
    "reservation_confirm": {
      "type": "integer",
      "description": "Подтверждение бронирования сделки (1 - подтверждена)",
      "example": 0
    },
    "reservation_confirm_hours": {
      "type": "integer",
      "description": "Кол-во часов, через которое неподтвержденная бронь будет отменена",
      "example": 3
    },
    "reservation_date_end": {
      "type": "string",
      "description": "Дата, до которой забронирована сделка",
      "format": "date-time",
      "example": "2020-10-12 10:04:41"
    },
    "reservation_date_start": {
      "type": "string",
      "description": "Дата, с которой забронирована сделка",
      "format": "date-time",
      "example": "2020-10-07 11:04:41"
    },
    "reservation_price": {
      "type": "integer",
      "description": "Стоимость бронирования сделки",
      "example": 3000
    },
    "resign_one_sided_act": {
      "type": "integer",
      "description": "Односторонний акт перепеодписан на двусторонний (0/1)",
      "example": 1
    },
    "responsible": {
      "type": "object",
      "properties": {
        "agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "avatar": {
          "…": "max_depth"
        },
        "custom_fields": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "divisions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": "krylov097@mail.ru"
        },
        "first_name": {
          "type": "string",
          "description": "Имя",
          "example": "Иван"
        },
        "full_name": {
          "type": "string",
          "description": "Полное ФИО",
          "example": "Крылов Иван Николаевич"
        },
        "grade": {
          "…": "max_depth"
        },
        "house_permissions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "id": {
          "type": "integer",
          "description": "Id Пользователя",
          "example": 4326
        },
        "last_name": {
          "type": "string",
          "description": "Фамилия",
          "example": "Крылов"
        },
        "middle_name": {
          "type": "string",
          "description": "Отчество",
          "example": "Николаевич"
        },
        "organization": {
          "…": "max_depth"
        },
        "personal_data": {
          "…": "max_depth"
        },
        "phone": {
          "type": "string",
          "description": "Телефон (обязательное поле, если пользователь должен авторизовываться в кабинете)",
          "example": "79002007300"
        },
        "provider_maps": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "roles": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "self_agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "signatures": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "status": {
          "…": "max_depth"
        },
        "user_group_id": {
          "type": "integer",
          "description": "Id группы пользователя (10 - клиент, 5 - сотрудник, 4 - администратор)",
          "example": 5
        }
      }
    },
    "room": {
      "type": "object",
      "properties": {
        "area": {
          "type": "number",
          "description": "Общая площадь",
          "format": "float"
        },
        "area_additional": {
          "type": "number",
          "description": "Площадь дополнительная",
          "format": "float"
        },
        "area_additional_fact": {
          "type": "number",
          "description": "Площадь дополнительная (факт)",
          "format": "float"
        },
        "area_balcony": {
          "type": "number",
          "description": "Площадь балкона",
          "format": "float"
        },
        "area_balcony_fact": {
          "type": "number",
          "description": "Площадь балкона (факт)",
          "format": "float"
        },
        "area_balcony_w_ratio": {
          "type": "number",
          "description": "Площадь лоджии с понижающим коэфф-ом",
          "format": "float"
        },
        "area_balcony_w_ratio_fact": {
          "type": "number",
          "description": "Площадь лоджии с понижающим коэфф-ом (факт)",
          "format": "float"
        },
        "area_fact": {
          "type": "number",
          "description": "Общая площадь (факт)",
          "format": "float"
        },
        "area_kitchen": {
          "type": "number",
          "description": "Площадь кухни",
          "format": "float"
        },
        "area_kitchen_fact": {
          "type": "number",
          "description": "Площадь кухни (факт)",
          "format": "float"
        },
        "area_living": {
          "type": "number",
          "description": "Площадь жилая",
          "format": "float"
        },
        "area_living_fact": {
          "type": "number",
          "description": "Площадь жилая (факт)",
          "format": "float"
        },
        "area_overall": {
          "type": "number",
          "description": "Общая площадь с коэфф-том",
          "format": "float"
        },
        "area_overall_fact": {
          "type": "number",
          "description": "Общая площадь с коэфф-том (факт)",
          "format": "float"
        },
        "area_rooms": {
          "type": "number",
          "description": "Площадь комнат",
          "format": "float"
        },
        "area_rooms_fact": {
          "type": "number",
          "description": "Площадь комнат (факт)",
          "format": "float"
        },
        "badges": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "balcony": {
          "type": "string",
          "description": "Тип балкона",
          "example": "Лоджия"
        },
        "balcony_id": {
          "type": "integer",
          "description": "ID типа балкона"
        },
        "bathroom": {
          "type": "string",
          "description": "Тип санузла"
        },
        "bathroom_id": {
          "type": "integer",
          "description": "ID типа санузал"
        },
        "cadastral_number": {
          "type": "string",
          "description": "Кадастровый номер помещения",
          "example": "77-77-09/020/2008-082"
        },
        "deal": {
          "$ref": "#/components/schemas/Deal",
          "note": "cycle"
        },
        "deco
```

### Schema `House`


```json
{
  "type": "object",
  "properties": {
    "city": {
      "type": "string",
      "description": "Город",
      "example": "г. Москва"
    },
    "commissioning_permit_date": {
      "type": "string",
      "description": "Дата разрешения на ввод в эксплуатацию дома",
      "example": "2023-10-12"
    },
    "commissioning_permit_number": {
      "type": "string",
      "description": "Номер разрешения на ввод в эксплуатацию дома",
      "example": "28475632"
    },
    "coordinates": {
      "type": "string",
      "description": "Координаты дома на карте",
      "example": "37.587874, 55.73367"
    },
    "development_end": {
      "type": "string",
      "description": "Окончание строительства",
      "example": "II квартал 2021"
    },
    "development_start": {
      "type": "string",
      "description": "Начало строительства",
      "example": "I квартал 2018"
    },
    "district_id": {
      "type": "integer",
      "description": "Id ЖК",
      "example": 175
    },
    "fias": {
      "type": "string",
      "description": "Код ФИАС (уникальный идентификатор российского адреса)",
      "example": "01000000-0000-0000-0000-000000000000"
    },
    "house": {
      "type": "string",
      "description": "Номер дома",
      "example": "24а"
    },
    "house_state_id": {
      "type": "integer",
      "description": "Id стадии строительства",
      "example": 1
    },
    "id": {
      "type": "integer",
      "description": "Id дома",
      "example": 327
    },
    "name": {
      "type": "string",
      "description": "Название дома",
      "example": "Очередь 1"
    },
    "position": {
      "type": "integer",
      "description": "Позиция в списке"
    },
    "self_inspection": {
      "type": "integer",
      "description": "Наличие бесконтактной приемки",
      "example": 0
    },
    "street": {
      "type": "string",
      "description": "Улица",
      "example": "ул. Зеленая"
    },
    "transfer_date": {
      "type": "string",
      "description": "Дата передачи дома по ДДУ",
      "example": "2024-10-12"
    },
    "warranty_end": {
      "type": "string",
      "description": "Дата окончания гарантии по дому",
      "example": "2026-12-01"
    },
    "warranty_start": {
      "type": "string",
      "description": "Дата начала гарантии по дому",
      "example": "2023-12-01"
    }
  }
}
```

### Schema `User`


```json
{
  "type": "object",
  "properties": {
    "agent_documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_id": {
            "…": "max_depth"
          },
          "approved": {
            "…": "max_depth"
          },
          "deal_id": {
            "…": "max_depth"
          },
          "has_signature_permit": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "issue_date": {
            "…": "max_depth"
          },
          "issuer_name": {
            "…": "max_depth"
          },
          "registration_number": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "avatar": {
      "type": "object",
      "properties": {
        "collection": {
          "type": "string",
          "description": "Коллекция файла",
          "example": ""
        },
        "created_at": {
          "type": "string",
          "description": "Дата и время загрузки",
          "format": "date-time",
          "example": "2020-08-11 09:21:44"
        },
        "extension": {
          "type": "string",
          "description": "Расширение файла",
          "example": "pdf"
        },
        "id": {
          "type": "integer",
          "description": "Id Файла",
          "example": 871
        },
        "name": {
          "type": "string",
          "description": "Название файла",
          "example": "Выписка ЕГРН"
        },
        "size": {
          "type": "integer",
          "description": "Размер в байтах",
          "example": 10680
        },
        "url": {
          "type": "string",
          "description": "URL файла",
          "example": "https://site.ru/uploads/37/_5eb531351f72f.pdf"
        },
        "user_id": {
          "type": "integer",
          "description": "Id пользователя, добавившего файл",
          "example": 2087
        }
      }
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "code": {
            "…": "max_depth"
          },
          "enabled": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "is_required": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "options": {
            "…": "max_depth"
          },
          "type": {
            "…": "max_depth"
          },
          "value": {
            "…": "max_depth"
          }
        }
      }
    },
    "divisions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "parent_id": {
            "…": "max_depth"
          },
          "path": {
            "…": "max_depth"
          },
          "resposible_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "email": {
      "type": "string",
      "description": "Email",
      "example": "krylov097@mail.ru"
    },
    "first_name": {
      "type": "string",
      "description": "Имя",
      "example": "Иван"
    },
    "full_name": {
      "type": "string",
      "description": "Полное ФИО",
      "example": "Крылов Иван Николаевич"
    },
    "grade": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "ID должности",
          "example": 3
        },
        "name": {
          "type": "string",
          "description": "Наименование",
          "example": "Прораб"
        }
      }
    },
    "house_permissions": {
      "type": "array",
      "items": {
        "type": "integer",
        "example": 327
      }
    },
    "id": {
      "type": "integer",
      "description": "Id Пользователя",
      "example": 4326
    },
    "last_name": {
      "type": "string",
      "description": "Фамилия",
      "example": "Крылов"
    },
    "middle_name": {
      "type": "string",
      "description": "Отчество",
      "example": "Николаевич"
    },
    "organization": {
      "type": "object",
      "properties": {
        "bank_account": {
          "type": "string",
          "description": "Расчетный счет банка"
        },
        "bank_bik": {
          "type": "string",
          "description": "БИК банка",
          "example": "044525225"
        },
        "bank_correspondent_account": {
          "type": "string",
          "description": "Корреспондентский счет банка",
          "example": "30101810400000000225"
        },
        "bank_name": {
          "type": "string",
          "description": "Наименование банка",
          "example": "ПАО СБЕРБАНК"
        },
        "contractor_contracts": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "customer_contracts": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": "prom-stroy-org@yandex.ru"
        },
        "external_id": {
          "type": "string",
          "description": "Внешний ID",
          "example": "123e4567-e89b-12d3-a456-426614174000"
        },
        "id": {
          "type": "integer",
          "description": "Id Организации",
          "example": 53
        },
        "inn": {
          "type": "string",
          "description": "ИНН",
          "example": "8074768313"
        },
        "kpp": {
          "type": "string",
          "description": "КПП",
          "example": "510645342"
        },
        "legal_address": {
          "type": "string",
          "description": "Юридический адрес",
          "example": "Санкт-Петербург, ул Ленина, д. 18, стр. 19, кв. 25, индекс 148754"
        },
        "name": {
          "type": "string",
          "description": "Название организации",
          "example": "ООО ПромСтройОрг"
        },
        "ogrn": {
          "type": "string",
          "description": "ОГРН",
          "example": "6032116467388"
        },
        "okpo": {
          "type": "string",
          "description": "ОКПО",
          "example": "29063984"
        },
        "phones": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "post_address": {
          "type": "string",
          "description": "Почтовый адрес",
          "example": "Санкт-Петербург, ул Ленина, д. 18, стр. 19, кв. 25, индекс 148754"
        },
        "types": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "users": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        }
      }
    },
    "personal_data": {
      "type": "object",
      "properties": {
        "address_match": {
          "type": "boolean",
          "description": "Совпадение адреса регистрации и адреса проживания",
          "example": true
        },
        "company_address": {
          "type": "string",
          "description": "Юр.лицо: Юридический адрес"
        },
        "company_bank_details": {
          "type": "string",
          "description": "Юр.лицо: Банковские реквизиты"
        },
        "company_inn": {
          "type": "string",
          "description": "Юр.лицо: ИНН"
        },
        "company_legal_document": {
          "type": "string",
          "description": "Юр.лицо: Документ, определяющий полномочия (устав, доверенность)",
          "example": "Доверенность №10 от 12.04.2021 г"
        },
        "company_name": {
          "type": "string",
          "description": "Юр.лицо: Название организации",
          "example": "ООО Инженерные сети"
        },
        "company_ogrn": {
          "type": "string",
          "description": "Юр.лицо: ОГРН"
        },
        "date_of_birth": {
          "type": "string",
          "description": "Дата рождения",
          "example": "12.12.2020"
        },
        "gender": {
          "type": "string",
          "description": "Пол"
        },
        "id": {
          "type": "integer",
          "description": "ID записи",
          "example": 4326
        },
        "inn": {
          "type": "string",
          "description": "ИНН физлица",
          "example": "124859687454"
        },
        "passport_department_code": {
          "type": "string",
          "description": "Код департамента",
          "example": "125-451"
        },
        "passport_issue_date": {
          "type": "string",
          "description": "Дата выдачи",
          "example": "01.01.1991"
        },
        "passport_issued_by": {
          "type": "string",
          "description": "Кем выдан",
          "example": "УФМС №123 по Ленинскому району"
        },
        "passport_number": {
          "type": "string",
          "description": "Номер паспорта",
          "example": "548562"
        },
        "passport_series": {
          "type": "string",
          "description": "Серия паспорта",
          "example": "4571"
        },
        "place_of_birth": {
          "type": "string",
          "description": "Место рождения",
          "example": "Город Ленинград"
        },
        "registration_address": {
          "type": "string",
          "description": "Адрес регистрации одной строкой",
          "example": "Санкт-Петербург, Ленинский р-н, ул Ленина, д. 18, стр. 19, кв. 25, индекс 148754"
        },
        "registration_apartment": {
          "type": "string",
          "description": "Квартира регистрации",
          "example": "25"
        },
        "registration_building": {
          "type": "string",
          "description": "Здание регистрации",
          "example": "19"
        },
        "registration_city": {
          "type": "string",
          "description": "Город регистрации",
          "example": "Санкт-Петербург"
        },
        "registration_district": {
          "type": "string",
          "description": "Район регистрации",
          "example": "Ленинский р-н"
        },
        "registration_house": {
          "type": "string",
          "description": "Дом регистрации",
          "example": "18"
        },
        "registration_postal_code": {
          "type": "string",
          "description": "Почтовый индекс регистрации",
          "example": "148754"
        },
        "registration_street": {
          "type": "string",
          "description": "Улица регистрации",
          "example": "ул Ленина"
        },
        "residential_address": {
          "type": "string",
          "description": "Адрес проживания одной строкой",
          "example": "Санкт-Петербург, Ленинский р-н, ул Ленина, д. 18, стр. 19, кв. 25, индекс 148754"
        },
        "residential_apartment": {
          "type": "string",
          "description": "Квартира проживания",
          "example": "25"
        },
        "residential_building": {
          "type": "string",
          "description": "Здание проживания",
          "example": "19"
        },
        "residential_city": {
          "type": "string",
          "description": "Город проживания",
          "example": "Санкт-Петербург"
        },
        "residential_district": {
          "type": "string",
          "description": "Район проживания",
          "example": "Ленинский р-н"
        },
        "residential_house": {
          "type": "string",
          "description": "Дом проживания",
          "example": "18"
        },
        "residential_postal_code": {
          "type": "string",
          "description": "Почтовый индекс проживания",
          "example": "148754"
        },
        "residential_street": {
          "type": "string",
          "description": "Улица проживания",
          "example": "ул Ленина"
        },
        "snils": {
          "type": "string",
          "description": "СНИЛС",
          "example": "145-789-157 47"
        },
        "user_id": {
          "type": "integer",
          "description": "ID пользователя",
          "example": 18
        }
      }
    },
    "phone": {
      "type": "string",
      "description": "Телефон (обязательное поле, если пользователь должен авторизовываться в кабинете)",
      "example": "79002007300"
    },
    "provider_maps": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "external_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "provider": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "roles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "title": {
            "…": "max_depth"
          }
        }
      }
    },
    "self_agent_documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "agent_id": {
            "…": "max_depth"
          },
          "approved": {
            "…": "max_depth"
          },
          "deal_id": {
            "…": "max_depth"
          },
          "has_signature_permit": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "issue_date": {
            "…": "max_depth"
          },
          "issuer_name": {
            "…": "max_depth"
          },
          "registration_number": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "signatures": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "created_at": {
            "…": "max_depth"
          },
          "error_description": {
            "…": "max_depth"
          },
          "expires_at": {
            "…": "max_depth"
          },
          "external_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "provider_id": {
            "…": "max_depth"
          },
          "registration_stage": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "status": {
      "type": "object",
      "properties": {
        "bg_color": {
          "type": "string",
          "description": "Цвет фона (если есть)",
          "example": "#000000"
        },
        "code": {
          "type": "string",
          "description": "Код статуса (если есть)",
          "example": "NEW"
        },
        "id": {
          "type": "integer",
          "description": "Id статуса",
          "example": 1
        },
        "name": {
          "type": "string",
          "description": "Название статуса",
          "example": "Новая"
        },
        "text_color": {
          "type": "string",
          "description": "Цвет текста (если есть)",
          "example": "#FFFFFF"
        }
      }
    },
    "user_group_id": {
      "type": "integer",
      "description": "Id группы пользователя (10 - клиент, 5 - сотрудник, 4 - администратор)",
      "example": 5
    }
  }
}
```

### Schema `Claim`


```json
{
  "type": "object",
  "properties": {
    "attachments": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "collection": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "extension": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "name": {
            "…": "max_depth"
          },
          "size": {
            "…": "max_depth"
          },
          "url": {
            "…": "max_depth"
          },
          "user_id": {
            "…": "max_depth"
          }
        }
      }
    },
    "author": {
      "type": "object",
      "properties": {
        "agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "avatar": {
          "…": "max_depth"
        },
        "custom_fields": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "divisions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": "krylov097@mail.ru"
        },
        "first_name": {
          "type": "string",
          "description": "Имя",
          "example": "Иван"
        },
        "full_name": {
          "type": "string",
          "description": "Полное ФИО",
          "example": "Крылов Иван Николаевич"
        },
        "grade": {
          "…": "max_depth"
        },
        "house_permissions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "id": {
          "type": "integer",
          "description": "Id Пользователя",
          "example": 4326
        },
        "last_name": {
          "type": "string",
          "description": "Фамилия",
          "example": "Крылов"
        },
        "middle_name": {
          "type": "string",
          "description": "Отчество",
          "example": "Николаевич"
        },
        "organization": {
          "…": "max_depth"
        },
        "personal_data": {
          "…": "max_depth"
        },
        "phone": {
          "type": "string",
          "description": "Телефон (обязательное поле, если пользователь должен авторизовываться в кабинете)",
          "example": "79002007300"
        },
        "provider_maps": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "roles": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "self_agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "signatures": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "status": {
          "…": "max_depth"
        },
        "user_group_id": {
          "type": "integer",
          "description": "Id группы пользователя (10 - клиент, 5 - сотрудник, 4 - администратор)",
          "example": 5
        }
      }
    },
    "author_id": {
      "type": "integer",
      "description": "Id автора",
      "example": 127
    },
    "category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "description": "Id",
          "example": 1
        },
        "is_public": {
          "type": "integer",
          "description": "Доступна собственникам в личном кабинете (1/0)",
          "example": 1
        },
        "name": {
          "type": "string",
          "description": "Название",
          "example": "Документы"
        }
      }
    },
    "category_id": {
      "type": "integer",
      "description": "Id Категории заявки",
      "example": 24
    },
    "created_at": {
      "type": "string",
      "description": "Дата и время создания заявки",
      "format": "date-time",
      "example": "2020-08-14 11:24:14"
    },
    "custom_fields": {
      "type": "object",
      "properties": {}
    },
    "date_complete": {
      "type": "string",
      "description": "Фактическая дата и время выполнения заявки",
      "format": "date-time",
      "example": "2020-08-22 14:43:20"
    },
    "date_planned": {
      "type": "string",
      "description": "Планируемая дата и время устранения",
      "format": "date-time",
      "example": "2020-08-20 00:00:00"
    },
    "date_review": {
      "type": "string",
      "description": "Время осмотра на объекте",
      "format": "date-time",
      "example": "2020-08-20 16:00:00"
    },
    "description": {
      "type": "string",
      "description": "Описание заявки",
      "example": "На кухне нет воды, в ванной и туалете есть"
    },
    "house": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "Город",
          "example": "г. Москва"
        },
        "commissioning_permit_date": {
          "type": "string",
          "description": "Дата разрешения на ввод в эксплуатацию дома",
          "example": "2023-10-12"
        },
        "commissioning_permit_number": {
          "type": "string",
          "description": "Номер разрешения на ввод в эксплуатацию дома",
          "example": "28475632"
        },
        "coordinates": {
          "type": "string",
          "description": "Координаты дома на карте",
          "example": "37.587874, 55.73367"
        },
        "development_end": {
          "type": "string",
          "description": "Окончание строительства",
          "example": "II квартал 2021"
        },
        "development_start": {
          "type": "string",
          "description": "Начало строительства",
          "example": "I квартал 2018"
        },
        "district_id": {
          "type": "integer",
          "description": "Id ЖК",
          "example": 175
        },
        "fias": {
          "type": "string",
          "description": "Код ФИАС (уникальный идентификатор российского адреса)",
          "example": "01000000-0000-0000-0000-000000000000"
        },
        "house": {
          "type": "string",
          "description": "Номер дома",
          "example": "24а"
        },
        "house_state_id": {
          "type": "integer",
          "description": "Id стадии строительства",
          "example": 1
        },
        "id": {
          "type": "integer",
          "description": "Id дома",
          "example": 327
        },
        "name": {
          "type": "string",
          "description": "Название дома",
          "example": "Очередь 1"
        },
        "position": {
          "type": "integer",
          "description": "Позиция в списке"
        },
        "self_inspection": {
          "type": "integer",
          "description": "Наличие бесконтактной приемки",
          "example": 0
        },
        "street": {
          "type": "string",
          "description": "Улица",
          "example": "ул. Зеленая"
        },
        "transfer_date": {
          "type": "string",
          "description": "Дата передачи дома по ДДУ",
          "example": "2024-10-12"
        },
        "warranty_end": {
          "type": "string",
          "description": "Дата окончания гарантии по дому",
          "example": "2026-12-01"
        },
        "warranty_start": {
          "type": "string",
          "description": "Дата начала гарантии по дому",
          "example": "2023-12-01"
        }
      }
    },
    "house_id": {
      "type": "integer",
      "description": "Id дома, к которому относится заявка",
      "example": 78
    },
    "id": {
      "type": "integer",
      "description": "Id Технической заявки",
      "example": 871
    },
    "last_status_history": {
      "type": "object",
      "properties": {
        "created_at": {
          "type": "string",
          "description": "Дата и время события",
          "format": "date-time",
          "example": "2024-07-05T05:06:04Z"
        },
        "id": {
          "type": "integer",
          "description": "Id записи",
          "example": 8701
        },
        "owner_id": {
          "type": "integer",
          "description": "Id сущности-владельца",
          "example": 1235
        },
        "owner_type": {
          "type": "string",
          "description": "Имя сущности-владельца",
          "example": "Remark"
        },
        "status_from": {
          "type": "integer",
          "description": "ID статуса, из которого изменилось",
          "example": 2
        },
        "status_to": {
          "type": "integer",
          "description": "ID статуса, в который изменилось",
          "example": 3
        },
        "text": {
          "type": "string",
          "description": "Текстовый комментарий к событию (название статуса)",
          "example": "В работе"
        },
        "type": {
          "type": "integer",
          "description": "Тип события (1 - изменение статуса)",
          "example": 1
        },
        "user_id": {
          "type": "integer",
          "description": "Id пользователя, совершившего действие",
          "example": 2087
        }
      }
    },
    "owner_id": {
      "type": "integer",
      "description": "Id объекта владельца",
      "example": 5
    },
    "owner_type": {
      "type": "string",
      "description": "Имя класса владельца",
      "example": "Inspection"
    },
    "priority_id": {
      "type": "integer",
      "description": "Id типа срочности",
      "example": 10
    },
    "remarks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "attachments": {
            "…": "max_depth"
          },
          "author": {
            "…": "max_depth"
          },
          "author_id": {
            "…": "max_depth"
          },
          "category": {
            "…": "max_depth"
          },
          "category_id": {
            "…": "max_depth"
          },
          "comment": {
            "…": "max_depth"
          },
          "created_at": {
            "…": "max_depth"
          },
          "custom_fields": {
            "…": "max_depth"
          },
          "date_complete": {
            "…": "max_depth"
          },
          "date_deadline": {
            "…": "max_depth"
          },
          "date_planned": {
            "…": "max_depth"
          },
          "date_start": {
            "…": "max_depth"
          },
          "defect_count": {
            "…": "max_depth"
          },
          "defect_type_id": {
            "…": "max_depth"
          },
          "floor": {
            "…": "max_depth"
          },
          "floor_id": {
            "…": "max_depth"
          },
          "house": {
            "…": "max_depth"
          },
          "house_id": {
            "…": "max_depth"
          },
          "id": {
            "…": "max_depth"
          },
          "inspection_step_id": {
            "…": "max_depth"
          },
          "instruction": {
            "…": "max_depth"
          },
          "owner_id": {
            "…": "max_depth"
          },
          "owner_type": {
            "…": "max_depth"
          },
          "plan": {
            "…": "max_depth"
          },
          "plan_id": {
            "…": "max_depth"
          },
          "plan_point_type": {
            "…": "max_depth"
          },
          "plan_points": {
            "…": "max_depth"
          },
          "price": {
            "…": "max_depth"
          },
          "room": {
            "…": "max_depth"
          },
          "room_id": {
            "…": "max_depth"
          },
          "section": {
            "…": "max_depth"
          },
          "section_id": {
            "…": "max_depth"
          },
          "standard": {
            "…": "max_depth"
          },
          "standard_id": {
            "…": "max_depth"
          },
          "status": {
            "…": "max_depth"
          },
          "status_id": {
            "…": "max_depth"
          },
          "step": {
            "…": "max_depth"
          },
          "tags": {
            "…": "max_depth"
          },
          "watchers": {
            "…": "max_depth"
          },
          "work": {
            "…": "max_depth"
          },
          "work_id": {
            "…": "max_depth"
          },
          "work_type_id": {
            "…": "max_depth"
          },
          "workers": {
            "…": "max_depth"
          }
        }
      }
    },
    "responsible": {
      "type": "object",
      "properties": {
        "agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "avatar": {
          "…": "max_depth"
        },
        "custom_fields": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "divisions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": "krylov097@mail.ru"
        },
        "first_name": {
          "type": "string",
          "description": "Имя",
          "example": "Иван"
        },
        "full_name": {
          "type": "string",
          "description": "Полное ФИО",
          "example": "Крылов Иван Николаевич"
        },
        "grade": {
          "…": "max_depth"
        },
        "house_permissions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "id": {
          "type": "integer",
          "description": "Id Пользователя",
          "example": 4326
        },
        "last_name": {
          "type": "string",
          "description": "Фамилия",
          "example": "Крылов"
        },
        "middle_name": {
          "type": "string",
          "description": "Отчество",
          "example": "Николаевич"
        },
        "organization": {
          "…": "max_depth"
        },
        "personal_data": {
          "…": "max_depth"
        },
        "phone": {
          "type": "string",
          "description": "Телефон (обязательное поле, если пользователь должен авторизовываться в кабинете)",
          "example": "79002007300"
        },
        "provider_maps": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "roles": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "self_agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "signatures": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "status": {
          "…": "max_depth"
        },
        "user_group_id": {
          "type": "integer",
          "description": "Id группы пользователя (10 - клиент, 5 - сотрудник, 4 - администратор)",
          "example": 5
        }
      }
    },
    "responsible_id": {
      "type": "integer",
      "description": "Id ответственного пользователя",
      "example": 23
    },
    "reviewer": {
      "type": "object",
      "properties": {
        "agent_documents": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "avatar": {
          "…": "max_depth"
        },
        "custom_fields": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "divisions": {
          "type": "array",
          "items": {
            "…": "max_depth"
          }
        },
        "email": {
          "type": "string",
          "description": "Email",
          "example": 
```


## Файлы

- Спецификация: `iflat_openapi_1.4.0.json`
- Машиночитаемый прогон: `iflat_get_probe_results.json`
- Скрипт повторения: `iflat_build_readonly_landscape.py`
