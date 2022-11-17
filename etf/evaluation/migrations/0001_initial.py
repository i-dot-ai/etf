# Generated by Django 3.2.16 on 2022-11-17 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_use_email_as_username.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="email address")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", django_use_email_as_username.models.BaseUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Evaluation",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("issue_description", models.TextField(blank=True, null=True)),
                ("those_experiencing_issue", models.TextField(blank=True, null=True)),
                ("why_improvements_matter", models.TextField(blank=True, null=True)),
                ("who_improvements_matter_to", models.TextField(blank=True, null=True)),
                ("current_practice", models.TextField(blank=True, null=True)),
                ("issue_relevance", models.TextField(blank=True, null=True)),
                ("doi", models.CharField(blank=True, max_length=256, null=True)),
                ("evaluation_start_date", models.DateField(blank=True, null=True)),
                ("evaluation_end_date", models.DateField(blank=True, null=True)),
                ("date_of_intended_publication", models.DateField(blank=True, null=True)),
                ("reasons_for_delays_in_publication", models.TextField(blank=True, null=True)),
                (
                    "rap_planned",
                    models.CharField(
                        blank=True,
                        choices=[("YES", "Yes"), ("NO", "No"), ("PARTIAL", "Partial")],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("rap_planned_detail", models.TextField(blank=True, null=True)),
                (
                    "rap_outcome",
                    models.CharField(
                        blank=True,
                        choices=[("YES", "Yes"), ("NO", "No"), ("PARTIAL", "Partial")],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("rap_outcome_detail", models.TextField(blank=True, null=True)),
                ("target_population", models.TextField(blank=True, null=True)),
                ("eligibility_criteria", models.TextField(blank=True, null=True)),
                ("process_for_recruitment", models.TextField(blank=True, null=True)),
                ("target_sample_size", models.TextField(blank=True, null=True)),
                ("intended_recruitment_schedule", models.TextField(blank=True, null=True)),
                ("date_of_first_recruitment", models.DateField(blank=True, null=True)),
                ("ethics_committee_approval", models.BooleanField(blank=True, null=True)),
                ("ethics_committee_details", models.TextField(blank=True, null=True)),
                ("ethical_state_given_existing_evidence_base", models.TextField(blank=True, null=True)),
                ("risks_to_participants", models.TextField(blank=True, null=True)),
                ("risks_to_study_team", models.TextField(blank=True, null=True)),
                ("participant_involvement", models.TextField(blank=True, null=True)),
                ("participant_consent", models.TextField(blank=True, null=True)),
                ("participant_information", models.TextField(blank=True, null=True)),
                ("participant_payment", models.TextField(blank=True, null=True)),
                ("confidentiality_and_personal_data", models.TextField(blank=True, null=True)),
                ("breaking_confidentiality", models.TextField(blank=True, null=True)),
                ("other_ethical_information", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OutcomeMeasure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "primary_or_secondary",
                    models.CharField(
                        blank=True,
                        choices=[("PRIMARY", "Primary"), ("SECONDARY", "Secondary")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "direct_or_surrogate",
                    models.CharField(
                        blank=True, choices=[("DIRECT", "Direct"), ("SURROGATE", "Surrogate")], max_length=10, null=True
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("collection_process", models.TextField(blank=True, null=True)),
                ("timepoint", models.TextField(blank=True, null=True)),
                ("minimum_difference", models.TextField(blank=True, null=True)),
                ("relevance", models.TextField(blank=True, null=True)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="outcome_measures",
                        to="evaluation.evaluation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OtherMeasure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("collection_process", models.TextField(blank=True, null=True)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="other_measures",
                        to="evaluation.evaluation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Intervention",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "brief_description",
                    models.TextField(blank=True, null=True, verbose_name="Brief description of intervention"),
                ),
                (
                    "rationale",
                    models.TextField(
                        blank=True, null=True, verbose_name="Rationale, theory or goals of intervention elements"
                    ),
                ),
                (
                    "materials_used",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Description of physical or informational materials used in the intervention, including those used in intervention delivery or in training of intervention providers",
                    ),
                ),
                (
                    "procedures",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Description of each of the procedures, activities and/or processes used in the intervention, including enabling or supporting activities",
                    ),
                ),
                ("modes_of_delivery", models.TextField(blank=True, null=True)),
                ("location", models.TextField(blank=True, null=True)),
                ("frequency_of_delivery", models.TextField(blank=True, null=True)),
                ("tailoring", models.TextField(blank=True, null=True)),
                ("fidelity", models.TextField(blank=True, null=True)),
                ("resource_requirements", models.TextField(blank=True, null=True)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interventions",
                        to="evaluation.evaluation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EvaluationType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("IMPACT", "Impact evaluation"),
                            ("PROCESS", "Process evaluation"),
                            ("ECONOMIC_COST_MINIMISATION", "Economic evaluation: Cost-minimisation analysis"),
                            ("ECONOMIC_COST_EFFECTIVENESS", "Economic evaluation: Cost-effectiveness analysis"),
                            ("ECONOMIC_COST_BENEFIT", "Economic evaluation: Cost-benefit analysis"),
                            ("ECONOMIC_COST_UTILITY", "Economic evaluation: Cost-utility"),
                            ("OTHER", "Other"),
                        ],
                        max_length=256,
                        null=True,
                    ),
                ),
                ("other_description", models.CharField(max_length=256)),
                (
                    "evaluation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="evaluation_types",
                        to="evaluation.evaluation",
                    ),
                ),
            ],
        ),
    ]
