class Rating(models.Model):
    """
    Node ratings
    
    """

    RATING_CHOICES = (
        ('+', _('up')),
        ('-', _('down'))
    )

    node                    = models.ForeignKey(Node)
    user                    = models.ForeignKey(User)
    score                   = models.CharField(max_length=1, choices=RATING_CHOICES, default=1, null=False)
    created_date            = models.DateTimeField(_('date created'), auto_now_add=True)
    
    objects                 = managers.RatingManager()
    
