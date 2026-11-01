from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.dependencies import get_current_user

from app.modules.auth.models import User
from app.modules.project.model import Project

from app.modules.proposal.model import (
    Proposal,
    ProposalStatus,
)

from app.modules.proposal.schema import (
    ProposalCreate,
    ProposalResponse,
)


router = APIRouter(
    prefix="/proposals",
    tags=["Proposals"],
)


# =========================================================
# FREELANCER APPLY TO PROJECT
# POST /api/v1/proposals/
# =========================================================

@router.post(
    "/",
    response_model=ProposalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_proposal(
    proposal_data: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only freelancer can apply
    if current_user.role.value != "freelancer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only freelancers can apply to projects.",
        )

    # Find project
    project = (
        db.query(Project)
        .filter(Project.id == proposal_data.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    # Project must be open
    if project.status != "open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This project is not open for applications.",
        )

    # Client cannot apply to own project
    if project.client_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot apply to your own project.",
        )

    # Prevent duplicate application
    existing_proposal = (
        db.query(Proposal)
        .filter(
            Proposal.project_id == proposal_data.project_id,
            Proposal.freelancer_id == current_user.id,
        )
        .first()
    )

    if existing_proposal:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied to this project.",
        )

    # Create proposal
    proposal = Proposal(
        project_id=proposal_data.project_id,
        freelancer_id=current_user.id,
        cover_letter=proposal_data.cover_letter.strip(),
        bid_amount=proposal_data.bid_amount,
        estimated_days=proposal_data.estimated_days,
        status=ProposalStatus.pending,
    )

    db.add(proposal)
    db.commit()
    db.refresh(proposal)

    return proposal


# =========================================================
# FREELANCER - MY PROPOSALS
# GET /api/v1/proposals/my
# =========================================================

@router.get(
    "/my",
    response_model=list[ProposalResponse],
)
def get_my_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value != "freelancer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only freelancers can view their proposals.",
        )

    proposals = (
        db.query(Proposal)
        .filter(
            Proposal.freelancer_id == current_user.id
        )
        .order_by(Proposal.created_at.desc())
        .all()
    )

    return proposals


# =========================================================
# CLIENT - RECEIVED PROPOSALS
# GET /api/v1/proposals/client
# =========================================================

@router.get(
    "/client",
    response_model=list[ProposalResponse],
)
def get_client_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Only client can see applications
    if current_user.role.value != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can view received proposals.",
        )

    # Get projects belonging to current client
    client_projects = (
        db.query(Project.id)
        .filter(
            Project.client_id == current_user.id
        )
        .subquery()
    )

    # Get proposals submitted to those projects
    proposals = (
        db.query(Proposal)
        .filter(
            Proposal.project_id.in_(
                db.query(client_projects.c.id)
            )
        )
        .order_by(Proposal.created_at.desc())
        .all()
    )

    return proposals
