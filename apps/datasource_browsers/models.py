from django.db import models


BROWSER_TYPES = [
    ("google", "Google"),
]


BROWSER_READING_ABILITIES = [
    # Remove these contents
    ("javascript", "JavaScript"),
    ("style", "Style"),
    ("inline_style", "Inline Style"),
    ("comments", "Comments"),
    ("links", "Links"),
    ("meta", "Meta"),
    ("page_structure", "Page Structure"),
    ("processing_instructions", "Processing Instructions"),
    ("embedded", "Embedded"),
    ("frames", "Frames"),
    ("forms", "Forms"),
    ("keep_tags", "Keep Tags"),
]


class BrowsingReadingAbilitiesNames:
    JAVASCRIPT = "javascript"
    STYLE = "style"
    INLINE_STYLE = "inline_style"
    COMMENTS = "comments"
    LINKS = "links"
    META = "meta"
    PAGE_STRUCTURE = "page_structure"
    PROCESSING_INSTRUCTIONS = "processing_instructions"
    EMBEDDED = "embedded"
    FRAMES = "frames"
    FORMS = "forms"
    REMOVE_TAGS = "remove_tags"


# Create your models here.

class DataSourceBrowserConnection(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    browser_type = models.CharField(max_length=100, choices=BROWSER_TYPES)

    assistant = models.ForeignKey("assistants.Assistant", on_delete=models.CASCADE)

    # hyper-parameters
    data_selectivity = models.FloatField(default=0.5)
    whitelisted_extensions = models.JSONField(default=list, blank=True, null=True)
    blacklisted_extensions = models.JSONField(default=list, blank=True, null=True)
    reading_abilities = models.JSONField(default=list, blank=True, null=True)
    minimum_investigation_sites = models.IntegerField(default=2)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.browser_type + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Data Source Browser Connection"
        verbose_name_plural = "Data Source Browser Connections"


class DataSourceBrowserBrowsingLog(models.Model):
    connection = models.ForeignKey(DataSourceBrowserConnection, on_delete=models.CASCADE, related_name="logs")
    action = models.CharField(max_length=1000)
    context_url = models.CharField(max_length=1000, blank=True, null=True)
    html_content = models.TextField(blank=True, null=True)
    context_content = models.TextField(blank=True, null=True)
    log_content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.connection.name + " - " + self.action + " - " + self.created_at.strftime("%Y%m%d%H%M%S")

    class Meta:
        verbose_name = "Data Source Browser Browsing Log"
        verbose_name_plural = "Data Source Browser Browsing Logs"
