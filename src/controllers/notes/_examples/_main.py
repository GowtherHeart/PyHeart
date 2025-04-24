from src.models.response import notes as notes_resp

NoteCoreResponseModelExample = notes_resp.NotesCoreRespModel(
    name="name",
    content="content",
    deleted=False,
    date_update="2025-01-01",  # type: ignore
    date_create="2025-01-01",  # type: ignore
)

NoteCoreResponseModelArrayExample = [NoteCoreResponseModelExample]
