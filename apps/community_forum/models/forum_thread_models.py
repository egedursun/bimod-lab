from django.db import models


class ForumThread(models.Model):
    """
    Represents a discussion thread within a forum category. Threads contain posts created
    by users and are typically focused on a specific topic.

    Attributes:
        id (AutoField): The primary key for the thread.
        category (ForeignKey): The category to which this thread belongs.
        title (CharField): The title of the thread.
        created_by (ForeignKey): The user who created the thread.
        created_at (DateTimeField): The date and time when the thread was created.
        updated_at (DateTimeField): The date and time when the thread was last updated.
        is_closed (BooleanField): A flag indicating whether the thread is closed to new posts.
    """

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey("ForumCategory", related_name='threads', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Forum Thread"
        verbose_name_plural = "Forum Threads"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['title', 'created_at']),
            models.Index(fields=['title', 'created_at', 'updated_at']),
        ]
