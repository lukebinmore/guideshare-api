# Generated by Django 4.1.2 on 2022-10-06 03:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=15)),
                ("last_name", models.CharField(blank=True, max_length=25)),
                ("dob", models.DateField(blank=True, null=True)),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "picture",
                    models.ImageField(
                        default="/profiles/default/placeholder",
                        upload_to=profiles.models.Profile.image_dir,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "saved_posts",
                    models.ManyToManyField(
                        blank=True, related_name="post_saves", to="posts.post"
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
    ]
