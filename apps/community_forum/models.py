"""
This module defines the data models for a community forum application.
The models include ForumCategory, ForumThread, ForumPost, ForumComment, and ForumLike,
which represent different aspects of the forum such as categories, threads, posts, comments,
and likes respectively.
"""

from django.db import models


class ForumCategory(models.Model):
    """
    Represents a category within the forum. Categories are used to group threads
    together based on a common theme or subject.

    Attributes:
        id (AutoField): The primary key for the category.
        name (CharField): The name of the category.
        description (TextField): A detailed description of the category.
        slug (SlugField): A URL-friendly slug for the category.
        created_at (DateTimeField): The date and time when the category was created.
        updated_at (DateTimeField): The date and time when the category was last updated.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.slug + " - " + self.created_at.strftime("%Y%m%d%H:%M:%S")

    class Meta:
        verbose_name = "Forum Category"
        verbose_name_plural = "Forum Categories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['name', 'slug', 'created_at']),
            models.Index(fields=['name', 'slug', 'created_at', 'updated_at']),
        ]


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


class ForumPost(models.Model):
    """
    Represents a post within a forum thread. Posts contain the content contributed
    by users in response to the thread's topic.

    Attributes:
        id (AutoField): The primary key for the post.
        thread (ForeignKey): The thread to which this post belongs.
        content (TextField): The content of the post.
        created_by (ForeignKey): The user who created the post.
        created_at (DateTimeField): The date and time when the post was created.
        updated_at (DateTimeField): The date and time when the post was last updated.
        is_verified (BooleanField): A flag indicating whether the post contains a verified answer.
        verified_comment (OneToOneField): The comment that is marked as the verified answer for this post.
    """

    id = models.AutoField(primary_key=True)
    thread = models.ForeignKey("ForumThread", related_name='posts', on_delete=models.CASCADE)

    content = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)  # Verification status for an answer
    verified_comment = models.OneToOneField("ForumComment", related_name='verified_post', on_delete=models.CASCADE,
                                            null=True, blank=True)

    def verify_comment(self, comment):
        """
        Marks the given comment as the verified comment for this post.

        Args:
            comment (ForumComment): The comment to be verified.
        """
        if self.created_by == comment.created_by:
            self.verified_comment = comment
            self.is_verified = True
            self.save()

    def __str__(self):
        return f"Post by {self.created_by} in {self.thread.title}"

    class Meta:
        verbose_name = "Forum Post"
        verbose_name_plural = "Forum Posts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['content', 'created_at']),
            models.Index(fields=['content', 'created_at', 'updated_at']),
        ]


class ForumComment(models.Model):
    """
    Represents a comment on a forum post. Comments allow users to discuss the content
    of a post and provide feedback or additional information.

    Attributes:
        id (AutoField): The primary key for the comment.
        content (TextField): The content of the comment.
        created_by (ForeignKey): The user who created the comment.
        post (ForeignKey): The post to which this comment belongs.
        created_at (DateTimeField): The date and time when the comment was created.
        updated_at (DateTimeField): The date and time when the comment was last updated.
        like_count (PositiveIntegerField): The number of unique likes this comment has received.
    """

    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    post = models.ForeignKey("ForumPost", related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)  # Storing the number of unique likes

    def __str__(self):
        return f"Comment by {self.created_by} on Post ID {self.post.id}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['content', 'created_at']),
            models.Index(fields=['content', 'created_at', 'updated_at']),
        ]


class ForumLike(models.Model):
    """
    Represents a like on a forum comment. Likes indicate that a user found a comment
    helpful or agreeable.

    Attributes:
        id (AutoField): The primary key for the like.
        user (ForeignKey): The user who liked the comment.
        comment (ForeignKey): The comment that was liked.
        created_at (DateTimeField): The date and time when the like was created.
    """

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    comment = models.ForeignKey("ForumComment", related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user} on Comment ID {self.comment.id}"

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['user', 'comment', 'created_at']),
        ]
