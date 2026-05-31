"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-01

NOTE: If you applied schema.sql directly in Supabase, run this as a baseline:
  alembic stamp 001
This marks the migration as done without re-running it.
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "plants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("company_name", sa.String, nullable=False),
        sa.Column("timezone", sa.String, nullable=False, server_default="America/Toronto"),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "divisions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "stations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("division_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("divisions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("kiosk_token", sa.String, unique=True, nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("TRUE")),
    )

    op.create_table(
        "workers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("employee_id", sa.String, nullable=True),
        sa.Column("pin_hash", sa.String, nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("TRUE")),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("division_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("divisions.id"), nullable=True),
        sa.Column("job_number", sa.String, nullable=False),
        sa.Column("customer_name", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("engineering_hours", sa.Numeric, nullable=True),
        sa.Column("status", sa.String, server_default="pending"),
        sa.Column("priority", sa.Integer, server_default="0"),
        sa.Column("due_date", sa.Date, nullable=True),
        sa.Column("started_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("completed_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.execute("""
        CREATE TABLE task_logs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            plant_id UUID REFERENCES plants(id) ON DELETE CASCADE NOT NULL,
            job_id UUID REFERENCES jobs(id) ON DELETE CASCADE NOT NULL,
            station_id UUID REFERENCES stations(id),
            worker_id UUID REFERENCES workers(id),
            started_at TIMESTAMPTZ NOT NULL,
            completed_at TIMESTAMPTZ,
            duration_minutes NUMERIC GENERATED ALWAYS AS (
                EXTRACT(EPOCH FROM (completed_at - started_at)) / 60
            ) STORED,
            synced_at TIMESTAMPTZ DEFAULT NOW(),
            offline_created BOOLEAN DEFAULT FALSE,
            notes TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    op.create_table(
        "simulation_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id"), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("jobs.id"), nullable=False),
        sa.Column("input_params", postgresql.JSONB, nullable=True),
        sa.Column("output_p50", sa.Date, nullable=True),
        sa.Column("output_p70", sa.Date, nullable=True),
        sa.Column("output_p95", sa.Date, nullable=True),
        sa.Column("iterations", sa.Integer, server_default="1000"),
        sa.Column("vertex_ai_request_id", sa.Text, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.create_table(
        "subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("plant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("plants.id"), nullable=False),
        sa.Column("stripe_customer_id", sa.String, nullable=True),
        sa.Column("stripe_subscription_id", sa.String, nullable=True),
        sa.Column("tier", sa.String, nullable=True),
        sa.Column("status", sa.String, nullable=True),
        sa.Column("current_period_end", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("NOW()")),
    )

    op.create_index("idx_jobs_plant_status", "jobs", ["plant_id", "status"])
    op.create_index("idx_task_logs_job", "task_logs", ["job_id"])
    op.create_index("idx_stations_kiosk_token", "stations", ["kiosk_token"])
    op.create_index("idx_workers_plant", "workers", ["plant_id"])
    op.create_index("idx_simulation_runs_job", "simulation_runs", ["job_id"])


def downgrade() -> None:
    op.drop_table("subscriptions")
    op.drop_table("simulation_runs")
    op.drop_table("task_logs")
    op.drop_table("jobs")
    op.drop_table("workers")
    op.drop_table("stations")
    op.drop_table("divisions")
    op.drop_table("plants")
