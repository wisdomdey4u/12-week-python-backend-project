from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.dependencies import CurrentUser, DbSession
from app.models import Resource, Workspace, WorkspaceMember
from app.schemas import (
    ResourceCreate,
    ResourceRead,
    WorkspaceCreate,
    WorkspaceRead,
)

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


async def require_workspace_member(
    workspace_id: UUID,
    user: CurrentUser,
    session: DbSession,
) -> Workspace:
    membership = await session.scalar(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user.id,
        )
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    workspace = await session.get(Workspace, workspace_id)
    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )
    return workspace


WorkspaceMemberAccess = Annotated[Workspace, Depends(require_workspace_member)]


@router.post(
    "",
    response_model=WorkspaceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    payload: WorkspaceCreate,
    user: CurrentUser,
    session: DbSession,
) -> Workspace:
    workspace = Workspace(name=payload.name.strip())
    session.add(workspace)
    await session.flush()
    session.add(
        WorkspaceMember(
            workspace_id=workspace.id,
            user_id=user.id,
            role="owner",
        )
    )
    await session.commit()
    await session.refresh(workspace)
    return workspace


@router.get("", response_model=list[WorkspaceRead])
async def list_workspaces(user: CurrentUser, session: DbSession) -> list[Workspace]:
    result = await session.scalars(
        select(Workspace)
        .join(WorkspaceMember)
        .where(WorkspaceMember.user_id == user.id)
        .order_by(Workspace.created_at, Workspace.id)
    )
    return list(result)


@router.post(
    "/{workspace_id}/resources",
    response_model=ResourceRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    workspace_id: UUID,
    payload: ResourceCreate,
    user: CurrentUser,
    workspace: WorkspaceMemberAccess,
    session: DbSession,
) -> Resource:
    resource = Resource(
        workspace_id=workspace.id,
        created_by_id=user.id,
        title=payload.title.strip(),
        url=str(payload.url) if payload.url is not None else None,
        notes=payload.notes,
    )
    session.add(resource)
    await session.commit()
    await session.refresh(resource)
    return resource


@router.get(
    "/{workspace_id}/resources",
    response_model=list[ResourceRead],
)
async def list_resources(
    workspace_id: UUID,
    workspace: WorkspaceMemberAccess,
    session: DbSession,
) -> list[Resource]:
    result = await session.scalars(
        select(Resource)
        .where(Resource.workspace_id == workspace.id)
        .order_by(Resource.created_at, Resource.id)
    )
    return list(result)


@router.get(
    "/{workspace_id}/resources/{resource_id}",
    response_model=ResourceRead,
)
async def read_resource(
    workspace_id: UUID,
    resource_id: UUID,
    workspace: WorkspaceMemberAccess,
    session: DbSession,
) -> Resource:
    resource = await session.scalar(
        select(Resource).where(
            Resource.id == resource_id,
            Resource.workspace_id == workspace.id,
        )
    )
    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )
    return resource
